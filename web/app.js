// Executive Sales Dashboard & Analytics Controller
document.addEventListener('DOMContentLoaded', () => {
  // Check that data payload is loaded
  if (typeof SALES_DATA === 'undefined' || typeof FORECAST_DATA === 'undefined') {
    console.error("Data payload not loaded!");
    return;
  }

  // --- State Management ---
  const state = {
    filters: {
      year: 'All',
      region: 'All',
      category: 'All',
      segment: 'All'
    },
    theme: 'dark',
    charts: {}
  };

  // --- Currency & Number Formatters ---
  const formatCurrency = (val) => {
    if (val === null || val === undefined || isNaN(val)) return '$0.00';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(val);
  };

  const formatNumber = (val) => {
    if (val === null || val === undefined || isNaN(val)) return '0';
    return new Intl.NumberFormat('en-US').format(val);
  };

  const formatPercent = (val) => {
    if (val === null || val === undefined || isNaN(val)) return '0.0%';
    const sign = val > 0 ? '+' : '';
    return `${sign}${val.toFixed(1)}%`;
  };

  // --- Filtering Logic ---
  const getFilteredData = () => {
    return SALES_DATA.filter(item => {
      if (state.filters.year !== 'All' && item.year.toString() !== state.filters.year) return false;
      if (state.filters.region !== 'All' && item.region_name !== state.filters.region) return false;
      if (state.filters.category !== 'All' && item.category !== state.filters.category) return false;
      if (state.filters.segment !== 'All' && item.customer_segment !== state.filters.segment) return false;
      return true;
    });
  };

  // --- Compute All 11 DAX Measures Dynamically ---
  const computeMeasures = (dataset) => {
    const totalSales = dataset.reduce((sum, d) => sum + (d.sales_amount || 0), 0);
    const totalQuantity = dataset.reduce((sum, d) => sum + (d.units_sold || 0), 0);
    const totalCost = dataset.reduce((sum, d) => sum + (d.cost || 0), 0);
    const totalProfit = dataset.reduce((sum, d) => sum + (d.profit || 0), 0);
    const targetSales = dataset.reduce((sum, d) => sum + (d.target_sales || 0), 0);
    
    // Distinct Orders
    const orderSet = new Set(dataset.map(d => d.order_id));
    const totalOrders = orderSet.size;

    // AOV
    const aov = totalOrders > 0 ? totalSales / totalOrders : 0;

    // Profit Margin %
    const profitMarginPct = totalSales > 0 ? (totalProfit / totalSales) * 100 : 0;

    // Quota Achievement %
    const achievementPct = targetSales > 0 ? (totalSales / targetSales) * 100 : 0;

    // Year-over-Year Growth (Compare 2025 vs 2024 in context)
    let s2024 = 0;
    let s2025 = 0;
    dataset.forEach(d => {
      if (d.year === 2024) s2024 += d.sales_amount;
      if (d.year === 2025) s2025 += d.sales_amount;
    });

    let growthPct = 0;
    let growthLabel = "+31.8% YoY";
    if (state.filters.year === '2025') {
      // Benchmark 2025 against full 2024 with same other slicers
      const pyDataset = SALES_DATA.filter(item => {
        if (item.year !== 2024) return false;
        if (state.filters.region !== 'All' && item.region_name !== state.filters.region) return false;
        if (state.filters.category !== 'All' && item.category !== state.filters.category) return false;
        if (state.filters.segment !== 'All' && item.customer_segment !== state.filters.segment) return false;
        return true;
      });
      const pySales = pyDataset.reduce((s, d) => s + d.sales_amount, 0);
      growthPct = pySales > 0 ? ((totalSales - pySales) / pySales) * 100 : 0;
      growthLabel = `${formatPercent(growthPct)} vs PY`;
    } else if (state.filters.year === '2024') {
      growthLabel = "Baseline Year";
      growthPct = 0;
    } else {
      growthPct = s2024 > 0 ? ((s2025 - s2024) / s2024) * 100 : 0;
      growthLabel = `${formatPercent(growthPct)} (FY25/24)`;
    }

    return {
      totalSales,
      totalQuantity,
      totalOrders,
      aov,
      totalCost,
      totalProfit,
      profitMarginPct,
      targetSales,
      achievementPct,
      growthPct,
      growthLabel
    };
  };

  // --- Update KPI Cards ---
  const updateKpiCards = (m, count) => {
    document.getElementById('kpiTotalSales').textContent = formatCurrency(m.totalSales);
    document.getElementById('kpiTargetPct').textContent = `${m.achievementPct.toFixed(1)}% Quota`;
    document.getElementById('kpiTargetSub').textContent = `Target: ${formatCurrency(m.targetSales)}`;

    document.getElementById('kpiGrowthPct').textContent = m.growthLabel;
    const badge = document.getElementById('kpiGrowthBadge');
    if (m.growthPct >= 0) {
      badge.textContent = "Growing";
      badge.className = "kpi-badge positive";
    } else {
      badge.textContent = "Declining";
      badge.className = "kpi-badge negative";
    }

    document.getElementById('kpiAov').textContent = formatCurrency(m.aov);
    document.getElementById('kpiTotalOrders').textContent = formatNumber(m.totalOrders);
    document.getElementById('kpiUnitsSub').textContent = `${formatNumber(m.totalQuantity)} Units Sold`;

    document.getElementById('kpiTotalProfit').textContent = formatCurrency(m.totalProfit);
    document.getElementById('kpiMarginPct').textContent = `${m.profitMarginPct.toFixed(1)}% Margin`;
    document.getElementById('kpiCostSub').textContent = `COGS: ${formatCurrency(m.totalCost)}`;

    document.getElementById('activeFilterBadge').textContent = `Showing ${count} of 600 Orders`;
  };

  // --- Render & Update Charts ---
  const initOrUpdateCharts = (dataset) => {
    // 1. Monthly Revenue Trend Chart (24 Chronological Months)
    const monthMap = {};
    // Seed all 24 months in order
    SALES_DATA.forEach(d => {
      const ym = d.year_month || `${d.year}-${String(d.month_number).padStart(2, '0')}`;
      if (!monthMap[ym]) {
        monthMap[ym] = {
          label: d.month_year || ym,
          ym: ym,
          year: d.year,
          actual: 0
        };
      }
    });

    // Populate filtered sums
    dataset.forEach(d => {
      const ym = d.year_month || `${d.year}-${String(d.month_number).padStart(2, '0')}`;
      if (monthMap[ym]) {
        monthMap[ym].actual += d.sales_amount;
      }
    });

    const sortedMonths = Object.values(monthMap).sort((a, b) => a.ym.localeCompare(b.ym));
    const labelsTrend = sortedMonths.map(m => m.label);
    const dataTrend = sortedMonths.map(m => m.actual);

    if (state.charts.monthlyTrend) {
      state.charts.monthlyTrend.data.labels = labelsTrend;
      state.charts.monthlyTrend.data.datasets[0].data = dataTrend;
      state.charts.monthlyTrend.update();
    } else {
      const ctx = document.getElementById('monthlyTrendChart').getContext('2d');
      state.charts.monthlyTrend = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labelsTrend,
          datasets: [{
            label: 'Total Revenue ($)',
            data: dataTrend,
            borderColor: '#3B82F6',
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointRadius: 3,
            pointHoverRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => `Revenue: ${formatCurrency(ctx.parsed.y)}`
              }
            }
          },
          scales: {
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.06)' },
              ticks: { callback: (val) => `$${val/1000}k` }
            },
            x: {
              grid: { display: false },
              ticks: { maxRotation: 45, minRotation: 45, font: { size: 10 } }
            }
          }
        }
      });
    }

    // 2. Category Revenue Bar Chart
    const catMap = {};
    dataset.forEach(d => {
      catMap[d.category] = (catMap[d.category] || 0) + d.sales_amount;
    });
    const catEntries = Object.entries(catMap).sort((a, b) => b[1] - a[1]);
    const catLabels = catEntries.map(e => e[0]);
    const catData = catEntries.map(e => e[1]);

    if (state.charts.category) {
      state.charts.category.data.labels = catLabels;
      state.charts.category.data.datasets[0].data = catData;
      state.charts.category.update();
    } else {
      const ctx = document.getElementById('categoryChart').getContext('2d');
      state.charts.category = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: catLabels,
          datasets: [{
            label: 'Category Revenue',
            data: catData,
            backgroundColor: ['#1E3A8A', '#0D9488', '#3B82F6', '#6366F1'],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => `${ctx.label}: ${formatCurrency(ctx.parsed.x)}`
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.06)' },
              ticks: { callback: (val) => `$${val/1000}k` }
            },
            y: { grid: { display: false } }
          }
        }
      });
    }

    // 3. Region Revenue Chart
    const regMap = { 'East': 0, 'South': 0, 'North': 0, 'West': 0 };
    dataset.forEach(d => {
      if (regMap[d.region_name] !== undefined) {
        regMap[d.region_name] += d.sales_amount;
      }
    });

    const regLabels = Object.keys(regMap);
    const regData = Object.values(regMap);

    if (state.charts.region) {
      state.charts.region.data.labels = regLabels;
      state.charts.region.data.datasets[0].data = regData;
      state.charts.region.update();
    } else {
      const ctx = document.getElementById('regionChart').getContext('2d');
      state.charts.region = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: regLabels,
          datasets: [{
            label: 'Regional Revenue',
            data: regData,
            backgroundColor: '#0D9488',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => `${ctx.label}: ${formatCurrency(ctx.parsed.y)}`
              }
            }
          },
          scales: {
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.06)' },
              ticks: { callback: (val) => `$${val/1000}k` }
            },
            x: { grid: { display: false } }
          }
        }
      });
    }

    // 4. Customer Segment & Channel Chart
    const segChanMap = {
      'Existing - Online': 0,
      'Existing - Offline': 0,
      'New - Online': 0,
      'New - Offline': 0
    };
    dataset.forEach(d => {
      const k = `${d.customer_segment} - ${d.sales_channel}`;
      if (segChanMap[k] !== undefined) {
        segChanMap[k] += d.sales_amount;
      }
    });

    const scLabels = ['Existing Accounts', 'New Acquisitions'];
    const onlineData = [segChanMap['Existing - Online'], segChanMap['New - Online']];
    const offlineData = [segChanMap['Existing - Offline'], segChanMap['New - Offline']];

    if (state.charts.segmentChannel) {
      state.charts.segmentChannel.data.datasets[0].data = onlineData;
      state.charts.segmentChannel.data.datasets[1].data = offlineData;
      state.charts.segmentChannel.update();
    } else {
      const ctx = document.getElementById('segmentChannelChart').getContext('2d');
      state.charts.segmentChannel = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: scLabels,
          datasets: [
            {
              label: 'Online Channel',
              data: onlineData,
              backgroundColor: '#3B82F6',
              borderRadius: 6
            },
            {
              label: 'Offline Channel',
              data: offlineData,
              backgroundColor: '#1E3A8A',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top', labels: { boxWidth: 12, font: { size: 10 } } },
            tooltip: {
              callbacks: {
                label: (ctx) => `${ctx.dataset.label}: ${formatCurrency(ctx.parsed.y)}`
              }
            }
          },
          scales: {
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.06)' },
              ticks: { callback: (val) => `$${val/1000}k` }
            },
            x: { grid: { display: false } }
          }
        }
      });
    }
  };

  // --- Render Product Performance Table ---
  const renderProductMatrix = (dataset) => {
    const prodMap = {};
    dataset.forEach(d => {
      if (!prodMap[d.product_name]) {
        prodMap[d.product_name] = {
          id: d.product_id,
          name: d.product_name,
          category: d.category,
          units: 0,
          revenue: 0,
          cost: 0,
          profit: 0
        };
      }
      prodMap[d.product_name].units += d.units_sold;
      prodMap[d.product_name].revenue += d.sales_amount;
      prodMap[d.product_name].cost += d.cost;
      prodMap[d.product_name].profit += d.profit;
    });

    const prodList = Object.values(prodMap).sort((a, b) => b.revenue - a.revenue);
    const tbody = document.getElementById('productMatrixBody');
    tbody.innerHTML = '';

    prodList.forEach(p => {
      const marginPct = p.revenue > 0 ? (p.profit / p.revenue) * 100 : 0;
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="badge-tag">${p.id}</span></td>
        <td><strong>${p.name}</strong></td>
        <td>${p.category}</td>
        <td>${formatNumber(p.units)}</td>
        <td>${formatCurrency(p.revenue)}</td>
        <td>${formatCurrency(p.cost)}</td>
        <td><strong style="color: var(--success);">${formatCurrency(p.profit)}</strong></td>
        <td>
          ${marginPct.toFixed(1)}%
          <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width: ${Math.min(100, marginPct * 1.8)}%;"></div>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });
  };

  // --- Render Full Product Catalog (Tab 3) ---
  const renderFullCatalog = () => {
    const prodMap = {};
    SALES_DATA.forEach(d => {
      if (!prodMap[d.product_name]) {
        prodMap[d.product_name] = {
          id: d.product_id,
          name: d.product_name,
          category: d.category,
          unit_price: d.unit_price,
          unit_cost: d.unit_cost,
          units: 0,
          revenue: 0,
          profit: 0
        };
      }
      prodMap[d.product_name].units += d.units_sold;
      prodMap[d.product_name].revenue += d.sales_amount;
      prodMap[d.product_name].profit += d.profit;
    });

    const tbody = document.getElementById('fullProductTableBody');
    tbody.innerHTML = '';

    Object.values(prodMap).sort((a, b) => b.revenue - a.revenue).forEach(p => {
      const unitMargin = p.unit_price - p.unit_cost;
      const marginPct = p.unit_price > 0 ? (unitMargin / p.unit_price) * 100 : 0;
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="badge-tag">${p.id}</span></td>
        <td><strong>${p.name}</strong></td>
        <td>${p.category}</td>
        <td>${formatCurrency(p.unit_price)}</td>
        <td>${formatCurrency(p.unit_cost)}</td>
        <td>${formatCurrency(unitMargin)}</td>
        <td>${formatNumber(p.units)}</td>
        <td>${formatCurrency(p.revenue)}</td>
        <td><strong style="color: var(--success);">${formatCurrency(p.profit)}</strong></td>
        <td>${marginPct.toFixed(1)}%</td>
      `;
      tbody.appendChild(tr);
    });
  };

  // --- Render Forecast View (Tab 2) ---
  const initForecastView = () => {
    const fTableBody = document.getElementById('forecastTableBody');
    fTableBody.innerHTML = '';

    const labels = FORECAST_DATA.map(d => d.year_month);
    const actualData = FORECAST_DATA.map(d => d.data_type === 'Actual' ? d.actual_revenue : null);
    const predData = FORECAST_DATA.map(d => d.predicted_revenue);
    const lowerData = FORECAST_DATA.map(d => d.data_type === 'Forecast' ? d.lower_bound_95 : null);
    const upperData = FORECAST_DATA.map(d => d.data_type === 'Forecast' ? d.upper_bound_95 : null);

    // Populate table with forecast months only
    FORECAST_DATA.filter(d => d.data_type === 'Forecast').forEach(d => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${d.year_month} (${d.month_name})</strong></td>
        <td><strong style="color: var(--accent-primary);">${formatCurrency(d.predicted_revenue)}</strong></td>
        <td>${formatCurrency(d.lower_bound_95)}</td>
        <td>${formatCurrency(d.upper_bound_95)}</td>
      `;
      fTableBody.appendChild(tr);
    });

    // Chart
    const ctx = document.getElementById('forecastChart').getContext('2d');
    state.charts.forecast = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Observed Actual Revenue ($)',
            data: actualData,
            borderColor: '#3B82F6',
            backgroundColor: 'transparent',
            borderWidth: 2.5,
            pointRadius: 3
          },
          {
            label: 'H1 2026 Forecast ($)',
            data: predData,
            borderColor: '#0D9488',
            borderDash: [5, 5],
            borderWidth: 2.5,
            pointRadius: 4,
            pointBackgroundColor: '#0D9488'
          },
          {
            label: 'Upper 95% Bound',
            data: upperData,
            borderColor: 'rgba(13, 148, 136, 0.3)',
            backgroundColor: 'rgba(13, 148, 136, 0.1)',
            fill: '+1',
            borderWidth: 1,
            pointRadius: 0
          },
          {
            label: 'Lower 95% Bound',
            data: lowerData,
            borderColor: 'rgba(13, 148, 136, 0.3)',
            backgroundColor: 'transparent',
            borderWidth: 1,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${formatCurrency(ctx.parsed.y)}`
            }
          }
        },
        scales: {
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.06)' },
            ticks: { callback: (val) => `$${val/1000}k` }
          },
          x: {
            grid: { display: false },
            ticks: { maxRotation: 45, minRotation: 45, font: { size: 10 } }
          }
        }
      }
    });
  };

  // --- Live ROI Calculator Logic ---
  const updateRoiCalculator = () => {
    const currentHours = parseFloat(document.getElementById('inputCurrentHours').value) || 0;
    const postHours = parseFloat(document.getElementById('inputPostHours').value) || 0;
    const hourlyRate = parseFloat(document.getElementById('inputHourlyRate').value) || 0;
    const initialCost = parseFloat(document.getElementById('inputInitialCost').value) || 0;
    const recurringCost = parseFloat(document.getElementById('inputRecurringCost').value) || 0;

    const hoursSaved = Math.max(0, currentHours - postHours);
    const grossLaborSaved = hoursSaved * hourlyRate;
    const netMonthlyBenefit = grossLaborSaved - recurringCost;

    let paybackMonths = "Indefinite";
    let firstYearRoi = "0.0%";
    let firstYearNet = "$0.00";

    if (netMonthlyBenefit > 0) {
      const pb = initialCost / netMonthlyBenefit;
      paybackMonths = `${pb.toFixed(1)} Months`;
      
      const annualBenefit = (netMonthlyBenefit * 12) - initialCost;
      const roi = (annualBenefit / initialCost) * 100;
      firstYearRoi = `${formatPercent(roi)} Year-1 ROI`;
      firstYearNet = formatCurrency(annualBenefit);
    } else {
      paybackMonths = "Negative Net Benefit";
      firstYearRoi = "Negative ROI";
      firstYearNet = formatCurrency((netMonthlyBenefit * 12) - initialCost);
    }

    document.getElementById('roiHoursSaved').textContent = `${hoursSaved.toFixed(1)} Hours`;
    document.getElementById('roiGrossLaborSaved').textContent = `${formatCurrency(grossLaborSaved)} / mo`;
    document.getElementById('roiNetMonthlyBenefit').textContent = `${formatCurrency(netMonthlyBenefit)} / mo`;
    document.getElementById('roiPaybackMonths').textContent = paybackMonths;
    document.getElementById('roiFirstYearRoi').textContent = firstYearRoi;
    document.getElementById('roiFirstYearNet').textContent = firstYearNet;
  };

  // --- Slicer Event Listeners ---
  const applyFilters = () => {
    const dataset = getFilteredData();
    const measures = computeMeasures(dataset);
    updateKpiCards(measures, dataset.length);
    initOrUpdateCharts(dataset);
    renderProductMatrix(dataset);
  };

  document.getElementById('yearSlicer').addEventListener('change', (e) => {
    state.filters.year = e.target.value;
    applyFilters();
  });

  document.getElementById('regionSlicer').addEventListener('change', (e) => {
    state.filters.region = e.target.value;
    applyFilters();
  });

  document.getElementById('categorySlicer').addEventListener('change', (e) => {
    state.filters.category = e.target.value;
    applyFilters();
  });

  document.getElementById('segmentSlicer').addEventListener('change', (e) => {
    state.filters.segment = e.target.value;
    applyFilters();
  });

  document.getElementById('resetFiltersBtn').addEventListener('click', () => {
    state.filters.year = 'All';
    state.filters.region = 'All';
    state.filters.category = 'All';
    state.filters.segment = 'All';

    document.getElementById('yearSlicer').value = 'All';
    document.getElementById('regionSlicer').value = 'All';
    document.getElementById('categorySlicer').value = 'All';
    document.getElementById('segmentSlicer').value = 'All';

    applyFilters();
  });

  // --- Tab Navigation ---
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      document.getElementById(targetId).classList.add('active');

      // Refresh Chart.js renders when tab becomes visible
      if (targetId === 'tab-forecasting' && !state.charts.forecast) {
        initForecastView();
      }
    });
  });

  // --- Theme Toggle ---
  document.getElementById('themeToggleBtn').addEventListener('click', () => {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    state.theme = next;
  });

  // --- ROI Input Listeners ---
  ['inputCurrentHours', 'inputPostHours', 'inputHourlyRate', 'inputInitialCost', 'inputRecurringCost'].forEach(id => {
    document.getElementById(id).addEventListener('input', updateRoiCalculator);
  });

  // --- Initial Render ---
  applyFilters();
  renderFullCatalog();
  initForecastView();
  updateRoiCalculator();
});
