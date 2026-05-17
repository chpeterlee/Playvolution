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
    for (const [key, val] of Object.entries(focusChoiceMap)) {
        if (lower.includes(key)) return val;
    }
    return null;
}
