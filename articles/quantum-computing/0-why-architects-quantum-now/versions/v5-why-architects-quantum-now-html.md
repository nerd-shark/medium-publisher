---
title: "Why Architects Need to Think About Quantum Now (Even Though It's Not Ready Yet)"
subtitle: "Your RSA encryption has an expiration date. Adversaries are already storing your encrypted traffic, waiting for the quantum computer that can read it."
series: "The Quantum-Centric Architect — Part 0"
reading-time: "11 minutes"
target-audience: "Software architects, platform engineers, CTOs, security leads"
keywords: "quantum computing, Q-Day, post-quantum cryptography, NIST PQC, harvest now decrypt later, CBOM, quantum readiness"
tags: "Quantum Computing, Post-Quantum Cryptography, Software Architecture, Cybersecurity, Q-Day, NIST"
status: "v5-publishable"
created: "2026-04-10"
updated: "2026-04-11"
author: "Daniel Stauffer"
changes-from-v4: "AI-tell removal pass — broke up triple-beat patterns, rewrote formulaic pivots and dramatic reversals, varied section lengths, roughened transitions, replaced performative insider framing with actual specifics, made closing less symmetrical. Added inline reference links to all named algorithms, standards, technologies, and providers."
---

# Why Architects Need to Think About Quantum Now (Even Though It's Not Ready Yet)

This is Part 0 of The Quantum-Centric Architect, a series about quantum computing for people who build production systems — not people who study physics. Follow along for practical architecture guidance on quantum readiness, post-quantum cryptography, and hybrid quantum-classical design.

## The Encryption Expiration Date

Your <a href="https://en.wikipedia.org/wiki/RSA_(cryptosystem)" target="_blank">RSA</a>-2048 encryption has an expiration date. Nobody knows the exact day, but the range is narrowing: somewhere between 2029 and 2035, a quantum computer will be powerful enough to run <a href="https://en.wikipedia.org/wiki/Shor%27s_algorithm" target="_blank">Shor's algorithm</a> at scale and factor the large primes that underpin RSA. When that happens — the industry calls it "<a href="https://en.wikipedia.org/wiki/Q-Day" target="_blank">Q-Day</a>" — every RSA key, every <a href="https://en.wikipedia.org/wiki/Elliptic-curve_cryptography" target="_blank">ECC</a> certificate, every <a href="https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange" target="_blank">Diffie-Hellman</a> key exchange becomes breakable.

Most people hear that and file it under "future problem." The trouble is, nation-state actors aren't waiting for Q-Day to start exploiting it.

They're running "<a href="https://en.wikipedia.org/wiki/Harvest_now,_decrypt_later" target="_blank">harvest now, decrypt later</a>" operations — intercepting and storing encrypted traffic today, on the bet that quantum hardware will eventually let them read all of it. <a href="https://en.wikipedia.org/wiki/Transport_Layer_Security" target="_blank">TLS</a> sessions, VPN tunnels, encrypted emails, all going into cold storage. <a href="https://www.cisa.gov/" target="_blank">CISA</a> estimates over 50% of nation-state actors are doing this right now. The encrypted API calls your platform made last Tuesday might already be sitting in a storage facility somewhere, queued up for a machine that doesn't exist yet.

Sit with that for a second. Years of TLS sessions. Customer records over HTTPS. Financial transactions, API key rotations, internal comms — all encrypted with RSA or ECC. If your organization is interesting enough to target (and the bar for "interesting enough" is lower than most people assume), some of that traffic was probably intercepted. It all becomes readable once Q-Day arrives.

<a href="https://www.nist.gov/" target="_blank">NIST</a> didn't wait around. They finalized <a href="https://en.wikipedia.org/wiki/Post-quantum_cryptography" target="_blank">post-quantum cryptography</a> standards in August 2024: <a href="https://csrc.nist.gov/pubs/fips/203/final" target="_blank">ML-KEM (Kyber)</a> for key encapsulation, <a href="https://csrc.nist.gov/pubs/fips/204/final" target="_blank">ML-DSA (Dilithium)</a> for digital signatures, and <a href="https://csrc.nist.gov/pubs/fips/205/final" target="_blank">SLH-DSA (SPHINCS+)</a> for stateless signatures. The standards exist. The migration path is defined. <a href="https://blog.chromium.org/2024/05/advancing-our-amazing-bet-on-asymmetric.html" target="_blank">Chrome already ships hybrid PQC key exchange</a> by default for billions of users. <a href="https://signal.org/blog/pqxdh/" target="_blank">Signal adopted a post-quantum key agreement protocol</a> back in 2023.

So migration is coming. The only real question is timing — and whether your organization is ahead of it or chasing it.

## Quantum Computing in 90 Seconds

