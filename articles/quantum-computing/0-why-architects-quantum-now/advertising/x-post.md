# X/Twitter Post

**Article**: Why Architects Need to Think About Quantum Now
**URL**: https://medium.com/@the-architect-ds/why-architects-need-to-think-about-quantum-now-even-though-its-not-ready-yet-e1706a5b055e

---

## Single Tweet

Your RSA encryption has an expiration date. It's called Q-Day (2029-2035).

Nation-state actors are already storing your encrypted traffic, waiting for the quantum computer that can read it.

NIST published the fix in 2024. Chrome already ships it.

New series: The Quantum-Centric Architect 🔗 https://medium.com/@the-architect-ds/why-architects-need-to-think-about-quantum-now-even-though-its-not-ready-yet-e1706a5b055e

---

## Thread Version

🧵 Your RSA encryption has an expiration date. Here's what architects need to know about quantum computing RIGHT NOW — even though it's not ready yet.

1/ Q-Day: somewhere between 2029-2035, quantum computers break RSA, ECC, and Diffie-Hellman. Every TLS session, every VPN tunnel, every code signature — breakable.

2/ But the real threat is TODAY. "Harvest now, decrypt later" — adversaries are storing your encrypted traffic right now, waiting for quantum hardware to read it. CISA says 50%+ of nation-state actors are doing this.

3/ What breaks: RSA, ECC, DH, DSA (your TLS, SSH, VPN, API auth)
What survives: AES-256 (weakened but fine), SHA-256 (fine)
Translation: your data in transit is on the clock. Data at rest is mostly OK.

4/ NIST published PQC standards in Aug 2024: ML-KEM (Kyber), ML-DSA (Dilithium), SLH-DSA (SPHINCS+). Chrome ships hybrid PQC by default. Signal adopted PQ protocol in 2023. The migration path is taking shape.

5/ Cost math: PQC migration = $200K-$2M. Average breach = $4.88M. Q-Day = most of your public-key encryption broken at once. For financial services: $50M-$500M exposure. The migration cost is rounding error.

6/ What to do Monday: Start a CBOM audit (inventory your crypto), talk to your CISO, read FIPS 203/204/205, pilot hybrid PQC on one service.

Full guide → https://medium.com/@the-architect-ds/why-architects-need-to-think-about-quantum-now-even-though-its-not-ready-yet-e1706a5b055e

#QuantumComputing #QDay

---

**Single tweet character count**: ~280
**Thread**: 6 tweets
