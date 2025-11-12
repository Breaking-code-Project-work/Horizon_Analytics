/**
 * File: dashboard_charts.js
 * Description: Chart.js visualizations for Visione d'Insieme dashboard
 * Last Modified: 2025-11-09
 */

// ==========================================
// PLACEHOLDER DATA
// ==========================================

const placeholderData = {
    kpi: {
        totale_progetti: 1500,
        valore_complessivo: 2500000000
    },
    statoAvanzamento: {
        labels: ["Conclusi", "In Corso", "Non Avviati"],
        data: [700, 500, 300]
    },
    ripartizione: {
        labels: ["Mezzogiorno", "Centro-Nord"],
        data: [1000000000, 1500000000]
    },
    progettiCostosi: {
        labels: [
            "Progetto A - Roma",
            "Progetto B - Milano",
            "Progetto C - Napoli",
            "Progetto D - Torino",
            "Progetto E - Firenze",
            "Progetto F - Bologna",
            "Progetto G - Bari",
            "Progetto H - Palermo",
            "Progetto I - Genova",
            "Progetto J - Venezia"
        ],
        data: [150000000, 135000000, 120000000, 110000000, 105000000, 95000000, 90000000, 85000000, 82000000, 80000000]
    },
    settori: {
        labels: ["Energia", "Trasporti", "Sanità", "Istruzione", "Digitale"],
        data: [500000000, 450000000, 300000000, 200000000, 150000000]
    },
    grandiProgetti: {
        labels: ["Lombardia"],
        data: [1]
    }
};

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

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.statoAvanzamento.labels,
            datasets: [{
                data: data.statoAvanzamento.data,
                backgroundColor: [
                    '#2b29a7',  // Blu principale
                    '#504f9c',  // Viola hover
                    '#7f7ec7'   // Azzurro chiaro
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

    new Chart(ctx, {
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

    new Chart(ctx, {
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

    new Chart(ctx, {
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
document.addEventListener('DOMContentLoaded', function() {
    // Aggiorna le KPI cards
    updateKPICards(placeholderData);

    // Crea tutti i grafici
    createPieChartStato(placeholderData);
    createBarChartRipartizione(placeholderData);
    createHorizontalBarProgettiCostosi(placeholderData);
    createHorizontalBarSettori(placeholderData);
});

// ==========================================
// API INTEGRATION (Per il futuro)
// ==========================================

/**
 * Funzione per caricare dati dal backend
 * Sostituisci placeholderData con questa funzione quando il backend è pronto
 */
async function loadDataFromAPI() {
    try {
        const response = await fetch('/api/visione-insieme');
        const data = await response.json();

        // Aggiorna KPI e grafici con dati reali
        updateKPICards(data);
        // Ricrea i grafici con i nuovi dati...

    } catch (error) {
        console.error('Errore nel caricamento dei dati:', error);
        // Usa i dati placeholder in caso di errore
        updateKPICards(placeholderData);
    }
}
