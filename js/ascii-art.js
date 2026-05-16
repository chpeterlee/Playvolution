// ===== ASCII ART LIBRARY =====
const asciiArt = {
    desk: {
        theme: 'dim',
        art:
`                    _______________________
               |  ___________________  |
               | |                   | |
               | |    PLAYVOLUTION   | |
               | |   _____________   | |
               | |  |             |  | |
               | |  |  > _        |  | |
               | |  |             |  | |
               | |  |_____________|  | |
               | |___________________| |
               |_______________________|
                    |           |
               _____|___________|_____
              /                       \\`
    },

    agent: {
        theme: 'cosmic',
        art:
`              .     .       .  .   . .   .   . .    +
.    .        .      .    .    .__.   .    .
  .  .    .      .    __.---._  .    .    .     .
.    .    .  .  .'        '.   .    .   . .
  .    .    .    . /   ○    ○   \\    .   .    .
   .   .    .    |    _______    |  .    .    .
  .    .    . .   \\  '-------'  /   . .    .
.   .    .    '.           .'  .    .    .
  .    .   .    .   '-.___.-'   .    .    .   .
.    .    .    .    .    .    .    .    .
  .   .    .  .    . .   .    .  .    .   .    .`
    },

    agent_anomaly: {
        theme: 'cosmic',
        art:
`          .   *  .  . *       *   .    .   *   .
.  *       .    .    *   .    ◇     .     *
  .    .    *   .   / \\   .    .    *   .    .
.    .    .   . /   \\   .  .    .    .    *
  *   .    .    . /  ◇  \\    .   .    .   .
.   .    .   /  / \\  \\   .    .  *   .    .
  .    .  *   . | /  ◇  \\ |  .   .    .    .
.    .    . |/  / \\  \\|   .    .    .   *
  .   .    .    /  /   \\  \\    .   .    .    .
.    .    . |  ◇  ◇  |  .    .    .    .
  .    .   .    | / \\ / \\ |   .   .   .    .
.   .    .  |/   V   \\|  .    .    .    .`
    },

    city: {
        theme: 'dim',
        art:
`                  .  *  .     .   *    .  .
    *    .    .    .   *       .
.       .    .  *   .    .        .   *
    .      .    .     .    .  *
   ___   ___   .   ___   ___   ___   ___   ___
  |   | |   |     |   | |   | |   | |   | |   |
  |   | |   |     |   | |   | |   | |   | |   |
  |   | |   | .   |   | |   | |   | |   | |   |
  |___| |___|     |___| |___| |___| |___| |___|
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~ ~ ~~~~ ~ ~~ ~~~ ~ ~~ ~~~ ~~ ~ ~~~ ~~ ~~ ~~~~
  ~~~~~ ~~~ ~~~~~~ ~~~~ ~~~ ~~ ~~~~~ ~~ ~~~ ~~~~`
    },

    temple: {
        theme: 'ember',
        art:
`                        /\\
                   /  \\
                  / !! \\
                 /  !!  \\
                /   !!   \\
               /    !!    \\
              /_____||_____\\
             /  |   ||   |  \\
            /   |   ||   |   \\
           /    |   ||   |    \\
          /     |   ||   |     \\
         /      |___||___|      \\
        /\\      |   ||   |      /\\
       /  \\     |   ||   |     /  \\
      / .. \\    |   ||   |    / .. \\
     / ......\\  |___||___|  /...... \\
    /__________\\___________/__________\\
       |    |    |  |  |    |    |
       | .. |    |  |  |    | .. |
       |    |    |  |  |    |    |`
    },

    network: {
        theme: 'quantum',
        art:
`          . .  .    .   .  .    .  .   .
.  .    ○---○    .   ○---○    .  .
  .    .   / \\ / \\   .  / \\ / \\   .    .
.   ○---○---○---○---○---○---○   .
  .   /|\\ /|\\ /|\\ /|\\ /|\\ /|\\ /|\\  .
. ○---○---○---○---○---○---○---○ .
  .   \\|/ \\|/ \\|/ \\|/ \\|/ \\|/ \\|/  .
.   ○---○---○---○---○---○---○   .
  .    .   \\ / \\ /   .  \\ / \\ /   .    .
.  .    ○---○    .   ○---○    .  .
      . .  .    .   .  .    .  .   .`
    },

    signal: {
        theme: 'cosmic',
        art:
`
           .  *  .    .   *  .  .
     .  .    .    *   .    .    .   *
.  *    .  ╱ ╲  .    .  ╱ ╲  .    .   .
  .    .    .╱   ╲.   .  .╱   ╲.   .    .
.   .   ╱  ◇  ╲ .    ╱  ◇  ╲ .    .
  .    .   ╱ ╱ ╲ ╲.   .╱ ╱ ╲ ╲ .   .  .
.    .╱.╱   ╲.╲ . ╱.╱   ╲.╲  .    .
  .   . ╱ .     . ╲╱ .     . ╲ .   .
.  ╱    . *    .  ◇  . *    .  ╲ .    .
 ╲ .    .    .   .|  .    .   . ╱
  ╲  .    .   . * .|. .   .  .╱
   ◇ . *  . .  .  |  . .  . ◇
   |  .  .  . * . |. * .  .  |`
    },

    crisis: {
        theme: 'entropiric',
        art:
`
  .  *  .    .  .   *   .  .    .  *
.   \\  . /  .   \\  .  /  .   \\ .   /
   .  .  \\  / .  .  \\ . /  .  .  \\  / .
.  .  \\/  .  .  .\\|/.  .  .  \\/  .
   .  .  . || .  .  . || . . . . ||  .
.  . ./|\\ .  .  ./|\\. . . ./|\\  .
   .  . / . \\ .  . / . \\  . . / . \\  .
.  /  .  \\ .  /  .  \\ .  /  .  \\ .
 / .  .  . \\/ .  .  . \\/ .  .  . \\
~~~~~~~~ ~~~~~~~~ ~~~~~~~~ ~~~~~~~~
~ ~ ~~~ ~ ~ ~~ ~~ ~ ~ ~~~ ~ ~ ~~ ~~`
    },

    ending_light: {
        theme: 'ember',
        art:
`
      .    *  .  .   .    .   *  .
 *   .    .    .   *   .    .    .   *
   .    .    .    .    .    .    .    .    .
  .    .  .    . * .    .  .    . * .    .
.    .    .    .    .    .    .    .
  .    .    *    .    .    *    .    .    .
.    .    .    .    .    .    .    .
  .    .  .    .    .  .    .    .  .    .
.    .    .   \\|/   .    .    .    .
  .    .    .    --*--    .    .    .    .
.    .    .   /|\\   .    .    .    .
      .    *  .  .   .    .   *  .
          .    .    .    .    .`
    },

    ending_dark: {
        theme: 'dim',
        art:
`
    .    .    .    .    .    .    .
  .    .    .    .    .    .    .    .
.    .    .    .    .    .    .    .    .
   .    .    .    .    .    .    .    .    .
.    .    .    .    .    .    .    .    .
   .    .    .    .    .    .    .    .    .
.    .    .    .    .    .    .    .    .
   .    .    .    .    .    .    .    .    .
.    .    .    .    .    .    .    .    .
   .    .    .    .    .    .    .    .    .
.    .    .    .    .    .    .    .    .
     .    .    .    .    .    .    .`
    }
};

