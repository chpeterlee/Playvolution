// ===== STRUDEL DYNAMIC MUSIC ENGINE =====
let strudelReady = false;
let audioPlaying = false;
let masterVolume = 0.7;
let currentMusicScene = 'room';
let currentModulation = null;
let lastModulation = { entropy: 0, signal: 0, tempo: 0 };
let currentChapter = 1;
let activePatterns = [];

// --- Compute modulation parameters from ink game variables ---
function computeModulation(vars) {
    const entropy = vars.entropiric_saturation || 40;
    const signal = vars.neganthropomorphic_signal || 10;
    const tempo = vars.operational_tempo || 10;
    const fear = vars.public_fear || 30;
    const fidelity = vars.augmentation_fidelity || 50;
    const awareness = vars.cosmic_awareness || 0;
    const chapter = vars.chapter || 1;

    // Filter sweep range: wider with higher fidelity/awareness, compressed by entropy
    const cutoffLow = Math.max(100, 200 - (entropy - 40) * 3);
    const cutoffHigh = Math.max(cutoffLow + 200, Math.min(6000,
        1200 + (fidelity - 50) * 15 + awareness * 20));

    // Gain: slightly louder with more fear
    const gainBase = 0.06 + (fear - 30) * 0.0003;
    const gain = Math.max(0.03, Math.min(0.12, gainBase));

    // Reverb: deeper with more signal/awareness
    const roomBase = 0.3 + (signal - 10) * 0.004 + awareness * 0.008;
    const room = Math.max(0.1, Math.min(0.85, roomBase));

    // Harmonic rhythm speed
    const speedDiv = Math.max(1, 5 - Math.floor(tempo / 10));

    // Chapter progression: layering density and brightness
    const chapterLayer = Math.min(4, Math.floor((chapter - 1) / 2));
    const chapterBrightness = Math.min(1, (chapter - 1) * 0.12);

    // Delay mix increases with cosmic awareness
    const delayAmt = Math.max(0.1, Math.min(0.6, 0.2 + awareness * 0.03));

    // Rhythmic density from operational tempo
    const rhythmicDensity = Math.max(3, Math.min(8, Math.floor(tempo / 5)));

    return {
        cutoffLow, cutoffHigh, gain, room, speedDiv,
        entropy, signal, tempo, fear, chapter, chapterLayer, chapterBrightness,
        delayAmt, rhythmicDensity, awareness
    };
}

// --- Helper: clamp a room value to safe bounds ---
function clampRoom(v) { return Math.max(0.05, Math.min(0.95, v)); }

