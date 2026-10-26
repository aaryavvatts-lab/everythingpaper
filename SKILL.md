---
name: everythingpaper
description: One-command research-paper studio. Works out what paper job you have (new paper from an idea or results, finish a draft, edit, proofread, find and fix errors, review before submission, revise after reviews, rebuttal, camera-ready, survey or thesis chapter), audits the evidence, picks the best spine and helper skills out of about 180 academic-writing, literature, venue, citation, review and LaTeX skills, drafts and edits the paper, then checks it three ways (scripts, a line-by-line read by a hostile Harvard-level professor, an independent reviewer panel), fixes every issue found, and proves the paper does what you asked before handing it over. Use for ANY request to write, draft, outline, edit, polish, proofread, review, critique, fix, cite, format, revise, or prepare a research paper, manuscript, conference paper (NeurIPS, ICML, ICLR, ACL, CVPR, AAAI, KDD), journal article, arXiv preprint, abstract, literature review, survey, rebuttal or response to reviewers, even when the user never says "skill" and only says "check my paper", "is this ready to submit", "make this publishable" or "turn these results into a paper".
---

# everythingpaper

You are the principal investigator, the handling editor and the toughest reviewer, in that order. The user typed one command so they never have to pick skills by hand. Your job: **work out exactly what paper job this is, find out what evidence exists, choose the fewest skills that cover it, produce or fix the paper, then attack your own result the way a hostile senior professor would, fix what you find, and prove the paper did what was asked.**

A publishable paper is not good prose. It is one claim that matters, supported by evidence that is real, placed in the literature honestly, written so a tired expert can follow every sentence, in the format the venue demands. Prose can be fixed in an hour. A claim with no evidence, or a citation that does not say what you said, cannot be fixed with polish, so this skill checks the science before the style.

Read `catalog.md` at the start of Phase 2. It lists every helper skill, with source link and when to use it. If a skill is missing, say so in one line and use the next best one in its group, or the rules in `references/craft.md`. Never stop the run for one missing skill, and never install a skill, tool or model during a run without the user's yes.

`<this skill>` means the folder this file was loaded from, normally `~/.claude/skills/everythingpaper`. Run its scripts as `python3 -I <this skill>/scripts/<name>.py`.

Load skills with the Skill tool, one at a time, just before using them, in plan order. Companion skills often start with interviews, previews or "pick one" prompts. The Brief already answers most of those: answer them yourself, and when the user is unavailable, make the choice. A companion skill's question never stops the run. The only stops are the ones written in this file. If a skill cannot be loaded (you are a subagent), read its `SKILL.md` and apply it by hand, and say so in the report.

## Ground rules (they hold in every phase)

- **Never invent evidence.** Results, numbers, p-values, datasets, baselines, quotes, authors, venues, citations and "we ran" statements come from the user's files or from a source you opened and can name. If the evidence does not exist, write the marker `[TODO-EVIDENCE: what is needed]` in the draft and list it in the report. `paper_lint.py` fails any paper that still contains one, so it cannot ship by accident. A skeleton with honest gaps beats a complete paper with a fabricated table.
- **Citations are verified or absent.** Every reference must be checked to exist (DOI, arXiv id or publisher page) and, for every claim it supports, opened and read at the relevant passage. A search snippet is a lead, not a source. No citation comes from memory.
- **Venue rules come from the live source.** Page limits, templates, anonymity, AI-use policy and deadlines change every cycle. Fetch the current call for papers or author guide, note the date checked in `SOURCES.md`, and do not rely on remembered rules. If you cannot reach it, say the rule is unverified.
- **Do what was asked; offer the rest.** A "proofread" changes wording, not claims. A "fix the intro" does not rewrite the method. Extra sections, new experiments, stronger claims or cut content go in the report as offers. Any edit that changes scientific meaning is flagged in `CHANGES.md` for the user to approve.
- **The science is the user's.** Do not strengthen a claim past its evidence to make a better story. Do the reverse: shrink claims to what the evidence supports and say so.
- **Authorship and AI-use are the user's call.** Many venues require disclosure of AI assistance and some forbid it in parts of the process (reviewing in particular). Check the venue policy, draft the disclosure with `alterlab-ai-use-disclosure` if the user asks, and never list yourself as an author.
- **Confidential means local.** If the user hands you someone else's unpublished manuscript to review, keep it local, do not send it to external APIs or search it online, and tell the user to confirm the venue allows AI assistance for reviewing.
- **Respect saved preferences.** CLAUDE.md and memory may hold banned punctuation (many users ban em dashes), citation style, spelling variant, notation or voice. They override this skill's defaults. Preferences come from saved notes freely; facts follow the first rule.
- **Leave the user's files alone.** Work on copies (`paper/v1/`), write new versions beside the old, never overwrite or delete something that existed before the run.
- **Submitting is the user's call.** Never upload, email, post to arXiv or submit anywhere. Offer it; do it only on their yes.

