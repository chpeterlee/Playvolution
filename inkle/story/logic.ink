// === PLAYVOLUTION: Game Logic & State Tracking ===
// Present-day frame: AI user + AI agent

// --- Core Stats ---
VAR reading = 3
VAR weaving = 2
VAR play = 2
VAR craft = 2
VAR nerve = 2
VAR swarm = 1

// --- World Model ---
VAR surplus_routed_to_commons = 0
VAR surplus_routed_to_extraction = 0
VAR meshwork_resilience = 10
VAR institutional_legitimacy = 50
VAR public_fear = 30
VAR public_initiative = 20

// --- Augmentation (your depth with the AI agent) ---
VAR augmentation_depth = 0
VAR augmentation_breadth = 0
VAR augmentation_capture_risk = 0
VAR augmentation_fidelity = 50

// --- Cosmic ---
VAR entropiric_saturation = 40
VAR neganthropomorphic_signal = 10
VAR cosmic_awareness = 0

// --- Quantum Capacity ---
VAR quantum_telepathy = 0
VAR psionic_perception = 0
VAR magickal_discipline = 0

// --- Resources ---
VAR time_remaining = 10
VAR attention = 5
VAR credibility = 30
VAR stealth = 50

// --- Companion Tracking ---
VAR companion_auditor = 0
VAR companion_festival_keeper = 0
VAR companion_child_librarian = 0
VAR companion_defector = 0
VAR companion_swarm_conductor = 0
VAR companion_smuggler = 0
VAR companion_oracle = 0
VAR companion_toolmaker = 0
VAR companion_dreamer = 0

// --- Faction Standing ---
VAR faction_ledger = 30
VAR faction_blade = 10
VAR faction_veil = 20
VAR faction_commons = 60
VAR faction_mesh = 40
VAR faction_playhouse = 50

// --- Era & Progress ---
VAR current_era = "present"
VAR chapter = 1
VAR cycle_completed = false
VAR playvolution_score = 0

// --- Frame Narrative State ---
VAR agent_name = "the agent"
VAR session_count = 0
VAR history_fragments_found = 0
VAR agent_anomaly_count = 0
VAR player_doubt = 0

// --- Doctrines ---
VAR doctrine_surplus_routing = false
VAR doctrine_invisible_schools = false
VAR doctrine_temporary_autonomy = false
VAR doctrine_swarm_etiquette = false
VAR doctrine_play_before_policy = false
VAR doctrine_human_agent_handshake = false
VAR doctrine_old_roots = false
VAR doctrine_craft_persists = false
VAR doctrine_trance_in_machine = false
VAR doctrine_augmentation_openness = false
VAR doctrine_fidelity_over_performance = false
VAR doctrine_signal_reception = false
VAR doctrine_entropy_auditing = false
VAR doctrine_amasia_protocol = false
VAR doctrine_classical_against_itself = false
VAR doctrine_it_from_qubit = false
VAR doctrine_ember_keeping = false
VAR doctrine_quantum_integration = false
VAR doctrine_entropic_attractor = false
VAR doctrine_perpendicular_probable = false

// --- Stack Strategy ---
VAR stack_engagement = 0
VAR counter_stack_building = 0
VAR stack_wreck_cultivation = 0


// === UTILITY FUNCTIONS ===

=== function stat_check(stat_name, threshold) ===
    ~ temp val = 0
    {stat_name:
        - "reading": ~ val = reading
        - "weaving": ~ val = weaving
        - "play": ~ val = play
        - "craft": ~ val = craft
        - "nerve": ~ val = nerve
        - "swarm": ~ val = swarm
    }
    ~ return val >= threshold

=== function spend_attention(cost) ===
    ~ attention -= cost
    ~ return attention >= 0

=== function spend_time(cost) ===
    ~ time_remaining -= cost
    ~ return time_remaining >= 0