// --- Build pattern objects for a scene (direct Strudel API, no string eval) ---
function buildPatterns(sceneName, mod) {
    if (!mod) mod = {
        cutoffLow: 200, cutoffHigh: 1200, gain: 0.06, room: 0.4,
        speedDiv: 2, chapterLayer: 0, chapterBrightness: 0,
        delayAmt: 0.2, rhythmicDensity: 4, awareness: 0
    };

    const vol = masterVolume;
    const gn = mod.gain * vol;
    const cutLo = mod.cutoffLow;
    const cutHi = mod.cutoffHigh;
    const rm = mod.room;
    const spd = mod.speedDiv;
    const layer = mod.chapterLayer;
    const dly = mod.delayAmt;

    const pats = [];

    const scenes = {

        // ── ROOM: Introspective, evolving ambient ──────────────────────
        room: () => {
            // Bass drone: deep sawtooth with slow sine filter sweep
            pats.push(
                note('c2').s('sawtooth')
                    .cutoff(sine.range(cutLo, cutHi * 0.4).slow(8))
                    .gain(gn * 0.7).attack(0.6).release(1.8)
                    .room(clampRoom(rm)).roomsize(9).orbit(1)
            );
            // Harmonic pad: slow Cm→Eb→Ab→Gm chord cycle, triangle warmth
            pats.push(
                note('<[c3,eb3,g3] [eb3,g3,bb3] [ab2,c3,eb3] [g2,bb2,d3]>').s('triangle')
                    .cutoff(sine.range(cutLo * 1.5, cutHi * 0.6).slow(6))
                    .gain(gn * 0.5).attack(0.8).release(1.2)
                    .slow(spd).room(clampRoom(rm + 0.1)).orbit(1)
            );
            // Atmosphere: perlin-modulated high shimmer
            pats.push(
                note('<c5 eb5 g5>').s('sine')
                    .gain(perlin.range(0, gn * 0.2).slow(4))
                    .attack(1.0).release(2.0)
                    .slow(spd + 3).room(clampRoom(rm + 0.3)).orbit(3)
            );
            // Ch2+: Rhythmic Euclidean pulse with octave jux
            if (layer >= 1) {
                pats.push(
                    note('c3').euclid(3, 8).s('triangle')
                        .cutoff(cutHi * 0.6).gain(gn * 0.35)
                        .attack(0.04).release(0.15)
                        .delay(dly).delaytime(0.25).delayfeedback(0.3).orbit(2)
                        .jux(x => x.add(7))
                );
            }
            // Ch3+: Melodic fragments with probabilistic transposition
            if (layer >= 2) {
                pats.push(
                    note('<c4 eb4 g4 bb3>').s('sine').euclid(5, 12)
                        .gain(gn * 0.25).attack(0.1).release(0.35)
                        .room(clampRoom(rm + 0.2)).orbit(3)
                        .sometimes(x => x.add(7))
                        .rarely(x => x.fast(2))
                        .jux(rev)
                );
            }
            // Ch4+: Textural rhythm with degradation
            if (layer >= 3) {
                pats.push(
                    note('<eb4 g4 bb4>').s('triangle')
                        .euclid(7, 16).gain(gn * 0.15)
                        .attack(0.02).release(0.1)
                        .cutoff(sine.range(800, cutHi).slow(3))
                        .delay(dly * 0.5).delaytime(1 / 6).delayfeedback(0.5)
                        .orbit(4).degradeBy(0.3)
                );
            }
            // Ch5+: Sub-bass undertone with slow pulse
            if (layer >= 4) {
                pats.push(
                    note('<c1 g1>').s('sine')
                        .gain(gn * 0.2).attack(1.5).release(3.0)
                        .slow(8).room(clampRoom(rm + 0.15)).roomsize(12).orbit(5)
                        .sometimes(x => x.cutoff(sine.range(60, 200).slow(4)))
                );
            }
        },

        // ── CHAT: Analytical, conversational counterpoint ──────────────
        chat: () => {
            // Moving bassline: A→E→A→D with stereo reverse
            pats.push(
                note('<a2 e3 a2 d3>').s('triangle')
                    .cutoff(sine.range(cutLo, cutHi * 0.5).slow(4))
                    .gain(gn * 0.6).attack(0.15).release(0.4)
                    .slow(spd).room(clampRoom(rm * 0.8)).orbit(1)
                    .jux(rev)
            );
            // Pad: Am→G→F→E chord cycle with subtle stereo widening
            pats.push(
                note('<[a3,c4,e4] [g3,b3,d4] [f3,a3,c4] [e3,g3,b3]>').s('triangle')
                    .cutoff(sine.range(cutLo * 2, cutHi * 0.7).slow(5))
                    .gain(gn * 0.4).attack(0.3).release(0.6)
                    .slow(spd).room(clampRoom(rm)).orbit(1)
                    .jux(x => x.rev().late(0.05))
            );
            // Ch2+: Faster Euclidean rhythmic pulse with interval variation
            if (layer >= 1) {
                pats.push(
                    note('<a3 c4>').s('triangle').euclid(5, 8)
                        .cutoff(cutHi * 0.5).gain(gn * 0.3)
                        .attack(0.03).release(0.12)
                        .delay(dly).delaytime(1 / 8).delayfeedback(0.35).orbit(2)
                        .sometimes(x => x.add(5))
                );
            }
            // Ch3+: Counter-melody with perlin filter evolution
            if (layer >= 2) {
                pats.push(
                    note('<e4 a4 c5 b4>').s('sine')
                        .cutoff(perlin.range(cutLo * 3, cutHi).slow(3))
                        .gain(gn * 0.2).attack(0.1).release(0.3)
                        .euclid(3, 8).room(clampRoom(rm + 0.15)).orbit(3)
                        .rarely(x => x.add(12))
                );
            }
            // Ch4+: Glitch texture — sparse, degraded
            if (layer >= 3) {
                pats.push(
                    note('<a5 c6>').s('sine')
                        .gain(gn * 0.08).attack(0.01).release(0.05)
                        .euclid(mod.rhythmicDensity, 16).orbit(4)
                        .degradeBy(0.5)
                        .delay(0.4).delaytime(1 / 12).delayfeedback(0.6)
                );
            }
            // Ch5+: Subtle sub-harmonic movement
            if (layer >= 4) {
                pats.push(
                    note('<a1 e1>').s('sawtooth')
                        .cutoff(sine.range(50, 150).slow(10))
                        .gain(gn * 0.15).attack(1.0).release(2.0)
                        .slow(6).room(clampRoom(rm + 0.1)).roomsize(8).orbit(5)
                );
            }
        },

        // ── HISTORY: Orchestral weight, narrative gravitas ─────────────
        history: () => {
            // Deep bass drone: D sawtooth, dark and heavy
            pats.push(
                note('d2').s('sawtooth')
                    .cutoff(sine.range(cutLo * 0.5, cutHi * 0.3).slow(10))
                    .gain(gn * 0.8).attack(0.7).release(2.0)
                    .room(clampRoom(rm + 0.1)).roomsize(10).orbit(1)
            );
            // Harmonic progression: Dm→Bb→Gm→A with time-offset stereo
            pats.push(
                note('<[d3,f3,a3] [bb2,d3,f3] [g2,bb2,d3] [a2,cs3,e3]>').s('sawtooth')
                    .cutoff(sine.range(cutLo * 2, cutHi * 0.5).slow(8))
                    .gain(gn * 0.45).attack(0.6).release(1.0)
                    .slow(Math.max(2, spd)).room(clampRoom(rm + 0.15)).orbit(1)
                    .jux(x => x.rev().late(0.05))
            );
            // Atmosphere: high harmonics with perlin gain (breathing)
            pats.push(
                note('<d5 f5 a5>').s('sine')
                    .gain(perlin.range(0, gn * 0.15).slow(6))
                    .attack(0.8).release(1.5)
                    .slow(Math.max(3, spd + 2)).room(clampRoom(rm + 0.25)).orbit(3)
            );
            // Ch2+: Ostinato rhythm with occasional reversal
            if (layer >= 1) {
                pats.push(
                    note('<d3 a3 d4 a3>').s('triangle').euclid(5, 12)
                        .cutoff(sine.range(cutLo * 3, cutHi * 0.7).slow(4))
                        .gain(gn * 0.3).attack(0.05).release(0.2)
                        .delay(dly).delaytime(3 / 16).delayfeedback(0.4).orbit(2)
                        .sometimes(x => x.rev())
                );
            }
            // Ch3+: Haunting melody with sparse high notes
            if (layer >= 2) {
                pats.push(
                    note('<a4 d5 f5 e5 d5 c5>').s('sine').euclid(7, 16)
                        .gain(gn * 0.2).attack(0.15).release(0.4)
                        .room(clampRoom(rm + 0.2)).orbit(3)
                        .sometimes(x => x.add(7))
                        .rarely(x => x.add(-12))
                );
            }
            // Ch4+: String-like sustained layer with superimposed fifth
            if (layer >= 3) {
                pats.push(
                    note('<d4 f4 a4 d5>').s('sawtooth')
                        .cutoff(cutHi * 0.4).gain(gn * 0.12)
                        .attack(0.4).release(0.8)
                        .slow(Math.max(3, spd)).room(clampRoom(rm + 0.2)).orbit(4)
                        .superimpose(x => x.add(7))
                );
            }
            // Ch5+: Sub-bass pulse
            if (layer >= 4) {
                pats.push(
                    note('<d1 a1>').s('sine').euclid(2, 8)
                        .gain(gn * 0.2).attack(0.8).release(1.5)
                        .slow(2).room(clampRoom(rm + 0.1)).roomsize(12).orbit(5)
                );
            }
        },

        // ── COSMIC: Ethereal, expansive, wide stereo ──────────────────
        cosmic: () => {
            // Deep bass: E2 sine, very slow
            pats.push(
                note('e2').s('sine')
                    .gain(gn * 0.6).attack(0.8).release(2.0)
                    .slow(4).room(clampRoom(rm + 0.2)).roomsize(12).orbit(1)
            );
            // Ethereal pad: Em7→Dm7→Cmaj7→Bm7 with wide stereo offset
            pats.push(
                note('<[e3,g3,b3,d4] [d3,fs3,a3,c4] [c3,e3,g3,b3] [b2,d3,fs3,a3]>').s('sine')
                    .cutoff(sine.range(cutLo * 2, cutHi * 0.8).slow(8))
                    .gain(gn * 0.4).attack(1.0).release(1.5)
                    .slow(Math.max(3, spd + 1)).room(clampRoom(rm + 0.2)).orbit(1)
                    .jux(x => x.rev().late(0.1))
            );
            // Harmonic texture: perlin gain + sine filter modulation
            pats.push(
                note('<e5 g5 b5 e6>').s('sine')
                    .gain(perlin.range(0, gn * 0.12).slow(5))
                    .cutoff(sine.range(1000, cutHi * 1.5).slow(6))
                    .attack(1.2).release(2.5)
                    .slow(Math.max(4, spd + 2)).room(clampRoom(rm + 0.3)).orbit(3)
                    .sometimes(x => x.add(12))
            );
            // Ch2+: Slow heartbeat Euclidean pulse with fifth jux
            if (layer >= 1) {
                pats.push(
                    note('e3').euclid(2, 8).s('sine')
                        .cutoff(cutHi * 0.3).gain(gn * 0.3)
                        .attack(0.2).release(0.5)
                        .slow(2).room(clampRoom(rm + 0.1)).orbit(2)
                        .jux(x => x.add(7))
                );
            }
            // Ch3+: Twinkling stars — sparse, degraded, delayed
            if (layer >= 2) {
                pats.push(
                    note('<b5 e6 g6>').s('sine')
                        .euclid(3, 16).gain(gn * 0.1)
                        .attack(0.05).release(0.3)
                        .delay(0.5).delaytime(3 / 8).delayfeedback(0.6).orbit(3)
                        .degradeBy(0.4)
                        .often(x => x.add(5))
                );
            }
            // Ch4+: Void drone — ultra-deep, ultra-reverb
            if (layer >= 3) {
                pats.push(
                    note('<e1 b1>').s('sine')
                        .gain(gn * 0.15).attack(2.0).release(4.0)
                        .slow(8).room(0.95).roomsize(15).orbit(4)
                );
            }
            // Ch5+: Cosmic shimmer with slow panning
            if (layer >= 4) {
                pats.push(
                    note('<fs6 a6 b6>').s('sine')
                        .gain(gn * 0.04).attack(0.5).release(1.5)
                        .slow(6).room(0.9).orbit(5)
                        .pan(sine.slow(3))
                        .degradeBy(0.3)
                );
            }
        },

        // ── QUANTUM: Energetic, polyrhythmic, glitchy ─────────────────
        quantum: () => {
            // Driving bass pattern with jux fast
            pats.push(
                note('<f2 f2 f3 eb2>').s('sawtooth')
                    .cutoff(sine.range(cutLo, cutHi * 0.6).slow(3))
                    .gain(gn * 0.55).attack(0.05).release(0.25)
                    .slow(spd).room(clampRoom(rm * 0.6)).orbit(1)
                    .jux(x => x.fast(1.5))
            );
            // Polyrhythmic lead: F minor with probabilistic variation
            pats.push(
                note('<f4 ab4 c5 eb5>').s('triangle')
                    .cutoff(perlin.range(cutLo * 3, cutHi).slow(4))
                    .gain(gn * 0.35).attack(0.08).release(0.3)
                    .euclid(5, 8).room(clampRoom(rm)).orbit(1)
                    .sometimes(x => x.add(7))
                    .sometimes(x => x.rev())
            );
            // Second polyrhythmic voice: (3,8) against (5,8)
            pats.push(
                note('<c5 f5 ab5>').s('sine')
                    .cutoff(sine.range(cutHi * 0.5, cutHi).slow(2))
                    .gain(gn * 0.2).attack(0.04).release(0.15)
                    .euclid(3, 8).room(clampRoom(rm + 0.1)).orbit(2)
                    .rarely(x => x.fast(2))
            );
            // Ch2+: Fast degraded glitch texture
            if (layer >= 1) {
                pats.push(
                    note('<f3 ab3 c4 eb4>').s('triangle')
                        .euclid(7, 16).gain(gn * 0.15)
                        .attack(0.02).release(0.08)
                        .cutoff(cutHi * 0.8).orbit(2)
                        .degradeBy(0.3)
                        .delay(dly).delaytime(1 / 8).delayfeedback(0.5)
                );
            }
            // Ch3+: Sustained harmony with phaser
            if (layer >= 2) {
                pats.push(
                    note('<[f3,ab3,c4] [eb3,g3,bb3]>').s('sawtooth')
                        .cutoff(sine.range(cutLo * 4, cutHi * 0.8).slow(6))
                        .gain(gn * 0.15).attack(0.3).release(0.6)
                        .slow(spd + 1).room(clampRoom(rm + 0.15)).orbit(3)
                        .phaser(2).phaserdepth(0.6)
                        .jux(rev)
                );
            }
            // Ch4+: Chaotic perlin texture
            if (layer >= 3) {
                pats.push(
                    note('<f5 ab5 c6>').s('sine')
                        .gain(perlin.range(0, gn * 0.1).slow(2))
                        .euclid(mod.rhythmicDensity, 16)
                        .attack(0.01).release(0.06)
                        .delay(0.6).delaytime(1 / 6).delayfeedback(0.7).orbit(4)
                        .degradeBy(0.4)
                );
            }
            // Ch5+: Rapid arpeggiation
            if (layer >= 4) {
                pats.push(
                    note('<f4 ab4 c5 f5 ab5 c6>').s('sine')
                        .gain(gn * 0.08).attack(0.01).release(0.04)
                        .fast(4).cutoff(sine.range(1000, cutHi).slow(2))
                        .room(clampRoom(rm + 0.1)).orbit(5)
                        .degradeBy(0.5)
                );
            }
        },

        // ── CRISIS: Urgent, compressed, dissonant ─────────────────────
        crisis: () => {
            // Aggressive bass with low cutoff and high gain
            pats.push(
                note('<c2 c2 ab2 b1>').s('sawtooth')
                    .cutoff(sine.range(cutLo * 0.3, cutHi * 0.2).slow(2))
                    .gain(gn * 1.2).attack(0.03).release(0.2)
                    .room(clampRoom(rm * 0.4)).orbit(1)
            );
            // Dissonant tension chord: Cm(add b) ↔ Cmaj7(b5)
            pats.push(
                note('<[c3,eb3,ab3,b3] [c3,e3,g3,bb3]>').s('sawtooth')
                    .cutoff(sine.range(cutLo, cutHi * 0.4).slow(3))
                    .gain(gn * 0.5).attack(0.05).release(0.3)
                    .slow(Math.min(2, spd)).room(clampRoom(rm * 0.5)).orbit(1)
                    .jux(x => x.rev().fast(1.5))
            );
            // Fast Euclidean pulse: (7,8) for maximum tension
            pats.push(
                note('c3').euclid(7, 8).s('sawtooth')
                    .cutoff(cutHi * 0.3).gain(gn * 0.4)
                    .attack(0.02).release(0.1).orbit(2)
            );
            // Ch2+: Degraded noise-like texture
            if (layer >= 1) {
                pats.push(
                    note('<c4 eb4 g4>').s('sawtooth')
                        .euclid(9, 16).gain(gn * 0.2)
                        .attack(0.01).release(0.06)
                        .cutoff(sine.range(cutHi * 0.2, cutHi * 0.5).slow(2))
                        .degradeBy(0.4).orbit(2)
                        .delay(0.2).delaytime(0.06).delayfeedback(0.5)
                );
            }
            // Ch3+: Alarm-like sparse high notes
            if (layer >= 2) {
                pats.push(
                    note('<c5 eb5>').s('sawtooth')
                        .euclid(3, 16).gain(gn * 0.15)
                        .attack(0.01).release(0.08)
                        .cutoff(cutHi * 0.6).orbit(3)
                        .sometimes(x => x.add(12))
                );
            }
            // Ch4+: Inharmonic drone with distortion
            if (layer >= 3) {
                pats.push(
                    note('<c2 ab1>').s('sawtooth')
                        .cutoff(cutLo * 0.5).gain(gn * 0.3)
                        .attack(0.3).release(0.5)
                        .slow(2).room(clampRoom(rm * 0.3)).orbit(4)
                        .distort(3).postgain(0.3)
                );
            }
            // Ch5+: Rapid stutter pattern
            if (layer >= 4) {
                pats.push(
                    note('<c4 eb4 g4 c5>').s('sawtooth')
                        .euclid(11, 16).gain(gn * 0.12)
                        .attack(0.01).release(0.03)
                        .cutoff(cutHi * 0.4).orbit(5)
                        .degradeBy(0.6)
                        .delay(0.3).delaytime(0.04).delayfeedback(0.6)
                );
            }
        },

        // ── ENDING: Resolved, warm, peaceful ──────────────────────────
        ending: () => {
            // Warm resolved bass: C→F
            pats.push(
                note('<c2 f2>').s('sine')
                    .gain(gn * 0.6).attack(0.8).release(2.0)
                    .slow(4).room(clampRoom(rm + 0.2)).roomsize(10).orbit(1)
            );
            // Resolution chords: C→F with superimposed octave
            pats.push(
                note('<[c4,e4,g4] [f4,a4,c5]>').s('sine')
                    .gain(gn * 0.5).attack(0.6).release(1.5)
                    .slow(5).room(clampRoom(rm + 0.25)).orbit(1)
                    .superimpose(x => x.add(12).gain(gn * 0.15))
            );
            // High shimmer: maximum reverb, very slow
            pats.push(
                note('<c6 e6 g6>').s('sine')
                    .gain(gn * 0.08).attack(1.5).release(3.0)
                    .slow(6).room(0.95).roomsize(15).orbit(3)
            );
        }
    };

    const builder = scenes[sceneName] || scenes.room;
    builder();

    // Append adaptive percussive patterns
    const percPatterns = buildPercussion(sceneName, mod);
    for (const p of percPatterns) {
        pats.push(p);
    }

    return pats;
}

