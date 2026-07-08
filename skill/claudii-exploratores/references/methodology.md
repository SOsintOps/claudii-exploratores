# OSINT Methodology — Analytic Standards, 5W1H, OPSEC

Condensed from the Exploratores toolkit guidelines. Read this when advising the
user on *how* to approach an investigation, how to express confidence, or how to
stay safe while collecting.

## Analytic standards (apply to every product)

Be **objective** (surface your own assumptions, mitigate bias), **independent** of
any agenda, **timely**, and **based on all available sources** while naming the
gaps. Additionally:

- Describe the **quality and credibility** of each source.
- Express **uncertainty** with a standardised likelihood vocabulary rather than
  vague words:

  | Almost no chance | Very unlikely | Unlikely | Roughly even | Likely | Very likely | Almost certain |
  |---|---|---|---|---|---|---|
  | 01–05% | 05–20% | 20–45% | 45–55% | 55–80% | 80–95% | 95–99% |

- Distinguish **information** from **assumptions/judgments**.
- Consider **alternative hypotheses** explicitly.
- Use clear argumentation; note **changes** from prior assessments; make accurate
  judgments given known gaps.

## The 5W1H method (structuring collection)

Use these six questions to decide *which* catalog categories to pull and to keep
the investigation focused:

- **Who** — actors, networks, key nodes, backers.
  → `names`, `usernames`, `email`, `facebook`, `instagram`, `x`, `vk`, `linkedin`,
  `keybase`, `publiccompanyrecords`.
- **What** — the event, capability, asset, vulnerability.
  → `domains`, `docs`, `images`, `videos`.
- **When** — precise timing, full timeline, temporal patterns.
  → archive/wayback tools within `domains`; date-scoped social searches.
- **Where** — physical (country/city/address/coords) and digital (site/IP/platform)
  location, plus jurisdiction. → `maps`, `address`, `ip`.
- **Why** — stated or inferred motive; why this target/timing/method; root cause.
- **How** — modus operandi, tools, TTPs, how detection was avoided.

## OPSEC — not optional

- **Identity segregation:** dedicated non-attributable personas and equipment;
  never personal accounts. Don't cross-link personas or tie them to your identity.
- **Secure infrastructure:** trusted no-log VPN; a dedicated VM for sensitive work;
  Tor Browser for `.onion` and higher anonymity.
- **Sterile browsing:** separate browser profile per persona; privacy extensions;
  clear cookies/cache/history.
- **Disciplined conduct:** minimise the personal data you reveal when registering;
  unique strong credentials per persona; watch your digital footprint.
- **Secure data handling:** encrypt case files; define retention and secure-deletion
  policy.

**Live-search caveat:** opening a target's own domain, tracker, or shortlink can
reveal your IP and browser fingerprint to infrastructure they control. Prefer
cached/archived views for first contact and route through a VPN.

## Further reading

Heuer, *Psychology of Intelligence Analysis*; Heuer & Pherson, *Structured Analytic
Techniques*; Bazzell, *Open Source Intelligence Techniques* and *Extreme Privacy*;
Baker, *Deep Dive*; UNODC, *Criminal Intelligence: Manual for Analysts*; ODNI
*ICD 203: Analytic Standards*.
