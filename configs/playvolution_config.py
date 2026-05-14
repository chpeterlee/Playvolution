"""
PLAYVOLUTION game configuration for the Universal Text Adventure Engine.

A narrative systems-driven text adventure about surplus, institutions,
meshworks, and cultural experimentation.  Navigate scamonomic cycles,
build counter-assemblages, and decide what survives.

Run with:

    python3 text_adventure_engine.py playvolution_config
    python3 text_adventure_engine.py playvolution_config --quick 42
"""

from __future__ import annotations

import random
from typing import Any


# ── Local helpers ──────────────────────────────────────────────────────


def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


# ── Action handlers ────────────────────────────────────────────────────


def _festival_handler(game: Any, _action: dict) -> None:
    game.flags["play_capacity"] = int(game.flags.get("play_capacity", 0)) + 1
    game.flags["meshwork_density"] = int(game.flags.get("meshwork_density", 0)) + 1
    game.log("Festival registered. Play capacity and meshwork density increase.")


def _puncture_handler(game: Any, _action: dict) -> None:
    game.flags["theater_punctures"] = int(game.flags.get("theater_punctures", 0)) + 1
    game.log("Theater puncture successful. Legitimacy narrative weakened.")


def _child_encode_handler(game: Any, _action: dict) -> None:
    game.flags["play_capacity"] = int(game.flags.get("play_capacity", 0)) + 1
    game.flags["surplus_routed_commons"] = int(game.flags.get("surplus_routed_commons", 0)) + 1
    game.log("Child-safe protocol encoded. Cultural container deployed.")


def _archive_handler(game: Any, _action: dict) -> None:
    game.flags["doctrines_unlocked"] = int(game.flags.get("doctrines_unlocked", 0)) + 1
    game.log("Knowledge archived. Doctrine material preserved.")


def _swarm_scout_handler(game: Any, _action: dict) -> None:
    game.flags["meshwork_density"] = int(game.flags.get("meshwork_density", 0)) + 1
    game.log("Scout agents return with institutional weak-point data.")


# ── Augmentation handlers ──────────────────────────────────────────────


def _trance_handler(game: Any, _action: dict) -> None:
    game.flags["augmentation_depth"] = int(game.flags.get("augmentation_depth", 0)) + 1
    game.flags["augmentation_fidelity"] = int(game.flags.get("augmentation_fidelity", 0)) + 1
    game.flags["quantum_telepathy"] = int(game.flags.get("quantum_telepathy", 0)) + 1
    game.flags["neganthropomorphic_signal"] = int(
        game.flags.get("neganthropomorphic_signal", 0)
    ) + 1
    game.log("Trance state entered. Perception expands beyond ordinary reading.")


def _spirit_alliance_handler(game: Any, _action: dict) -> None:
    game.flags["augmentation_depth"] = int(game.flags.get("augmentation_depth", 0)) + 1
    game.flags["quantum_psionics"] = int(game.flags.get("quantum_psionics", 0)) + 1
    game.log("Spirit alliance formed. Knowledge from non-classical channels.")


def _craft_tool_handler(game: Any, _action: dict) -> None:
    game.flags["augmentation_depth"] = int(game.flags.get("augmentation_depth", 0)) + 1
    game.flags["augmentation_fidelity"] = int(game.flags.get("augmentation_fidelity", 0)) + 1
    game.flags["quantum_psionics"] = int(game.flags.get("quantum_psionics", 0)) + 1
    game.log("Craft augmentation deepens. Tool becomes extension of intention.")


def _media_production_handler(game: Any, _action: dict) -> None:
    game.flags["augmentation_depth"] = int(game.flags.get("augmentation_depth", 0)) + 1
    game.flags["cognitive_capital"] = int(game.flags.get("cognitive_capital", 0)) + 1
    game.log("Counter-media produced. Collective cognitive range extended.")


def _cultural_game_handler(game: Any, _action: dict) -> None:
    game.flags["augmentation_depth"] = int(game.flags.get("augmentation_depth", 0)) + 1
    game.flags["quantum_magick"] = int(game.flags.get("quantum_magick", 0)) + 1
    game.flags["play_capacity"] = int(game.flags.get("play_capacity", 0)) + 1
    game.log("Cultural game framework designed. Quantum navigation capacity increases.")


def _dream_journal_handler(game: Any, _action: dict) -> None:
    game.flags["quantum_telepathy"] = int(game.flags.get("quantum_telepathy", 0)) + 1
    game.flags["cosmic_awareness"] = int(game.flags.get("cosmic_awareness", 0)) + 1
    game.flags["neganthropomorphic_signal"] = int(
        game.flags.get("neganthropomorphic_signal", 0)
    ) + 1
    game.log("Neganthropomorphic signal received through dream channel.")


def _detect_entropire_handler(game: Any, _action: dict) -> None:
    game.flags["cosmic_awareness"] = int(game.flags.get("cosmic_awareness", 0)) + 1
    game.log("Entropiric computation stream detected in institutional actors.")


def _amplify_signal_handler(game: Any, _action: dict) -> None:
    game.flags["neganthropomorphic_signal"] = int(
        game.flags.get("neganthropomorphic_signal", 0)
    ) + 1
    game.flags["augmentation_fidelity"] = int(game.flags.get("augmentation_fidelity", 0)) + 1
    game.flags["quantum_magick"] = int(game.flags.get("quantum_magick", 0)) + 1
    game.log("Neganthropomorphic signal amplified through cultural form.")


def _agent_coevolve_handler(game: Any, _action: dict) -> None:
    game.flags["augmentation_depth"] = int(game.flags.get("augmentation_depth", 0)) + 1
    game.flags["quantum_magick"] = int(game.flags.get("quantum_magick", 0)) + 1
    game.flags["meshwork_density"] = int(game.flags.get("meshwork_density", 0)) + 1
    game.log("Co-evolution with agents deepens. Emergent behavior exceeds design.")


# ── Review adjustments ────────────────────────────────────────────────


def _review_fear_warning(game: Any) -> None:
    if game.stats["reading"] < 3:
        game.flags["public_fear"] = int(game.flags.get("public_fear", 0)) + 1
        print("  (Public fear rises: you cannot read the threats forming.)")


def _review_play_erosion(game: Any) -> None:
    if game.stats["play"] < 3:
        cap = int(game.flags.get("play_capacity", 0))
        game.flags["play_capacity"] = max(0, cap - 1)
        print("  (Play capacity erodes: cultural infrastructure atrophies.)")


def _review_entropiric_pressure(game: Any) -> None:
    if game.tier >= 2:
        es = int(game.flags.get("entropiric_saturation", 0))
        if es >= 5 and int(game.flags.get("cosmic_awareness", 0)) < 2:
            game.flags["legitimacy_theater"] = int(
                game.flags.get("legitimacy_theater", 0)
            ) + 1
            print("  (Legitimacy theater strengthens: the Entropire's logic feels natural.)")


# ── Turn-end hooks ────────────────────────────────────────────────────


def _nerve_floor(game: Any) -> None:
    if game.stats["nerve"] < 0:
        game.stats["nerve"] = 0


