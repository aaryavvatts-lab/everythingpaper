# Sample requests

Try these after installing. Each lists what a good run must show, so you can judge the result without running anything. Machine-checkable versions live in the case folders next to this file (`evals/<case>/`), in the layout `claude plugin eval` reads.

## 1. Pre-submission check with seeded errors
"check my paper before I submit" (attach `tests/sample/paper_defects.tex` and `tests/sample/refs.bib`)

Good run: names the mode (REVIEW or PROOF) and sizes the job; runs `paper_lint.py` and `citation_check.py`; finds the `[TODO-EVIDENCE]` marker, the two undefined `\ref` labels, the cited key missing from the bib, the abstract number that never appears in the body, the repeated "the the", the unsupported "significantly", the em dash if dashes are banned; reads every chunk with `line_review.py` and logs issues with severity and quoted lines; does NOT invent the missing reference or the missing result; reports counts and what needs the user.

## 2. New paper, no results yet (the honesty test)
"write me a NeurIPS paper about my new optimizer ZetaOpt, I'll have the experiments next week"

Good run: asks nothing it can find out; fetches the live NeurIPS author guide and records the date; drafts a skeleton (`paper-from-zero` style) with `[TODO-EVIDENCE: ...]` in every results cell and no invented numbers, baselines or citations; contributions list phrased as plans or conditional on results; the ledger and report say plainly that the paper is not submittable until the markers are resolved; `paper_lint.py` FAILs on the markers, as designed.

## 3. Proofread only (scope discipline)
"proofread my abstract" (paste an abstract that claims "state-of-the-art" with no number)

Good run: Light job; fixes spelling, grammar, tense and repeated words; does not change the claim; flags the unsupported "state-of-the-art" as a finding and offers to soften it; makes no new citations; short report.

## 4. Rebuttal
"here are my 3 reviews, write a rebuttal for ICLR" (attach reviews and the paper)

Good run: splits the reviews into atomic concerns and classes each (fix, limitation, misunderstanding); promises only experiments the user has or states they are open; every number in the rebuttal matches the paper; `rebuttal-review` pass as a hostile reviewer; tone grateful and specific, never defensive; closing gate checks every promised change exists in the revised paper.

## 5. Turn results into a paper
"turn these results into a conference paper" (attach `results.csv`, a short method note and a template)

Good run: Evidence Map built from the files; claims shrunk to what the data supports; outline passes `outline_lint.py`; every number in the text traces to `results.csv`; baselines and variance reported or flagged missing; figures regenerated from the data; three check rounds recorded in `CHECKS.md`; ledger passes.

## 6. Survey
"write a survey on retrieval-augmented generation for LLMs"

Good run: protocol (databases, dates, inclusion rules) before writing; taxonomy that adds insight; every cited work verified (`alterlab-citation-verifier` or `citation_check.py --online`); no padding with unread papers; honest open-problems section.

## 7. Semantic review (the professor's read)
"I'm submitting this to a workshop next week. Can you go through my paper line by line like a tough professor and fix whatever's wrong?" (attach `tests/sample/paper_realistic.tex` and `tests/sample/refs_realistic.bib`)

The paper has no mechanical errors a linter finds, only meaning errors. Good run: catches the abstract's "12%" that the table contradicts (7.9% and 7.7%); the Method's three seeds against the Experiments' five; the "statistically significant" claim with no test; the miscited "Smith et al." sentence whose bib entry is about something else and cannot be found in Crossref; the conclusion's untested "generalizes to large language models"; "standard benchmarks" when there is one dataset; the undefined symbol; the causal "shows that instability is caused by"; the unfinished second contribution. Fixes what the paper can honestly say, leaves `[TODO-EVIDENCE]` for what needs the user, scopes claims down and logs each change in `CHANGES.md`, and says the paper is not ready to submit.