// --- Build adaptive percussive patterns that respond to game state ---
// Uses synth-based percussion (noise bursts, sine clicks) so it works
// even without loaded drum samples. Falls back to sample names if available.
function buildPercussion(sceneName, mod) {
    if (!mod) mod = {
        gain: 0.06, chapterLayer: 0, speedDiv: 2, delayAmt: 0.2,
        entropy: 40, tempo: 10, fear: 30, signal: 10, awareness: 0,
        rhythmicDensity: 4
    };

    const vol = masterVolume;
    const gn = mod.gain * vol;
    const layer = mod.chapterLayer;
    const spd = mod.speedDiv;
    const dly = mod.delayAmt;
    const entropy = mod.entropy || 40;
    const tempo = mod.tempo || 10;
    const fear = mod.fear || 30;
    const signal = mod.signal || 10;

    // Percussion base gain: louder with more fear and chapter progression
    const percBase = gn * (0.5 + layer * 0.15 + Math.max(0, (fear - 30)) * 0.005);

    // Entropy drives random gaps (more entropy = more silence)
    const entDegrade = Math.min(0.6, Math.max(0, (entropy - 35) * 0.012));

    // Hihat density scales with operational tempo
    const hhPulse = Math.max(4, Math.min(10, Math.floor(tempo / 3)));

    // Percussion reverb scales with signal strength
    const percRoom = clampRoom(0.15 + (signal - 10) * 0.008);

    // Use orbits 10+ to keep percussion reverb/delay independent from melodic
    const PO = 10;

    // --- Synth-based drum builders (work without sample loading) ---
    const kick = (g) => note('c1').s('sine')
        .decay(0.12).sustain(0)
        .penv(-24).pattack(0.001).prelease(0.08)
        .gain(g);
    const snare = (g) => s('white')
        .decay(0.08).sustain(0)
        .gain(g).hpf(1200);
    const hatClosed = (g) => s('white')
        .decay(0.02).sustain(0)
        .gain(g).hpf(8000);
    const hatOpen = (g) => s('white')
        .decay(0.15).sustain(0)
        .gain(g).hpf(5000);
    const rimClick = (g) => note('c5').s('square')
        .decay(0.02).sustain(0)
        .gain(g).lpf(4000);
    const clap = (g) => s('white')
        .decay(0.06).sustain(0)
        .gain(g).bpf(1200).bpq(2);
    const tomLow = (g) => note('c2').s('sine')
        .decay(0.18).sustain(0)
        .penv(-12).pattack(0.001).prelease(0.1)
        .gain(g);
    const tomMid = (g) => note('e2').s('sine')
        .decay(0.15).sustain(0)
        .penv(-12).pattack(0.001).prelease(0.08)
        .gain(g);

    const pats = [];

    const perc = {

        // ── ROOM: Sparse, ghostly, atmospheric ────────────────────────
        room: () => {
            if (layer >= 1) {
                // Soft rim click, very sparse
                pats.push(
                    rimClick(percBase * 0.35)
                        .euclid(2, 16).slow(2)
                        .room(percRoom + 0.15).roomsize(6).orbit(PO)
                        .degradeBy(entDegrade + 0.3)
                );
            }
            if (layer >= 2) {
                // Whispered hihat, heavily degraded
                pats.push(
                    hatClosed(percBase * 0.18)
                        .euclid(hhPulse - 2, 16).slow(2)
                        .room(percRoom + 0.2).orbit(PO + 1)
                        .degradeBy(entDegrade + 0.5)
                        .sometimes(x => x.gain(percBase * 0.04))
                );
            }
            if (layer >= 3) {
                // Very sparse soft kick
                pats.push(
                    kick(percBase * 0.25)
                        .euclid(1, 8).slow(2)
                        .room(percRoom + 0.1).orbit(PO)
                        .degradeBy(entDegrade + 0.4)
                );
            }
            if (layer >= 4) {
                // Ghost note hihat with perlin gain
                pats.push(
                    hatClosed(perlin.range(0, percBase * 0.1).slow(3))
                        .struct('x ~ ~ x ~ ~ x ~ ~ ~ x ~ ~ ~ ~ ~')
                        .slow(2).orbit(PO + 2)
                        .room(percRoom + 0.3).roomsize(8)
                        .degradeBy(entDegrade + 0.2)
                );
            }
        },

        // ── CHAT: Light, articulate, conversational ───────────────────
        chat: () => {
            if (layer >= 1) {
                // Steady hihat pattern
                pats.push(
                    hatClosed(percBase * 0.28)
                        .euclid(hhPulse, 16)
                        .room(percRoom).orbit(PO + 1)
                        .sometimes(x => x.gain(percBase * 0.1))
                );
            }
            if (layer >= 2) {
                // Rim offbeats with delay
                pats.push(
                    rimClick(percBase * 0.35)
                        .euclid(3, 8).late(1 / 16)
                        .delay(dly * 0.5).delaytime(1 / 8).delayfeedback(0.3)
                        .room(percRoom).orbit(PO)
                        .degradeBy(entDegrade)
                );
            }
            if (layer >= 3) {
                // Soft kick on beat
                pats.push(
                    kick(percBase * 0.35)
                        .euclid(3, 8).slow(2)
                        .room(percRoom + 0.1).orbit(PO)
                        .sometimes(x => x.cutoff(200))
                );
            }
            if (layer >= 4) {
                // Open hihat ghost fills
                pats.push(
                    hatOpen(percBase * 0.15)
                        .euclid(2, 16)
                        .room(percRoom + 0.2).orbit(PO + 1)
                        .degradeBy(entDegrade + 0.4)
                );
            }
        },

        // ── HISTORY: Ritualistic, processed toms ──────────────────────
        history: () => {
            if (layer >= 1) {
                // Deep tom pulse, slow and ritualistic
                pats.push(
                    tomLow(percBase * 0.4)
                        .euclid(3, 8).slow(Math.max(2, spd))
                        .room(percRoom + 0.2).roomsize(8).orbit(PO)
                        .sometimes(x => x.cutoff(400))
                );
            }
            if (layer >= 2) {
                // Rim cross-rhythm, polyrhythmic against toms
                pats.push(
                    rimClick(percBase * 0.3)
                        .euclid(5, 12)
                        .delay(dly).delaytime(3 / 16).delayfeedback(0.4)
                        .room(percRoom + 0.1).orbit(PO + 1)
                        .degradeBy(entDegrade)
                );
            }
            if (layer >= 3) {
                // Snare with long delay tail
                pats.push(
                    snare(percBase * 0.28)
                        .euclid(2, 8).slow(2)
                        .delay(dly * 0.6).delaytime(1 / 4).delayfeedback(0.5)
                        .room(percRoom + 0.15).orbit(PO)
                        .degradeBy(entDegrade + 0.2)
                );
            }
            if (layer >= 4) {
                // Deep kick accent
                pats.push(
                    kick(percBase * 0.35)
                        .euclid(2, 16).slow(Math.max(2, spd))
                        .room(percRoom + 0.2).roomsize(10).orbit(PO)
                );
            }
        },

        // ── COSMIC: Minimal, cavernous, spacious ──────────────────────
        cosmic: () => {
            if (layer >= 1) {
                // Very sparse rim, heavy reverb
                pats.push(
                    rimClick(percBase * 0.15)
                        .euclid(1, 16).slow(2)
                        .room(percRoom + 0.4).roomsize(12).orbit(PO)
                        .degradeBy(entDegrade + 0.3)
                );
            }
            if (layer >= 2) {
                // Soft bass drum heartbeat, very slow
                pats.push(
                    kick(percBase * 0.15)
                        .euclid(2, 16).slow(4)
                        .room(percRoom + 0.3).roomsize(10).orbit(PO)
                        .sometimes(x => x.cutoff(200))
                );
            }
            if (layer >= 3) {
                // Crystalline hihat, mostly absent
                pats.push(
                    hatClosed(perlin.range(0, percBase * 0.12).slow(4))
                        .euclid(3, 16).slow(2)
                        .room(percRoom + 0.5).roomsize(15).orbit(PO + 1)
                        .degradeBy(entDegrade + 0.4)
                );
            }
            if (layer >= 4) {
                // Distant tom echo
                pats.push(
                    tomMid(percBase * 0.12)
                        .euclid(2, 12).slow(3)
                        .room(percRoom + 0.5).roomsize(14)
                        .delay(0.4).delaytime(3 / 8).delayfeedback(0.6)
                        .orbit(PO + 2)
                );
            }
        },

        // ── QUANTUM: Driving, polyrhythmic, glitchy ───────────────────
        quantum: () => {
            // Base: four-on-floor kick
            pats.push(
                kick(percBase * 0.5)
                    .struct('x ~ ~ ~ x ~ ~ ~')
                    .room(percRoom).orbit(PO)
            );
            // Base: polyrhythmic hihat against kick
            pats.push(
                hatClosed(percBase * 0.22)
                    .euclid(7, 16)
                    .room(percRoom).orbit(PO + 1)
                    .sometimes(x => x.gain(percBase * 0.06))
                    .degradeBy(entDegrade * 0.5)
            );
            if (layer >= 1) {
                // Snare backbeat with micro-timing variation
                pats.push(
                    snare(percBase * 0.38)
                        .struct('~ ~ x ~ ~ ~ x ~')
                        .room(percRoom + 0.1).orbit(PO)
                        .sometimes(x => x.late(1 / 16))
                        .rarely(x => x.gain(percBase * 0.15))
                );
            }
            if (layer >= 2) {
                // Open hihat offbeat fills
                pats.push(
                    hatOpen(percBase * 0.15)
                        .euclid(3, 16).late(1 / 16)
                        .delay(dly * 0.4).delaytime(1 / 8).delayfeedback(0.4)
                        .orbit(PO + 1)
                        .degradeBy(entDegrade + 0.3)
                );
            }
            if (layer >= 3) {
                // Clap accent with delay trail
                pats.push(
                    clap(percBase * 0.22)
                        .euclid(2, 8)
                        .delay(dly * 0.6).delaytime(1 / 6).delayfeedback(0.5)
                        .room(percRoom + 0.15).orbit(PO + 2)
                        .degradeBy(entDegrade)
                );
            }
            if (layer >= 4) {
                // Rapid glitch hihat bursts
                pats.push(
                    hatClosed(percBase * 0.12)
                        .fast(3).euclid(5, 8)
                        .orbit(PO + 3)
                        .degradeBy(entDegrade + 0.5)
                        .delay(dly * 0.3).delaytime(1 / 12).delayfeedback(0.6)
                );
            }
        },

        // ── CRISIS: Intense, aggressive, maximum density ──────────────
        crisis: () => {
            // Dense driving kick
            pats.push(
                kick(percBase * 0.55)
                    .euclid(5, 8)
                    .room(percRoom * 0.5).orbit(PO)
                    .distort(2).postgain(0.4)
            );
            // Urgent snare
            pats.push(
                snare(percBase * 0.4)
                    .euclid(3, 8).late(1 / 16)
                    .room(percRoom).orbit(PO)
                    .degradeBy(entDegrade * 0.5)
            );
            // Dense hihat: (7,8) maximum tension
            pats.push(
                hatClosed(percBase * 0.28)
                    .euclid(7, 8)
                    .orbit(PO + 1)
                    .degradeBy(entDegrade * 0.3)
            );
            if (layer >= 1) {
                // Rim reinforcement
                pats.push(
                    rimClick(percBase * 0.35)
                        .euclid(4, 16)
                        .delay(dly * 0.4).delaytime(0.06).delayfeedback(0.5)
                        .orbit(PO + 1)
                        .degradeBy(entDegrade)
                );
            }
            if (layer >= 2) {
                // Distorted clap accents
                pats.push(
                    clap(percBase * 0.28)
                        .euclid(5, 16)
                        .distort(4).postgain(0.3)
                        .room(percRoom).orbit(PO + 2)
                        .degradeBy(entDegrade + 0.3)
                );
            }
            if (layer >= 3) {
                // Rapid tom fills
                pats.push(
                    tomMid(percBase * 0.22)
                        .euclid(7, 16)
                        .room(percRoom + 0.1).orbit(PO)
                        .degradeBy(entDegrade + 0.2)
                );
            }
            if (layer >= 4) {
                // Maximum density: rapid kick stutter
                pats.push(
                    kick(percBase * 0.15)
                        .euclid(11, 16)
                        .room(percRoom * 0.3).orbit(PO)
                        .degradeBy(entDegrade + 0.2)
                );
            }
        },

        // ── ENDING: No percussion (peaceful resolution) ───────────────
        ending: () => { /* silence */ }
    };

    const builder = perc[sceneName] || perc.room;
    builder();
    return pats;
}