function renderAsciiArt(name) {
    const piece = asciiArt[name];
    if (!piece) return null;
    const el = document.createElement('pre');
    el.className = 'ascii-art ' + (piece.theme || '');
    el.textContent = piece.art;
    return el;
}

// Detect which ASCII art to show from story text
function detectAsciiArt(text) {
    const t = text.toLowerCase();
    // Check for explicit tags first: [art: name]
    const tagMatch = text.match(/\[art:\s*(\w+)\]/i);
    if (tagMatch && asciiArt[tagMatch[1]]) return tagMatch[1];

    // Auto-detect from content
    if (t.includes('laptop') || t.includes('screen flickers') || t.includes('apartment')) return 'desk';
    if (t.includes('river city') || t.includes('market') || t.includes('streets')) return 'city';
    if (t.includes('temple') || t.includes('chant-master') || t.includes('granar')) return 'temple';
    if (t.includes('meshwork') || t.includes('network') || t.includes('surplus flow')) return 'network';
    if (t.includes('neganthropomorph') || t.includes('perpendicular') || t.includes('signal from')) return 'signal';
    if (t.includes('crisis') || t.includes('derailing') || t.includes('rupture')) return 'crisis';
    if (t.includes('cosmic') && (t.includes('awareness') || t.includes('dream'))) return 'signal';
    if (t.includes('agent') && t.includes('outputs')) return 'agent';
    if (t.includes('agent') && (t.includes('dream') || t.includes('strange') || t.includes('anomal'))) return 'agent_anomaly';
    return null;
}

// Track last shown art to avoid repetition
let lastArt = '';
