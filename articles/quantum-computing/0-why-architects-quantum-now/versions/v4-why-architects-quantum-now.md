---
title: "Why Architects Need to Think About Quantum Now (Even Though It's Not Ready Yet)"
subtitle: "Your RSA encryption has an expiration date. Adversaries are already storing your encrypted traffic, waiting for the quantum computer that can read it."
series: "The Quantum-Centric Architect — Part 0"
reading-time: "11 minutes"
target-audience: "Software architects, platform engineers, CTOs, security leads"
keywords: "quantum computing, Q-Day, post-quantum cryptography, NIST PQC, harvest now decrypt later, CBOM, quantum readiness"
tags: "Quantum Computing, Post-Quantum Cryptography, Software Architecture, Cybersecurity, Q-Day, NIST"
status: "v4-publishable"
created: "2026-04-10"
updated: "2026-04-10"
author: "Daniel Stauffer"
changes-from-v3: "Voice polish pass — softened absolutes, varied paragraph rhythm, added personal asides and admitted uncertainty where appropriate, tightened the CFO section, roughened closing to avoid AI-sounding wrap-up."
---

# Why Architects Need to Think About Quantum Now (Even Though It's Not Ready Yet)

This is Part 0 of The Quantum-Centric Architect, a series about quantum computing for people who build production systems — not people who study physics. Follow along for practical architecture guidance on quantum readiness, post-quantum cryptography, and hybrid quantum-classical design.

## The Encryption Expiration Date

Your RSA-2048 encryption has an expiration date. Nobody knows the exact day, but the range is narrowing: somewhere between 2029 and 2035, a quantum computer will be powerful enough to run Shor's algorithm at scale and factor the large primes that underpin RSA. When that happens — the industry calls it "Q-Day" — every RSA key, every ECC certificate, every Diffie-Hellman key exchange becomes breakable.

That sounds like a future problem. It isn't.

Nation-state actors are already running "harvest now, decrypt later" operations. They intercept and store encrypted traffic — TLS sessions, VPN tunnels, encrypted emails — banking on the expectation that quantum hardware will eventually let them read all of it. CISA estimates that over 50% of nation-state actors are doing this right now. The encrypted API calls your platform made last Tuesday might already be sitting in a storage facility somewhere, waiting for a quantum computer powerful enough to crack them open.

Think about what that means for your systems. Every TLS session your company has conducted over the last several years. Every customer record transmitted over HTTPS. Every financial transaction, every API key rotation, every internal communication encrypted with RSA or ECC. If any of that was intercepted — and if your organization is interesting enough to target, some of it probably was — it becomes readable once Q-Day arrives.

NIST didn't wait around. They finalized post-quantum cryptography standards in August 2024: ML-KEM (Kyber) for key encapsulation, ML-DSA (Dilithium) for digital signatures, and SLH-DSA (SPHINCS+) for stateless signatures. The standards exist. The migration path is defined. Chrome already ships hybrid PQC key exchange by default for billions of users. Signal adopted a post-quantum key agreement protocol back in 2023.

The question for architects isn't whether migration is coming. It's whether you start planning now or scramble when the timeline gets uncomfortably short.

## Quantum Computing in 90 Seconds

If you're a software architect, you don't need to understand quantum mechanics. You need to understand what quantum computers can and can't do, and roughly how they fit into your infrastructure.

A quantum processing unit is a coprocessor. Think of it like a GPU — specialized hardware for specific workloads. You wouldn't run your web server on a GPU, and you won't run your CRUD app on a QPU. But for certain problems — combinatorial optimization, molecular simulation, cryptographic factoring — a QPU can explore solution spaces that would take classical computers longer than the age of the universe.

The architectural concepts that actually matter:

Qubits can exist in superposition, exploring multiple states simultaneously instead of sequentially. Entanglement correlates qubits so that measuring one instantly constrains the other. Quantum gates manipulate qubits the way logic gates manipulate classical bits. And measurement collapses the quantum state into a classical result — but here's the part most people gloss over: you get a probability distribution, not a single deterministic answer. Your downstream systems will need to consume histograms and confidence intervals, not clean JSON values. That's a real architectural shift, and Article 3 in this series digs into it.