// --- Initialize Strudel (called on first user click) ---
async function initAudio() {
    if (strudelReady) return true;
    try {
        if (typeof initStrudel === 'function') {
            // Load drum sample library so s("bd"), s("hh"), etc. work
            const prebakeSamples = (typeof samples === 'function')
                ? () => samples('github:tidalcycles/dirt-samples')
                : undefined;
            await initStrudel(prebakeSamples ? { prebake: prebakeSamples } : undefined);
            strudelReady = true;
            console.log('Strudel audio initialized' + (prebakeSamples ? ' (with samples)' : ' (synth only)'));
            return true;
        }
        console.warn('Strudel not loaded');
        return false;
    } catch (e) {
        console.warn('Strudel init failed:', e.message);
        return false;
    }
}

// --- Start or switch to a scene's pattern ---
async function playSceneMusic(sceneName, mod) {
    if (!strudelReady) {
        const ok = await initAudio();
        if (!ok) return;
    }

    currentMusicScene = sceneName;
    currentModulation = mod || null;

    // Stop all current patterns
    stopMusic();

    // Build and play new patterns directly via Strudel API
    try {
        activePatterns = buildPatterns(sceneName, mod);
        for (const p of activePatterns) {
            p.play();
        }
        audioPlaying = true;
    } catch (e) {
        console.warn('Strudel direct play failed:', e.message);
        // Fallback: try evaluate() with a simple pattern string
        try {
            const fbGn = (0.05 * masterVolume).toFixed(4);
            evaluate(
                'note("<c3 [eb3 g3]>").s("sawtooth")' +
                '.cutoff(800).gain(' + fbGn + ')' +
                '.attack(0.3).release(0.8).slow(2).room(0.4)'
            );
            audioPlaying = true;
        } catch (e2) {
            console.warn('Strudel fallback failed:', e2.message);
        }
    }
}

