# Checks: ledger, CHECKS.md, the professor's read, grading

Contents: Requirements Ledger · Evidence Map · CHECKS.md · Round 2 protocol (the professor's line-by-line read) · Twelve-point sentence test · Global reviewer pass · Issue format and severity · Coverage · Round 3 rubric and grader prompt

## Requirements Ledger (`ledger.md`)

Written in Phase 1, before anything is drafted. It is the contract. Phase 8 grades the finished paper against it.

```markdown
# Ledger: <paper or job name>
User request (verbatim): "<their words>"

| ID | Kind | Requirement | Status | Evidence |
|----|------|-------------|--------|----------|
| R1 | Asked | Fix all errors in Section 3 | OPEN | |
| R2 | Asked | Fit NeurIPS 2026 page limit (9 pages main text) | OPEN | |
| R3 | Implied | Every citation verified to exist | OPEN | |
| R4 | Implied | No claim stronger than its evidence | OPEN | |
| R5 | Implied | No fabricated numbers or references | OPEN | |
| R6 | Implied | Meaning of claims unchanged unless listed in CHANGES.md | OPEN | |
```

Status is `OPEN` until Phase 8, then `PASS`, `FAIL` or `BLOCKED` (needs something only the user can supply). Evidence names a section, line ID, file or measurement. `ledger_check.py` counts them and exits non-zero while anything is not `PASS` or `BLOCKED`.

Write requirements so they can be checked. "Make it better" is not a requirement; "tighten the introduction to at most 700 words without dropping a contribution" is.

## Evidence Map (`EVIDENCE.md`)

```markdown
| Claim | Statement | Evidence (file / figure / table / citation) | Status |
|-------|-----------|---------------------------------------------|--------|
| C1 | Method A beats baseline B on three benchmarks | results/main.csv, Table 2, Fig 3 | supported |
| C2 | The gain comes from component X | ablation.csv, Table 4 | partial (one dataset) |
| C3 | A works for long contexts | none | missing |
```

Also list the traceable numbers: each number in the abstract and results, and the file it comes from.

## CHECKS.md template

```markdown
# CHECKS
Date: ... Paper: ... Venue: ... (rules read on <date> from <url>)

## Round 1 Technical
paper_lint: <n FAIL, n WARN> -> fixed / explained
citation_check: ...
compile_check: pages N / limit M, undefined refs 0, overfull boxes K

## Round 2 The professor's read
Chunks reviewed: N of N. Issues found: F FATAL, M MAJOR, m MINOR, n NIT.
Fixed: ... Blocked: ... (each with reason)
issue_register --gate: PASS

## Round 3 Independent review
Panel: <skills used>. Scores: significance 4, soundness 4, novelty 4, clarity 5, experiments 4, reproducibility 4, writing 5, venue fit 4.
Strongest remaining objection: ...
Fixes after scoring: ...

## Closing gate
Ledger: R1 PASS ... (see ledger.md)
```

## Round 2 protocol: the professor's read

**Persona.** A senior professor at a top university. Has sat on program committees and edited a journal for years, reads sixty papers a season, is tired, and is looking for reasons to reject. Fair, not cruel. Never hand-waves: every complaint quotes the line, says why it matters, and says how to fix it. Does not care about the author's feelings or effort, only whether the claims are true and clearly shown. Knows the field's standard baselines and common failure modes.

**Procedure.**

1. `python3 -I <this skill>/scripts/line_review.py paper.tex --out review/` writes one file per chunk (about 40 sentences) with line IDs (`L0001`), the section each sentence sits in, and an `issues.md` with a Coverage list.
2. Read chunk 1, then 2, in order. Do not skip, skim or sample. For each sentence apply the twelve-point test below. Quote the exact words in the issue.
3. After each chunk, append its issues to `issues.md` and change its Coverage line from `pending` to `reviewed` (also when it had no issues).
4. When all chunks are read, do the global reviewer pass (below).
5. Fix in severity order. After fixing, set the issue to `fixed` and write what changed. A fix that needs missing evidence sets the issue to `blocked`, puts a `[TODO-EVIDENCE]` in the paper and adds a line to the report. A fix that changes meaning is also recorded in `CHANGES.md`.
6. Run `line_review.py` again after edits, review only the chunks whose text changed, then run `issue_register.py review/issues.md --gate`.

Parallel option (Full jobs, long papers): hand non-overlapping chunk ranges to fresh subagents with this protocol and the Evidence Map, and merge their issue blocks. Renumber IDs when merging. You still do the global pass yourself.

## Twelve-point sentence test

For every sentence, ask:

1. **Support.** Is the claim backed in the paper (a table, figure, proof, citation) or is it asserted? Is the support strong enough for the verb used?
2. **Number.** Does every number trace to a result file or a citation? Does it match the table, abstract and other mentions? Are units, sample size and uncertainty given?
3. **Citation.** Is the cited work real, and does it say this? Is it the original source? Is a citation missing for a non-obvious claim?
4. **Term.** Is every term and symbol defined before first use and used consistently after?
5. **Logic.** Does this sentence follow from the previous one? Is there a missing step, a non sequitur, a "therefore" that does not follow?
6. **Referent.** Is "this", "it", "they", "the proposed method" unambiguous?
7. **Hedge.** Is the strength of language proportional to the evidence (see `craft.md`)? Overclaim or needless fog?
8. **Consistency.** Does it contradict another line (setup, a number, a claim, a definition, a figure)?
9. **Scope.** Does it generalise beyond what was tested? Is the scope stated?
10. **Fairness.** Does it treat prior work and baselines fairly? Is a comparison apples to apples?
11. **Redundancy and need.** Does the reader need this sentence? Is it repeated elsewhere or only announcing what follows?
12. **Form.** Grammar, tense, notation, spelling, reference to figure and table numbers, AI tells.

## Global reviewer pass

After the line read, answer in writing and log each answer that is a problem as an issue:

- Is the central claim clear within the first page? Could the reader restate it?
- What are a skeptic's three strongest objections? Does the paper answer each?
- Which baseline, control, ablation or dataset is missing that a reviewer would ask for?
- Which claim is the weakest link? What if the biggest result were a fluke or leakage?
- Is the novelty over the closest prior work stated honestly and correctly?
- Do the abstract, introduction, results and conclusion all say the same thing?
- Do the limitations section and the checklist tell the truth?
- Would the work reproduce from the paper alone?
- Is anything here that the venue forbids (anonymity break, wrong template, over the page limit, missing statement)?

## Issue format and severity

`issues.md` holds blocks the parser reads. Keep the header line exactly in this shape:

```markdown
### I-001 | MAJOR | open | L0123-L0124 | claim-support
Quote: "Our method significantly outperforms all baselines."
Problem: No significance test is reported and one baseline (Table 2, row 3) is higher on dataset B.
Fix: Replace with "outperforms the baselines on datasets A and C (Table 2)" and report seeds and a test, or run the test.
```

Header fields: ID, severity, status, line IDs (or section name for global issues), category. Statuses: `open`, `fixed`, `blocked` (needs evidence only the user has), `out-of-scope` (real, but the user's request does not cover it; needs a `Reason:` line), `wontfix` (needs a `Reason:` line). Categories: `claim-support`, `number`, `citation`, `definition`, `logic`, `referent`, `hedge`, `consistency`, `scope`, `fairness`, `redundancy`, `form`, `format`, `missing-evidence`.

**Severity**
- `FATAL`: invalidates a central claim or makes the paper unpublishable as written (fabricated or untraceable number, claim contradicted by data, leakage, a proof gap that breaks the main theorem, a fake citation, plagiarism).
- `MAJOR`: a reviewer would reject or demand a revision for this (missing key baseline, overclaim, undefined central term, unsupported causal claim, citation that does not support the claim, a number that disagrees with the table).
- `MINOR`: weakens the paper but would not by itself decide (ambiguous referent, wrong tense, loose hedge, redundant paragraph).
- `NIT`: typo, spacing, style.

`issue_register.py --gate` fails while any FATAL or MAJOR is `open` and while any chunk is not `reviewed`. It passes with blocked FATAL or MAJOR issues but prints them: a pass means "the read is finished", not "ready to submit".

## Coverage list

Generated by `line_review.py` at the end of `issues.md`:

```markdown
## Coverage
- chunk_01: pending
- chunk_02: pending
```

Change each to `reviewed` only after reading every sentence in it.

## Round 3 rubric and grader prompt

Score 1 to 5 (anchors: 5 = a strong accept at a top venue on this dimension; 4 = solid, minor fixes; 3 = borderline, needs real work; 2 = major problems; 1 = unfit):

1. Significance and contribution
2. Soundness of claims and evidence
3. Novelty and positioning against prior work
4. Clarity and structure
5. Experiments or analysis (design, baselines, statistics)
6. Reproducibility
7. Writing quality
8. Venue fit and compliance

Anything under 4 is fixed, then re-scored once.

**Grader prompt** (give it to a fresh subagent with the Brief, Ledger, Evidence Map, the paper, QC outputs, `craft.md`):

> You are a senior professor and program-committee member. You did not write this paper and you have not seen how it was made. Before scoring, spend your effort finding reasons to reject: unsupported claims, numbers that do not match, missing baselines or controls, unverifiable citations, undefined terms, unfair comparisons, scope creep, and violations of the venue's rules. Quote the line for each. Then score the eight dimensions 1 to 5 with one sentence of evidence each, state your recommendation (strong reject, reject, borderline, accept, strong accept) and the three strongest objections an author would have to answer in a rebuttal. Do not be polite and do not invent problems: every objection must point to a specific passage.

For a venue-matched panel, run one or two of: `paperjury` (CS conferences), `self-review` (NeurIPS-style form), `academic-paper-reviewer` (journals), `review-paper` (economics and social science), `paper-review` (independent reviews with a meta-review). Treat their scores as signals, not verdicts, and fix the specific passages they cite.