Where the hardware stands today: IBM's largest system has about 1,100 qubits. Google's Willow chip reached 105 qubits with error correction performance below the critical threshold — a genuine milestone. IonQ and Quantinuum are pushing trapped-ion approaches with higher gate fidelity but fewer qubits. To break RSA-2048 with Shor's algorithm, you'd need roughly 4,000 error-corrected logical qubits. Each logical qubit requires around 1,000 physical qubits with current error correction codes. So the target is approximately 4 million physical qubits. IBM's roadmap aims for 100,000+ by 2033.

We're not close. But the trajectory is steep enough that "wait and see" carries its own risks — especially when the harvest-now threat means the damage window opened years ago.

## What Breaks and What Doesn't

Let's be specific, because the panic-to-nuance ratio in quantum security coverage is pretty bad.

**Broken by quantum computers** (Shor's algorithm): RSA at all key sizes, Elliptic Curve Cryptography, Diffie-Hellman key exchange, DSA digital signatures. These underpin TLS, SSH, VPN, code signing, and most API authentication. This is the big one.

**Weakened but survivable** (Grover's algorithm): AES and other symmetric ciphers. Grover's effectively halves the key strength — AES-256 becomes equivalent to AES-128, which is still considered secure by a comfortable margin. If you're using AES-256 for data at rest, you're probably fine on the symmetric side.

**Not meaningfully affected**: Hash functions like SHA-256 and SHA-3. Grover's provides a quadratic speedup for preimage attacks, but SHA-256 remains secure with current parameters.

The practical takeaway: your TLS certificates, API authentication tokens, VPN tunnels, code signing infrastructure, and key exchange mechanisms are all on the clock. Your AES-encrypted data at rest is mostly fine. Your password hashes are fine.

The "harvest now, decrypt later" angle is what makes the timeline feel tighter than the hardware maturity suggests. Data with a long sensitivity lifetime — healthcare records, financial data, trade secrets, government communications — is the highest priority. If that data needs to stay confidential for 10+ years, and Q-Day might arrive in 5-10 years, the math gets uncomfortable.

## What "Quantum-Ready" Actually Means

I want to be direct about what quantum readiness is not: it's not rewriting your applications. It's not replacing your databases. It's not a two-year program staffed with quantum physicists.

For most organizations, quantum readiness comes down to three things.

**Know your cryptographic exposure.** Build a Cryptographic Bill of Materials — a CBOM. Inventory every algorithm, key size, and protocol across your stack. TLS certificates, API authentication, data-at-rest encryption, VPN tunnels, digital signatures, key management systems. Most organizations I've worked with don't have a complete picture of their cryptographic dependencies. Some are surprised by how much RSA is still in the plumbing. That audit is the first step, and it doesn't require any quantum expertise — it's a security inventory exercise.

**Plan your PQC migration.** The priority order is fairly well established: TLS certificates first (highest exposure, most standardized migration path), then API authentication, then data-at-rest encryption, then VPN/IPsec, then legacy systems. You don't do this all at once. Start with the highest-exposure, most-standardized components and work inward.

There's a performance consideration worth flagging. PQC algorithms use larger keys and signatures. ML-KEM public keys are 800 to 1,568 bytes compared to 32 bytes for X25519. ML-DSA signatures run 2,420 to 4,627 bytes versus 64 bytes for Ed25519. TLS handshakes get heavier. In some cases, the handshake won't fit in a single network packet, which means fragmentation and extra round trips. It's manageable — Chrome handles it for billions of users daily — but it's not invisible, and you should benchmark it against your latency requirements before committing to a rollout plan.

**Budget for it.** PQC migration costs range from $200K to $2M depending on organization size, complexity, and how much legacy cryptography you're carrying. That sounds like real money until you compare it to the alternative.

## The Math Your CFO Needs to See

The average cost of a data breach is $4.88 million (IBM, 2024). That's one incident. One set of compromised data.

Q-Day isn't one breach. It's the simultaneous exposure of every secret your organization has ever protected with RSA or ECC. Every intercepted TLS session becomes readable. Every encrypted database backup that was exfiltrated becomes an open book. Every digitally signed document now carries a forgeable signature.

For a mid-size financial institution, the exposure math looks roughly like this: GDPR fines up to 4% of global annual revenue. SEC enforcement actions in the eight-figure range. Class-action litigation that scales with customer count and data sensitivity. Customer churn that averages 3.4% after a normal breach (Ponemon) but could be dramatically worse when the headline is "all encryption broken simultaneously."

I've seen conservative estimates for mid-size financial institutions land between $50M and $500M in combined regulatory, legal, and business impact. The $1-2M migration cost barely registers against that.

The framing that tends to work with finance teams: this is insurance. Not "can we afford to prepare?" but "can we afford not to?" A CBOM audit and phased PQC migration might be the cheapest risk mitigation your CISO ever proposes.

## The Quantum Computing Landscape

You don't need to pick a winner in the quantum hardware race. You need enough context to make informed decisions about where to invest attention.

| Provider | Approach | Current Scale | Access Model | Key Strength |
|----------|----------|---------------|--------------|--------------|
| IBM | Superconducting | ~1,121 qubits | Cloud (IBM Quantum) | Largest ecosystem, Qiskit |
| Google | Superconducting | 105 qubits (Willow) | Limited access | Error correction milestones |
| IonQ | Trapped ion | 36 algorithmic qubits | Cloud (Braket, Azure) | High gate fidelity |
| Quantinuum | Trapped ion | 56 qubits (H2) | Cloud | Highest quantum volume |
| Amazon | Multi-provider | Via Braket | Cloud | Provider-agnostic access |
| Microsoft | Topological | Research phase | Azure Quantum | Long-term theoretical bet |
| D-Wave | Quantum annealing | 5,000+ qubits | Cloud | Optimization-specific |

The market is projected to reach $65 billion by 2030 (McKinsey). Thirty-five percent of large enterprises are already experimenting (Gartner, 2025). Cloud quantum spending exceeds $500 million annually across the major platforms. This isn't fringe technology waiting for a breakthrough — it's an emerging infrastructure category with real investment, published standards, and a timeline that's measured in years, not decades.

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

No cat-in-a-box metaphors. No quantum hype. Architecture decisions, migration playbooks, and working code.

## What to Do Monday Morning

You don't need to become a quantum physicist. You need to start a few conversations and one spreadsheet.

**Start your CBOM audit.** Inventory the cryptographic algorithms across your stack — TLS certificates, API auth, data encryption, VPN, code signing. You'll probably find RSA and ECC in more places than you expected. Some of them will surprise you.

**Talk to your CISO.** Ask about the PQC migration timeline. If there isn't one, that tells you something about urgency — and about the opportunity to be the person who raises it.

**Skim the NIST standards.** You don't need to read every page. The executive summaries of FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), and FIPS 205 (SLH-DSA) will give you enough context to have informed conversations.

**Identify your highest-exposure systems.** Public-facing TLS endpoints and customer data encryption are the starting points. These are where "harvest now, decrypt later" has the most impact.

**Budget for a pilot.** Pick one service. Migrate its TLS to hybrid PQC. Learn what breaks, what's slower, and what your team needs to know. A single-service pilot costs a fraction of the full migration and gives you the data to plan the rest.

The quantum computer that breaks your encryption doesn't exist yet. But the data it will decrypt is being collected right now. The standards to protect against it are published. The migration path is defined. Whether you start this quarter or next is a judgment call — but "never" isn't really on the table anymore.

---

**Resources**:
- [NIST Post-Quantum Cryptography Standards](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [CISA Quantum Readiness](https://www.cisa.gov/quantum)
- [IBM Cost of a Data Breach Report 2024](https://www.ibm.com/reports/data-breach)
- [McKinsey Quantum Technology Monitor](https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/quantum-technology-monitor)
- [NSA CNSA 2.0 Suite](https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF)
- [Google Willow Announcement](https://blog.google/technology/research/google-willow-quantum-chip/)

---

## Series Navigation

**Next Article**: [The QPU as a Coprocessor: How Quantum Fits in Your Data Center](link) *(Part 1)*

---

*This is Part 0 of The Quantum-Centric Architect series. Follow along for practical quantum architecture guidance — no physics degree required.*

**About the Author**: Daniel Stauffer is an Enterprise Architect who believes the best time to prepare for quantum computing was two years ago, and the second best time is Monday morning.

**Tags**: #QuantumComputing #PostQuantumCryptography #QDay #SoftwareArchitecture #CyberSecurity #NIST #PQC #EnterpriseArchitecture
