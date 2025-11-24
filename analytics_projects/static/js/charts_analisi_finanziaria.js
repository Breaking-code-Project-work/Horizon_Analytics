/**
 * File: charts_analisi_finanziaria.js
 * Description: Chart.js visualizations for Analisi Finanziaria dashboard
 * Last Modified: 2025-11-23
 */

// ==========================================
// GLOBAL VARIABLES
// ==========================================

let chartInstances = {
    pieChartFonti: null,
    barChartFondi: null,
    horizontalBarObiettivi: null,
    barChartTipologie: null,
    horizontalBarSottosettori: null,
    barChartCostoPagamenti: null
};

const originalMockData = {
    data: {
        funding_sources_analysis: {
            "UE": 1,
            "Stato": 1,
            "Regioni": 1,
            "Privato": 1,
            "Comune": 1,
            "Altro_Pubblico": 1,
            "Provincia": 1
        },
        specific_funds_contribution: {
            "FESR (UE)": 1,
            "FSE (UE)": 1,
            "FSC (Stato)": 1,
            "Fondo_di_Rotazione (Stato)": 1,
            "FEASR (UE)": 1,
            "FEAMP (UE)": 1,
            "IOG (UE)": 1,
            "PAC (Stato)": 1,
            "Completamenti (Stato)": 1,
            "Altri_Stato": 1
        },
        top10_thematic_objectives: [
            { "description": "Un'Europa piu sociale e inclusiva", "amount": 1 },
            { "description": "Un'Europa piu verde", "amount": 1 },
            { "description": "Un'Europa piu intelligente", "amount": 1 },
            { "description": "Un'Europa piu connessa", "amount": 1 },
            { "description": "Un'Europa piu vicina ai cittadini", "amount": 1 },
            { "description": "Rafforzare la capacita istituzionale", "amount": 1 },
            { "description": "OT non specificato", "amount": 1 },
            { "description": "Ricerca e Innovazione", "amount": 1 },
            { "description": "Transizione digitale", "amount": 1 },
            { "description": "Occupazione giovanile", "amount": 1 }
        ],
        top10_project_typologies: [
            { "nature": "ACQUISTO O REALIZZAZIONE DI SERVIZI", "amount": 1 },
            { "nature": "LAVORI PUBBLICI", "amount": 1 },
            { "nature": "CONCESSIONE DI INCENTIVI AD UNITA' PRODUTTIVE", "amount": 1 },
            { "nature": "ACQUISTO O REALIZZAZIONE DI BENI E ATTREZZATURE", "amount": 1 },
            { "nature": "CONCESSIONE DI INCENTIVI A ISTITUZIONI", "amount": 1 },
            { "nature": "ALTRO (NON RICONDUCIBILE)", "amount": 1 },
            { "nature": "STUDI E PROGETTAZIONI", "amount": 1 },
            { "nature": "ATTIVITA' PROMOZIONALI E DI SENSIBILIZZAZIONE", "amount": 1 },
            { "nature": "CONTRIBUTI ECONOMICI AD ENTI PUBBLICI", "amount": 1 },
            { "nature": "PROGRAMMI DI FORMAZIONE", "amount": 1 }
        ],
        top5_infrastructural_subsectors: [
            { "subsector": "OPERE STRADALI", "amount": 1 },
            { "subsector": "INFRASTRUTTURE FERROVIARIE E METROPOLITANE", "amount": 1 },
            { "subsector": "INFRASTRUTTURE IDRICHE E GESTIONE ACQUE", "amount": 1 },
            { "subsector": "RIFIUTI E BONIFICHE", "amount": 1 },
            { "subsector": "EDILIZIA SANITARIA", "amount": 1 }
        ],
        funds_to_be_found: {
            "number_of_projects_with_gap": 1,
            "total_missing_amount": 1
        },
        payments_realization_gap: {
            "total_realized_cost": 1,
            "total_payments_made": 1,
            "overall_difference": 1
        }
    }
};

// ==========================================
// API INTEGRATION
// ==========================================

/**
 * Recupera i dati dall'API con i filtri specificati
 */
