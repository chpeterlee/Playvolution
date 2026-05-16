// ===== P5.JS GENERATIVE BACKGROUND =====
let p5Scene = 'room';
let p5Transition = 0;
let p5TargetScene = 'room';

const p5Sketch = (p) => {
    let particles = [];
    const maxParticles = 60;

    p.setup = function() {
        const cnv = p.createCanvas(p.windowWidth, p.windowHeight);
        cnv.parent('p5-canvas');
        p.noiseSeed(42);
        p.colorMode(p.HSB, 360, 100, 100, 100);
        p.frameRate(30);

        for (let i = 0; i < maxParticles; i++) {
            particles.push({
                x: p.random(p.width),
                y: p.random(p.height),
                vx: 0, vy: 0,
                size: p.random(1, 2.5),
                life: p.random(0.3, 1)
            });
        }
    };

    p.draw = function() {
        p.background(0, 0, 0, 8); // slow fade
        const t = p.frameCount * 0.005;

        // Scene parameters
        const sceneParams = getSceneParams(p5Scene);
        p5Transition = p.lerp(p5Transition, 1, 0.02);

        switch (sceneParams.style) {
            case 'flow':
                drawFlowField(p, t, sceneParams);
                break;
            case 'network':
                drawNetwork(p, t, sceneParams);
                break;
            case 'rings':
                drawRings(p, t, sceneParams);
                break;
            case 'glitch':
                drawGlitch(p, t, sceneParams);
                break;
            case 'constellation':
                drawConstellation(p, t, sceneParams);
                break;
            default:
                drawFlowField(p, t, sceneParams);
        }
    };

    p.windowResized = function() {
        p.resizeCanvas(p.windowWidth, p.windowHeight);
    };

    // ===== SCENE DRAWING FUNCTIONS =====

    function drawFlowField(p, t, params) {
        const scale = 0.003;
        const h = params.hue;
        p.noStroke();
        for (let i = 0; i < particles.length; i++) {
            const pt = particles[i];
            const angle = p.noise(pt.x * scale, pt.y * scale, t * params.speed) * p.TWO_PI * 2;
            pt.vx = p.lerp(pt.vx, p.cos(angle) * params.force, 0.1);
            pt.vy = p.lerp(pt.vy, p.sin(angle) * params.force, 0.1);
            pt.x += pt.vx;
            pt.y += pt.vy;
            if (pt.x < 0) pt.x = p.width;
            if (pt.x > p.width) pt.x = 0;
            if (pt.y < 0) pt.y = p.height;
            if (pt.y > p.height) pt.y = 0;
            p.fill(h, params.sat, params.bri, pt.life * params.alpha * 60);
            p.circle(pt.x, pt.y, pt.size * params.sizeMul);
        }
    }

    function drawNetwork(p, t, params) {
        const count = 25;
        const pts = [];
        for (let i = 0; i < count; i++) {
            const x = p.width * 0.5 + p.cos(t * params.speed + i * 0.8) * p.width * 0.3 * p.sin(i * 0.3);
            const y = p.height * 0.5 + p.sin(t * params.speed * 0.7 + i * 1.1) * p.height * 0.3 * p.cos(i * 0.4);
            pts.push({ x, y });
            p.noStroke();
            p.fill(params.hue, params.sat, params.bri, params.alpha * 40);
            p.circle(x, y, 3);
        }
        // connections
        p.stroke(params.hue, params.sat, params.bri, params.alpha * 12);
        p.strokeWeight(0.5);
        for (let i = 0; i < pts.length; i++) {
            for (let j = i + 1; j < pts.length; j++) {
                const d = p.dist(pts[i].x, pts[i].y, pts[j].x, pts[j].y);
                if (d < 150) {
                    p.line(pts[i].x, pts[i].y, pts[j].x, pts[j].y);
                }
            }
        }
    }

    function drawRings(p, t, params) {
        p.noFill();
        const cx = p.width / 2;
        const cy = p.height / 2;
        for (let i = 0; i < 8; i++) {
            const r = 50 + i * 40 + p.sin(t * params.speed + i * 0.5) * 20;
            const wobble = p.noise(i * 0.5, t * params.speed) * 30;
            p.stroke(params.hue + i * 5, params.sat, params.bri, params.alpha * 15);
            p.strokeWeight(1);
            p.beginShape();
            for (let a = 0; a < p.TWO_PI; a += 0.1) {
                const rr = r + p.sin(a * 3 + t * 2) * wobble;
                p.vertex(cx + p.cos(a) * rr, cy + p.sin(a) * rr);
            }
            p.endShape(p.CLOSE);
        }
    }

    function drawGlitch(p, t, params) {
        // Horizontal glitch bars
        for (let i = 0; i < 8; i++) {
            const y = p.random(p.height);
            const h = p.random(1, 6);
            const offset = p.random(-30, 30) * (p.noise(t * 5, i) - 0.5) * 2;
            p.noStroke();
            p.fill(params.hue + p.random(-20, 20), params.sat, params.bri, params.alpha * 20);
            p.rect(offset, y, p.width, h);
        }
        // Scattered particles
        p.noStroke();
        for (let i = 0; i < 15; i++) {
            const x = p.random(p.width);
            const y = p.random(p.height);
            const s = p.random(2, 6);
            p.fill(params.hue, params.sat, params.bri, p.random(5, 25));
            p.rect(x, y, s, s * p.random(0.2, 3));
        }
    }

    function drawConstellation(p, t, params) {
        const count = 30;
        p.noStroke();
        for (let i = 0; i < count; i++) {
            const seed = i * 100;
            const x = (p.noise(seed, t * params.speed * 0.3) * 1.4 - 0.2) * p.width;
            const y = (p.noise(seed + 50, t * params.speed * 0.3) * 1.4 - 0.2) * p.height;
            const s = 1 + p.sin(t * 2 + i) * 0.8;
            const a = (0.1 + p.sin(t + i * 0.5) * 0.08) * params.alpha * 50;
            p.fill(params.hue + p.sin(i * 0.3) * 15, params.sat * 0.5, params.bri, a);
            p.circle(x, y, s + 1);
            // occasional bright star
            if (i % 7 === 0) {
                p.fill(params.hue, params.sat * 0.3, 100, a * 1.5);
                p.circle(x, y, s * 0.5);
            }
        }
    }

    function getSceneParams(scene) {
        const presets = {
            room:       { style: 'flow',         hue: 35,  sat: 40, bri: 50, speed: 0.5, force: 0.8, alpha: 0.5, sizeMul: 1.0 },
            chat:       { style: 'network',       hue: 210, sat: 30, bri: 55, speed: 0.6, force: 0.5, alpha: 0.6, sizeMul: 0.8 },
            history:    { style: 'rings',          hue: 25,  sat: 50, bri: 45, speed: 0.3, force: 0.6, alpha: 0.5, sizeMul: 1.2 },
            cosmic:     { style: 'constellation',  hue: 270, sat: 40, bri: 60, speed: 0.4, force: 0.3, alpha: 0.7, sizeMul: 0.6 },
            quantum:    { style: 'flow',           hue: 200, sat: 35, bri: 55, speed: 0.8, force: 1.2, alpha: 0.5, sizeMul: 0.7 },
            crisis:     { style: 'glitch',         hue: 0,   sat: 60, bri: 50, speed: 1.0, force: 2.0, alpha: 0.8, sizeMul: 1.5 },
            ending:     { style: 'constellation',  hue: 140, sat: 30, bri: 50, speed: 0.2, force: 0.2, alpha: 0.4, sizeMul: 0.5 }
        };
        return presets[scene] || presets.room;
    }
};

// Initialize p5
new p5(p5Sketch);

// Scene setter called by the game engine
window.setP5Scene = function(sceneName) {
    if (sceneName === p5Scene) return;
    p5Scene = sceneName;
};

window.setP5Scene('room');
