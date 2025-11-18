/**
 * File: dashboard_charts.js
 * Description: Chart.js visualizations for Visione d'Insieme dashboard
 * Last Modified: 2025-11-16
 */

// ==========================================
// GLOBAL VARIABLES
// ==========================================

let chartInstances = {
    pieChartStato: null,
    barChartRipartizione: null,
    horizontalBarProgettiCostosi: null,
    horizontalBarSettori: null
};

// ==========================================
// API INTEGRATION
// ==========================================

/**
 * Recupera i dati dall'API con i filtri specificati
 */
async function fetchDashboardData(region = 'nessun filtro', macroarea = 'nessun filtro') {
    const params = {
        region: region,
        macroarea: macroarea
    };

    const queryString = new URLSearchParams(params).toString();
    const url = `/api/overview/?${queryString}`;

    try {
        const response = await fetch(url, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Errore nella risposta del server');
        }

        const jsonData = await response.json();
        console.log('Risposta dal server:', jsonData);

        return jsonData.data;
    } catch (error) {
        console.error('Errore nella richiesta:', error);
        return null;
    }
}

/**
 * Trasforma i dati dell'API nel formato richiesto dai grafici
 */
function transformAPIData(apiData) {
    if (!apiData) return null;

    return {
        kpi: {
            totale_progetti: apiData.numProjects,
            valore_complessivo: apiData.totalFinancing
        },
        statoAvanzamento: {
            labels: ["Conclusi", "In Corso", "Non Avviati"],
            data: [
                apiData.numberEndedProjects,
                apiData.numberProjectsInProgress,
                apiData.numberNotStartedProjects
            ]
        },
        ripartizione: {
            labels: ["Mezzogiorno", "Centro-Nord"],
            data: [
                apiData.MiddayFinancing,
                apiData.MiddleNorthFinancing
            ]
        },
        progettiCostosi: {
            labels: [
                apiData.TopProjects.Project1[0] || "Progetto 1",
                apiData.TopProjects.Project2[0] || "Progetto 2",
                apiData.TopProjects.Project3[0] || "Progetto 3",
                apiData.TopProjects.Project4[0] || "Progetto 4",
                apiData.TopProjects.Project5[0] || "Progetto 5",
                apiData.TopProjects.Project6[0] || "Progetto 6",
                apiData.TopProjects.Project7[0] || "Progetto 7",
                apiData.TopProjects.Project8[0] || "Progetto 8",
                apiData.TopProjects.Project9[0] || "Progetto 9",
                apiData.TopProjects.Project10[0] || "Progetto 10"
            ],
            data: [
                apiData.TopProjects.Project1[1] || 0,
                apiData.TopProjects.Project2[1] || 0,
                apiData.TopProjects.Project3[1] || 0,
                apiData.TopProjects.Project4[1] || 0,
                apiData.TopProjects.Project5[1] || 0,
                apiData.TopProjects.Project6[1] || 0,
                apiData.TopProjects.Project7[1] || 0,
                apiData.TopProjects.Project8[1] || 0,
                apiData.TopProjects.Project9[1] || 0,
                apiData.TopProjects.Project10[1] || 0
            ]
        },
        settori: {
            labels: [
                apiData.TopSectors.Sector1[0] || "Settore 1",
                apiData.TopSectors.Sector2[0] || "Settore 2",
                apiData.TopSectors.Sector3[0] || "Settore 3"
            ],
            data: [
                apiData.TopSectors.Sector1[1] || 0,
                apiData.TopSectors.Sector2[1] || 0,
                apiData.TopSectors.Sector3[1] || 0
            ]
        },
        grandiProgetti: {
            labels: ["Totale"],
            data: [apiData.numberBigProjects]
        }
    };
}

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

/**
 * Formatta i numeri in valuta EUR
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('it-IT', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

/**
 * Formatta i numeri grandi con separatori
 */
function formatNumber(value) {
    return new Intl.NumberFormat('it-IT').format(value);
}

// ==========================================
// KPI CARDS
// ==========================================

function updateKPICards(data) {
    document.getElementById('totale-progetti').textContent = formatNumber(data.kpi.totale_progetti);
    document.getElementById('valore-complessivo').textContent = formatCurrency(data.kpi.valore_complessivo);
    document.getElementById('territorio-label').textContent = data.grandiProgetti.labels[0];
    document.getElementById('territorio-count').textContent = data.grandiProgetti.data[0] + ' Progetto';
}

// ==========================================
// CHART CONFIGURATIONS
// ==========================================

/**
 * Grafico a Torta - Distribuzione per Stato di Avanzamento
 */
