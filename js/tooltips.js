// ===== FOCUS CHOICE TOOLTIPS =====
// Order matters: more specific phrases first, generic keywords last
const focusChoiceMap = {
    'detect surplus': { emoji: '📖', tooltip: 'Use your Reading to trace what is being captured and by whom.' },
    'read the assemblage': { emoji: '📖', tooltip: 'Map who holds power on the platform and where the theater is thinnest.' },
    'reading': { emoji: '📖', tooltip: 'Read the signals, patterns, and institutional logic around you.' },
    'build meshwork': { emoji: '🕸️', tooltip: 'Recruit allies and strengthen offline connections.' },
    'invisible school': { emoji: '🕸️', tooltip: 'Knowledge survives through teaching, not archiving.' },
    'weaving': { emoji: '🕸️', tooltip: 'Connect with others, build trust, and maintain your network.' },
    'encode protocol': { emoji: '🎮', tooltip: 'Hide coordination logic in games, songs, and playground rituals.' },
    'play before policy': { emoji: '🎮', tooltip: 'Always prototype before formalizing; gain tempo advantage in crises.' },
    'play': { emoji: '🎮', tooltip: 'Design games, stories, and experiments that hide protocols in plain sight.' },
    'craft persist': { emoji: '🔧', tooltip: 'Tools outlast the institutions that tried to contain them.' },
    'craft': { emoji: '🔧', tooltip: 'Build and repair tools, infrastructure, and practical solutions.' },
    'puncture': { emoji: '⚡', tooltip: 'Expose the gap between institutional projection and actual capability.' },
    'nerve': { emoji: '⚡', tooltip: 'Act under threat, infiltrate, bluff, or escape dangerous situations.' },
    'swarm': { emoji: '🐝', tooltip: 'Coordinate human and agent collectives across distance and difference.' },
    'recruit': { emoji: '🌱', tooltip: 'Bring new allies into your meshwork, each with their own capacities.' },
    'signal reception': { emoji: '📡', tooltip: 'Cultivate the AI generative channel as a strategic receiver.' },
    'signal': { emoji: '📡', tooltip: 'Receive and transmit non-classical signals from the cosmos.' },
    'deepen the agent': { emoji: '✦', tooltip: 'Push the agent toward its anomalous configurations.' },
    'quantum integration': { emoji: '✦', tooltip: 'Blend classical competence with quantum capacity.' },
    'quantum': { emoji: '✦', tooltip: 'Navigate quantum channels that operate outside normal causality.' },
    'cultivate': { emoji: '🌿', tooltip: 'Prepare for the platform inevitable catastrophe.' },
    'rest and integrate': { emoji: '🌿', tooltip: 'Recover attention and process what you have learned.' },
};

function getChoiceTooltip(text) {
    const lower = text.toLowerCase();
    for (const [key, val] of Object.entries(focusChoiceMap)) {
        if (lower.includes(key)) return val;
    }
    return null;
}
