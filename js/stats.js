// ===== STATS =====
// === Two-level stat taxonomy ===
// Categories are thematic groupings shown as section headers.
// Each category contains sub-groups (the original groupings).
// This keeps backward-compatible keys for CSS while adding readable hierarchy.

// Accessors for shared state (set by game-engine.js)
function getStory() { return window._story; }
function getStatsPanel() { return window._statsPanel; }

const statCategories = [
    {
        id: 'personal',
        label: 'Personal',
        desc: 'Your capabilities and resources in the field',
        groups: [
            {
                key: 'capabilities', label: 'Skills',
                css: 'g-capabilities',
                desc: 'Core competencies you develop through choices',
                stats: [
                    { id: 'reading',  name: 'Reading',  max: 20, icon: '\u{1F4D6}', tip: 'Ability to decode hidden patterns' },
                    { id: 'weaving',  name: 'Weaving',  max: 20, icon: '\u{1FAA1}', tip: 'Connecting disparate threads together' },
                    { id: 'play',     name: 'Play',     max: 20, icon: '\u{1F3AE}', tip: 'Creative experimentation and risk' },
                    { id: 'craft',    name: 'Craft',    max: 20, icon: '\u{1F528}', tip: 'Building and refining artifacts' },
                    { id: 'nerve',    name: 'Nerve',    max: 20, icon: '\u{26A1}',  tip: 'Courage under pressure' },
                    { id: 'swarm',    name: 'Swarm',    max: 20, icon: '\u{1F41B}', tip: 'Coordinating distributed agents' }
                ]
            },
            {
                key: 'resources', label: 'Assets',
                css: 'g-resources',
                desc: 'Finite resources you must manage each chapter',
                stats: [
                    { id: 'time_remaining', name: 'Time',       max: 10,  icon: '\u{23F3}', tip: 'Turns remaining this chapter' },
                    { id: 'attention',      name: 'Attention',  max: 10,  icon: '\u{1F441}', tip: 'Focus capacity per turn' },
                    { id: 'credibility',    name: 'Credibility', max: 100, icon: '\u{1F4E2}', tip: 'How much others trust you' },
                    { id: 'stealth',        name: 'Stealth',    max: 100, icon: '\u{1F575}', tip: 'Visibility to hostile actors' }
                ]
            }
        ]
    },
    {
        id: 'transcendent',
        label: 'Transcendent',
        desc: 'Metaphysical and cosmic evolution',
        groups: [
            {
                key: 'cosmic', label: 'Cosmic Field',
                css: 'g-cosmic',
                desc: 'The macro-forces shaping reality',
                stats: [
                    { id: 'entropiric_saturation',    name: 'Entropic Sat.',     max: 100, icon: '\u{1F31F}', tip: 'How much the Entropire has saturated' },
                    { id: 'neganthropomorphic_signal', name: 'Neg. Signal',       max: 100, icon: '\u{1F4E1}', tip: 'Signal strength from the counter-future' },
                    { id: 'cosmic_awareness',          name: 'Cosmic Awareness',  max: 15,  icon: '\u{1F52E}', tip: 'Perception of non-classical reality' }
                ]
            },
            {
                key: 'quantum', label: 'Quantum Capacities',
                css: 'g-quantum',
                desc: 'Non-classical abilities emerging through play',
                stats: [
                    { id: 'quantum_telepathy',  name: 'Telepathy',  max: 10, icon: '\u{1F9E0}', tip: 'Direct mind-to-mind communication' },
                    { id: 'psionic_perception', name: 'Psionics',   max: 10, icon: '\u{1F443}', tip: 'Sensing beyond ordinary perception' },
                    { id: 'magickal_discipline',name: 'Magick',     max: 10, icon: '\u{2728}',  tip: 'Disciplined manipulation of reality' }
                ]
            }
        ]
    },
    {
        id: 'collective',
        label: 'Collective',
        desc: 'Your network and AI partner',
        groups: [
            {
                key: 'meshwork', label: 'Meshwork',
                css: 'g-meshwork',
                desc: 'The health and speed of your distributed network',
                stats: [
                    { id: 'meshwork_resilience', name: 'Resilience', max: 100, icon: '\u{1F310}', tip: 'Network robustness against attack' },
                    { id: 'operational_tempo',   name: 'Tempo',      max: 100, icon: '\u{1F3B5}', tip: 'Speed of adaptation vs institutions' },
                    { id: 'public_initiative',   name: 'Initiative', max: 100, icon: '\u{1F680}', tip: 'Momentum for public-facing action' }
                ]
            },
            {
                key: 'agent', label: 'Agent',
                css: 'g-agent',
                desc: 'Your AI companion\u2019s capabilities and autonomy',
                stats: [
                    { id: 'agent_classical_strength',   name: 'Classical',   max: 100, icon: '\u{1F916}', tip: 'Deterministic reasoning power' },
                    { id: 'agent_generative_strength',  name: 'Generative',  max: 100, icon: '\u{2728}',  tip: 'Creative and emergent capacity' },
                    { id: 'agent_autonomy',             name: 'Autonomy',    max: 10,  icon: '\u{1F513}', tip: 'Independence from your control' },
                    { id: 'augmentation_fidelity',      name: 'Fidelity',    max: 100, icon: '\u{1F3AF}', tip: 'How well agent augments your intent' }
                ]
            }
        ]
    },
    {
        id: 'political',
        label: 'Political',
        desc: 'Standing with the six factions',
        groups: [
            {
                key: 'factions', label: 'Factions',
                css: 'g-factions',
                desc: 'Your reputation with each faction (0\u2013100)',
                stats: [
                    { id: 'faction_ledger',    name: 'Ledger',    max: 100, icon: '\u{1F4B0}', tip: 'The financial arbitrage brokers' },
                    { id: 'faction_blade',     name: 'Blade',     max: 100, icon: '\u{1F5E1}', tip: 'The direct-action operators' },
                    { id: 'faction_veil',      name: 'Veil',      max: 100, icon: '\u{1F3AD}', tip: 'The narrative-shaping artists' },
                    { id: 'faction_commons',   name: 'Commons',   max: 100, icon: '\u{1F33F}', tip: 'The cooperative mutualists' },
                    { id: 'faction_mesh',      name: 'Mesh',      max: 100, icon: '\u{1F578}', tip: 'The network weavers' },
                    { id: 'faction_playhouse', name: 'Playhouse', max: 100, icon: '\u{1F3B2}', tip: 'The game-design revolutionaries' }
                ]
            }
        ]
    }
];

