# Why Architects Need to Think About Quantum Now (Even Though It's Not Ready Yet)

Part 0 of The Quantum-Centric Architect series. This isn't a physics lecture. It's a planning document for people who build production systems and need to know what's coming.

## The Encryption Expiration Date

Your RSA-2048 encryption has an expiration date. Nobody knows the exact day, but the range is narrowing: somewhere between 2029 and 2035, a quantum computer will be powerful enough to run Shor's algorithm at scale and factor the large primes that RSA depends on. When that happens — the industry calls it "Q-Day" — every RSA key, every ECC certificate, every Diffie-Hellman key exchange becomes breakable.

That sounds like a future problem. Here's why it's a today problem.

Nation-state actors are already running "harvest now, decrypt later" operations. They're intercepting and storing encrypted traffic — TLS sessions, VPN tunnels, encrypted emails — with the expectation that they'll be able to decrypt it all once quantum hardware catches up. CISA estimates that over 50% of nation-state actors are doing this. Your encrypted data from 2024 may be sitting in a storage facility in [redacted], waiting for Q-Day.

[Need to make this more concrete — maybe a scenario: "Imagine every TLS session your company has conducted in the last 5 years suddenly readable. Every API key, every customer record, every financial transaction." That hits harder.]

NIST didn't wait around. They finalized post-quantum cryptography standards in August 2024 — ML-KEM (Kyber) for key encapsulation, ML-DSA (Dilithium) for digital signatures, SLH-DSA (SPHINCS+) for stateless signatures. The standards exist. The migration path is defined. Chrome already ships hybrid PQC by default. Signal adopted a post-quantum protocol in 2023.

The question isn't whether you need to migrate. It's whether you start now or scramble later.

## Quantum Computing in 90 Seconds (For People Who Build Systems)

If you're an architect, you don't need to understand quantum mechanics. You need to understand what quantum computers can and can't do, and how they fit into your infrastructure.

A quantum processing unit (QPU) is a coprocessor. Think of it like a GPU — specialized hardware for specific workloads. You wouldn't run your web server on a GPU, and you won't run your CRUD app on a QPU. But for certain problems — optimization, molecular simulation, cryptographic factoring — a QPU can explore solution spaces that would take classical computers millennia.

The key concepts, stripped to what matters architecturally:

- **Qubits** can exist in superposition — exploring multiple states simultaneously instead of one at a time
- **Entanglement** correlates qubits so measuring one instantly determines the other
- **Quantum gates** manipulate qubits, like logic gates manipulate bits
- **Measurement** collapses superposition into a classical result — you get a probability distribution, not a deterministic answer

[That last point is important and underappreciated. Quantum computing is inherently probabilistic. Your APIs will need to consume histograms, not single values. Article 3 goes deep on this.]

Current state of the hardware: IBM's largest system has ~1,100 qubits. Google's Willow chip hit 105 qubits with error correction below threshold. IonQ and Quantinuum are pushing trapped-ion approaches with higher fidelity but fewer qubits. To break RSA-2048, you'd need roughly 4,000 error-corrected logical qubits — and each logical qubit requires ~1,000 physical qubits with current error correction. So we need ~4 million physical qubits. IBM's roadmap targets 100,000+ by 2033.

We're not there yet. But the trajectory is clear, and the "harvest now" threat means the clock started years ago.

## What "Quantum-Ready" Actually Means for Your Architecture

Let me be clear about what quantum readiness is NOT: it's not rewriting your applications. It's not replacing your databases. It's not some massive infrastructure overhaul.

For most organizations, quantum readiness means three things:

**1. Know your cryptographic exposure.** Build a Cryptographic Bill of Materials (CBOM). Inventory every algorithm, key size, and protocol in your stack. TLS certificates, API authentication, data-at-rest encryption, VPN tunnels, digital signatures. You probably don't know all of them — most organizations don't. That's the first problem to solve.

**2. Plan your PQC migration.** The vulnerable algorithms are RSA, ECC, DH, and DSA. AES-256 is mostly fine — Grover's algorithm halves the effective key strength, but AES-256 becomes AES-128 equivalent, which is still strong. Your migration priority: TLS certificates first (highest exposure, most standardized path), then API authentication, then data-at-rest, then VPN/IPsec, then legacy systems.

