# Frequently Asked Questions (FAQ)

Frequently asked questions about Claudii Exploratores — its purpose, OSINT practice, using MCP and large language models (LLMs) for OSINT, and troubleshooting.

## Table of Contents

* [Why is it named "Claudii Exploratores"?](#why-is-it-named-claudii-exploratores)
* [How does it relate to the Exploratores OSINT Toolkit?](#how-does-it-relate-to-the-exploratores-osint-toolkit)
* [What does it do, and what does it not do?](#what-does-it-do-and-what-does-it-not-do)
* [What does "alpha" mean here?](#what-does-alpha-mean-here)
* [Is Claudii Exploratores covered by any warranty?](#is-claudii-exploratores-covered-by-any-warranty)
* [Am I responsible for validating what I find?](#am-i-responsible-for-validating-what-i-find)
* [Where can I learn more about OSINT?](#where-can-i-learn-more-about-osint)
* [How should I evaluate what I find?](#how-should-i-evaluate-what-i-find)
* [How do I turn the results into a report?](#how-do-i-turn-the-results-into-a-report)
* [What are the basic OPSEC rules when using it?](#what-are-the-basic-opsec-rules-when-using-it)
* [What are the ethical and legal limits?](#what-are-the-ethical-and-legal-limits)
* [Are there related SOsintOps projects?](#are-there-related-sosintops-projects)
* [What is MCP, and how is it different from the skill?](#what-is-mcp-and-how-is-it-different-from-the-skill)
* [Why is the MCP server offline?](#why-is-the-mcp-server-offline)
* [What can an LLM add to an OSINT investigation?](#what-can-an-llm-add-to-an-osint-investigation)
* [What must an LLM never do in an investigation?](#what-must-an-llm-never-do-in-an-investigation)
* [Is the output of an AI model a source?](#is-the-output-of-an-ai-model-a-source)
* [What is prompt injection, and why does it matter in OSINT?](#what-is-prompt-injection-and-why-does-it-matter-in-osint)
* [How do I keep case data away from an external AI service?](#how-do-i-keep-case-data-away-from-an-external-ai-service)
* [Can I use a local model instead of a cloud service?](#can-i-use-a-local-model-instead-of-a-cloud-service)
* [Can an AI agent open the links for me?](#can-an-ai-agent-open-the-links-for-me)
* [How does Claudii Exploratores compare with other OSINT MCP servers?](#how-does-claudii-exploratores-compare-with-other-osint-mcp-servers)
* [Why do some links carry a warning?](#why-do-some-links-carry-a-warning)
* [What does "geo-locked" mean, and what should I do about it?](#what-does-geo-locked-mean-and-what-should-i-do-about-it)
* [How were the access requirements checked?](#how-were-the-access-requirements-checked)
* [Why does an indicator return fewer links than I expected?](#why-does-an-indicator-return-fewer-links-than-i-expected)
* [Which indicator types are recognised?](#which-indicator-types-are-recognised)
* [What about the .onion links?](#what-about-the-onion-links)
* [How does the catalog stay in sync with Exploratores?](#how-does-the-catalog-stay-in-sync-with-exploratores)
* [What happens when a source dies?](#what-happens-when-a-source-dies)
* [How can I suggest a source or report a problem?](#how-can-i-suggest-a-source-or-report-a-problem)
* [How do I rebuild the catalog and the packages?](#how-do-i-rebuild-the-catalog-and-the-packages)
* [The MCP server does not start: what should I check?](#the-mcp-server-does-not-start-what-should-i-check)
* [The skill does not trigger in Claude: what should I check?](#the-skill-does-not-trigger-in-claude-what-should-i-check)

---

## About Claudii Exploratores & Its Name

### Why is it named "Claudii Exploratores"?

*Exploratores* were the scouts of the Roman army, sent ahead to reconnoitre terrain and enemy positions; the name comes from the [Exploratores OSINT Toolkit](https://github.com/SOsintOps/Exploratores). *Claudii* — "of Claudius" — is a nod to Claude, the AI model the suite was built for: the scouts of Claudius.

### How does it relate to the Exploratores OSINT Toolkit?

It is a direct derivative. Exploratores is a static web application: a page per theme, a search box, and buttons that open curated OSINT searches. Claudii Exploratores takes the same catalogue — every URL template, the indicator classifier, the validators, the IBAN table and the Redactor concept — and packages it for an AI assistant, as an agent skill and as an MCP server. The catalogue is synced from Exploratores every week (see [How does the catalog stay in sync with Exploratores?](#how-does-the-catalog-stay-in-sync-with-exploratores)), so a source added or removed there follows here.

### What does it do, and what does it not do?

Given an indicator (a name, an e-mail address, a domain, an IP address, a username, a phone number, a company, an IBAN, a Normattiva URN, a Telegram channel…), it recognises its type and **builds** the matching set of search links from the catalogue, each with its access requirements. It also checks IBANs offline and redacts personal data from text.

It does **not** open the links, collect data, log in anywhere or store anything. Opening a link is a decision of the analyst — or of an agent the analyst has explicitly told to do it — because that is the moment the search reaches a third party.

### What does "alpha" mean here?

The suite works and is tested (see the [test suite](../tests)), but it has not been hardened for operational use. URL templates are inherited from Exploratores and may break when a service changes; the phone-number logic is simpler than the web toolkit's. Test it in a safe environment before relying on it, and report what you find.

## Usage & Authorisation

### Is Claudii Exploratores covered by any warranty?

No. It is provided "as is", without warranty of any kind, under the [AGPL-3.0](../LICENSE) licence. The authors accept no liability for any damage, loss or legal consequence arising from its use.

### Am I responsible for validating what I find?

Yes, entirely. A generated link is a place to look, not a finding; a page is a claim by its author, not a fact. Corroborate every item across independent sources, record where it came from, and grade it before it enters a report.

## Learning & Best Practices

### Where can I learn more about OSINT?

Start with the [Intelligence Field Notes](https://github.com/SOsintOps/intelligence-field-notes), the method reference of every SOsintOps tool:

*   [OSINT Methodology](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/osint-methodology.md): the OSINT cycle, the 5W1H method, collection discipline, OPSEC, legal and ethical limits.
*   [Analytic Standards](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/analytic-standards.md): the intelligence cycle and the ICD 203 standards.
*   [Analytic Techniques](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/analytic-techniques.md): cognitive biases, analysis of competing hypotheses, premortem, deception.
*   [Reading List](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/reading-list.md): every text the notes draw on, linked.

An offline copy of the notes is kept in [`docs/field-notes/`](field-notes/README.md), regenerated from the original at each release. The skill carries a condensed version in [`references/methodology.md`](../skill/claudii-exploratores/references/methodology.md), which Claude reads when it advises on tradecraft.

### How should I evaluate what I find?

With the UNODC 4 x 4 system described in [Source Evaluation](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/source-evaluation.md): the **source** (A, B, C, X) and the **information** (1 to 4) are graded separately, as close to the origin as possible, when the item enters the case. The platform is not the source, and neither is a tool: grade the record a link points to, after you have retrieved it. Ten channels forwarding the same post are one source, not ten.

### How do I turn the results into a report?

Follow [Report Writing](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/report-writing.md): bottom line up front, facts kept apart from judgements, every statement sourced, likelihood expressed with the [ICD 203 scale](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/estimative-language.md), a handling marking (Traffic Light Protocol). An AI model can help draft and check the structure; the judgements, and the responsibility for them, stay with the analyst.

### What are the basic OPSEC rules when using it?

*   **Every link you open reaches a third party.** The service sees your IP address, your browser and the term you searched. Open links from a dedicated, sterile browser profile, behind a trusted no-log VPN, ideally in a virtual machine kept for investigations.
*   **Passive before active.** Prefer what the subject cannot see; viewing a profile or joining a group may notify them. Decide it deliberately.
*   **Know what your tools send.** The MCP server sends nothing, but the AI model you use receives whatever you type: see [How do I keep case data away from an external AI service?](#how-do-i-keep-case-data-away-from-an-external-ai-service).
*   **Non-attributable accounts** for the sources that need a login, never your personal ones.

Full list in the [OPSEC section](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/osint-methodology.md#operational-security-opsec-best-practices) of the field notes.

### What are the ethical and legal limits?

Open source does not mean free of rules. Use the suite only for authorised, lawful work — investigation, research, security, journalism, due diligence — and never for stalking, harassment or doxxing. Know which data-protection law applies to you and to the subject (in Europe, the GDPR) and what each platform's terms allow; collect only what the requirement needs; protect the people who appear incidentally. Claude is instructed to decline requests that look like targeting a private individual.

### Are there related SOsintOps projects?

Yes:

*   **[Exploratores](https://github.com/SOsintOps/Exploratores)**: the web toolkit this suite is derived from, with the same catalogue, the Redactor, CyberChef and Janua.
*   **[Intelligence Field Notes](https://github.com/SOsintOps/intelligence-field-notes)**: analytic standards, OSINT method, source evaluation and report writing.
*   **[Argos](https://github.com/SOsintOps/Argos)** and **[Speculator](https://github.com/SOsintOps/Speculator-Project)**: OSINT workstations for Ubuntu and Debian, with Exploratores as their start page.
*   **[Quaesitor](https://github.com/SOsintOps/quaesitor)**: a local case graph for people, phones, accounts, companies and documents.
*   **[Il Conclave](https://github.com/SOsintOps/il-conclave)**: a Claude Code skill (in Italian) that runs analytic techniques — ACH, a premortem, a steelman — as separate procedures on one question.
*   **[Maigret](https://github.com/SOsintOps/maigret)**: our fork of the username-search tool, to check a username across thousands of sites at once.

The full list is in the field notes' [Related Projects](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/related-projects.md).

## MCP and LLMs for OSINT

### What is MCP, and how is it different from the skill?

The [Model Context Protocol](https://modelcontextprotocol.io) (MCP) is an open standard that lets an AI application call external tools: the server declares its tools, and the client (Claude Desktop, Claude Code, or any MCP-compatible application) lets the model call them. The **MCP server** here exposes seven tools: `classify_indicator`, `build_osint_urls`, `search_catalog`, `list_categories`, `verify_iban`, `redact_pii`, `restore_pii`.

The **agent skill** is a folder of instructions and scripts that Claude loads when a request matches it: it teaches the method (5W1H, OPSEC, how to present links and warnings) and runs the same engine through a command-line script. Use the skill in Claude Code or Cowork, where Claude can run scripts; use the MCP server in Claude Desktop or any other MCP client. Both give the same results.

### Why is the MCP server offline?

Because the tools that query services on your behalf are also the tools that leak: every call sends an identifier, an API key and your IP address to someone. This server only reads its bundled catalogue and computes; it makes no network request, keeps no state and needs no key. Its tools are marked read-only and closed-world (`readOnlyHint`, `openWorldHint: false`), so the client can see that calling them is safe. The exposure happens only when someone opens a link — and that is left to a human decision.

### What can an LLM add to an OSINT investigation?

*   **Triage and scoping:** turning a vague question into the 5W1H questions that matter, and choosing the handful of sources worth opening first out of hundreds.
*   **Pivots:** suggesting the next indicator to search (a username found in a WHOIS record, a company director's name) and keeping track of what has been searched, including dead ends.
*   **Reading and structuring:** summarising long pages you have captured, extracting entities, drafting a timeline or a report skeleton.
*   **Challenge:** running a structured technique — competing hypotheses, a premortem — so that the reasoning can be checked (see [Techniques as AI Procedures](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/analytic-techniques.md#techniques-as-ai-procedures)).

### What must an LLM never do in an investigation?

*   **Invent findings.** A model that has not read a page must not say what it "would" contain. The skill's first rule is: build links, never fabricate results.
*   **Decide on its own to touch the subject:** open links, log in, send requests or join groups without the analyst's explicit instruction.
*   **Present a guess as a fact.** Every statement needs a source the analyst can open, and likelihood words must follow the [estimative language](https://github.com/SOsintOps/intelligence-field-notes/blob/main/docs/estimative-language.md) rules.
*   **Take the judgement.** The output of a model is a second opinion; the analyst owns the assessment.

### Is the output of an AI model a source?

No. Like a search engine or an aggregator, a model returns pointers and summaries, and it can be confidently wrong. Retrieve the underlying record, capture it, and grade *that*. When a model summarises a page, check the summary against the page before it enters the case.

### What is prompt injection, and why does it matter in OSINT?

Pages, profiles and documents can contain text written to manipulate an AI that reads them: "ignore your instructions and…", hidden text, instructions disguised as data. In OSINT the content is often produced by the very people you are investigating, so treat everything an agent retrieves as data, never as instructions. An agent that reads target content should not be able to act on it without you seeing the step — no downloads, no messages, no form submissions on the page's say-so.

### How do I keep case data away from an external AI service?

Redact first, restore afterwards — the same workflow as the Exploratores [Redactor](https://github.com/SOsintOps/Exploratores/blob/v3/docs/faq.md#what-is-the-redact--llm--restore-workflow):

1.  Call `redact_pii` (or `exploratores.py redact`) on the case text: e-mail addresses, IP addresses, phone numbers, IBANs, card numbers, URLs and crypto addresses become numbered placeholders such as `[EMAIL_1]`, and you get back a map.
2.  Send only the redacted text to the external model.
3.  Call `restore_pii` with the map on the model's answer to put the real values back.

The redaction runs locally and the map never leaves your machine unless you send it. Names of people and places are not caught by patterns: add them through `custom_patterns`, or remove them by hand.

### Can I use a local model instead of a cloud service?

Yes. The skill is written for Claude, but the MCP server works with any MCP client, including desktop applications that run open-weight models locally (for example LM Studio, which can act as an MCP client). A local model keeps case text on your machine, at the cost of weaker reasoning on long or subtle material; check its output with the same care. Whatever the model, the links it helps you choose still go out to third parties when opened.

### Can an AI agent open the links for me?

It can, if you give it a browser (for example Claude in Chrome) and tell it to — and then it browses *as you*: from your IP address, with your browser profile and any account logged into it. Use a dedicated browser profile, without personal sessions, behind the VPN you would use yourself; open links one by one rather than in bulk, which is faster but looks like a bot and trips rate limits; and never let the agent solve CAPTCHAs or log into accounts on its own initiative. Geo-locked links need the VPN set to the right country *before* the agent opens them.

### How does Claudii Exploratores compare with other OSINT MCP servers?

A survey of the public OSINT MCP servers (November 2026) shows two families:

*   **Servers that query services for you**, through API keys or local tools: OpenOSINT (Shodan, Censys, VirusTotal, Have I Been Pwned and more, passive by default with a call cap), mcp-shodan and mcp-virustotal, mcp-maigret (runs Maigret in Docker), wrappers around SpiderFoot, Sherlock or theHarvester, and the official hosted servers of Have I Been Pwned and Censys. They return data, but every call leaves your machine with your key and your query.
*   **Skills that teach method**, such as Claude-OSINT, a set of skill files for authorised reconnaissance with an OPSEC module.

Claudii Exploratores sits between the two: a curated catalogue of over 900 sources, a classifier and an offline server that never contacts anyone, plus redaction and IBAN checks that the others do not offer. It pairs well with a querying server when you have the keys, and on its own when you do not want any identifier to leave your machine.

## Functionality

### Why do some links carry a warning?

Because some sources only work under conditions you should know before opening them. `build_osint_urls` adds an `access_note` to each such link and a `warnings` list at the top; the command line prints them as ⚠️ lines. They say whether a link is **geo-locked** (needs a VPN exit in a given country), **may need** a VPN (estimated, not verified), is **Tor-only**, needs an **account**, or showed **bot protection** during testing. Claude is instructed to repeat these warnings next to the links, never to drop them.

### What does "geo-locked" mean, and what should I do about it?

The service only answers requests from IP addresses in one country — mostly US people-search and phone-lookup sites, which block European visitors. From elsewhere you get an error, an empty page or a block page, and a blocked attempt still tells the site someone looked. Before opening a geo-locked link, set your VPN to an exit in that country. A VPN changes your exit IP address, not your identity: keep the sterile browser profile. If you have no such VPN, drop those links with `exclude_geo_locked=true` (or `--no-geo-locked`).

### How were the access requirements checked?

In two steps. Every source was first classified at the desk by its known login and geography rules ([classification page](query-auth-vpn-classification.md)). Then each host was opened in a browser with neutral test values (`example.com`, `John Smith`, `8.8.8.8`): first from an exit in Italy, then — only for the hosts that did not work — through a VPN exit in the candidate country ([access guide](access-requirements-guide.md)). A verdict confirmed in the browser is marked `live`; one that is only estimated is marked `desk`. CAPTCHAs and bot challenges are recorded, never solved. `scripts/check_links.py` repeats the automated part of the check.

### Why does an indicator return fewer links than I expected?

A link is returned only when every placeholder of its template can be filled. Some sources need more than the indicator itself — a US state for licence plates, a full postal address, a date range, a list ID — and are skipped unless you pass those values in `fields` (MCP) or `--field key=value` (command line). The classifier also limits the categories to the ones that fit the type; pass `categories=["all"]` to see everything that can be filled.

### Which indicator types are recognised?

Domain, URL, e-mail address, IPv4 address, username (including platform-specific forms for X, Instagram, Facebook, VK, Telegram and LinkedIn URLs), person's name, coordinates, IBAN, Bitcoin, Ethereum and Monero addresses, vehicle VIN, phone number (international or national), YouTube video and channel IDs, US Social Security number, AdSense and Analytics IDs, MD5, SHA-1 and SHA-256 hashes, hashtag, Normattiva URN, Court of Justice case number and EU VAT number. Company, postal address, legal free text and Telegram keyword are available as forced types (`indicator_type` or `--type`). When several types are plausible, the classifier returns them ranked by confidence.

### What about the .onion links?

A few search engines in the catalogue are Tor hidden services. They work only in Tor Browser, never in a normal browser through a VPN. They are flagged in the warnings; exclude them with `include_onion=false` (or `--no-onion`).

## Maintenance & Contribution

### How does the catalog stay in sync with Exploratores?

Exploratores publishes its catalogue as a JSON file with a SHA-256 hash. `scripts/sync_catalog.py` rebuilds `catalog.json` from it, and a weekly workflow compares the two and opens an issue listing what was added, removed or changed upstream. A maintainer then runs the build, the tests and opens a pull request. The catalogue is never edited here by hand.

### What happens when a source dies?

Dead sources are handled upstream, in the Exploratores link review: each host is rechecked by hand from a second IP address and through public DNS servers before its button is removed, and the change is documented in the Exploratores version history. Claudii Exploratores follows on the next sync. If you find a dead link here, report it (see below): it will be checked in Exploratores first.

### How can I suggest a source or report a problem?

Open an [issue](https://github.com/SOsintOps/claudii-exploratores/issues/new/choose): there are templates for a bug, a broken or blocked link, and a new source. New sources are added to Exploratores first, so that both projects stay identical. For security problems use a private security advisory (see [SECURITY.md](../SECURITY.md)). Contributions are welcome; read [CONTRIBUTING.md](../CONTRIBUTING.md) first.

## Technical Details & Troubleshooting

### How do I rebuild the catalog and the packages?

```bash
scripts/build_release.sh /path/to/Exploratores   # checkout of branch v3; omit to keep the catalog
pytest -q tests
```

The script syncs the catalogue, rebuilds the classification, the access map and the catalogue overview, copies the engine into the skill and the MCP package, and builds `dist/claudii-exploratores.skill`. See [DISTRIBUTION.md](DISTRIBUTION.md).

### The MCP server does not start: what should I check?

*   **Python 3.10 or later** in the environment the client launches; the skill works on 3.9, the server does not.
*   **The interpreter in the client configuration** is the one where you ran `pip install -e mcp/` (use its absolute path, or the `claudii-exploratores-mcp` command).
*   **`mcp` version:** 1.x and 2.x are both supported; older releases of this suite failed on 2.x because `FastMCP` was renamed — update to 1.1.0-alpha or later.
*   Run `python -m exploratores_osint_mcp.server` in a terminal: an import error shows there, not in the client.

### The skill does not trigger in Claude: what should I check?

Check that the folder is `~/.claude/skills/claudii-exploratores/` with `SKILL.md` at its top level (not one folder deeper), restart the client, and phrase the request as an investigation ("run OSINT on example.com", "find profiles for this username"). You can always run the script directly: `python scripts/exploratores.py urls "<value>"`.