// Flat lookup used by renderInlineStats and snapshot helpers
const statConfig = {};
statCategories.forEach(cat => {
    cat.groups.forEach(grp => {
        statConfig[grp.key] = { label: grp.label, key: grp.css, desc: grp.desc, stats: grp.stats };
    });
});

// --- Snapshot previous stat values for change detection ---
let prevStatSnapshot = {};
function snapshotStats() {
    if (!getStory()) return;
    const vars = getStory().variablesState;
    const snap = {};
    Object.values(statConfig).forEach(sec => {
        sec.stats.forEach(stat => {
            try {
                const raw = vars[stat.id];
                snap[stat.id] = (typeof raw === 'number') ? raw : 0;
            } catch(e) { snap[stat.id] = 0; }
        });
    });
    return snap;
}
// Take initial snapshot
prevStatSnapshot = snapshotStats() || {};

// --- Build an inline stats block replacing the ink stat dump ---
// Shows ALL stats grouped by category with delta indicators for changes
// Called whenever ink outputs stat dump lines, replacing raw text with styled block
function renderInlineStats(container) {
    if (!getStory()) return;
    const vars = getStory().variablesState;

    let html = '';
    let hasAnyStats = false;

    statCategories.forEach(cat => {
        let catHtml = '';

        cat.groups.forEach(grp => {
            let groupItems = [];

            grp.stats.forEach(stat => {
                const raw = vars[stat.id];
                if (raw === undefined || raw === null) return;
                const n = (typeof raw === 'number') ? raw : 0;
                const prev = prevStatSnapshot[stat.id] || 0;
                const delta = n - prev;

                hasAnyStats = true;
                const tipAttr = stat.tip ? ` title="${stat.tip}"` : '';

                // Show delta badge only if changed
                let deltaHtml = '';
                if (delta !== 0) {
                    const cls = delta > 0 ? 'positive' : 'negative';
                    const sign = delta > 0 ? '+' : '';
                    deltaHtml = `<span class="stat-inline-delta ${cls}">${sign}${delta}</span>`;
                }

                groupItems.push(`<span class="stat-inline ${grp.css}"${tipAttr}><span class="stat-inline-icon">${stat.icon}</span><span class="stat-inline-name">${stat.name}</span><span class="stat-inline-val">${n}</span>${deltaHtml}</span>`);
            });

            if (groupItems.length > 0) {
                catHtml += `<div class="stat-inline-group-label cat-${cat.id}">${grp.label}</div>`;
                catHtml += groupItems.join('');
            }
        });

        if (catHtml) {
            html += `<div class="stat-inline-cat cat-${cat.id}"><span class="stat-inline-cat-name">${cat.label}</span><span class="stat-inline-cat-desc">${cat.desc}</span></div>`;
            html += catHtml;
            html += '<div class="stat-inline spacer"></div>';
        }
    });

    // Only render if we have stats to show
    if (hasAnyStats) {
        const block = document.createElement('div');
        block.className = 'stats-block';
        block.innerHTML = '<div class="stats-block-title">Status Report</div>' + html;
        container.appendChild(block);
    }
}