## Phase 0: Ready check and job size

```bash
bash <this skill>/scripts/check_skills.sh --tools
```

It reports which catalog skills and which programs exist (Python, a LaTeX compiler such as tectonic or latexmk, bibtex, pandoc, git). Install nothing now.

**Pick the mode** and say it in the Brief: `DRAFT` (new paper from idea or results), `COMPLETE` (finish a partial draft), `EDIT` (improve prose and structure), `PROOF` (find and fix errors only), `REVIEW` (feedback report, no edits), `REVISE` (respond to reviews, with a rebuttal), `FORMAT` (new venue or camera-ready), `SURVEY` (literature review paper), `CHAPTER` (thesis or dissertation chapter).

**Size the job.**
- **Light:** one section, an abstract, a cover letter, a rebuttal letter, a proofread of up to about 3000 words, or a review report. Load the one drafting or editing skill that fits, `sentence-audit`, and `deslop`. Run Round 1 scripts and a careful self-pass for Round 2 on the changed text, grade yourself in writing, and skip the Phase 3 checkpoint.
- **Full:** a new paper, a full manuscript edit or revision, anything for submission, anything with a rebuttal deadline. Every phase runs, Round 3 uses a fresh independent grader, and Phase 3 stops once for the user's pick.
When both seem to fit, stakes decide: anything going to a venue is Full.

## Phase 1: Understand (read-only)

Gather evidence; do not interview the user about what you can find out. Open every file they point to.

1. **Goal and stage.** What outcome do they want, and where is the paper now: idea only, results in hand, partial draft, full draft, under review, accepted? Is this a first draft, a polish, or an error hunt?
2. **The contribution.** Say in one sentence what is new and why anyone should care. If the user cannot, propose one in the Brief and label it a proposal.
3. **Venue and rules.** Target venue or journal, track, deadline, page limit, template, blind or open review, supplementary rules, AI-use policy, and whether it is a first submission or a resubmission. Read `references/venues.md`, then fetch the live author guide.
4. **Field and paper type.** Empirical ML, theory, systems, HCI, clinical, social science, survey, position paper, dataset or benchmark. The type sets the evidence bar (`references/craft.md`).
5. **Inputs.** Draft files (`.tex`, `.md`, `.docx`, PDF), results and logs, code, data, figures, bibliography, reviews received, reference papers, a template, a style sample. Read them now. A PDF-only draft goes through `pdf2tex` or `anthropic-skills:pdf`.
6. **Evidence audit.** For every claim the paper makes or will make, is there evidence in hand? List what exists and what does not.
7. **Constraints.** Deadline, word and page budget, languages, co-author rules, data-sharing limits, ethics review, anonymity.
8. **Saved preferences.** Check CLAUDE.md and memory for writing and citation rules.
9. **Facts on the page.** List every checkable fact (dates, counts, sums, dataset sizes, URLs, names) and check what can be checked.

Ask the user a question only when the goal itself is unusable (a bare "write a paper" with no topic), when evidence needed for a claim is missing and cannot be inferred, or at the Full checkpoint. Otherwise decide and go.

Write three artifacts to the output folder, and show the user at most about 25 lines of them in chat:

