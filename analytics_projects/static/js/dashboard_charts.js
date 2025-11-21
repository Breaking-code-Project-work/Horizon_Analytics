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

        // Nota: Django Rest Framework restituisce di solito { data: { ... } } 
        // in base alla tua Response({"data": serializer.data})
        return jsonData.data;
    } catch (error) {
        console.error('Errore nella richiesta:', error);
        return null;
    }
}

/**
 * Trasforma i dati dell'API nel formato richiesto dai grafici
 * NOTA: Le chiavi qui sotto corrispondono ora a OverviewSerializer
 */
function transformAPIData(apiData) {
    if (!apiData) return null;

    // Helper per accedere in sicurezza agli oggetti annidati (nel caso manchino progetti)
    const getProj = (key) => apiData.top_projects && apiData.top_projects[key] ? apiData.top_projects[key] : {};
    const getSect = (key) => apiData.top_sectors && apiData.top_sectors[key] ? apiData.top_sectors[key] : {};

    return {
        kpi: {
            totale_progetti: apiData.number_of_projects,     // Corretto da numProjects
            valore_complessivo: apiData.total_financing      // Corretto da totalFinancing
        },
        statoAvanzamento: {
            labels: ["Conclusi", "In Corso", "Non Avviati"],
            data: [
                apiData.number_ended_projects,           // Corretto snake_case
                apiData.number_projects_in_progress,     // Corretto snake_case
                apiData.number_not_started_projects      // Corretto snake_case
            ]
        },
        ripartizione: {
            labels: ["Mezzogiorno", "Centro-Nord"],
            data: [
                apiData.midday_financing,        // Corretto da MiddayFinancing
                apiData.middle_north_financing   // Corretto da MiddleNorthFinancing
            ]
        },
        progettiCostosi: {
            // Il Serializer restituisce oggetti { title: "...", total_financing: ... }, non array [0], [1]
            labels: [
                getProj('project1').title || "Progetto 1",
                getProj('project2').title || "Progetto 2",
                getProj('project3').title || "Progetto 3",
                getProj('project4').title || "Progetto 4",
                getProj('project5').title || "Progetto 5",
                getProj('project6').title || "Progetto 6",
                getProj('project7').title || "Progetto 7",
                getProj('project8').title || "Progetto 8",
                getProj('project9').title || "Progetto 9",
                getProj('project10').title || "Progetto 10"
            ],
            data: [
                getProj('project1').total_financing || 0,
                getProj('project2').total_financing || 0,
                getProj('project3').total_financing || 0,
                getProj('project4').total_financing || 0,
                getProj('project5').total_financing || 0,
                getProj('project6').total_financing || 0,
                getProj('project7').total_financing || 0,
                getProj('project8').total_financing || 0,
                getProj('project9').total_financing || 0,
                getProj('project10').total_financing || 0
            ]
        },
        settori: {
            // Il Serializer restituisce oggetti { name: "...", total_financing: ... }
            labels: [
                getSect('sector1').name || "Settore 1",
                getSect('sector2').name || "Settore 2",
                getSect('sector3').name || "Settore 3"
            ],
            data: [
                getSect('sector1').total_financing || 0,
                getSect('sector2').total_financing || 0,
                getSect('sector3').total_financing || 0
            ]
        },
        grandiProgetti: {
            labels: ["Totale"],
            data: [apiData.number_big_projects] // Corretto da numberBigProjects
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
    // Controllo di sicurezza se i dati sono nulli
    if (!data) return; 
    
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
                            // Evita divisione per zero
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
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

    // Gestisci il click sul pulsante "Applica Filtri"
    const applyFiltersBtn = document.getElementById('applyFilters');
    const regionFilter = document.getElementById('regionFilter');
    const macroareaFilter = document.getElementById('macroareaFilter');

    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', async function() {
            const selectedRegion = regionFilter.value;
            const selectedMacroarea = macroareaFilter.value;
            
            await updateDashboard(selectedRegion, selectedMacroarea);
        });
    }
});