async function fetchAnalisiFinanziariaData(macroArea = 'nessun filtro', fundingSource = 'nessun filtro') {
    try {
        const params = new URLSearchParams();
        if (macroArea !== 'nessun filtro') params.append('macro_area', macroArea);
        if (fundingSource !== 'nessun filtro') params.append('funding_source', fundingSource);
        
        const queryString = params.toString();
        const url = queryString ? `/api/analysis/?${queryString}` : '/api/analysis/';

        console.log('Tentativo di fetch da:', url);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`Errore HTTP: ${response.status}`);
        }

        const jsonData = await response.json();
        console.log('Dati ricevuti dall\'API:', jsonData);
        
        return jsonData.data;
    } catch (error) {
        console.warn('Errore nel fetch dei dati. Utilizzo dati mock:', error.message);
        return originalMockData.data;
    }
}

/**
 * Trasforma i dati dell'API nel formato richiesto dai grafici - AGGIORNATO
 */
function transformAPIData(apiData) {
    if (!apiData) return null;

    const fundingSourcesTotal = Object.values(apiData.funding_sources_analysis).reduce((sum, amount) => sum + amount, 0);
    const fundingSourcesArray = Object.entries(apiData.funding_sources_analysis).map(([source, amount]) => ({
        source,
        amount,
        percentage: (amount / fundingSourcesTotal) * 100
    }));

    const specificFundsArray = Object.entries(apiData.specific_funds_contribution).map(([fund, amount]) => ({
        fund,
        amount
    }));

    return {
        kpi: {
            numero_progetti_con_gap: apiData.funds_to_be_found.number_of_projects_with_gap,
            importo_totale_mancante: apiData.funds_to_be_found.total_missing_amount
        },
        fontiFinanziamento: {
            labels: fundingSourcesArray.map(item => {
                const sourceMap = {
                    'UE': 'Unione Europea',
                    'Stato': 'Stato',
                    'Regioni': 'Regioni', 
                    'Privato': 'Privato',
                    'Comune': 'Comune',
                    'Altro_Pubblico': 'Altro Pubblico',
                    'Provincia': 'Provincia'
                };
                return sourceMap[item.source] || item.source;
            }),
            data: fundingSourcesArray.map(item => item.percentage),
            amounts: fundingSourcesArray.map(item => item.amount)
        },
        fondiSpecifici: {
            labels: specificFundsArray.map(item => item.fund),
            data: specificFundsArray.map(item => item.amount)
        },
        obiettiviTematici: {
            labels: apiData.top10_thematic_objectives.map(item => item.description),
            data: apiData.top10_thematic_objectives.map(item => item.amount)
        },
        tipologieProgetto: {
            labels: apiData.top10_project_typologies.map(item => item.nature),
            data: apiData.top10_project_typologies.map(item => item.amount)
        },
        sottosettoriInfrastrutturali: {
            labels: apiData.top5_infrastructural_subsectors.map(item => item.subsector),
            data: apiData.top5_infrastructural_subsectors.map(item => item.amount)
        },
        costoVsPagamenti: {
            labels: ['Costo Realizzato', 'Pagamenti Effettuati', 'Differenza'],
            data: [
                apiData.payments_realization_gap.total_realized_cost,
                apiData.payments_realization_gap.total_payments_made,
                apiData.payments_realization_gap.overall_difference
            ]
        }
    };
}

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