function createPieChartStato(data) {
    const ctx = document.getElementById('pieChartStato').getContext('2d');

    // Distruggi il grafico esistente se presente
    if (chartInstances.pieChartStato) {
        chartInstances.pieChartStato.destroy();
    }

    chartInstances.pieChartStato = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.statoAvanzamento.labels,
            datasets: [{
                data: data.statoAvanzamento.data,
                backgroundColor: [
                    '#2b29a7',
                    '#504f9c',
                    '#7f7ec7'
                ],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 13,
                            family: "'Arimo', sans-serif"
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${formatNumber(value)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });

    return chartInstances.pieChartStato;
}

/**
 * Grafico a Barre - Ripartizione Finanziamenti
 */
function createBarChartRipartizione(data) {
    const ctx = document.getElementById('barChartRipartizione').getContext('2d');

    if (chartInstances.barChartRipartizione) {
        chartInstances.barChartRipartizione.destroy();
    }

    chartInstances.barChartRipartizione = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.ripartizione.labels,
            datasets: [{
                label: 'Finanziamenti (€)',
                data: data.ripartizione.data,
                backgroundColor: ['#2b29a7', '#504f9c'],
                borderColor: ['#2b29a7', '#504f9c'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Finanziamento: ${formatCurrency(context.parsed.y)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        },
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: '#e0e0e0'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            family: "'Arimo', sans-serif"
                        }
                    }
                }
            }
        }
    });

    return chartInstances.barChartRipartizione;
}

/**
 * Grafico a Barre Orizzontali - I 10 Progetti più Costosi
 */
function createHorizontalBarProgettiCostosi(data) {
    const ctx = document.getElementById('horizontalBarProgettiCostosi').getContext('2d');

    if (chartInstances.horizontalBarProgettiCostosi) {
        chartInstances.horizontalBarProgettiCostosi.destroy();
    }

    chartInstances.horizontalBarProgettiCostosi = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.progettiCostosi.labels,
            datasets: [{
                label: 'Costo (€)',
                data: data.progettiCostosi.data,
                backgroundColor: '#2b29a7',
                borderColor: '#2b29a7',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Costo: ${formatCurrency(context.parsed.x)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        },
                        font: {
                            size: 10
                        }
                    },
                    grid: {
                        color: '#e0e0e0'
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11,
                            family: "'Arimo', sans-serif"
                        }
                    }
                }
            }
        }
    });

    return chartInstances.horizontalBarProgettiCostosi;
}

/**
 * Grafico a Barre Orizzontali - Settori con più Fondi
 */
function createHorizontalBarSettori(data) {
    const ctx = document.getElementById('horizontalBarSettori').getContext('2d');

    if (chartInstances.horizontalBarSettori) {
        chartInstances.horizontalBarSettori.destroy();
    }

    chartInstances.horizontalBarSettori = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.settori.labels,
            datasets: [{
                label: 'Fondi Totali (€)',
                data: data.settori.data,
                backgroundColor: '#504f9c',
                borderColor: '#504f9c',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Fondi: ${formatCurrency(context.parsed.x)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        },
                        font: {
                            size: 10
                        }
                    },
                    grid: {
                        color: '#e0e0e0'
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            family: "'Arimo', sans-serif"
                        }
                    }
                }
            }
        }
    });

    return chartInstances.horizontalBarSettori;
}

// ==========================================
// DASHBOARD UPDATE FUNCTION
// ==========================================

/**
 * Aggiorna tutti i grafici con nuovi dati
 */
async function updateDashboard(region, macroarea) {
    try {
        console.log(`Caricamento dati per Regione: ${region}, Macroarea: ${macroarea}`);

        const apiData = await fetchDashboardData(region, macroarea);

        if (!apiData) {
            console.error('Impossibile recuperare i dati dall\'API');
            return;
        }

        const chartData = transformAPIData(apiData);

        updateKPICards(chartData);
        createPieChartStato(chartData);
        createBarChartRipartizione(chartData);
        createHorizontalBarProgettiCostosi(chartData);
        createHorizontalBarSettori(chartData);

        console.log('Dashboard aggiornata con successo');
    } catch (error) {
        console.error('Errore durante l\'aggiornamento della dashboard:', error);
    }
}

// ==========================================
// INITIALIZATION
// ==========================================

/**
 * Inizializza la dashboard e gestisce gli eventi dei filtri
 */
document.addEventListener('DOMContentLoaded', async function() {
    // Carica i dati iniziali
    await updateDashboard('nessun filtro', 'nessun filtro');

    // Riferimenti agli elementi
    const applyFiltersBtn = document.getElementById('applyFilters');
    const regionFilter = document.getElementById('regionFilter');
    const macroareaFilter = document.getElementById('macroareaFilter');

    // Funzione per gestire l'abilitazione/disabilitazione dei filtri
    function handleFilterToggle() {
        const regionValue = regionFilter.value;
        const macroareaValue = macroareaFilter.value;

        // Se regione è selezionata (diversa da "nessun filtro"), disabilita macroarea
        if (regionValue !== 'nessun filtro') {
            macroareaFilter.disabled = true;
        } 
        // Se macroarea è selezionata (diversa da "nessun filtro"), disabilita regione
        else if (macroareaValue !== 'nessun filtro') {
            regionFilter.disabled = true;
        } 
        // Se entrambe sono su "nessun filtro", abilita entrambe
        else {
            regionFilter.disabled = false;
            macroareaFilter.disabled = false;
        }
    }

    // Event listener per il cambio di selezione su Regione
    regionFilter.addEventListener('change', function() {
        handleFilterToggle();
    });

    // Event listener per il cambio di selezione su Macroarea
    macroareaFilter.addEventListener('change', function() {
        handleFilterToggle();
    });

    // Gestisci il click sul pulsante "Applica Filtri"
    applyFiltersBtn.addEventListener('click', async function() {
        const selectedRegion = regionFilter.value;
        const selectedMacroarea = macroareaFilter.value;
        
        await updateDashboard(selectedRegion, selectedMacroarea);
    });
});

