/**
 * File: dashboard_charts.js
 * Description: Chart.js visualizations for Visione d'Insieme dashboard
 * Last Modified: 2025-11-15
 */

// ==========================================
// API INTEGRATION
// ==========================================

/**
 * Recupera i dati dall'API
 */
async function fetchDashboardData() {
    const params = {
        region: 'nessun filtro',
        macroarea: 'nessun filtro'
    };

    const queryString = new URLSearchParams(params).toString();
    const url = `api/overview/?${queryString}`; // Nota il '?' prima dei parametri

    try {
        const response = await fetch(url, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Errore nella risposta del server');
        }

        const jsonData = await response.json();
        console.log('Risposta dal server:', jsonData);

        return jsonData.data; // Ritorna solo la sezione 'data' della risposta
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

    return new Chart(ctx, {
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
}

/**
 * Grafico a Barre - Ripartizione Finanziamenti
 */
function createBarChartRipartizione(data) {
    const ctx = document.getElementById('barChartRipartizione').getContext('2d');

    return new Chart(ctx, {
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
}

/**
 * Grafico a Barre Orizzontali - I 10 Progetti più Costosi
 */
function createHorizontalBarProgettiCostosi(data) {
    const ctx = document.getElementById('horizontalBarProgettiCostosi').getContext('2d');

    return new Chart(ctx, {
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
}

/**
 * Grafico a Barre Orizzontali - Settori con più Fondi
 */
function createHorizontalBarSettori(data) {
    const ctx = document.getElementById('horizontalBarSettori').getContext('2d');

    return new Chart(ctx, {
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
}

// ==========================================
// INITIALIZATION
// ==========================================

/**
 * Inizializza tutti i grafici quando il DOM è pronto
 */
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Mostra un indicatore di caricamento (opzionale)
        console.log('Caricamento dati dalla API...');

        // Recupera i dati dall'API
        const apiData = await fetchDashboardData();

        if (!apiData) {
            console.error('Impossibile recuperare i dati dall\'API');
            return;
        }

        // Trasforma i dati nel formato corretto
        const chartData = transformAPIData(apiData);

        // Aggiorna le KPI cards
        updateKPICards(chartData);

        // Crea tutti i grafici
        createPieChartStato(chartData);
        createBarChartRipartizione(chartData);
        createHorizontalBarProgettiCostosi(chartData);
        createHorizontalBarSettori(chartData);

        console.log('Dashboard caricata con successo');
    } catch (error) {
        console.error('Errore durante l\'inizializzazione della dashboard:', error);
    }
});