function updateStats() {
    if (!getStory()) return;
    const vars = getStory().variablesState;
    const chapter = vars.chapter || 1;
    const score = vars.playvolution_score || 0;

    let html = `<h3>Character Sheet</h3>`;
    html += `<div class="stat-chapter-marker">Chapter ${chapter} &middot; Score ${score}</div>`;

    statCategories.forEach(cat => {
        // Category header
        html += `<div class="stat-category cat-${cat.id}">`;
        html += `<div class="stat-category-header">`;
        html += `<span class="stat-category-name">${cat.label}</span>`;
        html += `<span class="stat-category-desc">${cat.desc}</span>`;
        html += `</div>`;

        cat.groups.forEach(grp => {
            html += `<div class="stat-group ${grp.css}">`;
            html += `<div class="stat-group-label" title="${grp.desc || ''}">${grp.label}</div>`;
            grp.stats.forEach(stat => {
                try {
                    const raw = vars[stat.id];
                    if (raw !== undefined && raw !== null) {
                        const n = typeof raw === 'number' ? raw : 0;
                        const pct = Math.min(100, Math.max(0, (n / stat.max) * 100));
                        const highClass = (pct >= 70) ? ' stat-high' : '';
                        const tipAttr = stat.tip ? ` title="${stat.tip}"` : '';
                        html += `<div class="stat-row"${tipAttr}>
                            <span class="stat-name">${stat.icon} ${stat.name}</span>
                            <span class="stat-right">
                                <span class="stat-value${highClass}">${n}</span>
                                <span class="stat-bar-track"><span class="stat-bar-fill" style="width:${pct}%"></span></span>
                            </span>
                        </div>`;
                    }
                } catch(e) {}
            });
            html += '</div>';
        });

        html += '</div>'; // close stat-category
    });

    statsPanel = getStatsPanel();
    if (statsPanel) statsPanel.innerHTML = html;

    // Feed game variables to music modulation engine
    if (window.applyGameModulation) window.applyGameModulation(vars);
}
