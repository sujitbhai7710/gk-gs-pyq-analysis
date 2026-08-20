/* ===== GK GS Analysis - Main JavaScript ===== */

// Toggle subtopic expansion
function toggleSubtopic(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle('expanded');
}

// Mobile menu toggle
function toggleMobileMenu() {
  const links = document.querySelector('.nav-links');
  if (links) links.classList.toggle('open');
}

// Render subject bar chart
function renderSubjectChart(canvasId, labels, data, colors) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined') return;

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Number of Questions',
        data: data,
        backgroundColor: colors,
        borderColor: colors,
        borderWidth: 0,
        borderRadius: 6,
        maxBarThickness: 50
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(30,41,59,0.95)',
          padding: 12,
          titleFont: { size: 13, weight: 'bold' },
          bodyFont: { size: 13 },
          displayColors: false,
          callbacks: {
            label: function(context) {
              return `${context.parsed.y} questions`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(226,232,240,0.6)' },
          ticks: { font: { size: 11 }, color: '#64748b' }
        },
        x: {
          grid: { display: false },
          ticks: { font: { size: 11 }, color: '#64748b', maxRotation: 45, minRotation: 0 }
        }
      }
    }
  });
}

// Render donut chart
function renderDonutChart(canvasId, labels, data, colors) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined') return;

  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderColor: '#fff',
        borderWidth: 3,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '60%',
      plugins: {
        legend: {
          position: 'right',
          labels: {
            font: { size: 12 },
            color: '#1e293b',
            padding: 12,
            boxWidth: 14,
            boxHeight: 14
          }
        },
        tooltip: {
          backgroundColor: 'rgba(30,41,59,0.95)',
          padding: 12,
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a,b) => a+b, 0);
              const pct = ((context.parsed / total) * 100).toFixed(1);
              return ` ${context.label}: ${context.parsed} (${pct}%)`;
            }
          }
        }
      }
    }
  });
}

// Render horizontal bar chart for sub-topics
function renderSubtopicChart(canvasId, labels, data, color) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined') return;

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Questions',
        data: data,
        backgroundColor: color,
        borderColor: color,
        borderWidth: 0,
        borderRadius: 4,
        maxBarThickness: 30
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(30,41,59,0.95)',
          padding: 12,
          callbacks: {
            label: function(context) {
              return ` ${context.parsed.x} questions`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          grid: { color: 'rgba(226,232,240,0.6)' },
          ticks: { font: { size: 11 }, color: '#64748b' }
        },
        y: {
          grid: { display: false },
          ticks: { font: { size: 11 }, color: '#1e293b' }
        }
      }
    }
  });
}

// Expand/collapse all subtopics
function expandAll() {
  document.querySelectorAll('.subtopic-section').forEach(el => el.classList.add('expanded'));
}
function collapseAll() {
  document.querySelectorAll('.subtopic-section').forEach(el => el.classList.remove('expanded'));
}

// Search questions
function searchQuestions(inputId, containerId) {
  const input = document.getElementById(inputId);
  const container = document.getElementById(containerId);
  if (!input || !container) return;

  const term = input.value.toLowerCase().trim();
  const cards = container.querySelectorAll('.question-card');
  let visible = 0;

  cards.forEach(card => {
    const text = card.textContent.toLowerCase();
    if (text.includes(term)) {
      card.style.display = '';
      visible++;
    } else {
      card.style.display = 'none';
    }
  });

  // Show parent subtopic if it has visible children
  container.querySelectorAll('.subtopic-section').forEach(section => {
    const visibleChildren = section.querySelectorAll('.question-card[style=""], .question-card:not([style])');
    const hasVisible = Array.from(section.querySelectorAll('.question-card')).some(c => c.style.display !== 'none');
    if (hasVisible) {
      section.style.display = '';
      if (term) section.classList.add('expanded');
    } else {
      section.style.display = 'none';
    }
  });
}