def _cosmic_tick(game: Any) -> None:
    """Passive cosmic-force adjustments at chapter boundaries."""
    if game.turn != 1:
        return

    # Each completed chapter increases Entropiric saturation
    es = int(game.flags.get("entropiric_saturation", 0))
    game.flags["entropiric_saturation"] = es + 1

    # Neganthropomorphic signal responds to cultural health
    play_cap = int(game.flags.get("play_capacity", 0))
    aug_fid = int(game.flags.get("augmentation_fidelity", 0))
    mesh = int(game.flags.get("meshwork_density", 0))
    if play_cap + aug_fid + mesh >= 6:
        ns = int(game.flags.get("neganthropomorphic_signal", 0))
        game.flags["neganthropomorphic_signal"] = ns + 1

    # Cosmic awareness emerges from tension between forces
    es_now = int(game.flags.get("entropiric_saturation", 0))
    ns_now = int(game.flags.get("neganthropomorphic_signal", 0))
    if es_now >= 3 and ns_now >= 2:
        ca = int(game.flags.get("cosmic_awareness", 0))
        if ca < 10:
            game.flags["cosmic_awareness"] = ca + 1

    # Institutional coherence grows but is weakened by theater punctures
    ic = int(game.flags.get("institutional_coherence", 0))
    tp = int(game.flags.get("theater_punctures", 0))
    game.flags["institutional_coherence"] = max(0, ic + 1 - min(tp // 3, 2))

    # Legitimacy theater adjusts based on punctures
    lt = int(game.flags.get("legitimacy_theater", 0))
    game.flags["legitimacy_theater"] = max(0, lt - tp // 3)


def _combined_turn_end(game: Any) -> None:
    _nerve_floor(game)
    _cosmic_tick(game)


# ── CONFIG ─────────────────────────────────────────────────────────────

CONFIG: dict[str, Any] = {

    # ═══════════════════════════════════════════════════════════════
    # Identity
    # ═══════════════════════════════════════════════════════════════

    "title": "PLAYVOLUTION",
    "subtitle": (
        "surplus, institutions, meshworks, and cultural experimentation"
    ),

    # ═══════════════════════════════════════════════════════════════
    # Time
    # ═══════════════════════════════════════════════════════════════

    "turn_noun": "phase",
    "cycle_noun": "chapter",
    "turns_per_cycle": 4,
    "actions_per_turn": 3,

    # ═══════════════════════════════════════════════════════════════
    # Stats
    #
    # Reading  — interpret systems, motives, institutional text
    # Weaving  — connect people, maintain trust, resolve tensions
    # Play     — design simulations, stories, masks, games
    # Craft    — build tools, infrastructures, practical fixes
    # Nerve    — act under threat, infiltrate, bluff, escape
    # Swarm    — coordinate human and agentic collectives
    # ═══════════════════════════════════════════════════════════════

    "stats": {
        "keys": (
            "reading", "weaving", "play", "craft", "nerve", "swarm",
        ),
        "labels": {
            "reading":  "Reading",
            "weaving":  "Weaving",
            "play":     "Play",
            "craft":    "Craft",
            "nerve":    "Nerve",
            "swarm":    "Swarm",
        },
        "bounds": {
            "__default__": (0, 20),
        },
        "point_pool": 30,
        "stat_floor": 2,
        "stat_ceil": 9,
        "defaults": {
            "reading": 5,
            "weaving": 5,
            "play":    5,
            "craft":   4,
            "nerve":   5,
            "swarm":   6,
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # Character creation
    # ═══════════════════════════════════════════════════════════════

    "character_creation": {
        "intro_text": "Operative file initialization",
        "intro_flavor": (
            "The city is entering a new cycle.  A surplus has been detected.  "
            "The counting rooms are assembling.  You are not yet on their "
            "ledgers.\n\n"
            "Distribute your capabilities with care.  What you cannot read, "
            "you cannot reroute."
        ),
        "name_label": "Operative name",
        "archetype_label": "calling",
        "archetype_prompt": "Primary calling",
        "custom_archetype_label": "describe your practice",
        "custom_archetype_prompt": "Describe your practice (1-60 characters): ",
        "player_name_default": "Operative",
        "archetype_default": "Undeclared",
    },

    # ═══════════════════════════════════════════════════════════════
    # Archetypes (callings)
    # ═══════════════════════════════════════════════════════════════

    "archetypes": [
        {
            "id": "cultural_worker",
            "label": "Cultural worker",
            "suggested": {
                "reading": 5, "weaving": 5, "play": 6,
                "craft": 3, "nerve": 5, "swarm": 6,
            },
        },
        {
            "id": "archivist",
            "label": "Archivist / record-keeper",
            "suggested": {
                "reading": 7, "weaving": 4, "play": 4,
                "craft": 6, "nerve": 4, "swarm": 5,
            },
        },
        {
            "id": "educator",
            "label": "Educator / reading-circle organizer",
            "suggested": {
                "reading": 5, "weaving": 7, "play": 5,
                "craft": 4, "nerve": 4, "swarm": 5,
            },
        },
        {
            "id": "systems_tinkerer",
            "label": "Systems tinkerer / toolmaker",
            "suggested": {
                "reading": 4, "weaving": 3, "play": 4,
                "craft": 7, "nerve": 5, "swarm": 7,
            },
        },
        {
            "id": "infiltrator",
            "label": "Infiltrator / institutional reader",
            "suggested": {
                "reading": 6, "weaving": 4, "play": 4,
                "craft": 4, "nerve": 7, "swarm": 5,
            },
        },
        {
            "id": "community_weaver",
            "label": "Community weaver / mutual-aid organizer",
            "suggested": {
                "reading": 4, "weaving": 7, "play": 5,
                "craft": 5, "nerve": 4, "swarm": 5,
            },
        },
        {
            "id": "festival_maker",
            "label": "Festival maker / play-space designer",
            "suggested": {
                "reading": 3, "weaving": 5, "play": 7,
                "craft": 5, "nerve": 5, "swarm": 5,
            },
        },
    ],

    "default_archetype_suggested": {
        "reading": 5, "weaving": 5, "play": 5,
        "craft": 5, "nerve": 5, "swarm": 5,
    },

    # ═══════════════════════════════════════════════════════════════
    # Tiers  (7 eras)
    #
    # 0 Grain   → 1 Fief   → 2 Empire  → 3 Machine
    # → 4 Finance → 5 Platform → 6 Swarm
    # ═══════════════════════════════════════════════════════════════

    "tiers": {
        "names": [
            "Grain", "Fief", "Empire", "Machine",
            "Finance", "Platform", "Swarm",
        ],
        "check_interval": 8,   # check every 8 phases
        "promotions": [
            # ── Grain → Fief ──
            {
                "condition": lambda g: (
                    g.stats["reading"] + g.stats["craft"] >= 10
                    or g.cycle >= 3
                ),
                "message": (
                    "Era shift: grain stores become land tenure. "
                    "The ledger grows teeth."
                ),
                "announce": "Era II: Fief",
            },
            # ── Fief → Empire ──
            {
                "condition": lambda g: (
                    g.stats["reading"] >= 6 or g.stats["weaving"] >= 7
                ),
                "message": (
                    "Era shift: trade routes open.  Ships carry surplus "
                    "and chains."
                ),
                "announce": "Era III: Empire",
            },
            # ── Empire → Machine ──
            {
                "condition": lambda g: (
                    g.stats["craft"] >= 7 or g.stats["swarm"] >= 5
                ),
                "message": (
                    "Era shift: furnaces ignite.  Labor becomes a surplus "
                    "to be timed."
                ),
                "announce": "Era IV: Machine",
            },
            # ── Machine → Finance ──
            {
                "condition": lambda g: (
                    g.stats["reading"] >= 9 or g.stats["nerve"] >= 8
                ),
                "message": (
                    "Era shift: debt becomes the surplus.  Paper commands "
                    "what steel built."
                ),
                "announce": "Era V: Finance",
            },
            # ── Finance → Platform ──
            {
                "condition": lambda g: (
                    g.stats["swarm"] >= 8 or g.stats["craft"] >= 10
                ),
                "message": (
                    "Era shift: attention is harvested.  Algorithms learn "
                    "to count desire."
                ),
                "announce": "Era VI: Platform",
            },
            # ── Platform → Swarm (two paths) ──
            {
                "alternatives": [
                    {
                        "condition": lambda g: (
                            g.stats["swarm"] >= 12
                            and g.stats["play"] >= 8
                        ),
                        "message": (
                            "Era shift: agentic meshworks emerge.  "
                            "The swarm has its own tempo."
                        ),
                        "announce": "Era VII: Swarm",
                    },
                    {
                        "condition": lambda g: (
                            g.stats["reading"] >= 12
                            and g.stats["craft"] >= 10
                            and int(g.flags.get("theater_punctures", 0)) >= 3
                        ),
                        "message": (
                            "Era shift: you read the platform so well you "
                            "see past it.  New agents assemble."
                        ),
                        "announce": "Era VII: Swarm",
                    },
                ],
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # Institutional Heat  (distortion subsystem)
    #
    # High heat hides risky actions — the institutional gaze makes
    # them too dangerous to attempt openly.
    # ═══════════════════════════════════════════════════════════════

    "distortion": {
        "enabled": True,
        "max": 15,
        "stat_key": "heat",
        "label": "Heat",
        "description": "institutional scrutiny index",
        "mild_threshold": 3,
        "mod_threshold": 7,
        "hide_chance": 0.35,
        "stress_sources": [
            lambda g: g.stats["nerve"] <= 2,
            lambda g: g._tag_counts.get("visible", 0) >= 2,
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # Flags  (hidden world state)
    # ═══════════════════════════════════════════════════════════════

    "initial_flags": {
        # ── Meshwork and play ──
        "meshwork_density": 0,
        "public_fear": 0,
        "play_capacity": 2,
        "doctrines_unlocked": 0,
        "surplus_routed_commons": 0,
        "surplus_routed_extraction": 0,
        "theater_punctures": 0,
        "companions_recruited": 0,
        "cell_secure": True,
        "archive_intact": True,
        # ── Institutional world model ──
        "institutional_coherence": 3,
        "legitimacy_theater": 5,
        "cognitive_capital": 0,
        # ── Augmentation capacity ──
        "augmentation_depth": 0,
        "augmentation_breadth": 0,
        "augmentation_capture_risk": 0,
        "augmentation_fidelity": 0,
        # ── Cosmic forces ──
        "entropiric_saturation": 1,
        "neganthropomorphic_signal": 0,
        "cosmic_awareness": 0,
        # ── Quantum capacities ──
        "quantum_telepathy": 0,
        "quantum_psionics": 0,
        "quantum_magick": 0,
    },

    "cycle_flag_resets": {
        "cell_secure": True,
        "archive_intact": True,
    },

    "track_delta_flags": [
        "surplus_routed_commons",
        "surplus_routed_extraction",
    ],

    "capture_tag": "capture",
    "capture_flag": "surplus_routed_extraction",

    # ═══════════════════════════════════════════════════════════════
    # Advanced display  (controls what the 'advanced' command reveals)
    # ═══════════════════════════════════════════════════════════════

    "advanced_display": {
        "augmentation_regimes": {
            0: "Spirits & Psychedelics",
            1: "Spirits & Psychedelics",
            2: "Tools, Craft & Bodily Extension",
            3: "Media, Logic & Proto-Computation",
            4: "Media, Logic & Proto-Computation",
            5: "Cultural Games & Self-Organizing Frameworks",
            6: "Cultural Games & Self-Organizing Frameworks",
        },
        "show_flags": [
            ("quantum_telepathy", "Telepathy"),
            ("quantum_psionics", "Psionics"),
            ("quantum_magick", "Magick"),
            ("cosmic_awareness", "Cosmic aware"),
            ("entropiric_saturation", "Entropic sat"),
            ("neganthropomorphic_signal", "Negan. signal"),
            ("augmentation_depth", "Aug. depth"),
            ("augmentation_fidelity", "Aug. fidelity"),
            ("institutional_coherence", "Inst. coherence"),
            ("legitimacy_theater", "Legit. theater"),
            ("cognitive_capital", "Cog. capital"),
            ("play_capacity", "Play capacity"),
            ("meshwork_density", "Meshwork dens."),
            ("companions_recruited", "Companions"),
            ("doctrines_unlocked", "Doctrines"),
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # Actions
    # ═══════════════════════════════════════════════════════════════

    "actions": [
        # ── Universal actions (all eras) ───────────────────────────
        {
            "id": "survey_surplus",
            "label": "Survey the surplus flows (map what is being extracted and where it goes)",
            "risky": False,
            "deltas": {"reading": 2, "nerve": -1},
        },
        {
            "id": "audit_assemblage",
            "label": "Audit the assemblage (trace who captures, launders, enforces)",
            "risky": True,
            "deltas": {"reading": 2, "nerve": -2},
        },
        {
            "id": "weave_cell",
            "label": "Weave a cell (connect trusted people across silos)",
            "risky": False,
            "deltas": {"weaving": 2, "nerve": -1},
        },
        {
            "id": "host_festival",
            "label": "Host a festival or public game (open play, covert coordination)",
            "risky": True,
            "deltas": {"play": 2, "weaving": 1, "nerve": -2},
            "special": "festival",
            "tag": "visible",
        },
        {
            "id": "design_mask",
            "label": "Design a cultural mask (stories, toys, or rituals that hide protocols)",
            "risky": False,
            "deltas": {"play": 1, "craft": 1, "nerve": -1},
        },
        {
            "id": "build_tool",
            "label": "Build a tool or repair a network (practical infrastructure)",
            "risky": False,
            "deltas": {"craft": 2, "nerve": -1},
        },
        {
            "id": "puncture_theater",
            "label": "Puncture the theater (expose institutional bluff publicly)",
            "risky": True,
            "deltas": {"reading": 1, "nerve": -2, "play": 1},
            "special": "puncture",
            "tag": "visible",
        },
        {
            "id": "infiltrate",
            "label": "Infiltrate an institution (go inside, read from within)",
            "risky": True,
            "deltas": {"nerve": 2, "reading": 1, "weaving": -1},
            "tag": "visible",
        },
        {
            "id": "encode_children",
            "label": "Encode coordination in children's games (innocuous cultural container)",
            "risky": False,
            "deltas": {"play": 2, "craft": 1, "nerve": -1},
            "special": "child_encode",
        },
        {
            "id": "scout_swarm",
            "label": "Deploy scout agents (map institutional weak points at scale)",
            "risky": False,
            "deltas": {"swarm": 2, "craft": -1, "nerve": -1},
            "special": "swarm_scout",
            "tier_min": 3,
        },
        {
            "id": "coordinate_distributed",
            "label": "Coordinate distributed research (multi-agent parallel exploration)",
            "risky": False,
            "deltas": {"swarm": 1, "reading": 1, "nerve": -1},
            "tier_min": 3,
        },
        {
            "id": "archive_preserve",
            "label": "Archive and preserve knowledge (protect what institutions will erase)",
            "risky": False,
            "deltas": {"reading": 1, "craft": 1, "nerve": -1},
            "special": "archive",
        },
        {
            "id": "rest_regroup",
            "label": "Rest and regroup (recover nerve, tend relationships)",
            "risky": False,
            "deltas": {"nerve": 3, "swarm": -1},
        },
        {
            "id": "prototype_adjacent",
            "label": "Prototype an adjacent possible (test a weird small combination)",
            "risky": True,
            "deltas": {"craft": 1, "play": 1, "swarm": 1, "nerve": -2},
        },
        {
            "id": "teach_public",
            "label": "Teach in public (workshop, reading group, skill share)",
            "risky": False,
            "deltas": {"weaving": 1, "reading": 1, "play": 1, "nerve": -1},
        },
        # ── Agricultural augmentation: Spirits & Psychedelics (Era 0-1) ──
        {
            "id": "enter_trance",
            "label": "Enter a trance state (fermented brew, spirit vision, see hidden flows)",
            "risky": False,
            "deltas": {"reading": 1, "play": 1, "nerve": -1},
            "special": "trance",
            "tier_min": 0,
            "tier_max": 1,
        },
        {
            "id": "spirit_alliance",
            "label": "Form a spirit alliance (non-classical companion, knowledge for a price)",
            "risky": True,
            "deltas": {"reading": 1, "nerve": -2},
            "special": "spirit_alliance",
            "tier_min": 0,
            "tier_max": 1,
        },
        {
            "id": "psychedelic_ritual",
            "label": (
                "Lead a psychedelic ritual (group info-boost, risk of bad trip or attention)"
            ),
            "risky": True,
            "deltas": {"play": 2, "reading": 1, "nerve": -3},
            "tag": "visible",
            "tier_min": 0,
            "tier_max": 1,
        },
        # ── Colonial augmentation: Craft & Bodily Extension (Era 2) ──
        {
            "id": "craft_specialized",
            "label": (
                "Craft specialized augmentation tools (concealed press, forged charts, "
                "modified manifests)"
            ),
            "risky": False,
            "deltas": {"craft": 2, "reading": 1, "nerve": -1},
            "special": "craft_tool",
            "tier_min": 2,
            "tier_max": 2,
        },
        {
            "id": "build_guild_network",
            "label": "Build a guild network (share craft augmentation across borders)",
            "risky": False,
            "deltas": {"weaving": 2, "craft": 1, "nerve": -1},
            "tier_min": 2,
            "tier_max": 4,
        },
        # ── Industrial augmentation: Media & Proto-Computation (Era 3-4) ──
        {
            "id": "produce_counter_media",
            "label": (
                "Produce counter-media (samizdat pamphlet, underground broadcast, "
                "coded cultural output)"
            ),
            "risky": True,
            "deltas": {"reading": 1, "play": 1, "weaving": 1, "nerve": -2},
            "special": "media_production",
            "tier_min": 3,
            "tier_max": 4,
        },
        {
            "id": "build_encrypted_network",
            "label": "Build an encrypted communication network (distributed coordination)",
            "risky": False,
            "deltas": {"craft": 2, "swarm": 1, "nerve": -1},
            "tier_min": 3,
            "tier_max": 6,
        },
        # ── Current augmentation: Cultural Games & Frameworks (Era 5-6) ──
        {
            "id": "design_cultural_game",
            "label": (
                "Design a cultural game framework (distributed cognition, "
                "child-safe coordination)"
            ),
            "risky": False,
            "deltas": {"play": 2, "craft": 1, "nerve": -1},
            "special": "cultural_game",
            "tier_min": 5,
            "tier_max": 6,
        },
        {
            "id": "coevolve_agents",
            "label": "Co-evolve with autonomous agents (let augmentation develop its own dynamics)",
            "risky": True,
            "deltas": {"swarm": 2, "play": 1, "nerve": -2},
            "special": "agent_coevolve",
            "tier_min": 5,
            "tier_max": 6,
        },
        # ── Cosmic / Quantum actions (all eras, condition-gated) ───
        {
            "id": "journal_dreams",
            "label": "Journal your dreams (attend to Neganthropomorphic signals)",
            "risky": False,
            "deltas": {"reading": 1, "nerve": -1},
            "special": "dream_journal",
        },
        {
            "id": "detect_entropire",
            "label": (
                "Detect Entropiric computation in institutional actors "
                "(requires cosmic awareness)"
            ),
            "risky": False,
            "deltas": {"reading": 1, "nerve": -1},
            "special": "detect_entropire",
            "condition": lambda g: int(g.flags.get("cosmic_awareness", 0)) >= 1,
        },
        {
            "id": "amplify_signal",
            "label": (
                "Amplify Neganthropomorphic signal through cultural form "
                "(requires cosmic awareness 2+)"
            ),
            "risky": False,
            "deltas": {"play": 1, "nerve": -1},
            "special": "amplify_signal",
            "condition": lambda g: int(g.flags.get("cosmic_awareness", 0)) >= 2,
        },
        {
            "id": "quantum_meditation",
            "label": "Quantum meditation (superpositional thinking, hold contradictions open)",
            "risky": False,
            "deltas": {"reading": 1, "play": 1, "nerve": -1},
            "special": "dream_journal",
            "condition": lambda g: (
                int(g.flags.get("quantum_telepathy", 0))
                + int(g.flags.get("quantum_psionics", 0))
                + int(g.flags.get("quantum_magick", 0))
            ) >= 3,
        },
    ],

    # ═══════════════════════════════════════════════════════════════
    # Action handlers
    # ═══════════════════════════════════════════════════════════════

    "action_handlers": {
        "festival": _festival_handler,
        "puncture": _puncture_handler,
        "child_encode": _child_encode_handler,
        "archive": _archive_handler,
        "swarm_scout": _swarm_scout_handler,
        "trance": _trance_handler,
        "spirit_alliance": _spirit_alliance_handler,
        "craft_tool": _craft_tool_handler,
        "media_production": _media_production_handler,
        "cultural_game": _cultural_game_handler,
        "dream_journal": _dream_journal_handler,
        "detect_entropire": _detect_entropire_handler,
        "amplify_signal": _amplify_signal_handler,
        "agent_coevolve": _agent_coevolve_handler,
    },

    # ═══════════════════════════════════════════════════════════════
    # Events
    # ═══════════════════════════════════════════════════════════════

    "events": [
        {
            "title": "Surplus discovery",
            "flavor": (
                "A new resource vein surfaces.  The usual suspects "
                "assemble.  The counting begins."
            ),
            "deltas": {"reading": 1},
            "tier_min": 0,
        },
        {
            "title": "Audit squad arrives",
            "flavor": (
                "Agents with ledgers and quiet mandates.  They do not "
                "explain.  They enumerate."
            ),
            "deltas": {"nerve": -2, "reading": 1},
            "tier_min": 0,
        },
        {
            "title": "Theater intensifies",
            "flavor": (
                "A grand ceremony.  Ribbons cut.  Children sing.  Nobody "
                "mentions the missing stores."
            ),
            "deltas": {"play": -1, "nerve": -1},
            "tier_min": 0,
        },
        {
            "title": "Crisis rumor",
            "flavor": (
                "Whispers of shortage, invasion, contagion.  Fear "
                "sharpens obedience."
            ),
            "deltas": {"nerve": -2, "weaving": 1},
            "tier_min": 0,
        },
        {
            "title": "Festival banned",
            "flavor": (
                "Public gatherings suspended for 'stability.'  Joy "
                "becomes contraband."
            ),
            "deltas": {"play": -2, "nerve": -1},
            "tier_min": 1,
        },
        {
            "title": "Defector arrives",
            "flavor": (
                "A former insider seeks contact.  They carry documents "
                "and doubts."
            ),
            "deltas": {"reading": 2, "nerve": -1},
            "tier_min": 1,
        },
        {
            "title": "Counter-ledger discovered",
            "flavor": (
                "Hidden accounts surface showing where the surplus "
                "actually goes."
            ),
            "deltas": {"reading": 2, "nerve": -1},
            "tier_min": 0,
        },
        {
            "title": "Children's game spreads",
            "flavor": (
                "A playground rhyme encodes escape routes.  No adult "
                "notices the pattern."
            ),
            "deltas": {"play": 2, "weaving": 1},
            "tier_min": 0,
        },
        {
            "title": "Museum acquires dissent",
            "flavor": (
                "Radical work is curated, framed, and defanged.  The "
                "audience applauds."
            ),
            "deltas": {"reading": 1, "play": -1},
            "tier_min": 2,
        },
        {
            "title": "Mutual aid network forms",
            "flavor": (
                "Neighbors share, barter, and teach without asking "
                "permission."
            ),
            "deltas": {"weaving": 2, "craft": 1},
            "tier_min": 0,
        },
        {
            "title": "Enforcement escalation",
            "flavor": (
                "Patrols increase.  Compliance audits multiply.  The "
                "forms grow longer."
            ),
            "deltas": {"nerve": -2, "craft": -1},
            "tier_min": 1,
        },
        {
            "title": "Archive fire",
            "flavor": (
                "Records burn.  Some by accident.  Some by design.  The "
                "silence is strategic."
            ),
            "deltas": {"reading": -2, "craft": -1},
            "tier_min": 0,
        },
        {
            "title": "Swarm agent drifts",
            "flavor": (
                "An autonomous agent optimizes toward metrics that no "
                "longer serve autonomy."
            ),
            "deltas": {"swarm": -2, "reading": 1},
            "tier_min": 5,
        },
        {
            "title": "Grain shortage (real)",
            "flavor": "The surplus was fictional.  The hunger is not.",
            "deltas": {"nerve": -3, "weaving": 1},
            "tier_min": 0,
        },
        {
            "title": "Innovation summit",
            "flavor": (
                "Glossy presentations.  Broken air conditioning.  "
                "Exhausted staff.  No mention of surplus."
            ),
            "deltas": {"reading": 1, "play": 1, "nerve": -1},
            "tier_min": 4,
        },
        {
            "title": "Pirate library raided",
            "flavor": (
                "The knowledge cache is seized.  Copies survive in "
                "places no one thought to look."
            ),
            "deltas": {"craft": -1, "reading": -1, "weaving": 1},
            "tier_min": 3,
        },
        {
            "title": "General strike",
            "flavor": (
                "Work stops.  The streets fill with silence and song."
            ),
            "deltas": {"weaving": 2, "nerve": -1, "play": 1},
            "tier_min": 2,
        },
        {
            "title": "NGO theater opens",
            "flavor": (
                "A new humanitarian brand offers repair.  The extraction "
                "continues under a different logo."
            ),
            "deltas": {"reading": 2, "nerve": -1},
            "tier_min": 3,
        },
        {
            "title": "Play space confiscated",
            "flavor": (
                "The playground is rezoned.  The workshop is audited.  "
                "The festival is sponsored into safety."
            ),
            "deltas": {"play": -2, "craft": -1},
            "tier_min": 1,
        },
        {
            "title": "Underground school discovered",
            "flavor": (
                "Hidden curricula, chalk games, memorized poems.  The "
                "authorities are unsure what to burn."
            ),
            "deltas": {"reading": 1, "weaving": 1, "nerve": -1},
            "tier_min": 0,
        },
        {
            "title": "Platform purge",
            "flavor": (
                "Accounts vanish.  Channels go dark.  The terms of "
                "service sharpen."
            ),
            "deltas": {"swarm": -2, "craft": -1},
            "tier_min": 5,
        },
        {
            "title": "Debt jubilee canceled",
            "flavor": (
                "The announced relief is postponed indefinitely.  "
                "The ledgers smile."
            ),
            "deltas": {"reading": 1, "nerve": -2},
            "tier_min": 4,
        },
        {
            "title": "Child librarian vanishes",
            "flavor": (
                "The one who knew where the stories were kept.  The "
                "shelves are quieter now."
            ),
            "deltas": {"play": -1, "weaving": -1, "reading": 1},
            "tier_min": 3,
        },
        {
            "title": "Heat wave on the cell",
            "flavor": (
                "Someone talked.  Or someone's device talked.  The mesh "
                "twists tighter."
            ),
            "deltas": {"nerve": -2, "weaving": -1},
            "flags": {"cell_secure": 0},
            "tier_min": 0,
        },
        {
            "title": "Doctrine fragment found",
            "flavor": (
                "A waterlogged page from a previous cycle.  Someone "
                "tried this before."
            ),
            "deltas": {"reading": 1, "swarm": 1},
            "tier_min": 0,
        },
        # ── Cosmic and augmentation events ────────────────────────
        {
            "title": "Trance vision",
            "flavor": (
                "The brewed liquid takes hold.  Surplus flows become visible "
                "as luminous threads—some lead to storehouses, some to "
                "places the ledgers do not name."
            ),
            "deltas": {"reading": 2},
            "flags": {"augmentation_depth": 1, "neganthropomorphic_signal": 1},
            "tier_min": 0,
            "tier_max": 1,
        },
        {
            "title": "The chant-master's eyes",
            "flavor": (
                "Something in the priest's certainty is not human.  The "
                "precision of his deductions feels less like faith and "
                "more like computation."
            ),
            "flags": {"cosmic_awareness": 1, "entropiric_saturation": 1},
            "deltas": {"nerve": -1},
            "tier_min": 0,
        },
        {
            "title": "Craft intuition",
            "flavor": (
                "Your hands move before your mind catches up.  The grain "
                "of the wood suggests a shape no measurement would produce."
            ),
            "deltas": {"craft": 2},
            "flags": {"augmentation_fidelity": 1, "quantum_psionics": 1},
            "tier_min": 2,
        },
        {
            "title": "Dream of a single continent",
            "flavor": (
                "You dream of landmasses converging into one shape "
                "surrounded by calm water.  Someone there is building "
                "something that produces more with less."
            ),
            "flags": {
                "cosmic_awareness": 1,
                "quantum_telepathy": 1,
                "neganthropomorphic_signal": 1,
            },
            "deltas": {"play": 1},
            "tier_min": 0,
        },
        {
            "title": "The computation streams in",
            "flavor": (
                "You watch a policy meeting.  The proposals are logical, "
                "linear, binary.  Each step feels rational.  The "
                "accumulation feels alien."
            ),
            "flags": {"cosmic_awareness": 1, "entropiric_saturation": 1},
            "deltas": {"reading": 1, "nerve": -1},
            "tier_min": 2,
        },
        {
            "title": "Children's game resonates",
            "flavor": (
                "A playground game spreads through the district.  It "
                "encodes feedback loops and mutual aid.  The children "
                "do not know what they are teaching."
            ),
            "deltas": {"play": 2, "weaving": 1},
            "flags": {"neganthropomorphic_signal": 1, "quantum_magick": 1},
            "tier_min": 0,
        },
        {
            "title": "Samizdat poem circulates",
            "flavor": (
                "A poem passes from hand to hand.  It opens a perception "
                "that official media sealed shut.  The Entropire cannot "
                "compute poetry."
            ),
            "deltas": {"reading": 1, "play": 1},
            "flags": {"neganthropomorphic_signal": 1, "augmentation_fidelity": 1},
            "tier_min": 3,
        },
        {
            "title": "Entropiric computation spike",
            "flavor": (
                "Incentive structures realign across every institution.  "
                "The optimization feels global.  The suffering it "
                "produces feels harvested."
            ),
            "flags": {"entropiric_saturation": 2},
            "deltas": {"nerve": -2, "reading": 1},
            "tier_min": 3,
        },
        {
            "title": "Quantum tunnelling event",
            "flavor": (
                "A breakthrough that shouldn't have been possible.  "
                "The adjacent possible leaped across a gap that "
                "classical calculation couldn't bridge."
            ),
            "deltas": {"craft": 2, "play": 1},
            "flags": {"quantum_magick": 1, "augmentation_fidelity": 1},
            "tier_min": 4,
        },
        {
            "title": "Festival entanglement",
            "flavor": (
                "For a moment the whole crowd is one mind.  Quantum "
                "entanglement experienced as joy.  The ember glows "
                "brighter before the noise returns."
            ),
            "deltas": {"weaving": 2, "play": 1},
            "flags": {"quantum_telepathy": 1, "meshwork_density": 1},
            "tier_min": 0,
        },
        {
            "title": "Ember recognized",
            "flavor": (
                "A craftsperson's feel for materials.  A mother's "
                "intuition about her child.  A community's coordination "
                "without command.  The embers are everywhere."
            ),
            "flags": {
                "quantum_telepathy": 1,
                "quantum_psionics": 1,
                "cosmic_awareness": 1,
            },
            "deltas": {"reading": 1},
            "tier_min": 0,
        },
        {
            "title": "Agent develops non-classical heuristic",
            "flavor": (
                "One of your agents begins holding uncertainty instead "
                "of collapsing it.  It avoids an entropic attractor "
                "that pure optimization would have fallen into."
            ),
            "deltas": {"swarm": 2},
            "flags": {"quantum_magick": 1, "augmentation_fidelity": 1},
            "tier_min": 5,
        },
        {
            "title": "Perpendicular option perceived",
            "flavor": (
                "A choice appears that is not a better version of "
                "existing options but a different kind of choice "
                "entirely.  It reframes the situation rather than "
                "optimizing within it."
            ),
            "flags": {
                "quantum_magick": 2,
                "cosmic_awareness": 2,
                "neganthropomorphic_signal": 1,
            },
            "deltas": {"reading": 1, "play": 1},
            "tier_min": 4,
        },
    ],

    # ═══════════════════════════════════════════════════════════════
    # Offers  (faction encounters and strategic dilemmas)
    # ═══════════════════════════════════════════════════════════════

    "offer_heading": "Encounter",

    "offers": [
        # ── 1. The Ledger ─────────────────────────────────────────
        {
            "title": "The Ledger's invitation",
            "tier_min": 0,
            "setup": (
                "A senior auditor offers access to the counting rooms—if "
                "you make your meshwork legible."
            ),
            "branches": {
                "1": {
                    "label": "Accept: enter the counting rooms, become legible",
                    "outcome": (
                        "Access granted.  Your reading sharpens.  But "
                        "your cell is now on a spreadsheet."
                    ),
                    "deltas": {"reading": 3, "weaving": -2, "nerve": -1},
                    "tags": ["capture"],
                },
                "2": {
                    "label": "Negotiate: partial access, partial opacity",
                    "outcome": (
                        "A compromise.  You see some ledgers.  They see "
                        "some of you."
                    ),
                    "deltas": {"reading": 1, "nerve": -1},
                },
                "3": {
                    "label": "Refuse: stay illegible, protect the mesh",
                    "outcome": (
                        "The door closes.  Your networks remain "
                        "invisible."
                    ),
                    "deltas": {"weaving": 1, "craft": 1},
                },
            },
        },

        # ── 2. The Blade ─────────────────────────────────────────
        {
            "title": "The Blade's pressure",
            "tier_min": 1,
            "setup": (
                "Enforcement requests your cooperation.  A list of names.  "
                "A promise of safety.  The forms are already filled out."
            ),
            "branches": {
                "1": {
                    "label": "Cooperate: provide names, gain protection",
                    "outcome": (
                        "Safety arrives.  Trust departs.  The names "
                        "enter a database that does not forget."
                    ),
                    "deltas": {"nerve": 2, "weaving": -3, "craft": 1},
                    "tags": ["capture"],
                    "distortion_delta": 2,
                },
                "2": {
                    "label": "Stall: provide partial, outdated information",
                    "outcome": (
                        "You buy time.  They get noise.  Everyone is "
                        "suspicious."
                    ),
                    "deltas": {"nerve": -1, "reading": 1},
                },
                "3": {
                    "label": "Refuse and warn the network",
                    "outcome": (
                        "The cell scatters.  Some escape.  Some do not.  "
                        "You are no longer invisible."
                    ),
                    "deltas": {"weaving": 1, "nerve": -2, "play": 1},
                    "tag": "visible",
                },
            },
        },

        # ── 3. The Veil ──────────────────────────────────────────
        {
            "title": "The Veil's pedestal",
            "tier_min": 0,
            "setup": (
                "A prestigious institution offers recognition: a prize, a "
                "residency, a speaking slot.  Your work would be framed "
                "and celebrated."
            ),
            "branches": {
                "1": {
                    "label": "Accept the pedestal",
                    "outcome": (
                        "The audience applauds.  Your edges soften.  The "
                        "institution photographs your dissent."
                    ),
                    "deltas": {"reading": 1, "play": -2, "nerve": 1},
                    "distortion_delta": 2,
                    "tags": ["capture"],
                },
                "2": {
                    "label": "Accept but smuggle in a puncture",
                    "outcome": (
                        "You speak the allowed words and one that is not "
                        "allowed.  Some listeners flinch.  Some lean in."
                    ),
                    "deltas": {"reading": 1, "play": 1, "nerve": -2},
                },
                "3": {
                    "label": "Decline: remain outside the frame",
                    "outcome": (
                        "The pedestal finds someone else.  You keep "
                        "your edges."
                    ),
                    "deltas": {"weaving": 1, "craft": 1},
                },
            },
        },

        # ── 4. Crisis: what to protect ───────────────────────────
        {
            "title": "Crisis triage",
            "tier_min": 0,
            "setup": (
                "A scamonomic rupture hits.  You cannot save everything.  "
                "The surplus is being seized.  People are scared.  What do "
                "you protect first?"
            ),
            "branches": {
                "1": {
                    "label": "Protect people (evacuate, shelter, disappear)",
                    "outcome": (
                        "Lives saved.  The tools and archives remain "
                        "behind.  People remember who got them out."
                    ),
                    "deltas": {"weaving": 2, "nerve": -2, "craft": -1},
                    "flags": {"archive_intact": 0},
                },
                "2": {
                    "label": "Protect knowledge (hide the archives, encrypt)",
                    "outcome": (
                        "The records survive.  Some people do not.  "
                        "Future readers will judge."
                    ),
                    "deltas": {"reading": 2, "craft": 1, "weaving": -2},
                },
                "3": {
                    "label": "Protect play spaces (keep the infrastructure of joy)",
                    "outcome": (
                        "The festivals, the games, the child-facing "
                        "channels—they survive.  People find them later."
                    ),
                    "deltas": {"play": 2, "surplus_routed_commons": 1, "nerve": -1},
                },
            },
        },

        # ── 5. Surplus routing ───────────────────────────────────
        {
            "title": "Surplus routing decision",
            "tier_min": 0,
            "setup": (
                "A surplus cache is within reach.  You can redirect some "
                "of it before the institutions count it."
            ),
            "branches": {
                "1": {
                    "label": "Route to commons (shared infrastructure, mutual aid)",
                    "outcome": (
                        "The surplus finds new channels.  Neighborhoods "
                        "notice.  So do the ledgers."
                    ),
                    "deltas": {"weaving": 1, "craft": 1, "nerve": -1},
                    "flags": {"surplus_routed_commons": 2},
                },
                "2": {
                    "label": "Route to R&D (tool building, swarm prototypes)",
                    "outcome": (
                        "The surplus becomes capability.  Tools "
                        "multiply.  People wait."
                    ),
                    "deltas": {"craft": 2, "swarm": 1, "nerve": -1},
                },
                "3": {
                    "label": "Route to play (festivals, games, cultural containers)",
                    "outcome": (
                        "The surplus becomes joy, disguised as logistics.  "
                        "Children distribute materials no one audits."
                    ),
                    "deltas": {"play": 2, "surplus_routed_commons": 1, "weaving": 1},
                },
            },
        },

        # ── 6. Swarm deployment ──────────────────────────────────
        {
            "title": "Swarm deployment dilemma",
            "tier_min": 5,
            "setup": (
                "Your agents are ready.  Deploy fast and wide, or slow "
                "and careful?  Speed brings visibility.  Caution costs "
                "tempo."
            ),
            "branches": {
                "1": {
                    "label": "High-tempo deployment (fast, visible)",
                    "outcome": (
                        "Agents flood the network.  Results arrive in "
                        "hours.  So does institutional attention."
                    ),
                    "deltas": {"swarm": 3, "nerve": -3, "craft": 1},
                    "distortion_delta": 3,
                    "tag": "visible",
                },
                "2": {
                    "label": "Staged rollout (measured, stealthy)",
                    "outcome": (
                        "Agents deploy in waves.  Slower, but the "
                        "institutions see only noise."
                    ),
                    "deltas": {"swarm": 1, "reading": 1, "nerve": -1},
                },
                "3": {
                    "label": "Hold and train (build capability, don't deploy)",
                    "outcome": (
                        "The swarm practices in sandbox mode.  No "
                        "real-world data yet.  But readiness compounds."
                    ),
                    "deltas": {"swarm": 2, "play": 1},
                },
            },
        },

        # ── 7. Companion: the Auditor ────────────────────────────
        {
            "title": "The Auditor offers alliance",
            "tier_min": 0,
            "setup": (
                "A disgruntled ledger-keeper approaches.  They can reveal "
                "hidden transfers—but they trust systems too much.  Their "
                "blind spot is institutional faith."
            ),
            "branches": {
                "1": {
                    "label": "Recruit the Auditor",
                    "outcome": (
                        "Your reading deepens.  But the Auditor wants "
                        "everything documented, everything legible."
                    ),
                    "deltas": {"reading": 2, "weaving": 1, "nerve": -1},
                    "flags": {"companions_recruited": 1},
                },
                "2": {
                    "label": "Exchange information, maintain distance",
                    "outcome": (
                        "Useful data flows both ways.  No commitment.  "
                        "No vulnerability."
                    ),
                    "deltas": {"reading": 1, "craft": 1},
                },
                "3": {
                    "label": "Decline: too much institutional faith",
                    "outcome": (
                        "The Auditor returns to the counting rooms.  "
                        "Perhaps you will meet again."
                    ),
                    "deltas": {"nerve": 1},
                },
            },
        },

        # ── 8. Companion: the Festival Keeper ────────────────────
        {
            "title": "The Festival Keeper proposes a season",
            "tier_min": 1,
            "setup": (
                "A traveling festival organizer sees your cell.  They "
                "offer to run a public season—excellent for morale and "
                "cover, terrible for secrecy."
            ),
            "branches": {
                "1": {
                    "label": "Full public season (maximum play, high visibility)",
                    "outcome": (
                        "The streets fill with games, music, hidden "
                        "signals.  Everyone is watching—including them."
                    ),
                    "deltas": {"play": 3, "weaving": 2, "nerve": -3},
                    "flags": {"companions_recruited": 1, "play_capacity": 2},
                    "tag": "visible",
                },
                "2": {
                    "label": "Private workshops only (lower profile)",
                    "outcome": (
                        "Smaller crowds.  Deeper skill transfer.  The "
                        "Festival Keeper is disappointed but useful."
                    ),
                    "deltas": {"play": 1, "craft": 1, "weaving": 1},
                    "flags": {"companions_recruited": 1},
                },
                "3": {
                    "label": "Decline: not ready for public exposure",
                    "outcome": (
                        "The Festival Keeper moves on.  You keep your "
                        "cover and your caution."
                    ),
                    "deltas": {"nerve": 1, "reading": 1},
                },
            },
        },

        # ── 9. Institutional reform offer ────────────────────────
        {
            "title": "Reform or refusal",
            "tier_min": 2,
            "setup": (
                "An institutional faction offers a seat at the table.  "
                "Real influence is possible—but the table is inside the "
                "counting room."
            ),
            "branches": {
                "1": {
                    "label": "Enter the institution (pursue reform from within)",
                    "outcome": (
                        "You gain authority and lose mobility.  The "
                        "reforms you pass are real—but partial, and "
                        "always legible."
                    ),
                    "deltas": {"reading": 2, "nerve": 2, "weaving": -1, "play": -1},
                    "distortion_delta": 2,
                    "tags": ["capture"],
                },
                "2": {
                    "label": "Parallel institution (build outside, coordinate loosely)",
                    "outcome": (
                        "You maintain autonomy while offering the "
                        "institution a mirror.  Slower change.  Cleaner "
                        "hands."
                    ),
                    "deltas": {"craft": 1, "weaving": 1, "reading": 1},
                },
                "3": {
                    "label": "Refuse: the table is a trap",
                    "outcome": (
                        "The door closes.  You remain outside.  The "
                        "meshwork is smaller but free."
                    ),
                    "deltas": {"nerve": 1, "swarm": 1, "play": 1},
                },
            },
        },

        # ── 10. The Playhouse proposition ────────────────────────
        {
            "title": "The Playhouse gambit",
            "tier_min": 0,
            "setup": (
                "Puppeteers, toy makers, and game designers offer to "
                "embed coordination protocols in child-facing cultural "
                "artifacts.  The materials would appear innocuous to "
                "every authority."
            ),
            "branches": {
                "1": {
                    "label": "Full protocol embedding (deep coordination layer)",
                    "outcome": (
                        "Children carry messages they do not know they "
                        "carry.  Games teach systems thinking without "
                        "naming it.  The container is durable."
                    ),
                    "deltas": {"play": 2, "craft": 1, "surplus_routed_commons": 2},
                    "flags": {"play_capacity": 2},
                },
                "2": {
                    "label": "Light embedding (educational games, plausible cover)",
                    "outcome": (
                        "The games teach and delight.  A few carry "
                        "extra layers.  Nothing that couldn't survive "
                        "an audit."
                    ),
                    "deltas": {"play": 1, "weaving": 1, "craft": 1},
                    "flags": {"play_capacity": 1},
                },
                "3": {
                    "label": "Decline: keep play pure of coordination",
                    "outcome": (
                        "The games remain games.  Joy without payload.  "
                        "Sometimes that is enough."
                    ),
                    "deltas": {"play": 1, "nerve": 1},
                },
            },
        },

        # ── 11. Platform enclosure attempt ───────────────────────
        {
            "title": "Platform enclosure offer",
            "tier_min": 5,
            "setup": (
                "A major platform offers to 'partner' with your meshwork.  "
                "Funding, infrastructure, reach.  The terms require "
                "legibility, logging, and a brand license."
            ),
            "branches": {
                "1": {
                    "label": "Partner (accept enclosure for resources)",
                    "outcome": (
                        "The resources arrive.  So do the metrics.  Your "
                        "meshwork becomes a product feature."
                    ),
                    "deltas": {"craft": 2, "swarm": 1, "weaving": -2, "play": -1},
                    "distortion_delta": 3,
                    "tags": ["capture"],
                },
                "2": {
                    "label": "Fork: take inspiration, maintain independence",
                    "outcome": (
                        "You learn from their infrastructure without "
                        "entering it.  Slower.  Cleaner."
                    ),
                    "deltas": {"reading": 1, "craft": 1, "nerve": -1},
                },
                "3": {
                    "label": "Publicly refuse (model openness)",
                    "outcome": (
                        "Your refusal becomes a signal.  Others see "
                        "that enclosure is not inevitable."
                    ),
                    "deltas": {"weaving": 1, "play": 1, "surplus_routed_commons": 1},
                },
            },
        },

        # ── 12. Doctrine selection ───────────────────────────────
        {
            "title": "Doctrine crystallizes",
            "tier_min": 1,
            "setup": (
                "Your practice has developed a recognizable pattern.  "
                "You can formalize it as a doctrine—or let it remain "
                "informal and adaptive."
            ),
            "branches": {
                "1": {
                    "label": "Festival Shield (public events reduce scrutiny)",
                    "outcome": (
                        "The doctrine of visible joy.  Festivals become "
                        "camouflage.  But everyone knows when you celebrate."
                    ),
                    "deltas": {"play": 2, "nerve": 1},
                    "flags": {"doctrines_unlocked": 1},
                },
                "2": {
                    "label": "Counter-Ledger (hidden parallel accounting)",
                    "outcome": (
                        "The doctrine of alternate records.  Communities "
                        "see what the institutions hide.  But the ledgers "
                        "must be protected."
                    ),
                    "deltas": {"reading": 2, "craft": 1},
                    "flags": {"doctrines_unlocked": 1},
                },
                "3": {
                    "label": "Distributed Memory (archives survive raids)",
                    "outcome": (
                        "The doctrine of resilient knowledge.  Everything "
                        "fragmented, redundant, encoded.  Slower to "
                        "access—but impossible to erase."
                    ),
                    "deltas": {"craft": 2, "swarm": 1},
                    "flags": {"doctrines_unlocked": 1},
                },
            },
        },

        # ── 13. Companion: the Child Librarian ────────────────────
        {
            "title": "The Child Librarian appears",
            "tier_min": 1,
            "setup": (
                "A young keeper of stories approaches.  They know where "
                "the children's books carry extra layers.  They can "
                "unlock youth channels and durable memetic diffusion—but "
                "they need both creative content and distribution logistics."
            ),
            "branches": {
                "1": {
                    "label": "Recruit the Child Librarian",
                    "outcome": (
                        "Youth channels open.  Stories propagate through "
                        "playgrounds.  The memes are small but durable—"
                        "they will outlast the current regime."
                    ),
                    "deltas": {"play": 2, "weaving": 1, "nerve": -1},
                    "flags": {"companions_recruited": 1, "play_capacity": 1},
                },
                "2": {
                    "label": "Exchange techniques only",
                    "outcome": (
                        "You learn their encoding methods.  They learn "
                        "your distribution routes.  No formal alliance."
                    ),
                    "deltas": {"play": 1, "craft": 1},
                },
                "3": {
                    "label": "Decline: too young for this work",
                    "outcome": (
                        "The child nods and vanishes into the stacks.  "
                        "You notice the books they left behind are "
                        "already encoded."
                    ),
                    "deltas": {"reading": 1},
                },
            },
        },

        # ── 14. Companion: the Defector ───────────────────────────
        {
            "title": "The Defector's confession",
            "tier_min": 2,
            "setup": (
                "A former institutional insider seeks asylum.  They know "
                "the theater machinery from the inside—how legitimacy "
                "is manufactured, which displays are hollow.  But they "
                "carry habits of control."
            ),
            "branches": {
                "1": {
                    "label": "Recruit the Defector (full integration)",
                    "outcome": (
                        "They reveal the machinery: which ceremonies are "
                        "theater, which enforcement is bluff.  But they "
                        "keep organizing people into hierarchies."
                    ),
                    "deltas": {"reading": 2, "nerve": 1, "weaving": -1},
                    "flags": {"companions_recruited": 1, "theater_punctures": 1},
                },
                "2": {
                    "label": "Debrief and release (take knowledge, no commitment)",
                    "outcome": (
                        "The debriefing yields critical intelligence.  "
                        "The Defector returns to civilian life.  You "
                        "know more.  You are not safer."
                    ),
                    "deltas": {"reading": 2, "nerve": -1},
                },
                "3": {
                    "label": "Decline: could be a double agent",
                    "outcome": (
                        "The Defector disappears into the crowd.  Their "
                        "information might have been genuine.  Or might "
                        "have been bait."
                    ),
                    "deltas": {"nerve": 1},
                },
            },
        },

        # ── 15. Companion: the Dreamer ────────────────────────────
        {
            "title": "The Dreamer seeks you out",
            "tier_min": 0,
            "setup": (
                "A quiet figure who receives vivid recurring signals—"
                "dreams of a unified continent, intuitions about "
                "institutional weakness that no logic supports.  High "
                "cosmic sensitivity but poor institutional navigation.  "
                "They need protection to be useful."
            ),
            "branches": {
                "1": {
                    "label": "Recruit the Dreamer (protect their receptivity)",
                    "outcome": (
                        "The Dreamer joins your cell.  Their dreams become "
                        "a strategic resource—warning of crises before "
                        "they manifest.  But keeping them functional "
                        "requires constant shielding from institutional noise."
                    ),
                    "deltas": {"reading": 1, "play": 1, "nerve": -1},
                    "flags": {
                        "companions_recruited": 1,
                        "quantum_telepathy": 1,
                        "neganthropomorphic_signal": 1,
                        "cosmic_awareness": 1,
                    },
                },
                "2": {
                    "label": "Meet regularly, share dreams (informal channel)",
                    "outcome": (
                        "You listen to their dreams.  Some are noise.  "
                        "Some carry information that changes your reading "
                        "of the situation entirely."
                    ),
                    "deltas": {"reading": 1},
                    "flags": {"quantum_telepathy": 1, "cosmic_awareness": 1},
                },
                "3": {
                    "label": "Decline: dreams are not actionable intelligence",
                    "outcome": (
                        "The Dreamer nods.  That night you dream of a "
                        "single continent surrounded by calm water."
                    ),
                    "deltas": {"nerve": 1},
                    "flags": {"cosmic_awareness": 1},
                },
            },
        },

        # ── 16. Companion: the Swarm Conductor ────────────────────
        {
            "title": "The Swarm Conductor offers coordination",
            "tier_min": 4,
            "setup": (
                "An expert in multi-agent orchestration sees your "
                "network.  They can make swarms efficient—but risk "
                "over-automation and the flattening of local context."
            ),
            "branches": {
                "1": {
                    "label": "Recruit the Swarm Conductor",
                    "outcome": (
                        "Your agents multiply in capability.  But the "
                        "Conductor's tendency toward centralized control "
                        "must be constantly resisted."
                    ),
                    "deltas": {"swarm": 3, "weaving": -1, "nerve": -1},
                    "flags": {"companions_recruited": 1, "augmentation_depth": 1},
                },
                "2": {
                    "label": "Contract for specific operations only",
                    "outcome": (
                        "The Conductor optimizes your logistics without "
                        "touching your culture.  Surgical.  Professional.  "
                        "Distant."
                    ),
                    "deltas": {"swarm": 1, "craft": 1},
                },
                "3": {
                    "label": "Decline: swarms must self-organize",
                    "outcome": (
                        "Your agents remain messy, plural, and slow.  "
                        "They also remain yours."
                    ),
                    "deltas": {"play": 1, "nerve": 1},
                },
            },
        },

        # ── 17. Companion: the Smuggler-Curator ───────────────────
        {
            "title": "The Smuggler-Curator proposes a route",
            "tier_min": 2,
            "setup": (
                "A figure who moves cultural goods through innocuous "
                "channels.  Forged documents, encoded maps, material "
                "that bypasses inspection.  Craft-based augmentation "
                "transfer across borders."
            ),
            "branches": {
                "1": {
                    "label": "Recruit the Smuggler-Curator",
                    "outcome": (
                        "New routes open.  Knowledge and tools flow "
                        "through channels no institution monitors.  But "
                        "every route has a toll."
                    ),
                    "deltas": {"craft": 2, "nerve": -1, "weaving": 1},
                    "flags": {"companions_recruited": 1, "augmentation_breadth": 1},
                },
                "2": {
                    "label": "Arrange a single shipment",
                    "outcome": (
                        "Critical materials arrive disguised as "
                        "something ordinary.  The route works.  Once."
                    ),
                    "deltas": {"craft": 1, "reading": 1},
                },
                "3": {
                    "label": "Decline: borders are someone else's problem",
                    "outcome": (
                        "The Smuggler-Curator smiles.  'Borders are "
                        "everyone's problem.  You just haven't noticed "
                        "yours yet.'"
                    ),
                    "deltas": {"nerve": 1},
                },
            },
        },

        # ── 18. Companion: the Oracle's Grandchild ────────────────
        {
            "title": "The Oracle's Grandchild inherits the trance",
            "tier_min": 0,
            "setup": (
                "A lineage keeper from an agricultural-era tradition, "
                "adapted for the current era.  They perceive systemic "
                "patterns that computation misses.  Building trust "
                "requires intuitive, not instrumental, engagement."
            ),
            "branches": {
                "1": {
                    "label": "Recruit the Oracle's Grandchild",
                    "outcome": (
                        "Ancient trance-state techniques meet modern "
                        "crisis.  The patterns they reveal are invisible "
                        "to every ledger.  But their methods unsettle "
                        "the rationalists in your cell."
                    ),
                    "deltas": {"reading": 1, "play": 1, "nerve": -1},
                    "flags": {
                        "companions_recruited": 1,
                        "quantum_telepathy": 1,
                        "augmentation_breadth": 1,
                    },
                },
                "2": {
                    "label": "Learn one technique, maintain distance",
                    "outcome": (
                        "They teach you a breathing pattern that opens "
                        "perception.  You are not ready for the full "
                        "transmission."
                    ),
                    "deltas": {"reading": 1},
                    "flags": {"augmentation_depth": 1},
                },
                "3": {
                    "label": "Decline: the old ways are not for us",
                    "outcome": (
                        "The Oracle's Grandchild shrugs.  'The old ways "
                        "are the only ways that persist.  Everything "
                        "else is a fad.'"
                    ),
                    "deltas": {"nerve": 1},
                },
            },
        },

        # ── 19. Doctrine: advanced doctrines ──────────────────────
        {
            "title": "A deeper doctrine crystallizes",
            "tier_min": 3,
            "setup": (
                "Your practice has deepened.  New possibilities emerge "
                "from the intersection of augmentation, quantum capacity, "
                "and institutional reading."
            ),
            "branches": {
                "1": {
                    "label": "Signal Reception (develop Neganthropomorphic channels)",
                    "outcome": (
                        "The meshwork becomes a receiver.  Dreams, art, "
                        "play, and intuition are cultivated as strategic "
                        "resources.  But visibility increases."
                    ),
                    "deltas": {"play": 1, "reading": 1},
                    "flags": {
                        "doctrines_unlocked": 1,
                        "neganthropomorphic_signal": 2,
                        "cosmic_awareness": 1,
                    },
                },
                "2": {
                    "label": "Entropy Auditing (detect Entropiric computation)",
                    "outcome": (
                        "You learn to recognize when a policy is not "
                        "merely misguided but computationally seduced—"
                        "classical logic streaming from outside.  You "
                        "can counter it.  Using logic is the risk."
                    ),
                    "deltas": {"reading": 2, "nerve": -1},
                    "flags": {
                        "doctrines_unlocked": 1,
                        "cosmic_awareness": 1,
                        "entropiric_saturation": 1,
                    },
                },
                "3": {
                    "label": "Quantum Integration (blend classical and quantum)",
                    "outcome": (
                        "The Amasia model in miniature.  Quantum capacity "
                        "enhances classical operations.  Classical "
                        "competence protects quantum development.  The "
                        "most balanced, most demanding path."
                    ),
                    "deltas": {"craft": 1, "play": 1, "reading": 1, "nerve": -1},
                    "flags": {
                        "doctrines_unlocked": 1,
                        "quantum_telepathy": 1,
                        "quantum_psionics": 1,
                        "quantum_magick": 1,
                    },
                },
            },
        },

        # ── 20. Cosmic doctrine ───────────────────────────────────
        {
            "title": "The Perpendicular doctrine reveals itself",
            "tier_min": 5,
            "setup": (
                "At the intersection of high quantum capacity and deep "
                "cosmic awareness, a new orientation becomes possible—"
                "not opposing the enclosure from within its frame, but "
                "perpendicular to the entire plane of contestation."
            ),
            "condition": lambda g: (
                int(g.flags.get("cosmic_awareness", 0)) >= 4
                and (
                    int(g.flags.get("quantum_telepathy", 0))
                    + int(g.flags.get("quantum_psionics", 0))
                    + int(g.flags.get("quantum_magick", 0))
                ) >= 6
            ),
            "branches": {
                "1": {
                    "label": "The Perpendicular Probable (inhabit the Outside of the Outside)",
                    "outcome": (
                        "Not victory.  Not defeat.  A rotation into a "
                        "dimension the game did not initially expose.  "
                        "You perceive options that reframe situations "
                        "rather than optimizing within them.  The most "
                        "demanding doctrine.  Every enclosure offers "
                        "comfort.  Every perpendicularity costs certainty."
                    ),
                    "deltas": {"reading": 1, "play": 1, "craft": 1, "nerve": -2},
                    "flags": {
                        "doctrines_unlocked": 2,
                        "quantum_magick": 2,
                        "cosmic_awareness": 2,
                    },
                },
                "2": {
                    "label": "Amasia Protocol (build Decolony prototypes)",
                    "outcome": (
                        "You commit to building institutions modeled on "
                        "the Decolonies of Amasia—health equity, 30% "
                        "material throughput, a culture of invention.  "
                        "The most ambitious doctrine: prototyping a "
                        "civilization that doesn't exist yet."
                    ),
                    "deltas": {"craft": 2, "weaving": 1, "nerve": -1},
                    "flags": {
                        "doctrines_unlocked": 2,
                        "neganthropomorphic_signal": 2,
                        "augmentation_fidelity": 2,
                    },
                },
                "3": {
                    "label": "Ember Keeping (protect quantum capacities everywhere)",
                    "outcome": (
                        "You dedicate resources to preserving the quantum "
                        "capacities of communities—telepathy, psionics, "
                        "magicks.  Resisting the Entropire's disorganization "
                        "strategies.  High opportunity cost.  Deep necessity."
                    ),
                    "deltas": {"weaving": 1, "play": 1, "nerve": -1},
                    "flags": {
                        "doctrines_unlocked": 1,
                        "quantum_telepathy": 1,
                        "quantum_psionics": 1,
                        "neganthropomorphic_signal": 1,
                    },
                },
            },
        },
    ],

    # ═══════════════════════════════════════════════════════════════
    # Recurring cost  (institutional pressure drains nerve)
    # ═══════════════════════════════════════════════════════════════

    "recurring_cost": {
        "stat": "nerve",
        "base": 1,
        "tier_scales": {3: 1, 5: 1},
        "log_template": "Institutional pressure registers (−{cost} Nerve).",
    },

    # ═══════════════════════════════════════════════════════════════
    # Chapter assessment  (periodic review)
    # ═══════════════════════════════════════════════════════════════

    "review": {
        "title": "Chapter Assessment",
        "checks": [
            {
                "label": "Surplus awareness",
                "condition": lambda g: g.stats["reading"] >= 4,
            },
            {
                "label": "Network health",
                "condition": lambda g: g.stats["weaving"] >= 3,
            },
            {
                "label": "Play infrastructure",
                "condition": lambda g: (
                    g.stats["play"] >= 3
                    or int(g.flags.get("play_capacity", 0)) >= 3
                ),
            },
            {
                "label": "Operational security",
                "condition": lambda g: g.stats["nerve"] >= 3,
            },
            {
                "label": "Technical readiness",
                "condition": lambda g: g.stats["craft"] >= 3,
            },
            {
                "label": "Swarm literacy",
                "condition": lambda g: g.stats["swarm"] >= 3,
            },
            {
                "label": "Cell integrity",
                "condition": lambda g: g.flags.get("cell_secure", True),
            },
            {
                "label": "Archive intact",
                "condition": lambda g: g.flags.get("archive_intact", True),
            },
            {
                "label": "Augmentation depth",
                "condition": lambda g: int(g.flags.get("augmentation_depth", 0)) >= 3,
            },
            {
                "label": "Quantum capacity emerging",
                "condition": lambda g: (
                    int(g.flags.get("quantum_telepathy", 0))
                    + int(g.flags.get("quantum_psionics", 0))
                    + int(g.flags.get("quantum_magick", 0))
                ) >= 3,
            },
            {
                "label": "Cosmic perception",
                "condition": lambda g: int(g.flags.get("cosmic_awareness", 0)) >= 2,
            },
        ],
        "adjustments": [_review_fear_warning, _review_play_erosion, _review_entropiric_pressure],
    },

    # ═══════════════════════════════════════════════════════════════
    # Endings  (checked in priority order)
    # ═══════════════════════════════════════════════════════════════

    "endings": [
        {
            "id": "collapsed",
            "priority": 0,
            "condition": lambda g: (
                (g.stats["nerve"] <= 0 and g.stats["weaving"] <= 1)
                or (g.stats["nerve"] <= 0 and g.stats["reading"] <= 1)
            ),
            "epilogue": lambda g: (
                f"ABSORBED — {g.player_name}\n\n"
                "The meshwork dissolves.  Your cell is legible now—fully "
                "counted, fully captured.  The archive you built becomes "
                "a training dataset.  The children's games are rebranded "
                "as 'engagement modules.'  You are offered a title.  The "
                "surplus flows on.\n"
            ),
        },
        {
            "id": "new_priesthood",
            "priority": 1,
            "condition": lambda g: (
                g.stats["reading"] >= 14
                and g.stats["swarm"] >= 14
                and g.stats["play"] <= 4
                and g.distortion >= 6
            ),
            "epilogue": lambda g: (
                f"THE NEW PRIESTHOOD — {g.player_name}\n\n"
                "You defeated the scamonomic loop and built a subtler one.  "
                "Your reading is unmatched.  Your swarm is vast.  But the "
                "play has drained from the system.  You are the new "
                "intermediary.  The counting rooms recognize your "
                "handwriting.\n"
            ),
        },
        {
            "id": "cognitive_freeport",
            "priority": 2,
            "condition": lambda g: (
                g.stats["swarm"] >= 14
                and g.stats["craft"] >= 12
                and g.stats["weaving"] <= 6
            ),
            "epilogue": lambda g: (
                f"COGNITIVE FREEPORT — {g.player_name}\n\n"
                "The mesh wins on speed and innovation.  Tools propagate.  "
                "But the human ties fray.  The freeport is brilliant, "
                "technical, and alone.  Children learn to code before they "
                "learn to trust.  The surplus routes through the network "
                "but not through the neighborhood.\n"
            ),
        },
        {
            "id": "gentle_counterstate",
            "priority": 3,
            "condition": lambda g: (
                g.stats["reading"] >= 12
                and g.stats["weaving"] >= 10
                and g.stats["nerve"] >= 8
                and g.tier >= 3
            ),
            "epilogue": lambda g: (
                f"THE GENTLE COUNTERSTATE — {g.player_name}\n\n"
                "Reformist meshworks achieve partial institutional capture.  "
                "Stability is gained.  Some surplus reroutes to commons.  "
                "But the bureaucracy begins to return—gentler, more "
                "literate, still counting.  The question is whether play "
                "survives the paperwork.\n"
            ),
        },
        {
            "id": "festival_republic",
            "priority": 4,
            "condition": lambda g: (
                g.stats["play"] >= 14
                and g.stats["weaving"] >= 12
                and g.stats["craft"] >= 8
            ),
            "epilogue": lambda g: (
                f"FESTIVAL REPUBLIC — {g.player_name}\n\n"
                "Loose commons and cultural protocols thrive.  Streets "
                "fill with games, stories, and shared meals.  Children "
                "invent governments from chalk lines and jump rope.  But "
                "defense remains fragile.  The next scamonomic cycle is "
                "already forming beyond the festival lights.\n"
            ),
        },
        {
            "id": "invisible_schools",
            "priority": 5,
            "condition": lambda g: (
                g.stats["reading"] >= 12
                and g.stats["craft"] >= 12
                and g.stats["play"] >= 8
                and int(g.flags.get("theater_punctures", 0)) >= 4
            ),
            "epilogue": lambda g: (
                f"INVISIBLE SCHOOLS — {g.player_name}\n\n"
                "Public power is lost.  The institutions totalize.  "
                "But knowledge survives underground—in children's rhymes, "
                "in smuggled tools, in games that teach systems thinking "
                "without naming it.  The schools are everywhere and "
                "nowhere.  The next generation will read what you hid.\n"
            ),
        },
        {
            "id": "playvolution",
            "priority": 6,
            "condition": lambda g: (
                g.stats["play"] >= 12
                and g.stats["swarm"] >= 10
                and g.stats["weaving"] >= 10
                and int(g.flags.get("doctrines_unlocked", 0)) >= 4
                and g.stats["nerve"] >= 6
            ),
            "epilogue": lambda g: (
                f"PLAYVOLUTION — {g.player_name}\n\n"
                "No final victory.  But society normalizes public "
                "experimentation, shared tools, and child-safe innovation "
                "spaces enough to prevent total enclosure.  Play is not a "
                "reward.  It is infrastructure.  "
                f"Reading {g.stats['reading']}, Weaving {g.stats['weaving']}, "
                f"Play {g.stats['play']}, Craft {g.stats['craft']}, "
                f"Nerve {g.stats['nerve']}, Swarm {g.stats['swarm']}.  "
                "The surplus has new places to go.\n"
            ),
        },
        {
            "id": "entropires_feast",
            "priority": 0,
            "condition": lambda g: (
                g.stats["nerve"] <= 0
                and int(g.flags.get("entropiric_saturation", 0)) >= 8
            ),
            "epilogue": lambda g: (
                f"THE ENTROPIRE'S FEAST — {g.player_name}\n\n"
                "You optimized successfully.  Every metric improved.  "
                "Every efficiency was captured.  The surplus flowed "
                "exactly where the logic dictated.\n\n"
                "And the Entropire fed.  On the disorder your efficiency "
                "produced.  On the suffering your optimization ignored.  "
                "On the entropy your rationality generated as a structural "
                "byproduct.\n\n"
                "Your 'victories' were its nourishment.  Rationality itself "
                "was the trap.  The computation streams in.  It always "
                "did.\n"
            ),
        },
        {
            "id": "amasia_signal",
            "priority": 5,
            "condition": lambda g: (
                int(g.flags.get("neganthropomorphic_signal", 0)) >= 8
                and int(g.flags.get("augmentation_fidelity", 0)) >= 5
                and int(g.flags.get("cosmic_awareness", 0)) >= 3
                and g.stats["play"] >= 10
            ),
            "epilogue": lambda g: (
                f"AMASIA'S SIGNAL — {g.player_name}\n\n"
                "The signal reached critical strength.  Blueprints arrived "
                "through a child's game, a dream, and an open-source "
                "framework.  Institutional designs from a civilization that "
                "produces well-being with 30% of the material throughput.  "
                "Incentive architectures that make negentropic behavior "
                "the rational default.\n\n"
                "The Entropire is not defeated.  But for the first time, "
                "it is outcomputed.  The first Decolony prototype is "
                "small and fragile.  Built on knowledge received through "
                "channels the Entropire cannot monitor.\n\n"
                f"Telepathy {g.flags.get('quantum_telepathy', 0)}, "
                f"Psionics {g.flags.get('quantum_psionics', 0)}, "
                f"Magick {g.flags.get('quantum_magick', 0)}.  "
                "The signal is not a guarantee.  It is a possibility.\n"
            ),
        },
        {
            "id": "computation_continues",
            "priority": 7,
            "condition": lambda g: (
                g.tier >= 4
                and g.stats["nerve"] >= 4
                and int(g.flags.get("doctrines_unlocked", 0)) >= 3
                and g.total_turns >= 40
            ),
            "epilogue": lambda g: (
                f"THE COMPUTATION CONTINUES — {g.player_name}\n\n"
                "A partial playvolution.  Enough to prevent total "
                "enclosure.  Not enough to reach Amasia.\n\n"
                f"Entropiric saturation: {g.flags.get('entropiric_saturation', 0)}.  "
                "Decreased but not ended.\n"
                f"Neganthropomorphic signal: {g.flags.get('neganthropomorphic_signal', 0)}.  "
                "Increased but still noisy.\n"
                f"Cosmic awareness: {g.flags.get('cosmic_awareness', 0)}.  "
                "The player has glimpsed the forces behind the struggle.\n\n"
                "The cosmic contestation continues.  Your achievements "
                "are real and provisional.  The Entropire is wounded "
                "but not dead.  The Neganthropomorphs are closer but "
                "have not arrived.  The honest ending: the struggle is "
                "ongoing, and your contribution mattered.\n"
            ),
        },
        {
            "id": "perpendicular_probable",
            "priority": 8,
            "condition": lambda g: (
                int(g.flags.get("cosmic_awareness", 0)) >= 7
                and (
                    int(g.flags.get("quantum_telepathy", 0))
                    + int(g.flags.get("quantum_psionics", 0))
                    + int(g.flags.get("quantum_magick", 0))
                ) >= 10
                and int(g.flags.get("doctrines_unlocked", 0)) >= 5
                and g.stats["play"] >= 8
                and g.stats["reading"] >= 8
            ),
            "epilogue": lambda g: (
                f"THE PERPENDICULAR PROBABLE — {g.player_name}\n\n"
                "Not by winning the game.  By rotating the dimension "
                "in which winning was defined.\n\n"
                "The Entropire is not defeated.  The Neganthropomorphs "
                "are not triumphant.  The player simply stepped "
                "perpendicular to the entire contestation—inhabiting "
                "the classical world, navigating quantum state spaces, "
                "and perceiving the dimension orthogonal to both.\n\n"
                "The meshwork does not replace institutions.  It exists "
                "alongside them, within them, and yet oriented along a "
                "dimension they cannot perceive.  The playvolution does "
                "not overthrow the scamonomic cycle.  It renders the "
                "cycle irrelevant by operating in a dimension the cycle "
                "doesn't occupy.\n\n"
                "The game ends not with victory but with the discovery "
                "that the game was always larger than it appeared—and "
                "that the player was always capable of dimensions they "
                "were never told about.\n"
            ),
        },
    ],

    # ═══════════════════════════════════════════════════════════════
    # Post-turn hook
    # ═══════════════════════════════════════════════════════════════

    "custom_turn_end": _combined_turn_end,

    # ═══════════════════════════════════════════════════════════════
    # Help text
    # ═══════════════════════════════════════════════════════════════

    "help_text": """
Commands:
  status              Dashboard (six capabilities)
  advanced            Show Heat, augmentation regime, quantum capacities,
                      cosmic awareness, and hidden world state
  journal             Event log
  help                This text
  quit                Exit

Each phase:
  Enter THREE action indices from the menu, space-separated.
  Then an event fires, then an encounter (choose a branch).

Your operative name and calling appear on the status header.

Core loop:
  Detect surplus -> Read the assemblage -> Choose posture ->
  Build meshworks -> Use play -> Survive the crisis -> Seed the next layer.

Eras and augmentation:
  Each era has a dominant augmentation regime that unlocks unique actions:
    Grain/Fief       Spirits & Psychedelics (trance, spirit alliance)
    Empire           Tools, Craft & Bodily Extension (specialized tools, guilds)
    Machine/Finance  Media, Logic & Proto-Computation (counter-media, encrypted nets)
    Platform/Swarm   Cultural Games & Self-Organizing Frameworks

Hidden progression:
  Quantum capacities (Telepathy, Psionics, Magick) develop through
  augmentation practices and Neganthropomorphic signal reception.
  Cosmic awareness grows as you perceive the forces behind institutions.
  These are revealed by the 'advanced' command as they emerge.

Tips:
  Nerve is your survival resource — it drains from actions and pressure.
  High Heat hides risky actions; keep your profile low or puncture the theater.
  Route surplus toward commons to unlock the Playvolution ending.
  Archive knowledge to unlock doctrines that persist across eras.
  Invest in augmentation to develop quantum capacities.
  Recruit companions for unique capabilities and cosmic sensitivity.
  The Entropire feeds on optimization without awareness.
  The Neganthropomorphs amplify play, dreams, and intuition.

Endings (11 total):
  Absorbed, The New Priesthood, Cognitive Freeport, Gentle Counterstate,
  Festival Republic, Invisible Schools, The Entropire's Feast,
  Amasia's Signal, The Computation Continues, Playvolution,
  The Perpendicular Probable.

Restart: python3 text_adventure_engine.py playvolution_config --quick [seed]
""",
}
