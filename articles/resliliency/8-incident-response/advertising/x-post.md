# X/Twitter Post

**Article**: Incident Response: From Detection to Resolution in 10 Minutes
**URL**: [TO BE ADDED AFTER PUBLICATION]

---

## Single Tweet

3:07 AM. PagerDuty fires. Someone asked "is anyone looking at this?" 12 minutes ago. Nobody responded.

18 minutes of silence. ~$230K in failed checkouts.

The first 10 minutes of an incident determine everything. Here's the playbook:

🔗 [URL]

#ResilienceEngineering #SRE

---

## Thread Version

🧵 The industry average MTTR is 197 minutes. Elite teams resolve incidents in under 10. The difference isn't better engineers — it's better process for the first 10 minutes.

1/ Minutes 0-1: ACKNOWLEDGE. Just say "I'm looking at this" in the channel. The worst dynamic during an incident is everyone assuming someone else is handling it. One message changes everything.

2/ Minutes 1-3: TRIAGE. Three questions: What's broken? Who's affected? What changed recently? That last question resolves ~40% of incidents immediately — bad deploy, config change, or dependency down.

3/ Minutes 3-5: DECLARE AND ASSIGN. Incident Commander (coordinates, does NOT debug), Technical Lead (investigates), Communications Lead (status updates). Three roles. Non-negotiable.

4/ Minutes 5-10: MITIGATE. Not root cause. Stop the bleeding. Rollback → Feature flag → Failover → Scale → Restart. In that order. Understand later. Fix it when you're awake and caffeinated.

5/ The IC anti-pattern: the IC starts debugging because they're curious. The moment the IC debugs, nobody coordinates. Parallel investigations without awareness. Signals missed. Incident drags on.

6/ Your 3 AM brain runs at 60%. Runbooks compensate. Not "investigate and resolve" — step-by-step procedures. Tested quarterly. Stored where you can find them half-asleep.

Full playbook → [URL]

---

**Single tweet character count**: ~280
**Thread**: 6 tweets
