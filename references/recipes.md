# Recipes by job type

Why this file exists: different jobs need different step orders. Pick the matching recipe after choosing the spine (SKILL.md Phase 2a), then adjust. Each recipe gives the sequence, the skills in order, and the traps. Phases 7 and 8 (three check rounds, closing gate) apply to every recipe.

Contents: New ML or CS conference paper · New journal article · Finish a partial draft · Edit and polish a full draft · Proofread only · Review only (a report on a paper) · Revise after reviews and write the rebuttal · Camera-ready or new venue · Survey or literature review paper · Thesis chapter · Theory paper · Abstract, intro or one section only

## New ML or CS conference paper

1. Brief, ledger, venue rules (live author guide, page limit, anonymity, checklist, AI-use policy).
2. Evidence audit: experiment logs, tables, code. `experiment-result-to-claim` to decide what the results support.
3. Claims, outline, figure plan. `outline_lint.py`.
4. Spine: `paper-orchestra` (idea plus experiment log plus template) or `paper-assembly`. Venue skill for desk-reject risks. `ml-paper-writing` for the template and style.
5. Literature: `literature-search`, `paper-lookup`; verify each paper; `related-work-writing`.
6. Draft: `method-writing`, `results-writing`, `intro-related-writing`, `abstract-writing`, `conclusion-writing`, `caption-writing`, `figure-creation`, `table-generation`.
7. Edit ladder, then `deslop`.
8. Checks: Round 1 scripts, Round 2 professor read, Round 3 `paperjury` and `self-review`.
9. Appendix with `supplement-writing`; checklist; AI disclosure; compile to the page limit.

Traps: weak or untuned baselines, one seed, claims wider than the benchmarks, page-limit overflow, an anonymity slip (author names, self-revealing links, acknowledgements), forgetting the venue's checklist.

## New journal article

1. Brief and ledger; target journal rules (word limit, structure, reporting guideline, data and code policy, cover letter).
2. Evidence audit and claim shrinking. `statistical-analysis` and `stats-reporting-audit` for the analysis.
3. Spine: `academic-pipeline`. Add `journal-targeting` if the journal is open, `paper-journal-style` once chosen, `scientific-writing` and `sciwrite-manuscript` for prose, `nature-paper-workflow` for Nature-family targets.
4. Draft in the Phase 5 order. Methods in the journal's reporting style.
5. Edit ladder, `anti-defensive-writing`, `nature-polishing` if the writer is non-native, `deslop`.
6. Checks with `academic-paper-reviewer` and `submission-audit`; `data-availability`; cover letter; `alterlab-ai-use-disclosure`.

Traps: causal claims without a causal design, no limitations section, missing reporting checklist, an abstract that overstates the discussion, undeclared conflicts and funding.

## Finish a partial draft

1. Read what exists. List what is missing against the outline (Phase 3 on the existing text).
2. Evidence audit: for each existing claim, is evidence in hand? Mark gaps.
3. Complete missing sections with `paper-write` or the section skills, using only real evidence; mark gaps `[TODO-EVIDENCE]`.
4. Keep the user's voice: `paper-style-calibration` from their existing sections.
5. Run the edit ladder and the checks.

Trap: rewriting the sections the user already wrote well. Edit those only where Round 2 finds a problem.

## Edit and polish a full draft

1. Copy to `paper/v1/`. Evidence Map from the existing claims.
2. `manuscript-optimizer` for argument and structure; fix at that level first.
3. Section passes with the matching skill (`abstract-writing`, `intro-related-writing`, `method-writing`, `results-writing`).
4. `sentence-audit`, `paper-refine`, `latex-polish`; then `anti-defensive-writing` and `deslop`.
5. Checks. Report each meaning-changing edit.

Trap: changing meaning while "polishing". Anything that changes a claim, number or scope is logged in `CHANGES.md` and flagged to the user.

## Proofread only

1. Light job unless the paper is for submission.
2. `paper_lint.py`, `citation_check.py`, `compile_check.sh`.
3. `line_review.py` and the twelve-point test, but fix only `form`, `number`, `definition` and `referent` issues. Report anything about claims, evidence or logic as a finding, do not rewrite it.
4. Skills: `sentence-audit`, `latex-polish` (light), `reference-checker`.

Trap: scope creep. A proofread does not change the argument.

## Review only (a report on a paper)

1. Confidentiality first: if it is someone else's unpublished paper, stay local and confirm the venue allows AI help with reviewing.
2. Read in full. Round 2 protocol, with no edits. Evidence Map of what the paper claims and what supports it.
3. Skills: `paper-review`, `academic-paper-reviewer`, `peer-review`, `paperjury` or `self-review` for the venue.
4. Output: summary, strengths, weaknesses (quoted), questions for the authors, missing experiments, a recommendation, and what would change your mind. Be specific and kind about the author, hard on the claims.

## Revise after reviews and write the rebuttal

1. Read every review. Split into atomic concerns (`rebuttal-writing` stage 1) and label each: valid and fixable, valid and not fixable now, misunderstanding, out of scope.
2. For each valid concern decide the fix: new experiment, text change, clarification, honest limitation. Only run or claim experiments the user actually has; otherwise promise nothing and mark `[TODO-EVIDENCE]`.
3. `paper-revision` applies the edits; `rebuttal-pipeline` or `review-response` writes the letter point by point. Quote each comment, answer directly, point to the changed text.
4. `rebuttal-review` reads the letter as a hostile reviewer. Tone: grateful, specific, never defensive.
5. Checks: every promised change exists in the paper; every number in the rebuttal matches the paper; length within the venue's limit.

Traps: promising experiments that will not be run, answering a different question from the one asked, arguing with a reviewer instead of fixing the paper.

## Camera-ready or new venue

1. Fetch the live camera-ready or new-venue guide. List differences (template, page limit, de-anonymisation, copyright form, required statements).
2. `latex-fmt`, `latex-formatting`, `venue-compliance`; `latex-conference-template-organizer` if given a template zip.
3. Apply the reviewers' promised changes. Un-anonymise only as the venue directs.
4. `paper-compilation` and `compile_check.sh`; check fonts, figures and the page count.

## Survey or literature review paper

1. Scope, research questions, protocol (databases, search strings, dates, inclusion and exclusion). `deep-research`, `kd-literature-review`, `sr-screener` for a systematic review.
2. Spine: `survey-generation` and `review-article-architecture`.
3. Taxonomy that adds insight; a table of surveyed work; open problems.
4. Verify every cited work; `citation-audit` at the end.

Trap: a list of summaries with no synthesis, and stale coverage.

## Thesis chapter

1. Read the thesis outline and neighbouring chapters so terms and notation match.
2. `academic-writing-skills`, `scientific-article-writing` for a paper-style chapter; section skills as needed.
3. Check that the chapter's claims match the thesis' overall claims.
4. Round 2 on the chapter. Follow the university's formatting rules, which are the venue here.

## Theory paper

1. Statements precise, assumptions listed, proof sketch in main text, full proofs in appendix.
2. `proof-writer` and `proof-checker`; every lemma used is stated or cited.
3. Compare bounds to known results in a table. Give a tightness or sanity example.
4. Round 2 reads each proof step. A gap is FATAL.

## Abstract, intro or one section only

Light job. Load the single section skill (`abstract-writing`, `intro-related-writing`, ...), `sentence-audit`, `deslop`. Ask for the context you need (claims, results) only if it is not in the files. Run `paper_lint.py` on the text and self-review it as the professor.
