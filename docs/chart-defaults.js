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
  Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif";
  Chart.defaults.font.size   = 12.5;
  Chart.defaults.color       = palette.inkSoft;
  Chart.defaults.borderColor = palette.grid;

  Chart.defaults.plugins.tooltip.backgroundColor = palette.ink;
  Chart.defaults.plugins.tooltip.titleFont  = { family: "'Space Grotesk', sans-serif", size: 13, weight: '500' };
  Chart.defaults.plugins.tooltip.bodyFont   = { family: "'Inter', sans-serif", size: 13 };
  Chart.defaults.plugins.tooltip.padding    = 12;
  Chart.defaults.plugins.tooltip.cornerRadius = 8;
  Chart.defaults.plugins.tooltip.displayColors = false;
  Chart.defaults.plugins.tooltip.titleMarginBottom = 6;

  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.padding  = 16;
  Chart.defaults.plugins.legend.labels.boxWidth = 8;
  Chart.defaults.plugins.legend.labels.boxHeight = 8;
  Chart.defaults.plugins.legend.labels.font = { family: "'Inter', sans-serif", size: 12.5 };

  // ---- Bar defaults: rounded ends, no side-skip ----
  if (Chart.defaults.datasets && Chart.defaults.datasets.bar) {
    Chart.defaults.datasets.bar.borderRadius  = 6;
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

  window.SDPD = { palette, highlightColors, xAxis, yAxis, catAxis };
})();