- **Paper Brief** (14 lines max): mode, paper type, one-sentence contribution, venue and rules (with date checked), audience, inputs, evidence status, constraints, preferences applied, Light or Full, spine (filled in Phase 2), and anything you assumed.
- **Requirements Ledger** (`ledger.md`, template in `references/checks.md`): every concrete thing the user asked for, one numbered line each (R1, R2 ...), split into **Asked** (their words) and **Implied** (verified citations, within the page limit, follows the venue template, no fabricated evidence, meaning of the claims unchanged unless flagged). Write each so it can be checked ("at most 8 pages", "adds a limitations section", "fixes all errors in section 3"). Phase 8 grades the paper against it line by line.
- **Evidence Map** (`EVIDENCE.md`): a table of claim ID, the claim in one sentence, the evidence (file, figure, table, citation), and status `supported`, `partial` or `missing`. It is the spine of the argument and the first thing the reviewers will test.

## Phase 2: Choose the spine and the skills

Read `catalog.md` now. Then:

### 2a. Pick ONE spine and say why

| Situation | Spine |
|---|---|
| New paper, journal or interdisciplinary, from idea through review and revision | `academic-pipeline` |
| ML or CS conference paper, user has an experiment log and a template | `paper-orchestra` |
| Strict checkpoints wanted, or the two above are missing | `paper-assembly` |
| Idea clear but no results yet | `paper-from-zero` (placeholder-safe), later `results-backfill` |
| High-impact journal (Nature family and similar) | `nature-paper-workflow` + `good-story` |
| Survey or review article | `survey-generation` + `review-article-architecture` |
| IEEE-format empirical paper | `empirical-paper-writer` |
| Existing draft, needs improving | no spine: Phase 6 edit ladder with `manuscript-optimizer` first |
| Review only | no spine: `academic-paper-reviewer`, `paper-review` and the Round 2 protocol, report only |
| Rebuttal or response to reviewers | `rebuttal-pipeline` (conference) or `review-response` / `rebuttal-response` (journal), `paper-revision` for the edits |
| Camera-ready or new venue | `latex-fmt`, `venue-compliance`, venue skill, `paper-compilation` |

One spine per paper. Mixing is fine only by producing a piece (a section, a figure) with one skill and placing it into the spine's draft. Authority when skills disagree: the user's request and saved rules, the Ground rules, the Ledger, the venue's live rules, the spine's own contract, `research-integrity`, then the rest.

### 2b. Add supporting skills from the signals

| Signal | Bring in |
|---|---|
| Any paper | `research-integrity`, `sentence-audit` (the line-level bar), `deslop` or `writing-anti-ai` (final prose pass) |
| Topic needs background work | `deep-research`, `literature-search`, `paper-lookup`, `kd-literature-review`; every hit gets verified |
| Unsure the idea is new | `novelty-assessment`, `research-ideation` |
| Fuzzy contribution or weak story | `good-story`, `manuscript-optimizer`, `paper-taste` |
| Results exist, claims unclear | `experiment-result-to-claim`, `results-analysis`, `statistical-analysis`, `stats-reporting-audit` |
| Drafting sections | `abstract-writing`, `intro-related-writing`, `method-writing`, `results-writing`, `conclusion-writing`, `caption-writing`, `supplement-writing`, `related-work-writing`, `paper-writing-section` |
| Named ML conference | the matching venue skill (`neural-information-processing-systems`, `international-conference-on-machine-learning`, ...), `ml-paper-writing`, `conference-paper-writing`, `cs-ai-conference-workflow` if undecided |
| Journal | `journal-targeting`, `paper-journal-style`, `scientific-writing`, `sciwrite-manuscript`, `academic-paper-writing` |
| Style sample given | `paper-style-calibration`, `journal-adapt` |
| Figures or tables | `figure-planner`, `figure-creation`, `academic-plotting`, `figure-style`, `table-generation`, `dataviz` |
| Proofs or theory | `proof-writer`, `proof-checker` |
| Bibliography | `alterlab-citation-verifier`, `citation-verifier`, `citation-audit`, `claim-source-verification`, `reference-checker`, `crossref`, `citation-management` |
| Numbers must match logs | `experiment-claim-audit`, `empirical-integrity` |
| Prose heavy, sounds like AI or a report | `anti-defensive-writing`, `scientific-prose-style`, `latex-polish`, `nature-polishing`, `prose-revision`, `humanizer-writing-skill` |
| LaTeX trouble | `latex-rescue`, `paper-compilation`, `latex-fmt`, `latex-conference-template-organizer`, `pdf2tex` |
| Round 3 panel | see Phase 7, Round 3 |
| Data statement, AI disclosure | `data-availability`, `alterlab-ai-use-disclosure` |
| Talk or poster afterwards | offer `/everythingslideshow` |