**3. Budget for it.** PQC migration costs $200K-$2M depending on organization size and complexity. That sounds like a lot until you compare it to the alternative.

[The performance tax is real but manageable — ML-KEM keys are 800-1,568 bytes vs 32 bytes for X25519. TLS handshakes get heavier. But Chrome's already doing it for billions of users. It works.]

## The Math Your CFO Needs to See

Average cost of a data breach: $4.88 million (IBM Cost of a Data Breach Report, 2024).

That's one breach. One incident. One set of compromised data.

Q-Day isn't one breach. It's every RSA-encrypted secret in your organization exposed simultaneously. Every TLS session that was ever intercepted. Every encrypted database backup. Every signed document with a forgeable signature.

For a mid-size financial institution, the exposure looks something like this:

- GDPR fines: up to 4% of global annual revenue
- SEC enforcement actions: varies, but think eight figures
- Class-action litigation: depends on customer count and data sensitivity
- Customer trust destruction: post-breach churn averages 3.4% (Ponemon), but a "literally all encryption broken" event is unprecedented
- Competitive disadvantage: customers move to quantum-ready competitors

Conservative estimate for a mid-size financial institution: $50M-$500M in total exposure. The $1-2M migration cost is rounding error.

[Frame this as insurance. The cheapest insurance policy your CISO will ever buy. Not "can we afford to prepare?" but "can we afford not to?"]

## The Quantum Landscape (Who's Building What)

You don't need to pick a winner. You need to understand the field.

| Provider | Approach | Current Scale | Access Model | Strength |
|----------|----------|---------------|--------------|----------|
| IBM | Superconducting | 1,121 qubits (Condor) | Cloud (IBM Quantum) | Largest ecosystem, Qiskit |
| Google | Superconducting | 105 qubits (Willow) | Limited access | Error correction milestones |
| IonQ | Trapped ion | 36 algorithmic qubits | Cloud (via Braket, Azure) | High fidelity |
| Quantinuum | Trapped ion | 56 qubits (H2) | Cloud | Highest quantum volume |
| Amazon | Multi-provider | Via Braket | Cloud (Braket) | Provider-agnostic access |
| Microsoft | Topological | Research phase | Azure Quantum | Long-term bet |
| D-Wave | Quantum annealing | 5,000+ qubits | Cloud | Optimization-specific |

The market is projected to hit $65 billion by 2030 (McKinsey). 35% of large enterprises are already experimenting with quantum (Gartner 2025). This isn't fringe technology anymore.

## What This Series Covers

This is the first article in an 11-part series. Every article answers the same question: "What do I need to design, budget, or migrate today to be ready for quantum's impact on my systems?"

The roadmap:

1. **The QPU as a Coprocessor** — how quantum hardware fits in your data center
2. **Quantum-Classical Hybrid Patterns** — the dominant architecture for near-term quantum apps
3. **Designing for Probabilistic Outputs** — APIs that consume histograms instead of values
4. **Run Your First Quantum Circuit** — hands-on tutorial with Qiskit
5. **The Cryptographic Bill of Materials** — auditing your quantum exposure
6. **Post-Quantum Cryptography in Practice** — the migration playbook
7. **The Quantum Control Plane** — DevOps for cryogenic hardware
8. **The Quantum Price Tag** — what QPU time actually costs
9. **Quantum Machine Learning Pipelines** — integrating QML into your architecture
10. **The Fault-Tolerant Future** — designing for logical qubits

No cat metaphors. No quantum hype. Architecture-first, practical focus.

## What to Do Monday Morning

- Start your CBOM audit — just inventory what cryptography you're using across your stack
- Talk to your CISO about PQC migration timeline and budget
- Read the NIST PQC standard executive summaries (FIPS 203, 204, 205)
- Identify your highest-exposure systems (public-facing TLS, customer data encryption)
- Budget for a PQC pilot project — start with one service's TLS certificates

The quantum computer that breaks your encryption doesn't exist yet. But the data it will decrypt is being collected right now. The standards to protect against it are already published. The migration path is defined. The only question is whether you start now or explain to your board later why you didn't.

Target: ~1,800 words when complete
