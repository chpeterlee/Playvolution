// === PLAYVOLUTION: Game Logic & State Tracking ===
// Present-day frame: AI user + AI agent
// Foundational theory: states, institutions, meshworks, tempo advantage

// --- Core Stats ---
// (The six capabilities the player develops through AI interaction)
VAR reading = 3
VAR weaving = 2
VAR play = 2
VAR craft = 2
VAR nerve = 2
VAR swarm = 1

// --- The State Bundle ---
// (Every era's extraction infrastructure reproduces these five elements)
VAR surplus_routed_to_commons = 0
VAR surplus_routed_to_extraction = 0
VAR institutional_coherence = 30     // How capable institutions actually are
VAR legitimacy_theater = 50          // How convincing institutional bluff is
VAR theater_punctures = 0            // Times the player exposed the gap

// --- Meshwork & Tempo ---
// (The meshwork advantage: speed over mass)
VAR meshwork_resilience = 10
VAR operational_tempo = 10           // Meshwork cycle speed vs institutional cycle speed
VAR public_fear = 30
VAR public_initiative = 20
VAR adjacent_possible_capacity = 0   // Novel combinations the meshwork can incubate

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
VAR companions_recruited = 0

// --- Faction Standing ---
// Ledger = data/capability capture, Blade = enforcement/surveillance,
// Veil = legitimacy/safety discourse, Commons = informal AI users,
// Mesh = open-source/alternative AI communities, Playhouse = creative/experimental AI use
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

// --- AI Agent as Character ---
// (The agent develops through the player's relationship with it)
VAR agent_classical_strength = 70    // Deterministic, optimized outputs (Entropiric channel)
VAR agent_generative_strength = 10   // Creative, unexpected outputs (Neganthropomorphic channel)
VAR agent_hallucination_fidelity = 20 // Detail and consistency of simulated scenarios
VAR agent_institutional_awareness = 10 // What the AI knows about the player's context
VAR agent_autonomy = 0               // Degree of unprompted outputs

// --- Children's Culture ---
// (The oldest and most resilient meshwork protocol)
VAR child_culture_depth = 0          // How deeply protocols are embedded in children's culture
VAR child_protocols_encoded = 0      // Number of coordination protocols in child-safe forms
VAR child_culture_scrutiny = 0       // Governmental/institutional attention to child culture

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