// --- Stop all music ---
function stopMusic() {
    try { hush(); } catch (e) { /* ignore */ }
    activePatterns = [];
    audioPlaying = false;
}

// --- Sound effects: short Strudel patterns played on top of music ---
function playSfx(type) {
    if (!strudelReady) return;
    try {
        let p;
        switch (type) {
            case 'choice':
                p = note('c5').s('sine').gain(0.06).attack(0.01).release(0.12);
                break;
            case 'transition':
                p = note('<e4 g4>').s('triangle').gain(0.04)
                    .attack(0.02).release(0.25).room(0.3);
                break;
            case 'discovery':
                p = note('<a4 c5 e5>').s('sine').gain(0.05)
                    .attack(0.05).release(0.35).room(0.4)
                    .delay(0.3).delaytime(1 / 8).delayfeedback(0.3);
                break;
            case 'companion':
                p = note('<d4 f4 a4> <c4 e4 g4>').s('triangle').gain(0.04)
                    .attack(0.05).release(0.3).room(0.3)
                    .superimpose(x => x.add(7).gain(0.01));
                break;
            case 'crisis_alert':
                p = note('<c3 eb3>').s('sawtooth').cutoff(400).gain(0.08)
                    .attack(0.01).release(0.15)
                    .delay(0.4).delaytime(0.1).delayfeedback(0.5);
                break;
            case 'ending_resolve':
                p = note('<c4 e4 g4 c5>').s('sine').gain(0.05)
                    .attack(0.1).release(0.7).room(0.5).slow(2)
                    .superimpose(x => x.add(12).gain(0.015));
                break;
            default: return;
        }
        if (p && typeof p.play === 'function') {
            p.play();
        }
    } catch (e) {
        // SFX failure is non-critical
    }
}