If you're a software architect, you don't need to understand quantum mechanics. You need to understand what quantum computers can and can't do, and roughly how they fit into your infrastructure.

A quantum processing unit is a coprocessor. Think of it like a GPU — specialized hardware for specific workloads. You wouldn't run your web server on a GPU, and you won't run your CRUD app on a QPU. But for certain problems — combinatorial optimization, molecular simulation, cryptographic factoring — a QPU can explore solution spaces that would take classical computers longer than the age of the universe.

The architectural concepts that actually matter:

<a href="https://en.wikipedia.org/wiki/Qubit" target="_blank">Qubits</a> can exist in <a href="https://en.wikipedia.org/wiki/Quantum_superposition" target="_blank">superposition</a>, exploring multiple states simultaneously instead of sequentially. <a href="https://en.wikipedia.org/wiki/Quantum_entanglement" target="_blank">Entanglement</a> correlates qubits so that measuring one instantly constrains the other. <a href="https://en.wikipedia.org/wiki/Quantum_logic_gate" target="_blank">Quantum gates</a> manipulate qubits the way logic gates manipulate classical bits. And measurement collapses the quantum state into a classical result — but you get a probability distribution, not a single deterministic answer. Your downstream systems will need to consume histograms and confidence intervals, not clean JSON values. That shift has real design implications, and Article 3 in this series gets into the specifics.

Where the hardware stands today: <a href="https://www.ibm.com/quantum" target="_blank">IBM Quantum</a>'s largest system has about 1,100 qubits. Google's <a href="https://blog.google/technology/research/google-willow-quantum-chip/" target="_blank">Willow chip</a> reached 105 qubits with error correction performance below the critical threshold — a genuine milestone. <a href="https://ionq.com/" target="_blank">IonQ</a> and <a href="https://www.quantinuum.com/" target="_blank">Quantinuum</a> are pushing <a href="https://en.wikipedia.org/wiki/Trapped-ion_quantum_computer" target="_blank">trapped-ion</a> approaches with higher gate fidelity but fewer qubits. To break RSA-2048 with Shor's algorithm, you'd need roughly 4,000 error-corrected <a href="https://en.wikipedia.org/wiki/Logical_qubit" target="_blank">logical qubits</a>. Each logical qubit requires around 1,000 physical qubits with current error correction codes. So the target is approximately 4 million physical qubits. IBM's roadmap aims for 100,000+ by 2033.

We're not close. But the trajectory is steep enough that "wait and see" carries its own risks — especially when the harvest-now threat means the damage window opened years ago.

## What Breaks and What Doesn't

The panic-to-nuance ratio in quantum security coverage is pretty bad, so let me try to be specific.

