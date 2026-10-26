# Venues: find the live rules, record them, check them

Why this file exists: venue rules change every cycle (page limits, templates, anonymity, checklists, AI-use policy, deadlines). Remembered rules are the most common cause of a desk reject. Always read the live source and record what it said and when.

Contents: How to find the rules · What to record · What to check by venue family · AI-use policy · Desk-reject list

## How to find the rules

1. Search for "<venue> <year> call for papers" and "<venue> <year> author instructions". Prefer the official site (the venue's own domain, the sponsoring society or publisher, OpenReview).
2. Read the page itself with a fetch or the browser; a search snippet is not the rule.
3. Look for: submission deadlines, page and word limits, template and style file links, review model, anonymity rules, supplementary material rules, checklists, ethics and reproducibility statements, preprint policy, AI-use policy, camera-ready rules.
4. Use the venue skill (`neural-information-processing-systems`, `international-conference-on-machine-learning`, `annual-meeting-of-the-association-for-computational-linguistics`, ...) for fit, framing and common desk-reject risks. They are strategy aids and say to check the live call. Do that.
5. If a page cannot be reached, mark the rule `unverified` in the Brief and report. Do not guess.

## Workshops, tracks and unnamed venues

A workshop paper follows the workshop's own call, which is usually a short page limit (4 to 8 pages), often non-archival, with the parent conference's template and anonymity rules. If the user says "a workshop" and names nothing, do not guess a venue to look up. Read the live rules of the parent conference's workshop guidelines if the user names the conference; otherwise write to a neutral template, mark every venue rule `unverified` in the Brief, and ask in the report for the workshop name, page limit, template, anonymity and AI-use policy. The same applies to an unnamed journal: use the field's norms from `craft.md` and say the format is unverified.

## What to record (in `SOURCES.md` under "Venue")

| Item | Value | Source URL | Date read |
|---|---|---|---|
| Venue and year, track | | | |
| Page or word limit (main text, references, appendix) | | | |
| Template and style file | | | |
| Review model (double blind, single blind, open) | | | |
| Anonymity rules (self-citation, links, acknowledgements) | | | |
| Required statements and checklists | | | |
| Supplement and code rules | | | |
| Preprint and concurrent-submission policy | | | |
| AI-use policy | | | |
| Deadline (timezone) | | | |

## What to check by venue family

- **ML conferences (NeurIPS, ICML, ICLR, AAAI, IJCAI, COLM):** strict page limit for main text; an official LaTeX style file used unmodified (no margin or font tricks); double-blind; a reproducibility or paper checklist; limitations and broader-impact statements; appendix rules; OpenReview formatting; reciprocal reviewing duties.
- **Vision and NLP conferences (CVPR, ICCV, ECCV, ACL, EMNLP, NAACL):** page limit with references outside it (check), double blind with an anonymity policy covering preprints, a responsible-NLP or ethics checklist, a limitations section required (ACL family), supplementary-material rules, an artifact and licence checklist.
- **Data, web and IR (KDD, WWW, SIGIR, VLDB, SIGMOD):** track-specific rules (research, applied data science, resource), reproducibility requirements, data and code availability, often a rolling or multi-round review.
- **Systems and security (OSDI, SOSP, NSDI, USENIX Security, IEEE S&P):** artifact evaluation, ethics and disclosure sections for security work, strict formatting, often multiple submission cycles.
- **HCI (CHI):** accessibility of the PDF, participant and ethics reporting, positionality, a contribution type declared up front.
- **Journals (Nature family, Science, Cell, IEEE and ACM journals, discipline journals):** article type and word limit, structured abstract rules, reporting guideline (CONSORT, STROBE, PRISMA, ARRIVE), data and code availability statement, author contributions, competing interests, funding, cover letter, suggested reviewers, preprint policy.
- **arXiv:** category choice, licence, the template is free; check if the venue allows posting and when.

## AI-use policy

Policies differ and move fast. Typical rules: authors are responsible for all content; AI tools cannot be authors; use must be disclosed (where depends on the venue); AI may not be used to write reviews or may need disclosure there; uploading confidential manuscripts to external tools can be forbidden. Read the live policy and use `alterlab-ai-use-disclosure` to draft the statement when the user asks. Record the policy and the date in `SOURCES.md`.

## Desk-reject list (check before submit)

- Over the page limit, or margins, font or spacing altered.
- Wrong or modified template.
- Anonymity broken (names in the text, files, links, metadata; "our previous work [self-citation]" phrased to reveal identity; acknowledgements, funding).
- Missing required checklist, ethics or limitations statement.
- Concurrent submission or a policy-breaking preprint.
- Out of scope for the venue or track.
- Compile errors, missing figures, broken references showing as `??`.
- Supplement that contains main-text content the rules forbid.
- Plagiarised or reused text, or an undeclared AI disclosure where it is required.