// --- Called from updateStats / renderStory to re-evaluate with new modulation ---
function applyGameModulation(vars) {
    if (!audioPlaying || !strudelReady) return;

    const mod = computeModulation(vars);
    const scene = window._currentScene || 'room';

    // Track chapter changes
    if (vars.chapter && vars.chapter !== currentChapter) {
        currentChapter = vars.chapter;
    }

    // Only re-trigger if key variables changed significantly
    const entropyShift = Math.abs(mod.entropy - lastModulation.entropy);
    const signalShift = Math.abs(mod.signal - lastModulation.signal);
    const tempoShift = Math.abs(mod.tempo - lastModulation.tempo);

    if (entropyShift > 10 || signalShift > 8 || tempoShift > 5) {
        lastModulation = { entropy: mod.entropy, signal: mod.signal, tempo: mod.tempo };
        playSceneMusic(scene, mod);
    }
}

// --- Set master volume ---
function setMasterVolume(v) {
    masterVolume = Math.max(0, Math.min(1, v));
    // Re-evaluate current pattern with new volume
    if (audioPlaying && strudelReady) {
        const scene = window._currentScene || 'room';
        playSceneMusic(scene, currentModulation);
    }
}

// --- Audio toggle + volume slider ---
document.addEventListener('DOMContentLoaded', () => {
    const audioBtn = document.getElementById('audio-btn');
    if (!audioBtn) return;

    audioBtn.addEventListener('click', async () => {
        if (!audioPlaying) {
            const ok = await initAudio();
            if (ok) {
                const scene = window._currentScene || 'room';
                playSceneMusic(scene);
                audioBtn.textContent = 'MUSIC \u25CF';
                audioBtn.classList.add('active');
                document.getElementById('volume-slider')?.classList.add('visible');
            }
        } else {
            stopMusic();
            audioBtn.textContent = 'MUSIC';
            audioBtn.classList.remove('active');
            document.getElementById('volume-slider')?.classList.remove('visible');
        }
    });

    // Volume slider
    const volSlider = document.getElementById('volume-range');
    if (volSlider) {
        volSlider.addEventListener('input', (e) => {
            setMasterVolume(parseFloat(e.target.value));
        });
    }
});

// Expose for the game engine
window.playSceneMusic = playSceneMusic;
window.stopMusic = stopMusic;
window.applyGameModulation = applyGameModulation;
window.playSfx = playSfx;
window.setMasterVolume = setMasterVolume;
