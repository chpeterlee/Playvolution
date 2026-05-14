#!/usr/bin/env python3
"""
Universal Text Adventure Engine
================================

A data-driven game engine for turn-based text adventures.  All theme
content (stats, actions, events, offers, endings, ...) lives in a
separate Python config module that exports a ``CONFIG`` dict.  The
engine itself is fully generic.

Features
--------
- Point-buy character creation with archetypes/classes
- Configurable stats with per-stat bounds
- Per-turn actions (pick N from a menu)
- Random events (tier-gated)
- Branching offers with multiple outcomes
- Optional distortion/stress subsystem (hides risky actions)
- Tier promotion system with custom conditions
- Multiple endings with priority-based checking
- Journal / event log
- Periodic review subsystem
- Recurring cost (e.g. rent) subsystem
- Custom action handlers for special mechanics

Usage
-----
    python3 text_adventure_engine.py <config_module> [--quick] [seed]

Examples
--------
    python3 text_adventure_engine.py artcraft_config
    python3 text_adventure_engine.py artcraft_config --quick
    python3 text_adventure_engine.py artcraft_config --quick 42

Creating a new game
-------------------
Create a Python file that defines a ``CONFIG`` dict with all game
content.  See ``artcraft_config.py`` for a complete working example.

Minimal CONFIG keys required:
    title, subtitle, stats, archetypes, default_archetype_suggested,
    tiers, actions_per_turn, actions, events, offers, endings

Run from https://github.com/anthropics/claude-code
"""

from __future__ import annotations

import importlib
import os
import random
import sys
from typing import Any


# ── Utilities ──────────────────────────────────────────────────────────


def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


