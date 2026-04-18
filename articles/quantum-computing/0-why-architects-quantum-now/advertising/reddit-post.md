# Reddit Post

**Article**: Why Architects Need to Think About Quantum Now
**URL**: https://medium.com/@the-architect-ds/why-architects-need-to-think-about-quantum-now-even-though-its-not-ready-yet-e1706a5b055e

---

## Subreddits
- r/programming
- r/netsec
- r/cybersecurity
- r/softwarearchitecture
- r/ExperiencedDevs

## Title
Why software architects should start thinking about post-quantum cryptography now (even though quantum computers can't break RSA yet)

## Post Body (r/netsec / r/cybersecurity)

I wrote a practical guide for software architects on quantum readiness — not the physics, but the architectural and security implications.

The TL;DR: "harvest now, decrypt later" attacks mean data encrypted with RSA/ECC today is potentially at risk once quantum computers scale up (estimated 2029-2035). NIST finalized PQC standards in August 2024. Chrome already ships hybrid ML-KEM + X25519. The migration path exists.

The article covers:
- What breaks (RSA, ECC, DH) vs. what doesn't (AES-256, SHA-256)
- What a CBOM (Cryptographic Bill of Materials) audit looks like
- PQC migration priority order (TLS certs first)
- The performance tax of larger PQC keys (800-1,568 bytes vs. 32 bytes)
- Cost analysis ($200K-$2M migration vs. breach exposure)

This is Part 0 of an 11-part series. No quantum hype, no cat metaphors. Architecture-first, practical focus.

Curious what others are seeing — is your org tracking a PQC migration timeline? Anyone done a CBOM audit yet?

https://medium.com/@the-architect-ds/why-architects-need-to-think-about-quantum-now-even-though-its-not-ready-yet-e1706a5b055e

## Post Body (r/programming / r/ExperiencedDevs)

Wrote a practical overview of why quantum computing matters for software architects right now — focused on the security and architectural implications, not the physics.

Key points: NIST published PQC standards in 2024, Chrome ships hybrid post-quantum key exchange by default, and "harvest now, decrypt later" means data encrypted today with RSA is potentially at risk. The migration path is defined but most orgs haven't started.

First article in an 11-part series covering quantum architecture, PQC migration, hybrid quantum-classical patterns, and the operational side of quantum computing.

https://medium.com/@the-architect-ds/why-architects-need-to-think-about-quantum-now-even-though-its-not-ready-yet-e1706a5b055e

---

**No hashtags** (Reddit convention)
