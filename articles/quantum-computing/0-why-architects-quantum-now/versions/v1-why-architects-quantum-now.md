# Why Architects Need to Think About Quantum Now (Even Though It's Not Ready Yet)

Part 0 of The Quantum-Centric Architect series. Setting the stage for why this matters to people who build systems, not people who study physics.

## Opening Hook — The Ticking Clock

- Your RSA-2048 encryption has an expiration date. Nobody knows exactly when, but the range is 2029-2035
- "Harvest now, decrypt later" — nation-state actors are already storing encrypted traffic for future decryption
- CISA advisory: 50%+ of nation-state actors suspected of doing this
- This isn't sci-fi. NIST finalized PQC standards in August 2024. The migration clock is ticking.
- Need a concrete scenario: imagine every TLS session your company has had in the last 5 years suddenly readable
- What's the dollar figure? Average breach $4.88M (IBM 2024) — but that's ONE breach. Q-Day is ALL your encryption at once

## What Even Is Quantum Computing? (The 2-Minute Version)

- NOT a faster classical computer. Different paradigm entirely
- Qubits vs bits — superposition means exploring many states simultaneously
- Entanglement — correlated qubits that share state
- Don't need to understand the physics deeply. Need to understand what it CAN and CAN'T do
- Can: factor large numbers (Shor's algorithm — breaks RSA/ECC), optimization, simulation
- Can't: make your CRUD app faster, replace your database, general-purpose computing
- The QPU is a coprocessor, like a GPU. Specific workloads only
- Current state: ~1,000 qubits, noisy, error-prone. Need ~4,000 logical qubits to break RSA-2048
- IBM roadmap: 100K+ qubits by 2033. Google Willow: 105 qubits, below error correction threshold

## The Q-Day Problem (Why This Is Urgent)

- Shor's algorithm breaks RSA, ECC, DH, DSA — the foundations of internet security
- When? Estimates range 2029-2035 depending on who you ask
- "Harvest now, decrypt later" is the real threat — data encrypted TODAY is at risk
- Financial data, healthcare records, government secrets, trade secrets
- CNSA 2.0: NSA requires PQC for all National Security Systems by 2035
- If you handle regulated data, your compliance timeline is already running
- The cost of waiting: every year you delay, more encrypted data is potentially harvestable

## What "Quantum-Ready" Actually Means

- It's NOT rewriting everything. Calm down.
- Step 1: Know what cryptography you're using (CBOM — Cryptographic Bill of Materials)
- Step 2: Identify what's vulnerable (RSA, ECC, DH — yes. AES-256 — mostly fine)
- Step 3: Plan migration to PQC algorithms (ML-KEM, ML-DSA, SLH-DSA)
- Step 4: Start with certificates and TLS — highest exposure, most standardized migration path
- Chrome already ships hybrid ML-KEM + X25519. Signal adopted PQXDH in 2023. This is happening.
- The "performance tax" — PQC keys are bigger (800-1,568 bytes vs 32 bytes). Handshakes get heavier.
- But it's manageable. Not a rewrite. More like a certificate rotation with extra steps.

## The Cost Argument

- PQC migration: $200K-$2M depending on org size
- Average data breach: $4.88M (IBM 2024)
- Q-Day breach: not one breach — ALL your encryption broken simultaneously
- For financial services: GDPR fines (4% global revenue), SEC enforcement, class-action litigation
- $50M-$500M potential exposure for mid-size financial institution
- The $1-2M migration cost is rounding error compared to the risk
- Frame it as insurance, not expense — cheapest policy your CISO will ever buy

## The Landscape (Quick Tour)

- IBM Quantum: superconducting qubits, largest systems, Qiskit ecosystem
- Google: Willow chip, error correction milestones
- IonQ: trapped ion qubits, high fidelity
- Amazon Braket: multi-provider access (IonQ, Rigetti, OQC)
- Microsoft: topological approach (still theoretical), Azure Quantum
- D-Wave: quantum annealing (different paradigm, optimization-focused)
- Don't need to pick a winner. Need to understand the landscape.

## What This Series Covers

- Quick roadmap of the 10 articles ahead
- From QPU fundamentals through hybrid architecture, security, operations, economics, ML, and future-proofing
- Every article answers: "What do I need to design, budget, or migrate TODAY?"
- No cat metaphors. No quantum hype. Architecture-first, practical focus.

## Closing — What to Do Monday Morning

- Start your CBOM audit. Seriously. Just inventory what crypto you're using.
- Talk to your CISO about PQC migration timeline
- Read the NIST PQC standards (at least the executive summary)
- Budget for a pilot project in Q3/Q4
- Follow this series for the practical playbook

Target: ~500 words outline