function formatCurrency(value) {
    if (value >= 1000000000) {
        return '€ ' + (value / 1000000000).toFixed(1) + 'B';
    } else if (value >= 1000000) {
        return '€ ' + (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
        return '€ ' + (value / 1000).toFixed(1) + 'K';
    }
    return '€ ' + new Intl.NumberFormat('it-IT').format(value);
}

function formatNumber(value) {
    return new Intl.NumberFormat('it-IT').format(value);
}

// ==========================================
// KPI CARDS
// ==========================================

function updateKPICards(data) {
    document.getElementById('numero-progetti-gap').textContent = formatNumber(data.kpi.numero_progetti_con_gap);
    document.getElementById('importo-totale-mancante').textContent = formatCurrency(data.kpi.importo_totale_mancante);
}

// ==========================================
// CHART CONFIGURATIONS
// ==========================================

/**
 * 1) Grafico a Torta - Fonti di Finanziamento
 */
function createPieChartFonti(data) {
    const ctx = document.getElementById('pieChartFonti').getContext('2d');

    // Distruggi il grafico esistente se presente
    if (chartInstances.pieChartFonti) {
        chartInstances.pieChartFonti.destroy();
    }

    chartInstances.pieChartFonti = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.fontiFinanziamento.labels,
            datasets: [{
                data: data.fontiFinanziamento.data,
                backgroundColor: [
                    '#2b29a7', '#504f9c', '#7f7ec7', '#a5a4d6', 
                    '#c7c7e7', '#e0e0f0', '#f0f0f8'
                ],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 11,
                            family: "'Arimo', sans-serif"
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const amount = data.fontiFinanziamento.amounts[context.dataIndex];
                            return `${label}: ${value.toFixed(1)}% (${formatCurrency(amount)})`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * 2) Grafico a Barre Orizzontali - Fondi Specifici
 */
function createBarChartFondi(data) {
    const ctx = document.getElementById('barChartFondi').getContext('2d');

    if (chartInstances.barChartFondi) {
        chartInstances.barChartFondi.destroy();
    }

    chartInstances.barChartFondi = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.fondiSpecifici.labels,
            datasets: [{
                label: 'Importo (€)',
                data: data.fondiSpecifici.data,
                backgroundColor: '#2b29a7',
                borderColor: '#2b29a7',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Importo: ${formatCurrency(context.parsed.x)}`;
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
                            size: 10,
                            family: "'Arimo', sans-serif"
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
 * 3) Grafico a Barre Orizzontali Ordinate - Obiettivi Tematici
 */
function createHorizontalBarObiettivi(data) {
    const ctx = document.getElementById('horizontalBarObiettivi').getContext('2d');

    if (chartInstances.horizontalBarObiettivi) {
        chartInstances.horizontalBarObiettivi.destroy();
    }

    chartInstances.horizontalBarObiettivi = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.obiettiviTematici.labels,
            datasets: [{
                label: 'Finanziamento (€)',
                data: data.obiettiviTematici.data,
                backgroundColor: '#504f9c',
                borderColor: '#504f9c',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Finanziamento: ${formatCurrency(context.parsed.x)}`;
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
                            size: 10,
                            family: "'Arimo', sans-serif"
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
 * 4) Grafico a Barre Verticali - Tipologie di Progetto
 */
function createBarChartTipologie(data) {
    const ctx = document.getElementById('barChartTipologie').getContext('2d');

    if (chartInstances.barChartTipologie) {
        chartInstances.barChartTipologie.destroy();
    }

    const shortLabels = data.tipologieProgetto.labels.map(label => {
        if (label.length > 30) {
            return label.substring(0, 30) + '...';
        }
        return label;
    });

    chartInstances.barChartTipologie = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: shortLabels,
            datasets: [{
                label: 'Importo (€)',
                data: data.tipologieProgetto.data,
                backgroundColor: '#2b29a7',
                borderColor: '#2b29a7',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            const fullLabel = data.tipologieProgetto.labels[tooltipItems[0].dataIndex];
                            return fullLabel.length > 30 ? fullLabel : '';
                        },
                        label: function(context) {
                            return `Importo: ${formatCurrency(context.parsed.y)}`;
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
                            size: 10,
                            family: "'Arimo', sans-serif"
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
 * 5) Grafico a Barre Orizzontali - Sottosettori Infrastrutturali
 */
function createHorizontalBarSottosettori(data) {
    const ctx = document.getElementById('horizontalBarSottosettori').getContext('2d');

    if (chartInstances.horizontalBarSottosettori) {
        chartInstances.horizontalBarSottosettori.destroy();
    }

    chartInstances.horizontalBarSottosettori = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.sottosettoriInfrastrutturali.labels,
            datasets: [{
                label: 'Importo (€)',
                data: data.sottosettoriInfrastrutturali.data,
                backgroundColor: '#7f7ec7',
                borderColor: '#7f7ec7',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Importo: ${formatCurrency(context.parsed.x)}`;
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
                            size: 10,
                            family: "'Arimo', sans-serif"
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
 * 6) Grafico a Barre Affiancate - Costo Realizzato vs Pagamenti Effettuati
 */
function createBarChartCostoPagamenti(data) {
    const ctx = document.getElementById('barChartCostoPagamenti').getContext('2d');

    if (chartInstances.barChartCostoPagamenti) {
        chartInstances.barChartCostoPagamenti.destroy();
    }

    chartInstances.barChartCostoPagamenti = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.costoVsPagamenti.labels,
            datasets: [{
                label: 'Importo (€)',
                data: data.costoVsPagamenti.data,
                backgroundColor: [
                    '#2b29a7',
                    '#504f9c',
                    '#7f7ec7'
                ],
                borderColor: [
                    '#2b29a7',
                    '#504f9c',
                    '#7f7ec7'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${formatCurrency(context.parsed.y)}`;
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
                            size: 10,
                            family: "'Arimo', sans-serif"
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
                            size: 11,
                            family: "'Arimo', sans-serif"
                        }
                    }
                }
            }
        }
    });
}

// ==========================================
// FILTERS MANAGEMENT
// ==========================================

function updateFilterStates() {
    const macroAreaFilter = document.getElementById('macroAreaFilter');
    const fundingSourceFilter = document.getElementById('fundingSourceFilter');

    const filters = [macroAreaFilter, fundingSourceFilter];

    filters.forEach(filter => {
        filter.addEventListener('change', function() {
            const selectedValue = this.value;
            const isDefault = selectedValue === 'nessun filtro';

            console.log(`Filtro cambiato: ${this.id} = ${selectedValue}`);

            // Se è stato selezionato un filtro non di default, disabilita l'altro
            if (!isDefault) {
                filters.forEach(otherFilter => {
                    if (otherFilter !== this) {
                        otherFilter.disabled = true;
                        otherFilter.value = 'nessun filtro'; // Reset al valore default
                    }
                });
            } else {
                // Se è stato deselezionato, riabilita tutti i filtri
                filters.forEach(otherFilter => {
                    otherFilter.disabled = false;
                });
            }
        });
    });
}

// ==========================================
// DASHBOARD UPDATE FUNCTION
// ==========================================

/**
* Aggiorna tutti i grafici con nuovi dati
*/
async function updateDashboard(macroArea = 'nessun filtro', fundingSource = 'nessun filtro') {
    try {
        console.log(`=== AGGIORNAMENTO DASHBOARD ===`);
        console.log(`Filtri attivi: Macro Area="${macroArea}", Fonte Finanziamento="${fundingSource}"`);

        // Mostra indicatori visivi del caricamento
        document.getElementById('numero-progetti-gap').textContent = '...';
        document.getElementById('importo-totale-mancante').textContent = '...';

        const apiData = await fetchAnalisiFinanziariaData(macroArea, fundingSource);

        if (!apiData) {
            console.error('Impossibile recuperare i dati');
            return;
        }

        console.log('Dati ricevuti:', apiData);

        const chartData = transformAPIData(apiData);
        console.log('Dati trasformati per grafici:', chartData);

        updateKPICards(chartData);

        createPieChartFonti(chartData);
        createBarChartFondi(chartData);
        createHorizontalBarObiettivi(chartData);
        createBarChartTipologie(chartData);
        createHorizontalBarSottosettori(chartData);
        createBarChartCostoPagamenti(chartData);

        console.log('Dashboard Analisi Finanziaria aggiornata con successo');
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
    console.log('Inizializzazione dashboard Analisi Finanziaria');
    
    // Inizializza il sistema di filtri mutualmente esclusivi
    updateFilterStates();

    // Carica i dati iniziali
    await updateDashboard();

    // Gestisci il click sul pulsante "Applica Filtri"
    const applyFiltersBtn = document.getElementById('applyFilters');
    applyFiltersBtn.addEventListener('click', async function() {
        console.log('Pulsante "Applica Filtri" cliccato');
        
        const macroArea = document.getElementById('macroAreaFilter').value;
        const fundingSource = document.getElementById('fundingSourceFilter').value;
        
        await updateDashboard(macroArea, fundingSource);
    });

    // Aggiungi CSS per le animazioni
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
});
