// ===== STATE =====
let story = null;
let historyLog = [];
let currentScene = 'room';
let endingReached = false;

// ===== DOM =====
const $ = id => document.getElementById(id);
const sceneEl = $('scene');
const storyArea = $('story-area');
const storyContent = $('story-content');
const choicesArea = $('choices-area');
const choicesInner = $('choices-inner');
const historyPanel = $('history-panel');
const statsPanel = $('stats-panel');
const scrollHint = $('scroll-down-hint');

// Expose shared state for external modules
window._statsPanel = statsPanel;

// Scroll hint: show when there's unread text below
function updateScrollHint() {
    const hasScroll = storyArea.scrollHeight > storyArea.clientHeight + 20;
    const atBottom = (storyArea.scrollHeight - storyArea.scrollTop - storyArea.clientHeight) < 30;
    const show = hasScroll && !atBottom;

    // Position just above the choices pane
    if (choicesArea.classList.contains('open')) {
        scrollHint.style.bottom = (choicesArea.offsetHeight + 8) + 'px';
    } else {
        scrollHint.style.bottom = '14px';
    }

    if (show) {
        scrollHint.classList.add('visible');
    } else {
        scrollHint.classList.remove('visible');
    }
}

storyArea.addEventListener('scroll', updateScrollHint);
window.addEventListener('resize', updateScrollHint);

// Scroll story area to show a specific element at the top
function scrollToElement(el) {
    if (!el) return;
    const offset = el.offsetTop - storyArea.offsetTop;
    storyArea.scrollTo({ top: Math.max(0, offset - 10), behavior: 'smooth' });
    // Check hint after scroll settles
    setTimeout(updateScrollHint, 600);
    setTimeout(updateScrollHint, 1200);
}


// ===== SCENE DETECTION =====
// Priority 1: ink tags (# scene:name)
// Priority 2: text keyword fallback
function setSceneFromTags(tags) {
    for (const tag of tags) {
        const sceneMatch = tag.match(/^scene:(\w+)$/);
        if (sceneMatch) {
            const name = sceneMatch[1];
            if (name !== currentScene) {
                currentScene = name;
                sceneEl.className = 'scene-' + name;
                if (window.setP5Scene) window.setP5Scene(name);
                window._currentScene = name;
                if (window.playSceneMusic && typeof audioPlaying !== 'undefined' && audioPlaying) {
                    window.playSceneMusic(name);
                }
            }
            return true;
        }
    }
    return false;
}

function processSfxTags(tags) {
    for (const tag of tags) {
        const sfxMatch = tag.match(/^sfx:(\w+)$/);
        if (sfxMatch && window.playSfx) {
            window.playSfx(sfxMatch[1]);
        }
    }
}

function setScene(text) {
    const t = text.toLowerCase();
    let name = 'room';
    if (t.includes('crisis') || t.includes('derailing') || t.includes('rupture')) name = 'crisis';
    else if (t.includes('cosmic') || t.includes('neganthropomorph') || t.includes('perpendicular')) name = 'cosmic';
    else if (t.includes('quantum') || t.includes('telepathy') || t.includes('psionic') || t.includes('magick')) name = 'quantum';
    else if (t.includes('river city') || t.includes('granar') || t.includes('temple') || t.includes('chant-master') ||
             t.includes('feudal') || t.includes('colonial') || t.includes('teotihuacan')) name = 'history';
    else if (t.includes('chat') || t.includes('agent') || t.includes('output') || t.includes('prompt')) name = 'chat';

    if (name === currentScene) return;
    currentScene = name;
    sceneEl.className = 'scene-' + name;

    // Update p5.js generative visuals to match
    if (window.setP5Scene) window.setP5Scene(name);

    // Update dynamic music to match scene
    window._currentScene = name;
    if (window.playSceneMusic && typeof audioPlaying !== 'undefined' && audioPlaying) {
        window.playSceneMusic(name);
    }
}

