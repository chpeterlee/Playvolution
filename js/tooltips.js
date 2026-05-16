// ===== FOCUS CHOICE TOOLTIPS =====
const focusChoiceMap = {
    'reading': { emoji: '📖', tooltip: 'Read the signals, patterns, and institutional logic around you.' },
    'weaving': { emoji: '🕸️', tooltip: 'Connect with others, build trust, and maintain your network.' },
    'play': { emoji: '🎮', tooltip: 'Design games, stories, and experiments that hide protocols in plain sight.' },
    'craft': { emoji: '🔧', tooltip: 'Build and repair tools, infrastructure, and practical solutions.' },
    'nerve': { emoji: '⚡', tooltip: 'Act under threat, infiltrate, bluff, or escape dangerous situations.' },
    'swarm': { emoji: '🐝', tooltip: 'Coordinate human and agent collectives across distance and difference.' },
    'recruit': { emoji: '🌱', tooltip: 'Bring new allies into your meshwork, each with their own capacities.' },
    'signal': { emoji: '📡', tooltip: 'Receive and transmit non-classical signals from the cosmos.' },
    'quantum': { emoji: '✦', tooltip: 'Navigate quantum channels that operate outside normal causality.' },
};

function getChoiceTooltip(text) {
    const lower = text.toLowerCase();
    // Direct keyword matches from the map
    for (const [key, val] of Object.entries(focusChoiceMap)) {
        if (lower.includes(key)) return val;
    }
    // Fallback pattern matching - order matters (more specific first)
    const fallbacks = [
        { pattern: /detect surplus|trace.*captur/i, emoji: '📖', tooltip: 'Read the signals, patterns, and institutional logic around you.' },
        { pattern: /read.*assemblage|map who|power on the platform/i, emoji: '🕸️', tooltip: 'Map power structures and find where theater is thinnest.' },
        { pattern: /build meshwork|recruit ally|strengthen.*connection/i, emoji: '🕸️', tooltip: 'Recruit allies and strengthen offline connections.' },
        { pattern: /use play|launch.*game|cultural experiment/i, emoji: '🎮', tooltip: 'Launch games, cultural experiments, or protocols disguised as toys.' },
        { pattern: /push.*agent|deepen.*agent/i, emoji: '✦', tooltip: 'Push the agent toward its anomalous configurations.' },
        { pattern: /cultivate.*stack|tend.*growth|prepare.*catastroph/i, emoji: '🌿', tooltip: 'Tend what is growing, prepare for inevitable change.' },
        { pattern: /build tool|infrastructure|counter-assemblage/i, emoji: '🔧', tooltip: 'Build infrastructure and tools for the counter-assemblage.' },
        { pattern: /decode|puzzle game.*generated/i, emoji: '🔮', tooltip: 'Decode and interpret hidden logics in the system.' },
        { pattern: /deepen.*capac|navigate.*beyond/i, emoji: '✦', tooltip: 'Deepen your capacity to navigate what lies beyond ordinary channels.' },
        { pattern: /signal reception|cultivate.*channel/i, emoji: '📡', tooltip: 'Receive and transmit non-classical signals from the cosmos.' },
        { pattern: /quantum|telepathy|psionics/i, emoji: '✦', tooltip: 'Navigate quantum channels that operate outside normal causality.' },
        { pattern: /recruit/i, emoji: '🌱', tooltip: 'Bring new allies into your meshwork, each with their own capacities.' },
        { pattern: /meshwork|weave.*cell|connect.*people/i, emoji: '🕸️', tooltip: 'Connect with others, build trust, and maintain your network.' },
        { pattern: /play|festival|game.*design/i, emoji: '🎮', tooltip: 'Design games, stories, and experiments that hide protocols in plain sight.' },
        { pattern: /craft|tool|build.*infrastructure/i, emoji: '🔧', tooltip: 'Build and repair tools, infrastructure, and practical solutions.' },
        { pattern: /nerve|infiltrat|threat|bluff/i, emoji: '⚡', tooltip: 'Act under threat, infiltrate, bluff, or escape dangerous situations.' },
        { pattern: /swarm|agent|collective|orchestrat/i, emoji: '🐝', tooltip: 'Coordinate human and agent collectives across distance and difference.' },
        { pattern: /reading|interpret|trace|audit/i, emoji: '📖', tooltip: 'Read the signals, patterns, and institutional logic around you.' },
    ];
    for (const fb of fallbacks) {
        if (fb.pattern.test(text)) return { emoji: fb.emoji, tooltip: fb.tooltip };
    }
    return null;
}