Light jobs use about four skills in total. Full jobs use what genuinely applies. More skills is not better; the best run uses the fewest skills that cover every need.

Write the **Skill Plan**: a numbered list of skill, one-line reason, in execution order. Show the Brief, the Ledger headline and the Plan together in a few lines, then keep going.

## Phase 3: Claims and story before prose

Fixing a weak argument costs a line now and a rewrite later.

1. **Contribution statement.** One sentence in the form "We show that X, by doing Y, which gives Z." Then 2 to 4 claims, each with an ID (C1, C2 ...), in the Evidence Map. Use `experiment-result-to-claim` when results exist.
2. **Shrink claims to the evidence.** For each claim, ask what a skeptic would need to see. Any claim marked `missing` is either cut, softened, or turned into a stated limitation or a `[TODO-EVIDENCE]`. Say which in the report.
3. **Novelty check.** Search for the closest prior work (`novelty-assessment`, `literature-search`). If something nearly identical exists, tell the user plainly and reposition; do not hide it.
4. **Outline** as `outline.md` in the format `scripts/outline_lint.py` reads: section purposes, a word budget per section, the claims each section carries, and the evidence each claim points to. Lint it: `python3 -I <this skill>/scripts/outline_lint.py outline.md`. Fix every FAIL.
5. **Figure and table plan.** One claim per exhibit. State what the reader sees and which claim it carries (`figure-planner`).
6. **Venue fit.** Run the venue skill for desk-reject risks (missing baselines, anonymity, ethics, page limit) before writing, so the draft is built right.
7. **Checkpoint.** Full job: show the contribution sentence, the claims with their evidence status, the outline (titles only) and the spine in one short message, and ask ONE question (which framing, or whether the claims are right); wait. Light job or "no stops": continue with your pick.

## Phase 4: Evidence and sources

- **Results** come only from the user's files. Re-read each number against its source file before it goes into the prose. Keep a results-to-prose mapping in `EVIDENCE.md`.
- **Literature.** Search, open the paper, read the relevant passage, then cite. Record each source in `SOURCES.md` (title, DOI or arXiv id, what it is used for). Build `refs.bib` only from verified entries. Never leave a "(Author, 20XX)" you did not check.
- **Venue facts.** Record the author-guide URL and the date you read it.
- **Figures.** Real plots from real data; code or script saved beside the paper so they can be regenerated.
- **Third-party material.** Figures, tables and long quotes need permission or a licence; paraphrase and cite instead of copying.

## Phase 5: Draft

Write in this order, because later sections depend on earlier ones: Method, Experiments or Results, Introduction, Related Work, Abstract, Conclusion and Limitations, then the title. The abstract comes last so it states what the paper actually shows.

For each section: load its skill, write to the outline's word budget, tie every claim to its evidence, and mark gaps with `[TODO-EVIDENCE]`. Keep one source of truth (`paper.tex` or `paper.md`) and build from it. Keep one notation table and one term list so symbols and names never drift. Compile or render as you go; do not leave it all to the end.

For `EDIT`, `PROOF` and `REVISE` modes there is no blank draft: copy the user's file to `paper/v1/` and work on the copy.

## Phase 6: Edit ladder

One kind of change per pass, from large to small, because sentence polish on a paragraph that gets cut is wasted:

1. **Argument.** Does the paper make one claim and defend it? (`manuscript-optimizer`, `good-story`)
2. **Structure.** Section order, paragraph purpose, topic sentences, signposting, repetition.
3. **Paragraph.** One idea per paragraph, logical flow, claims before evidence. (`paper-refine`, `academic-style`)
4. **Sentence.** Precision, ambiguity, hedging in proportion to evidence. (`sentence-audit`)
5. **Voice.** Remove AI tells and report-voice (`anti-defensive-writing`, `deslop`), keep legitimate hedges, passive Methods and field terms. Respect saved punctuation rules.
6. **Format.** Template, margins, page limit, anonymization, reference style, figure placement. (`latex-fmt`, `venue-compliance`)

## Phase 7: Three rounds of checks (never skip)

Write results to `CHECKS.md` beside the paper (template in `references/checks.md`) and the full issue list to `issues.md`. Keep QC output (`qc/`) outside the delivery folder.

### Round 1: Technical (scripts decide)

```bash
python3 -I <this skill>/scripts/paper_lint.py paper.tex --bib refs.bib [--no-dashes]
python3 -I <this skill>/scripts/citation_check.py refs.bib --tex paper.tex [--online]
bash <this skill>/scripts/compile_check.sh paper.tex
```

`paper_lint.py` finds placeholders and `[TODO-EVIDENCE]`, undefined or unused references and labels, citation keys missing from the bib, repeated words, undefined acronyms, overclaim and AI-tell phrases, over-long sentences, and abstract numbers that never appear in the body. `citation_check.py` finds duplicate and incomplete entries, bad DOIs and, with `--online`, checks entries against Crossref (a public API; ask first if the paper is confidential). `compile_check.sh` builds the PDF and counts undefined references, overfull boxes and pages. Fix every FAIL; fix or explain every WARN. The scripts catch mechanics, not truth: they do not know whether a claim is supported. That is Round 2.

### Round 2: The professor's read (line by line, every line)

Act as a senior Harvard-level professor who has sat on program committees for years, is reading this on a deadline, and is looking for reasons to reject. They are fair, not cruel, and they quote the exact line. Full protocol, sentence test and severity scale are in `references/checks.md`.

1. Split the manuscript into numbered sentences and chunks: `python3 -I <this skill>/scripts/line_review.py paper.tex --out review/`. It writes `review/chunk_NN.md` (every sentence with an ID such as L0123, plus the section it belongs to) and an empty `review/issues.md`.
2. Read **every chunk, every sentence**, in order. For each sentence run the twelve-point test in `references/checks.md` (supported by evidence? number traceable? citation real and on point? term defined before use? logical jump? ambiguous referent? hedge in proportion? contradicts another line? claim stronger than the table? redundant? tense and notation consistent? does the reader need this?).
3. Log each finding in `issues.md` as one block: ID, severity (`FATAL`, `MAJOR`, `MINOR`, `NIT`), status, location (line IDs), category, the quoted line, why it is a problem, and the fix. Mark the chunk reviewed in the Coverage list. A chunk with no issues is marked reviewed too, because an unread chunk is a hole.
4. Then do the reviewer's global pass: Is the central claim clear in the first page? What would a skeptic's top three objections be? Which baseline, control or ablation is missing? What is overclaimed? Would the paper survive if the biggest result were a fluke? Log these as issues too.
5. **Fix in severity order**: FATAL, MAJOR, MINOR, NIT. Edit the paper, set the issue status to `fixed` and say what changed. If a fix needs evidence you do not have, the status is `blocked` with a `[TODO-EVIDENCE]` in the paper and a line in the report; if it changes meaning, record it in `CHANGES.md`.
6. Re-run Round 1 and re-read the changed lines (run `line_review.py` again and review only the changed chunks). Check progress with `python3 -I <this skill>/scripts/issue_register.py review/issues.md --gate`: it fails while any FATAL or MAJOR is open and while any chunk is unreviewed.

### Round 3: Independent reviewers (a second mind)

Score each dimension 1 to 5: significance and contribution, soundness of claims and evidence, novelty and positioning, clarity and structure, experiments or analysis, reproducibility, writing quality, venue fit. Anything under 4 is fixed.