def _number_word(n: int) -> str:
    return {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE"}.get(n, str(n))


# ── Config validation ─────────────────────────────────────────────────


REQUIRED_KEYS = {
    "title", "subtitle", "stats", "archetypes",
    "default_archetype_suggested", "tiers", "actions_per_turn",
    "actions", "events", "offers", "endings",
}


def validate_config(cfg: dict) -> list[str]:
    """Return a list of validation errors (empty means valid)."""
    errors: list[str] = []
    missing = REQUIRED_KEYS - set(cfg.keys())
    if missing:
        errors.append(f"Missing required config keys: {', '.join(sorted(missing))}")
    sc = cfg.get("stats", {})
    for k in ("keys", "labels", "bounds", "defaults", "point_pool",
              "stat_floor", "stat_ceil"):
        if k not in sc:
            errors.append(f"Missing stats.{k}")
    if "keys" in sc and "defaults" in sc:
        for k in sc["keys"]:
            if k not in sc["defaults"]:
                errors.append(f"Stat key '{k}' missing from stats.defaults")
    return errors


# ── Character creation ────────────────────────────────────────────────


def validate_point_buy(stats: dict[str, int], cfg: dict) -> str | None:
    sc = cfg["stats"]
    keys = sc["keys"]
    floor = sc["stat_floor"]
    ceil = sc["stat_ceil"]
    pool = sc["point_pool"]
    labels = sc["labels"]
    for k in keys:
        if k not in stats:
            return f"Missing stat: {k}"
        v = stats[k]
        if not isinstance(v, int):
            return "All stats must be integers."
        if v < floor or v > ceil:
            return f"{labels.get(k, k)} must be between {floor} and {ceil} (got {v})."
    total = sum(stats[k] for k in keys)
    if total != pool:
        return f"Stats must sum to exactly {pool} (currently {total})."
    return None


def parse_stats_line(line: str, keys: list[str]) -> dict[str, int] | None:
    parts = line.replace(",", " ").split()
    if len(parts) != len(keys):
        return None
    out: dict[str, int] = {}
    for k, p in zip(keys, parts):
        if not p.lstrip("-").isdigit():
            return None
        out[k] = int(p)
    return out


def interactive_point_buy(cfg: dict) -> dict[str, int] | None:
    sc = cfg["stats"]
    keys = sc["keys"]
    floor = sc["stat_floor"]
    ceil = sc["stat_ceil"]
    pool = sc["point_pool"]
    labels = sc["labels"]

    stats: dict[str, int] = {}
    remaining = pool
    n = len(keys)
    for i, k in enumerate(keys):
        if i == n - 1:
            if not (floor <= remaining <= ceil):
                print(
                    f"Cannot complete: {remaining} points left for last stat "
                    f"(need {floor}-{ceil}). Start allocation again."
                )
                return None
            stats[k] = remaining
            return stats
        rem_slots = n - i - 1
        vmin = max(floor, remaining - ceil * rem_slots)
        vmax = min(ceil, remaining - floor * rem_slots)
        while True:
            prompt = f"  {labels[k]} ({vmin}-{vmax}), {remaining} points left in pool: "
            raw = input(prompt).strip()
            if not raw.isdigit():
                print("Enter a whole number.")
                continue
            v = int(raw)
            if v < vmin or v > vmax:
                print(f"Must be between {vmin} and {vmax}.")
                continue
            stats[k] = v
            remaining -= v
            break
    return stats


def run_character_creation(cfg: dict) -> dict[str, Any]:
    """Interactive character creation.  Returns a profile dict."""
    cc = cfg.get("character_creation", {})
    sc = cfg["stats"]
    keys = sc["keys"]
    labels = sc["labels"]

    intro = cc.get("intro_text", "Character creation")
    print(f"\n── {intro} ──\n")
    if cc.get("intro_flavor"):
        print(cc["intro_flavor"] + "\n")

    # ── Name ──
    name_label = cc.get("name_label", "Character name")
    while True:
        name = input(f"{name_label} (1-40 characters): ").strip()
        if 0 < len(name) <= 40:
            break
        print("Name cannot be empty or longer than 40 characters.")

    # ── Archetype ──
    archetypes = cfg["archetypes"]
    archetype_label = cc.get("archetype_label", "archetype")
    archetype_prompt = cc.get("archetype_prompt", f"Choose a {archetype_label}")
    print(f"\n{archetype_prompt} (choose a number):")
    for idx, a in enumerate(archetypes, 1):
        print(f"  {idx}. {a['label']}")
    custom_label = cc.get("custom_archetype_label", "describe yours")
    print(f"  {len(archetypes) + 1}. Other ({custom_label})")

    archetype_chosen = ""
    suggested: dict[str, int] = {}

    while True:
        raw = input(f"\n> {archetype_label} (number): ").strip()
        if not raw.isdigit():
            print("Enter a menu number.")
            continue
        choice = int(raw)
        if 1 <= choice <= len(archetypes):
            entry = archetypes[choice - 1]
            archetype_chosen = entry["label"]
            suggested = dict(entry["suggested"])
            break
        if choice == len(archetypes) + 1:
            custom_prompt = cc.get(
                "custom_archetype_prompt",
                f"Describe your {archetype_label} (1-60 characters): ",
            )
            while True:
                custom = input(custom_prompt).strip()
                if 0 < len(custom) <= 60:
                    archetype_chosen = custom
                    suggested = dict(cfg["default_archetype_suggested"])
                    break
                print("Please enter 1-60 non-empty characters.")
            break
        print(f"Enter 1-{len(archetypes) + 1}.")

    # ── Stat allocation ──
    print("\nSuggested opening stats for this profile:")
    for k in keys:
        print(f"  {labels[k]:14} {suggested[k]}")

    while True:
        mode = input("\nAccept suggested stats [a], or customize [c]? ").strip().lower()
        if mode in ("a", "accept"):
            err = validate_point_buy(suggested, cfg)
            if err:
                print(f"Internal error: {err}")
                continue
            return {"player_name": name, "archetype": archetype_chosen, "stats": suggested}
        if mode in ("c", "custom", "customize"):
            break
        print("Type 'a' to accept or 'c' to customize.")

    pool = sc["point_pool"]
    floor = sc["stat_floor"]
    ceil = sc["stat_ceil"]
    print(
        f"\nCustom allocation: exactly {pool} points across {len(keys)} stats.\n"
        f"Each stat must be {floor}-{ceil} (inclusive).\n"
        "Order: " + ", ".join(f"{labels[k]} ({k})" for k in keys) + ".\n"
        "Enter integers on one line, or type 'interactive' for step-by-step prompts."
    )

    while True:
        line = input("\n> ").strip().lower()
        if line in ("interactive", "i"):
            built = interactive_point_buy(cfg)
            if built is None:
                print("Allocation failed; try again.")
                continue
            err = validate_point_buy(built, cfg)
            if err:
                print(err)
                continue
            return {"player_name": name, "archetype": archetype_chosen, "stats": built}

        parsed = parse_stats_line(line, keys)
        if parsed is None:
            print(f"Need exactly {len(keys)} integers, or 'interactive'.")
            continue
        err = validate_point_buy(parsed, cfg)
        if err:
            print(err)
            continue
        return {"player_name": name, "archetype": archetype_chosen, "stats": parsed}


# ── Game engine ────────────────────────────────────────────────────────


class Game:
    """Generic text adventure game engine driven entirely by a config dict."""

    def __init__(
        self,
        config: dict[str, Any],
        seed: int | None = None,
        profile: dict[str, Any] | None = None,
    ):
        self.cfg = config
        if seed is not None:
            random.seed(seed)
        self.seed = seed

        # ── Stats config ──
        self.stat_keys: list[str] = config["stats"]["keys"]
        self.stat_labels: dict[str, str] = config["stats"]["labels"]
        bounds_cfg = config["stats"].get("bounds", {})
        self._stat_bounds: dict[str, tuple[int, int]] = {}
        for k in self.stat_keys:
            self._stat_bounds[k] = bounds_cfg.get(
                k, bounds_cfg.get("__default__", (0, 20))
            )

        # ── Time ──
        self.turn_noun: str = config.get("turn_noun", "turn")
        self.cycle_noun: str = config.get("cycle_noun", "cycle")
        self.turns_per_cycle: int = config.get("turns_per_cycle", 4)
        self.actions_per_turn: int = config["actions_per_turn"]
        self.turn: int = 1
        self.cycle: int = 1
        self.total_turns: int = 0
        self.tier: int = 0

        # ── Identity ──
        cc = config.get("character_creation", {})
        self.player_name: str = cc.get("player_name_default", "Player")
        self.archetype: str = cc.get("archetype_default", "Unspecified")

        # ── Stats ──
        if profile is not None:
            self.player_name = str(profile.get("player_name", self.player_name))[:40]
            self.archetype = str(profile.get("archetype", self.archetype))[:60]
            self.stats: dict[str, int] = {
                k: int(profile["stats"][k]) for k in self.stat_keys
            }
        else:
            self.stats = dict(config["stats"]["defaults"])

        # ── Distortion (optional subsystem) ──
        dist_cfg = config.get("distortion")
        self.distortion_enabled: bool = (
            dist_cfg is not None and dist_cfg.get("enabled", False)
        )
        self.distortion: int = 0
        if dist_cfg:
            self.distortion_max = dist_cfg.get("max", 15)
            self.distortion_key = dist_cfg.get("stat_key", "distortion")
            self.distortion_label = dist_cfg.get("label", "Distortion")
            self.distortion_desc = dist_cfg.get("description", "")
            self.distortion_mild = dist_cfg.get("mild_threshold", 3)
            self.distortion_mod = dist_cfg.get("mod_threshold", 7)
            self.distortion_hide_chance = dist_cfg.get("hide_chance", 0.35)
            self.distortion_stress_sources = dist_cfg.get("stress_sources", [])
        else:
            self.distortion_max = 15
            self.distortion_key = "distortion"
            self.distortion_label = "Distortion"
            self.distortion_desc = ""
            self.distortion_mild = 3
            self.distortion_mod = 7
            self.distortion_hide_chance = 0.35
            self.distortion_stress_sources = []

        # ── Flags ──
        self.flags: dict[str, Any] = dict(config.get("initial_flags", {}))

        # ── Per-turn tag tracking (e.g. how many "sellout" actions picked) ──
        self._tag_counts: dict[str, int] = {}

        # ── Journal ──
        self.journal: list[str] = []

        # ── Ending ──
        self.ending: str | None = None

        # ── Delta-flag tracking ──
        self._track_delta_flags: list[str] = config.get("track_delta_flags", [])

        # ── Capture tag (optional) ──
        self._capture_tag: str | None = config.get("capture_tag")
        self._capture_flag: str | None = config.get("capture_flag")

    # ── Internal helpers ───────────────────────────────────────────

    def _get_bounds(self, key: str) -> tuple[int, int]:
        return self._stat_bounds.get(key, (0, 20))

    def _apply_stat_deltas(self, deltas: dict[str, int] | None) -> None:
        if not deltas:
            return
        for k, v in deltas.items():
            if k in self.stats:
                lo, hi = self._get_bounds(k)
                self.stats[k] = clamp(self.stats[k] + v, lo, hi)

    def _apply_distortion_delta(self, deltas: dict[str, int] | None) -> None:
        if not deltas or not self.distortion_enabled:
            return
        if self.distortion_key in deltas:
            self.distortion = clamp(
                self.distortion + int(deltas[self.distortion_key]),
                0,
                self.distortion_max,
            )

    def _apply_flag_deltas(self, deltas: dict[str, int] | None) -> None:
        if not deltas:
            return
        for dk in self._track_delta_flags:
            if dk in deltas and dk in self.flags and isinstance(self.flags[dk], int):
                self.flags[dk] += int(deltas[dk])

    def _apply_explicit_flags(self, flags: dict[str, Any] | None) -> None:
        if not flags:
            return
        for k, v in flags.items():
            if k in self.flags:
                if isinstance(self.flags[k], bool):
                    self.flags[k] = bool(v)
                elif isinstance(self.flags[k], int):
                    self.flags[k] = int(self.flags[k]) + int(v)

    # ── Calendar ───────────────────────────────────────────────────

    def log(self, line: str) -> None:
        self.journal.append(
            f"{self.cycle_noun[0].upper()}{self.cycle} "
            f"{self.turn_noun[0].upper()}{self.turn}: {line}"
        )

    def advance_calendar(self) -> None:
        self.total_turns += 1
        self.turn += 1
        if self.turn > self.turns_per_cycle:
            self.turn = 1
            self.cycle += 1
            for k, v in self.cfg.get("cycle_flag_resets", {}).items():
                if k in self.flags:
                    self.flags[k] = v

    def current_tier_name(self) -> str:
        names = self.cfg["tiers"]["names"]
        return names[min(self.tier, len(names) - 1)]

    # ── Distortion ─────────────────────────────────────────────────

    def apply_passive_distortion_tick(self) -> None:
        if not self.distortion_enabled:
            return
        stress = sum(1 for src in self.distortion_stress_sources if src(self))
        self.distortion = clamp(self.distortion + stress, 0, self.distortion_max)

    def distort_menu(self, actions: list[dict]) -> list[dict]:
        if not self.distortion_enabled:
            return actions
        d = self.distortion
        out: list[dict] = []
        for a in actions:
            if a.get("risky") and d > self.distortion_mod:
                continue
            if a.get("risky") and d > self.distortion_mild and random.random() < self.distortion_hide_chance:
                continue
            out.append(a)
        return out if out else actions[:3]

    # ── Actions ────────────────────────────────────────────────────

    def get_actions(self) -> list[dict]:
        pool = [
            a for a in self.cfg["actions"]
            if a.get("tier_min", 0) <= self.tier <= a.get("tier_max", 999)
            and (a.get("condition") is None or a["condition"](self))
        ]
        return self.distort_menu(pool)

    def resolve_special(self, action: dict) -> None:
        sp = action.get("special")
        if not sp:
            return
        handlers = self.cfg.get("action_handlers", {})
        if sp in handlers:
            handlers[sp](self, action)

    def apply_action(self, action: dict) -> None:
        self._apply_stat_deltas(action.get("deltas"))
        tag = action.get("tag")
        if tag:
            self._tag_counts[tag] = self._tag_counts.get(tag, 0) + 1
        self.resolve_special(action)
        self.log(f"Action: {action['label']}")

    # ── Recurring cost ─────────────────────────────────────────────

    def pay_recurring_cost(self) -> None:
        cfg = self.cfg.get("recurring_cost")
        if not cfg:
            return
        base = cfg["base"]
        bonus = sum(
            v for t, v in cfg.get("tier_scales", {}).items() if self.tier >= t
        )
        cost = base + bonus
        lo, hi = self._get_bounds(cfg["stat"])
        self.stats[cfg["stat"]] = clamp(self.stats[cfg["stat"]] - cost, lo, hi)
        self.log(cfg["log_template"].format(cost=cost))

    # ── Events ─────────────────────────────────────────────────────

    def random_event(self) -> dict:
        pool = [e for e in self.cfg["events"] if e.get("tier_min", 0) <= self.tier]
        return random.choice(pool) if pool else self.cfg["events"][0]

    def apply_event(self, evt: dict) -> None:
        self.log(f"Event: {evt['title']}")
        print(f"\n── Event ──\n{evt['flavor']}")
        self._apply_stat_deltas(evt.get("deltas"))
        self._apply_distortion_delta(evt.get("deltas"))
        self._apply_flag_deltas(evt.get("deltas"))
        self._apply_explicit_flags(evt.get("flags"))

    # ── Offers ─────────────────────────────────────────────────────

    def random_offer(self) -> dict:
        pool = [o for o in self.cfg["offers"] if o.get("tier_min", 0) <= self.tier]
        return random.choice(pool) if pool else self.cfg["offers"][0]

    def apply_offer_branch(self, offer: dict, branch_key: str) -> None:
        br = offer["branches"][branch_key]
        print(f"\n── Resolution ──\n{br['outcome']}")
        d = br.get("deltas") or {}
        self._apply_stat_deltas(d)
        self._apply_flag_deltas(d)
        if br.get("distortion_delta"):
            self.distortion = clamp(
                self.distortion + int(br["distortion_delta"]),
                0,
                self.distortion_max,
            )
        if self._capture_tag and self._capture_flag:
            if self._capture_tag in br.get("tags", []):
                self.flags[self._capture_flag] = (
                    int(self.flags.get(self._capture_flag, 0)) + 1
                )
        self._apply_explicit_flags(br.get("flags"))
        self.log(f"Offer «{offer['title']}»: branch {branch_key}")

    # ── Periodic review ────────────────────────────────────────────

    def periodic_review(self) -> None:
        review_cfg = self.cfg.get("review")
        if not review_cfg:
            return
        if self.turn != self.turns_per_cycle:
            return
        title = review_cfg.get("title", "Periodic Review")
        print(f"\n{'═' * 8} {title} {'═' * 8}")
        for check in review_cfg["checks"]:
            ok = check["condition"](self)
            mark = "☑" if ok else "☐"
            print(f"  {mark} {check['label']}")
        for adj in review_cfg.get("adjustments", []):
            adj(self)
        print("═" * (16 + len(title)) + "\n")

    # ── Tier promotion ─────────────────────────────────────────────

    def maybe_promote_tier(self) -> None:
        promotions = self.cfg["tiers"].get("promotions", [])
        check_interval = self.cfg["tiers"].get(
            "check_interval", self.turns_per_cycle
        )
        if self.total_turns == 0 or self.total_turns % check_interval != 0:
            return
        if self.tier >= len(promotions):
            return
        promo = promotions[self.tier]
        # Support multiple alternative conditions per tier
        if "alternatives" in promo:
            for alt in promo["alternatives"]:
                if alt["condition"](self):
                    self.tier += 1
                    self.log(alt["message"])
                    print(f"\n*** {alt['announce']} ***\n")
                    break
        elif promo["condition"](self):
            self.tier += 1
            self.log(promo["message"])
            print(f"\n*** {promo['announce']} ***\n")

    # ── Endings ────────────────────────────────────────────────────

    def check_endings(self) -> None:
        endings = sorted(
            self.cfg.get("endings", []), key=lambda e: e.get("priority", 0)
        )
        for ending in endings:
            if ending["condition"](self):
                self.ending = ending["id"]
                return

    def epilogue(self) -> None:
        endings_map = {e["id"]: e for e in self.cfg.get("endings", [])}
        e = endings_map.get(self.ending)
        if not e:
            print("\nUnknown ending.\n")
            return
        text = e["epilogue"](self) if callable(e["epilogue"]) else e["epilogue"]
        print("\n" + "=" * 50 + "\n" + text)

    # ── Display ────────────────────────────────────────────────────

    def show_status(self, advanced: bool = False) -> None:
        title = self.cfg["title"]
        subtitle = f"{self.player_name} · {self.archetype}"
        if len(subtitle) > 44:
            subtitle = subtitle[:41] + "..."
        print(f"\n{'─' * 46}")
        print(
            f"  {title}  │  {self.cycle_noun.capitalize()} {self.cycle}  "
            f"{self.turn_noun.capitalize()} {self.turn}  │  {self.current_tier_name()}"
        )
        print(f"  {subtitle}")
        print(f"{'─' * 46}")
        for k in self.stat_keys:
            print(f"  {self.stat_labels[k]:14} {self.stats[k]:3}")
        if advanced and self.distortion_enabled:
            desc = f"  ({self.distortion_desc})" if self.distortion_desc else ""
            print(f"  {self.distortion_label:14} {self.distortion:3}{desc}")
        if advanced:
            adv = self.cfg.get("advanced_display", {})
            # Augmentation regime label for current era
            aug_regimes = adv.get("augmentation_regimes", {})
            aug_label = aug_regimes.get(self.tier, "")
            if aug_label:
                print(f"  {'Augmentation':14} {aug_label}")
            # Show tracked hidden flags with non-zero values
            for flag_key, label in adv.get("show_flags", []):
                val = int(self.flags.get(flag_key, 0))
                if val > 0:
                    print(f"  {label:14} {val:3}")
        print(f"  {'Turns done':14} {self.total_turns:3}")
        print(f"{'─' * 46}")

    def show_help(self) -> None:
        print(self.cfg.get("help_text", "Commands: status, advanced, journal, help, quit\n"))

    def show_journal(self) -> None:
        if not self.journal:
            print("\n(Journal empty.)")
            return
        print("\n── Journal ──")
        for line in self.journal[-24:]:
            print(" ", line)
        if len(self.journal) > 24:
            print(f"  ... ({len(self.journal) - 24} earlier entries)")

    # ── Game loop ──────────────────────────────────────────────────

    def play_turn(self) -> bool:
        """Play one full turn.  Return True to continue, False to stop."""
        if self.ending:
            return False

        self._tag_counts = {}

        # Pre-turn hook
        hook = self.cfg.get("custom_turn_start")
        if hook:
            hook(self)

        actions = self.get_actions()
        self.show_status()

        n = self.actions_per_turn
        print(
            f"\n── {self.turn_noun.capitalize()} actions "
            f"(pick {_number_word(n)}, space-separated) ──"
        )
        for i, a in enumerate(actions, 1):
            print(f"  {i:2}. {a['label']}")

        raw = input(f"\n> {n} indices (e.g. 1 4 7), or command: ").strip().lower()
        if raw in ("quit", "exit", "q"):
            return False
        if raw == "status":
            self.show_status()
            return True
        if raw == "advanced":
            self.show_status(advanced=True)
            return True
        if raw == "journal":
            self.show_journal()
            return True
        if raw == "help":
            self.show_help()
            return True

        parts = raw.replace(",", " ").split()
        nums: list[int] = []
        for p in parts:
            if not p.isdigit():
                print("Use positive integers, or a command.")
                return True
            idx = int(p)
            if idx < 1 or idx > len(actions):
                print(f"Index {idx} out of range (1-{len(actions)}).")
                return True
            nums.append(idx)
        if len(nums) != n:
            print(f"Exactly {n} indices required.")
            return True

        for i in nums:
            self.apply_action(actions[i - 1])

        self.apply_event(self.random_event())

        offer = self.random_offer()
        offer_heading = self.cfg.get("offer_heading", "Offer")
        print(f"\n── {offer_heading} ──\n{offer['setup']}")
        for k in sorted(offer["branches"].keys()):
            b = offer["branches"][k]
            print(f"  [{k}] {b['label']}")

        branch_keys = set(offer["branches"].keys())
        while True:
            c = input("\n> offer branch, or status/journal: ").strip().lower()
            if c in ("quit", "exit", "q"):
                return False
            if c == "status":
                self.show_status(advanced=True)
                continue
            if c == "journal":
                self.show_journal()
                continue
            if c in branch_keys:
                self.apply_offer_branch(offer, c)
                break
            print(f"Choose from: {', '.join(sorted(branch_keys))}")

        self.apply_passive_distortion_tick()
        self.pay_recurring_cost()
        self.periodic_review()
        self.advance_calendar()
        self.maybe_promote_tier()
        self.check_endings()

        # Post-turn hook
        hook = self.cfg.get("custom_turn_end")
        if hook:
            hook(self)

        if self.ending:
            self.show_status(advanced=True)
            self.epilogue()
            return False
        return True

    def play(self) -> None:
        """Main entry point: run the full game."""
        print(f"\n{self.cfg['title']} — {self.cfg['subtitle']}\n")
        if self.seed is not None:
            print(f"(RNG seed: {self.seed})\n")
        self.log(f"File opened: {self.player_name} ({self.archetype}).")
        self.show_help()
        while self.play_turn():
            pass
        if not self.ending:
            print("\nSession ended without resolution.\n")


# ── CLI ────────────────────────────────────────────────────────────────


def parse_cli_args(argv: list[str]) -> tuple[str, bool, int | None]:
    """Return (config_module, quick_mode, seed)."""
    config_module = ""
    quick = False
    seed: int | None = None
    for a in argv:
        if a in ("--quick", "-q"):
            quick = True
        elif a.lstrip("-").isdigit() and not a.startswith("--"):
            seed = int(a)
        elif not a.startswith("-"):
            config_module = a
    return config_module, quick, seed


def load_config(module_name: str) -> dict:
    """Import a Python module and return its CONFIG dict."""
    # Ensure current dir and engine dir are on sys.path
    for p in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
        if p not in sys.path:
            sys.path.insert(0, p)
    if module_name.endswith(".py"):
        module_name = module_name[:-3]
    module = importlib.import_module(module_name)
    return module.CONFIG


def main() -> None:
    config_module, quick, seed = parse_cli_args(sys.argv[1:])
    if not config_module:
        print(
            "Universal Text Adventure Engine\n"
            "===============================\n\n"
            "Usage: python3 text_adventure_engine.py <config_module> [--quick] [seed]\n\n"
            "Arguments:\n"
            "  config_module  Python file with CONFIG dict (e.g. artcraft_config)\n"
            "  --quick / -q   Skip character creation, use defaults\n"
            "  seed           Optional RNG seed for reproducible games\n\n"
            "Examples:\n"
            "  python3 text_adventure_engine.py artcraft_config\n"
            "  python3 text_adventure_engine.py artcraft_config --quick 42\n"
        )
        sys.exit(1)

    cfg = load_config(config_module)
    errors = validate_config(cfg)
    if errors:
        print("Config validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    profile: dict[str, Any] | None = None
    if not quick:
        profile = run_character_creation(cfg)

    Game(config=cfg, seed=seed, profile=profile).play()


if __name__ == "__main__":
    main()