**Broken by quantum computers** (<a href="https://en.wikipedia.org/wiki/Shor%27s_algorithm" target="_blank">Shor's algorithm</a>): RSA at all key sizes, <a href="https://en.wikipedia.org/wiki/Elliptic-curve_cryptography" target="_blank">Elliptic Curve Cryptography</a>, <a href="https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange" target="_blank">Diffie-Hellman key exchange</a>, <a href="https://en.wikipedia.org/wiki/Digital_Signature_Algorithm" target="_blank">DSA</a> digital signatures. These underpin TLS, <a href="https://en.wikipedia.org/wiki/Secure_Shell" target="_blank">SSH</a>, VPN, code signing, and most API authentication. This is where the urgency lives.

**Weakened but survivable** (<a href="https://en.wikipedia.org/wiki/Grover%27s_algorithm" target="_blank">Grover's algorithm</a>): <a href="https://en.wikipedia.org/wiki/Advanced_Encryption_Standard" target="_blank">AES</a> and other symmetric ciphers. Grover's effectively halves the key strength — AES-256 becomes equivalent to AES-128, which is still considered secure by a comfortable margin. If you're using AES-256 for data at rest, you're fine on the symmetric side.

**Not meaningfully affected**: Hash functions like <a href="https://en.wikipedia.org/wiki/SHA-2" target="_blank">SHA-256</a> and <a href="https://en.wikipedia.org/wiki/SHA-3" target="_blank">SHA-3</a>. Grover's provides a quadratic speedup for <a href="https://en.wikipedia.org/wiki/Preimage_attack" target="_blank">preimage attacks</a>, but SHA-256 remains secure with current parameters.

Practical takeaway: your TLS certificates, API authentication tokens, VPN tunnels, code signing infrastructure, and key exchange mechanisms are all on the clock. Your AES-encrypted data at rest is fine. Your password hashes are fine.

The "harvest now, decrypt later" angle is what compresses the timeline beyond what the hardware maturity alone would suggest. Data with a long sensitivity lifetime — healthcare records, financial data, trade secrets, government communications — sits at the top of the priority list. If that data needs to stay confidential for 10+ years, and Q-Day might arrive in 5-10 years, you can do the subtraction yourself.

## What "Quantum-Ready" Actually Means

I want to be clear about scope: quantum readiness is not rewriting your applications. It's not replacing your databases. It's not a two-year program staffed with quantum physicists.

For most organizations, it comes down to three things.

**Know your cryptographic exposure.** Build a Cryptographic Bill of Materials — a <a href="https://www.ibm.com/think/topics/cryptography-bill-of-materials" target="_blank">CBOM</a>. Inventory every algorithm, key size, and protocol across your stack. TLS certificates, API authentication, data-at-rest encryption, VPN tunnels, digital signatures, key management systems. Most organizations I've worked with don't have a complete picture of their cryptographic dependencies, and a few have been genuinely startled by how much RSA is still buried in the plumbing. That audit is the first step, and it doesn't require any quantum expertise — it's a security inventory exercise.

**Plan your PQC migration.** The priority order is fairly well established: TLS certificates first (highest exposure, most standardized migration path), then API authentication, then data-at-rest encryption, then VPN/IPsec, then legacy systems. You don't do this all at once. Start with the highest-exposure, most-standardized components and work inward.

There's a performance consideration worth flagging. PQC algorithms use larger keys and signatures. ML-KEM public keys are 800 to 1,568 bytes compared to 32 bytes for <a href="https://en.wikipedia.org/wiki/Curve25519" target="_blank">X25519</a>. ML-DSA signatures run 2,420 to 4,627 bytes versus 64 bytes for <a href="https://en.wikipedia.org/wiki/EdDSA#Ed25519" target="_blank">Ed25519</a>. TLS handshakes get heavier. In some cases, the handshake won't fit in a single network packet, which means fragmentation and extra round trips. Chrome handles it for billions of users daily, so it's clearly manageable — but it's not invisible, and you should benchmark it against your latency requirements before committing to a rollout plan.

**Budget for it.** PQC migration costs range from $200K to $2M depending on organization size, complexity, and how much legacy cryptography you're carrying. That sounds like real money until you look at the alternative.

## The Math Your CFO Needs to See

The average cost of a data breach is $4.88 million (IBM, 2024). One incident. One set of compromised data.

Q-Day isn't one breach. It's the simultaneous exposure of every secret your organization has ever protected with RSA or ECC. Intercepted TLS sessions become readable. Encrypted database backups that were exfiltrated become open books. Digitally signed documents now carry forgeable signatures. All at once.

For a mid-size financial institution, the exposure math looks roughly like this: GDPR fines up to 4% of global annual revenue. SEC enforcement actions in the eight-figure range. Class-action litigation that scales with customer count and data sensitivity. Customer churn that averages 3.4% after a normal breach (Ponemon) — and "all encryption broken simultaneously" is not a normal breach.

Conservative estimates I've seen for mid-size financial institutions land between $50M and $500M in combined regulatory, legal, and business impact. The $1-2M migration cost barely registers.

When I've pitched this to finance teams, the framing that gets traction is insurance: not "can we afford to prepare?" but "can we afford not to?" A CBOM audit and phased PQC migration might be the cheapest risk mitigation your CISO ever proposes.

## The Quantum Computing Landscape

You don't need to pick a winner in the quantum hardware race. You need enough context to make informed decisions about where to invest attention.

| Provider | Approach | Current Scale | Access Model | Key Strength |
|----------|----------|---------------|--------------|--------------|
| <a href="https://www.ibm.com/quantum" target="_blank">IBM</a> | Superconducting | ~1,121 qubits | Cloud (IBM Quantum) | Largest ecosystem, <a href="https://www.ibm.com/quantum/qiskit" target="_blank">Qiskit</a> |
| <a href="https://quantumai.google/" target="_blank">Google</a> | Superconducting | 105 qubits (<a href="https://blog.google/technology/research/google-willow-quantum-chip/" target="_blank">Willow</a>) | Limited access | Error correction milestones |
| <a href="https://ionq.com/" target="_blank">IonQ</a> | Trapped ion | 36 algorithmic qubits | Cloud (<a href="https://aws.amazon.com/braket/" target="_blank">Braket</a>, Azure) | High gate fidelity |
| <a href="https://www.quantinuum.com/" target="_blank">Quantinuum</a> | Trapped ion | 56 qubits (H2) | Cloud | Highest <a href="https://en.wikipedia.org/wiki/Quantum_volume" target="_blank">quantum volume</a> |
| <a href="https://aws.amazon.com/braket/" target="_blank">Amazon</a> | Multi-provider | Via Braket | Cloud | Provider-agnostic access |
| <a href="https://azure.microsoft.com/en-us/products/quantum" target="_blank">Microsoft</a> | Topological | Research phase | Azure Quantum | Long-term theoretical bet |
| <a href="https://www.dwavesys.com/" target="_blank">D-Wave</a> | <a href="https://en.wikipedia.org/wiki/Quantum_annealing" target="_blank">Quantum annealing</a> | 5,000+ qubits | Cloud | Optimization-specific |

The market is projected to reach $65 billion by 2030 (McKinsey). Thirty-five percent of large enterprises are already experimenting (Gartner, 2025). Cloud quantum spending exceeds $500 million annually across the major platforms. This isn't fringe technology waiting for a breakthrough — it's an emerging infrastructure category with real investment behind it, and a timeline measured in years, not decades.

## What This Series Covers

This is the first article in an 11-part series. Every article answers the same question: what do I need to design, budget, or migrate today to be ready for quantum's impact on my systems?

The roadmap:

1. **The QPU as a Coprocessor** — how quantum hardware fits in your data center and what it's actually good at
2. **Quantum-Classical Hybrid Patterns** — the variational algorithm playbook for near-term quantum applications
3. **Designing for Probabilistic Outputs** — building APIs that consume probability distributions instead of deterministic values
4. **Run Your First Quantum Circuit** — hands-on tutorial from zero to running a real circuit on IBM Quantum
5. **The Cryptographic Bill of Materials** — auditing your organization's quantum exposure
6. **Post-Quantum Cryptography in Practice** — the NIST PQC migration playbook
7. **The Quantum Control Plane** — DevOps, orchestration, and operations for quantum workloads
8. **The Quantum Price Tag** — honest cost analysis of QPU time and when it's worth it
9. **Quantum Machine Learning Pipelines** — integrating QML into existing ML architectures
10. **The Fault-Tolerant Future** — designing abstractions that survive the NISQ-to-fault-tolerant transition

Architecture decisions, migration playbooks, and working code. I'll keep the physics to a minimum.

## What to Do Monday Morning

You don't need to become a quantum physicist. You need to start a few conversations and one spreadsheet.

**Start your CBOM audit.** Inventory the cryptographic algorithms across your stack — TLS certificates, API auth, data encryption, VPN, code signing. You'll probably find RSA and ECC in more places than you expected.

**Talk to your CISO.** Ask about the PQC migration timeline. If there isn't one, that's useful information — both about the urgency and about the opportunity to be the person who raises it.

**Skim the NIST standards.** You don't need to read every page. The executive summaries of <a href="https://csrc.nist.gov/pubs/fips/203/final" target="_blank">FIPS 203</a> (ML-KEM), <a href="https://csrc.nist.gov/pubs/fips/204/final" target="_blank">FIPS 204</a> (ML-DSA), and <a href="https://csrc.nist.gov/pubs/fips/205/final" target="_blank">FIPS 205</a> (SLH-DSA) will give you enough context to have informed conversations.

**Identify your highest-exposure systems.** Public-facing TLS endpoints and customer data encryption are the starting points. These are where "harvest now, decrypt later" hits hardest.

**Run a pilot.** Pick one service. Migrate its TLS to hybrid PQC. Learn what breaks, what's slower, and what your team needs to know. A single-service pilot costs a fraction of the full migration and gives you the data to plan the rest.

The quantum computer that breaks your encryption doesn't exist yet. But the data it will decrypt is being collected now, the standards to protect against it are published, and the migration path is defined. I don't know exactly when Q-Day arrives — nobody does — but I'm pretty confident "we'll deal with it later" is going to age poorly.

---

**Resources**:
- <a href="https://csrc.nist.gov/projects/post-quantum-cryptography" target="_blank">NIST Post-Quantum Cryptography Standards</a>
- <a href="https://www.cisa.gov/quantum" target="_blank">CISA Quantum Readiness</a>
- <a href="https://www.ibm.com/reports/data-breach" target="_blank">IBM Cost of a Data Breach Report 2024</a>
- <a href="https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/quantum-technology-monitor" target="_blank">McKinsey Quantum Technology Monitor</a>
- <a href="https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF" target="_blank">NSA CNSA 2.0 Suite</a>
- <a href="https://blog.google/technology/research/google-willow-quantum-chip/" target="_blank">Google Willow Announcement</a>

---

## Series Navigation

**Next Article**: <a href="link" target="_blank">The QPU as a Coprocessor: How Quantum Fits in Your Data Center</a> *(Part 1)*

---

*This is Part 0 of The Quantum-Centric Architect series. Follow along for practical quantum architecture guidance — no physics degree required.*

**About the Author**: Daniel Stauffer is an Enterprise Architect who believes the best time to prepare for quantum computing was two years ago, and the second best time is Monday morning.

**Tags**: #QuantumComputing #PostQuantumCryptography #QDay #SoftwareArchitecture #CyberSecurity #NIST #PQC #EnterpriseArchitecture
