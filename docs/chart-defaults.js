/* ============================================================
   Seattle Dog Park Data — shared chart + palette defaults
   Requires Chart.js 4. Optional plugins registered if present:
     - chartjs-plugin-datalabels
     - chartjs-plugin-annotation
   Exposes window.SDPD with palette + helpers.
   ============================================================ */
(function () {
  const palette = {
    bg:         '#FAF8F3',
    surface:    '#FFFFFF',
    ink:        '#1A1712',
    inkSoft:    '#4C4A44',
    inkFaint:   '#8A877E',
    rule:       '#E8E5DC',

    orange:     '#D1481A',
    orangeSoft: '#F9E7DB',
    orangeMute: 'rgba(209,72,26,0.55)',
    navy:       '#1F3A5F',
    navySoft:   '#E1EAF5',
    navyMute:   'rgba(31,58,95,0.55)',
    sage:       '#4C6B54',
    sageSoft:   '#E2EAE0',
    sageMute:   'rgba(76,107,84,0.55)',
    gold:       '#B8872B',
    goldSoft:   '#F2E9CE',
    danger:     '#8B2518',

    grid:       'rgba(26,23,18,0.06)',
    gridStrong: 'rgba(26,23,18,0.12)'
  };

  // ---- Chart.js global defaults ----
  Chart.defaults.font.family = "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, system-ui, sans-serif";
  Chart.defaults.font.size   = 12.5;
  Chart.defaults.color       = palette.inkSoft;
  Chart.defaults.borderColor = palette.grid;

  Chart.defaults.plugins.tooltip.backgroundColor = palette.ink;
  Chart.defaults.plugins.tooltip.titleFont  = { family: "'Schibsted Grotesk', sans-serif", size: 13, weight: '500' };
  Chart.defaults.plugins.tooltip.bodyFont   = { family: "'IBM Plex Sans', sans-serif", size: 13 };
  Chart.defaults.plugins.tooltip.padding    = 12;
  Chart.defaults.plugins.tooltip.cornerRadius = 8;
  Chart.defaults.plugins.tooltip.displayColors = false;
  Chart.defaults.plugins.tooltip.titleMarginBottom = 6;

  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.padding  = 16;
  Chart.defaults.plugins.legend.labels.boxWidth = 8;
  Chart.defaults.plugins.legend.labels.boxHeight = 8;
  Chart.defaults.plugins.legend.labels.font = { family: "'IBM Plex Sans', sans-serif", size: 12.5 };

  // ---- Bar defaults: round the ends of a bar, never the middle of a stack ----
  // A flat borderRadius rounds every segment of a stacked bar, which puts rounded
  // corners partway up a column where two segments meet. This rounds only the
  // outermost segments: the top of the stack and the bottom, or the two far ends
  // on a horizontal chart. A chart that sets borderRadius itself overrides this.
  const BAR_RADIUS = 6;

  const stackedBarRadius = (ctx) => {
    const chart = ctx.chart;
    const sets = chart.data.datasets;
    const me = sets[ctx.datasetIndex];
    if (!me) return BAR_RADIUS;
    const value = Number(me.data[ctx.dataIndex]);
    if (!value) return 0;                 // nothing drawn, nothing to round

    const key = (d) => (d.stack != null ? d.stack : d.label);
    const mine = key(me);
    let atTop = true;
    for (let i = ctx.datasetIndex + 1; i < sets.length; i++) {
      if (key(sets[i]) !== mine) continue;
      if (!chart.isDatasetVisible(i)) continue;
      if (Number(sets[i].data[ctx.dataIndex])) { atTop = false; break; }
    }

    // Only the far end is rounded. The baseline corners stay square so a bar
    // sits flat on its axis, and a segment join inside a stack stays square.
    const r = atTop ? BAR_RADIUS : 0;
    if (chart.options && chart.options.indexAxis === 'y') {
      return { topLeft: 0, bottomLeft: 0, topRight: r, bottomRight: r };
    }
    return { topLeft: r, topRight: r, bottomLeft: 0, bottomRight: 0 };
  };

  if (Chart.defaults.datasets && Chart.defaults.datasets.bar) {
    Chart.defaults.datasets.bar.borderRadius  = stackedBarRadius;
    Chart.defaults.datasets.bar.borderSkipped = false;
  }

  // ---- Register optional plugins if present ----
  if (window.ChartDataLabels) {
    Chart.register(window.ChartDataLabels);
    Chart.defaults.set('plugins.datalabels', {
      display: false,                 // opt-in per chart
      color:   palette.ink,
      font:    { family: "'IBM Plex Mono', monospace", size: 11, weight: 500 },
      anchor:  'end',
      align:   'end',
      offset:  6,
      clamp:   true
    });
  }

  // ---- Helpers ----
  const highlightColors = (labels, focal, focalColor, otherColor) =>
    labels.map(l => l === focal ? focalColor : otherColor);

  // Standard axis styling — call as ...SDPD.axis() inside `scales:`
  const xAxis = (opts = {}) => Object.assign({
    grid: { color: palette.grid, drawTicks: false },
    border: { display: false },
    ticks: { padding: 6, color: palette.inkSoft }
  }, opts);

  const yAxis = (opts = {}) => Object.assign({
    grid: { color: palette.grid, drawTicks: false },
    border: { display: false },
    ticks: { padding: 8, color: palette.inkSoft }
  }, opts);

  // Category axis (no grid on the label axis)
  const catAxis = (opts = {}) => Object.assign({
    grid: { display: false },
    border: { display: false },
    ticks: { padding: 8, color: palette.inkSoft }
  }, opts);

  // ---- Basemap ----------------------------------------------------------
  // Single owner for the Leaflet basemap on every map in the site. Call as
  // SDPD.basemap(map) right after L.map(...); pass { maxZoom } to cap zoom.
  //
  // September 2026: CARTO began burning an "API KEY REQUIRED" watermark into
  // its keyless light_all tiles, so those tiles are no longer usable without a
  // paid key. Esri's World Light Gray canvas is keyless and unwatermarked, and
  // its warm neutral greys match the site palette better than OSM standard,
  // whose blues, greens and route shields fight the data overlays.
  //
  // Esri splits the canvas in two: a label-free Base and a transparent
  // Reference layer carrying place names. Esri also orders its tile path
  // {z}/{y}/{x}, y before x, unlike the XYZ convention. The labels ride in a
  // pane at z-index 250, between the tile pane (200) and the overlay pane
  // (400), so they sit *under* the data the way CARTO's baked-in labels did.
  const ESRI_CANVAS =
    'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/{id}/MapServer/tile/{z}/{y}/{x}';
  const ESRI_ATTRIB =
    'Tiles &copy; <a href="https://www.esri.com/">Esri</a> &mdash; Esri, HERE, Garmin, ' +
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

  const basemap = (map, opts) => {
    const maxZoom = (opts && opts.maxZoom) || 19;
    L.tileLayer(ESRI_CANVAS.replace('{id}', 'World_Light_Gray_Base'),
      { attribution: ESRI_ATTRIB, maxZoom }).addTo(map);
    const labelPane = map.createPane('sdpd-labels');
    labelPane.style.zIndex = 250;
    labelPane.style.pointerEvents = 'none';
    L.tileLayer(ESRI_CANVAS.replace('{id}', 'World_Light_Gray_Reference'),
      { maxZoom, pane: 'sdpd-labels' }).addTo(map);
    return map;
  };

  window.SDPD = { palette, highlightColors, xAxis, yAxis, catAxis, basemap };
})();