// ===== RENDER STORY =====
function renderStory() {
    let paragraphs = [];
    let allTags = [];
    while (story.canContinue) {
        let text = story.Continue();
        if (text && text.trim()) paragraphs.push(text.trim());
        // Collect ink tags
        if (story.currentTags && story.currentTags.length > 0) {
            allTags.push(...story.currentTags);
        }
    }

    if (paragraphs.length === 0) {
        if (story.currentChoices.length > 0) showChoices();
        else if (!story.canContinue) showEnding();
        return;
    }

    // Process SFX tags first (e.g., # sfx:companion, # sfx:ending_resolve)
    const fullText = paragraphs.join(' ');
    if (allTags.length > 0) {
        processSfxTags(allTags);
        // Scene detection: try ink tags first, fall back to text keywords
        if (!setSceneFromTags(allTags)) {
            setScene(fullText);
        }
    } else {
        // Fallback to text keyword detection
        setScene(fullText);
    }

    // ASCII art detection
    const artName = detectAsciiArt(fullText);
    if (artName && artName !== lastArt) {
        lastArt = artName;
        const artEl = renderAsciiArt(artName);
        if (artEl) storyContent.appendChild(artEl);
    }

    // Build section
    const section = document.createElement('div');
    section.className = 'story-section';

    // Detect stat-dump lines from ink and suppress them in favor of styled block
    // Matches: -- Read:6 Weave:2 Play:4 ... --  or  -- Quantum - Tele:2 Psion:1 ... --
    const statLinePattern = /^--\s*\w[\w\s-]*:\d+.*--$/;
    const endOutputPattern = /^--\s*End output\s*--$/i;
    const focusPromptPattern = /^Choose your focus/i;
    let hasStatDump = false;

    paragraphs.forEach(p => {
        // Stat-dump lines (-- Read:6 Weave:2 ... --)
        if (statLinePattern.test(p)) {
            hasStatDump = true;
            return; // suppress
        }

        // "End output --" — suppress always (it's just a marker), but don't trigger stats block
        if (endOutputPattern.test(p)) {
            return; // suppress
        }

        // "Choose your focus:" prompt
        if (focusPromptPattern.test(p)) {
            return; // suppress
        }

        // Section headers (-- TITLE --)
        const headerMatch = p.match(/^--\s*(.+?)\s*--$/);
        if (headerMatch) {
            const hdr = document.createElement('div');
            hdr.className = 'section-header';
            hdr.textContent = headerMatch[1];
            section.appendChild(hdr);
            return;
        }

        // Agent dialogue (quoted)
        if (p.startsWith('"') && p.endsWith('"') && p.length > 30) {
            const el = document.createElement('p');
            el.className = 'agent-text';
            el.textContent = p.slice(1, -1);
            section.appendChild(el);
            addToLog('the agent', p.slice(1, -1));
            return;
        }

        // Player/narrator text
        const el = document.createElement('p');
        el.className = 'narrator-text';
        el.textContent = p;
        section.appendChild(el);
        addToLog('', p);
    });

    storyContent.appendChild(section);

    // Replace raw stat dump with styled status report block
    if (hasStatDump) {
        renderInlineStats(section);
    }

    // Always update the snapshot so changes accumulate correctly
    prevStatSnapshot = snapshotStats() || prevStatSnapshot;

    // Feed game variables to music modulation after each story beat
    if (window.applyGameModulation) {
        try { window.applyGameModulation(story.variablesState); } catch(e) {}
    }

    // Scroll to the start of the new section
    requestAnimationFrame(() => {
        scrollToElement(section);
    });

    // Show choices if available
    if (story.currentChoices.length > 0) {
        showChoices();
    } else if (!story.canContinue) {
        showEnding();
    }
}

// ===== CHOICES =====