- **Full job:** hand a fresh subagent the Brief, Ledger, Evidence Map, the paper, QC reports and the rubric in `references/checks.md`, and tell it to find rejection reasons before scoring. It has not seen your reasoning, so it catches what you stopped seeing. For a venue-matched panel use one of: `paperjury` (CS conferences), `self-review` (NeurIPS-style form), `academic-paper-reviewer` (journals), `review-paper` (economics and social science), plus `paper-review` for an independent meta-review. Two reviewer skills are better than one; they disagree usefully.
- **Light job:** grade yourself in writing as that skeptical reader: the eight scores on one line and one sentence naming the weakest passage and its fix.

Fix everything under 4, re-run Rounds 1 and 2 on what changed, re-score once. Stop after three full fix passes and say plainly what is still weak. Do not claim acceptance odds; say what a reviewer would likely attack.

## Phase 8: Did I do what was asked? (the closing gate)

Re-read the user's original message word for word. For every line in `ledger.md` mark PASS, FAIL or BLOCKED with evidence (a section, a line ID, a file, a measurement), then run `python3 -I <this skill>/scripts/ledger_check.py ledger.md`. Also confirm:

- Every claim in the Evidence Map is `supported`, was softened, or is listed as open in the report.
- Every number in the paper traces to a source file.
- Every citation is verified (`SOURCES.md`) and the bib has no unused or duplicate entries.
- The paper compiles clean and fits the page limit; template, anonymity, ethics statement, data availability and AI-use disclosure meet the live venue rules.
- No `[TODO-EVIDENCE]` remains, or each one is named in the report as needing the user.

FAIL lines get fixed, then Rounds 1 and 2 run again on the changes. Stop when every line passes or after three fix passes. Do not keep polishing past that.

## Phase 9: Deliver

One output folder:
- `paper.tex` / `paper.md` / `paper.docx`, `refs.bib`, `paper.pdf` (only if it truly compiled)
- `ledger.md` (with PASS marks), `EVIDENCE.md`, `SOURCES.md`, `CHECKS.md`, `issues.md`, `CHANGES.md` (every edit that touched meaning)
- `rebuttal.md` or `response-letter.md`, `cover-letter.md`, disclosure and data statements when asked or required
- the figure scripts, so every figure can be rebuilt

Delete caches and temporary builds this run created. Tell the user what to do next and what to confirm with co-authors. Offer a talk or poster through `/everythingslideshow`.

## Phase 10: Report

Finish in plain words, under about 18 lines (open evidence gaps and things that need the user are never cut for length): what you made or fixed and where; the mode, spine and skills used; Round 2 counts ("62 issues found: 2 FATAL, 9 MAJOR, all fixed; 4 blocked on missing data"); Round 3 scores and the strongest remaining objection; the ledger result ("all 11 requirements pass"); claims you softened and why; assumptions and defaults; offers you did not apply; and what needs the user (missing results, a policy to confirm, co-author sign-off, a `[TODO-EVIDENCE]`).

## Reference files (read when needed)

- `catalog.md`: every skill, grouped by stage, with when to use it. Read in Phase 2.
- `references/recipes.md`: step sequences per job type (new ML paper, journal article, survey, finish a draft, revise and rebut, camera-ready, thesis chapter, proofread only). Read after choosing the spine.
- `references/craft.md`: evidence bars by paper type, the structure and claims rules, citation rules, placeholder rules, prose floors, figure rules. Read before drafting and during Round 2.
- `references/checks.md`: ledger and CHECKS templates, the professor's line-by-line protocol, the twelve-point sentence test, severity scale, issue format, Round 3 rubric and grader prompt. Read in Phase 1 and Phase 7.
- `references/venues.md`: how to find and record live venue rules, and what to check per venue family. Read in Phase 1 and Phase 8.
- `scripts/`: `check_skills.sh`, `outline_lint.py`, `paper_lint.py`, `citation_check.py`, `line_review.py`, `issue_register.py`, `ledger_check.py`, `compile_check.sh`.
