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

// Map specific focus action choice text to emoji/tooltip
const focusActionPatterns = [
    { pattern: /detect surplus/i, val: { emoji: '📖', tooltip: 'Read the signals, patterns, and institutional logic around you.' } },
    { pattern: /read the assemblage/i, val: { emoji: '📖', tooltip: 'Map who holds power and where the theater is thinnest.' } },
    { pattern: /build meshwork/i, val: { emoji: '🕸️', tooltip: 'Recruit allies and strengthen offline connections.' } },
    { pattern: /deepen the agent/i, val: { emoji: '✦', tooltip: 'Push the agent toward its anomalous configurations.' } },
    { pattern: /cultivate.*stack/i, val: { emoji: '🌿', tooltip: 'Prepare for the platform\'s inevitable catastrophe.' } },
    { pattern: /practice quantum/i, val: { emoji: '✦', tooltip: 'Invest time in telepathy, psionics, or magicks.' } },
    { pattern: /encode protocol/i, val: { emoji: '🎮', tooltip: 'Hide coordination logic in games, songs, and playground rituals.' } },
    { pattern: /puncture/i, val: { emoji: '⚡', tooltip: 'Expose the gap between institutional projection and actual capability.' } },
    { pattern: /rest and integrate/i, val: { emoji: '🌿', tooltip: 'Recover attention and process what you\'ve learned.' } },
    // Doctrine choices
    { pattern: /play before policy/i, val: { emoji: '🎮', tooltip: 'Always prototype before formalizing; gain tempo advantage in crises.' } },
    { pattern: /invisible school/i, val: { emoji: '🕸️', tooltip: 'Knowledge survives through teaching, not archiving.' } },
    { pattern: /craft persist/i, val: { emoji: '🔧', tooltip: 'Tools outlast the institutions that tried to contain them.' } },
    { pattern: /signal reception/i, val: { emoji: '📡', tooltip: 'Cultivate the AI\'s generative channel as a strategic receiver.' } },
    { pattern: /quantum integration/i, val: { emoji: '✦', tooltip: 'Blend classical competence with quantum capacity.' } },
];

function getChoiceTooltip(text) {
    const lower = text.toLowerCase();
    // Check specific focus action patterns first
    for (const { pattern, val } of focusActionPatterns) {
        if (pattern.test(text)) return val;
    }
    // Then check direct keyword matches
    for (const [key, val] of Object.entries(focusChoiceMap)) {
        if (lower.includes(key)) return val;
    }
    return null;
}