function showChoices() {
    // Clean up any body-appended tooltips from previous choices
    document.querySelectorAll('.choice-tooltip').forEach(el => el.remove());
    choicesInner.innerHTML = '';
    choicesArea.classList.add('open');
    updateScrollHint();

    story.currentChoices.forEach((choice, i) => {
        const card = document.createElement('div');
        card.className = 'choice-card';
        const tooltip = getChoiceTooltip(choice.text);
        const emojiHtml = tooltip ? `<span class="choice-emoji">${tooltip.emoji}</span>` : '';
        card.innerHTML = `<span class="choice-text">${emojiHtml}${choice.text}</span><span class="choice-index">&rarr;</span>`;

        // Append tooltip to body so it can't interfere with card hover/layout
        let tooltipEl = null;
        if (tooltip) {
            tooltipEl = document.createElement('div');
            tooltipEl.className = 'choice-tooltip';
            tooltipEl.textContent = tooltip.tooltip;
            tooltipEl.style.display = 'none';
            document.body.appendChild(tooltipEl);

            card.addEventListener('mouseenter', () => {
                const rect = card.getBoundingClientRect();
                tooltipEl.style.top = (rect.top - 8) + 'px';
                tooltipEl.style.left = Math.max(8, rect.left + rect.width / 2 - 140) + 'px';
                tooltipEl.style.display = 'block';
                requestAnimationFrame(() => {
                    tooltipEl.style.top = (rect.top - tooltipEl.offsetHeight - 8) + 'px';
                });
            });
            card.addEventListener('mouseleave', () => {
                tooltipEl.style.display = 'none';
            });
        }

        card.addEventListener('click', () => {
            choicesArea.classList.remove('open');
            // Play choice SFX
            if (window.playSfx) window.playSfx('choice');
            story.ChooseChoiceIndex(i);
            addToLog('You', choice.text);

            // Show player's choice in story
            const choiceSection = document.createElement('div');
            choiceSection.className = 'story-section';
            const el = document.createElement('p');
            el.className = 'player-text';
            el.style.color = 'var(--accent)';
            el.textContent = '> ' + choice.text;
            choiceSection.appendChild(el);
            storyContent.appendChild(choiceSection);

            setTimeout(() => {
                renderStory();
            }, 150);
        });
        choicesInner.appendChild(card);
    });

    // Scroll so new text before choices is visible
    requestAnimationFrame(() => {
        const lastSection = storyContent.lastElementChild;
        if (lastSection) scrollToElement(lastSection);
    });
}

// ===== ENDING =====
function showEnding() {
    endingReached = true;

    // Switch to ending scene music
    window._currentScene = 'ending';
    if (window.playSceneMusic && typeof audioPlaying !== 'undefined' && audioPlaying) {
        window.playSceneMusic('ending');
    }
    if (window.setP5Scene) window.setP5Scene('ending');
    if (window.playSfx) window.playSfx('ending_resolve');

    // Find ending title from recent log
    const recent = historyLog.slice(-20);
    let title = 'THE END';
    let body = [];

    for (let i = recent.length - 1; i >= 0; i--) {
        const t = recent[i].text.trim();
        if (t === t.toUpperCase() && t.length > 3 && t.length < 60 && !t.includes(':')) {
            title = t;
            break;
        }
        body.unshift(t);
    }
    if (body.length === 0) body = ['The story has ended.'];

    $('ending-title').textContent = title;
    $('ending-body').textContent = body.join(' ').slice(0, 2000);
    $('ending-overlay').classList.add('open');
    sceneEl.className = 'scene-ending';
}

// ===== LOG =====
function addToLog(speaker, text) {
    historyLog.push({ speaker, text });
    const entry = document.createElement('div');
    entry.className = 'log-entry' + (speaker === 'the agent' ? ' agent-entry' : '');
    if (speaker) {
        const tag = document.createElement('div');
        tag.className = 'speaker-tag';
        tag.textContent = speaker;
        entry.appendChild(tag);
    }
    const content = document.createElement('div');
    content.textContent = text;
    entry.appendChild(content);
    historyPanel.appendChild(entry);
}


// ===== EVENT HANDLERS =====
let statsOpen = false;
$('stats-btn').addEventListener('click', () => {
    statsOpen = !statsOpen;
    if (statsOpen) { updateStats(); statsPanel.classList.add('open'); }
    else statsPanel.classList.remove('open');
});

let logOpen = false;
$('log-btn').addEventListener('click', () => {
    logOpen = !logOpen;
    if (logOpen) {
        historyPanel.classList.add('open');
        $('history-close').style.display = 'block';
        historyPanel.scrollTop = historyPanel.scrollHeight;
    } else {
        historyPanel.classList.remove('open');
        $('history-close').style.display = 'none';
    }
});

$('history-close').addEventListener('click', () => {
    logOpen = false;
    historyPanel.classList.remove('open');
    $('history-close').style.display = 'none';
});

// ===== LOAD =====
async function loadStory() {
    try {
        const resp = await fetch('inkle/story.json');
        if (!resp.ok) throw new Error('Could not load story.json: ' + resp.status);
        const json = await resp.json();
        if (typeof inkjs === 'undefined') throw new Error('inkjs not loaded');
        story = new inkjs.Story(json);
        window._story = story;
        $('loading-screen').classList.add('hidden');
        setTimeout(() => $('loading-screen').style.display = 'none', 1000);
        renderStory();
    } catch (err) {
        $('loading-screen').textContent = 'Error: ' + err.message;
        console.error(err);
    }
}

loadStory();
