# everythingpaper

**One command for research papers, start to finish.** A Claude Code skill that acts as principal investigator, editor and the harshest reviewer you will ever meet. It works out what paper job you have, checks the evidence, picks the best skills for the job from a catalog of about 180, drafts or fixes the paper, then reads it **sentence by sentence like a hostile senior professor**, fixes what it finds, and proves the paper does what you asked before handing it over.

```
/everythingpaper turn these results into a NeurIPS paper
/everythingpaper check my paper before I submit
/everythingpaper write the rebuttal for these three reviews
/everythingpaper proofread my abstract
/everythingpaper make this publishable
```

Built the same way as [`/everythingvideo`, `/everythingslideshow` and `/fulldesign`](#how-it-was-built): a director skill that understands the request, audits what exists, chooses skills from a catalog, executes in order, checks three ways, and closes with a gate against a written contract.

## Why it is different

Most "write my paper" prompts produce fluent text that falls apart under review: claims with no evidence, citations that do not exist, numbers that disagree with the table. everythingpaper is built around those failures.

- **It never invents evidence.** Missing results become `[TODO-EVIDENCE: ...]` markers, and the linter fails any paper that still has one. A skeleton with honest gaps beats a finished-looking paper with a made-up table.
- **Claims come before prose.** A claim list with an Evidence Map (claim, evidence, status) is built first. Claims are shrunk to what the data supports.
- **Citations are verified or absent.** Every reference is checked to exist and read where it is used; `citation_check.py --online` confirms DOIs and titles against Crossref and arXiv and flags retractions.
- **The professor's read covers every sentence.** `line_review.py` numbers every sentence and splits the paper into chunks; each is read against a twelve-point test and logged in `issues.md` with severity and the quoted line. A gate refuses to pass while any chunk is unread or any FATAL or MAJOR issue is open.
- **An independent panel judges it.** A fresh subagent that never saw the writing process scores eight dimensions and lists the objections a reviewer would raise, using venue-matched reviewer skills.
- **A closing gate checks your request.** Every thing you asked for is a numbered ledger line that must be marked PASS with evidence.
- **Live venue rules.** Page limits, templates, anonymity and AI-use policy are fetched from the venue, with the date recorded, never remembered.

## The process

| Phase | What happens |
|---|---|
| 0 Ready check | Which helper skills and tools exist; mode (DRAFT, COMPLETE, EDIT, PROOF, REVIEW, REVISE, FORMAT, SURVEY, CHAPTER); Light or Full job |
| 1 Understand | Goal, contribution, venue and live rules, inputs, evidence audit. Writes the **Paper Brief**, the **Requirements Ledger**, the **Evidence Map** |
| 2 Choose | One spine (for example `academic-pipeline` or `paper-orchestra`) plus the fewest supporting skills that cover the job |
| 3 Claims and story | One central claim, 2 to 4 supporting claims, outline linted by `outline_lint.py`, figure plan, one checkpoint with you |
| 4 Evidence and sources | Numbers from your files, citations verified, venue facts recorded |
| 5 Draft | Method, results, intro, related work, abstract last |
| 6 Edit ladder | Argument, structure, paragraph, sentence, voice, format, one kind of change per pass |
| 7 Three check rounds | **Round 1** scripts. **Round 2** the professor's line-by-line read and fix. **Round 3** independent reviewer panel and scores |
| 8 Closing gate | Ledger PASS or FAIL against your original words; claims, numbers, citations, build and venue rules confirmed |
| 9 Deliver | Paper, bib, ledger, evidence map, sources, checks, issues, changes |
| 10 Report | Plain words: what was made, what was found, what needs you |

## Install

```bash
git clone https://github.com/aaryavvatts-lab/everythingpaper.git
bash everythingpaper/install.sh
```

Then start a new Claude Code session and type `/everythingpaper`. Add `--dry-run` to preview, `--target DIR` to install elsewhere, `--companions` to print how to get the helper skills.

Requirements: Python 3 for the checkers. A LaTeX engine ([tectonic](https://tectonic-typesetting.github.io/), latexmk or pdflatex) lets it verify builds; without one it says so and never claims a clean build.

### Helper skills

The director works on its own using `references/craft.md` and `references/checks.md`, and gets stronger with the specialist skills it routes to. `catalog.md` lists every one with its source repository and when to use it. These repositories hold most of them (read a skill before installing it; skills run with your permissions):

[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) ·
[Alexyskoutnev/research-skills](https://github.com/Alexyskoutnev/research-skills) ·
[Ar9av/PaperOrchestra](https://github.com/Ar9av/PaperOrchestra) ·
[boom5426/nature-paper-skills](https://github.com/boom5426/nature-paper-skills) ·
[Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) ·
[lingzhi227/agent-research-skills](https://github.com/lingzhi227/agent-research-skills) ·
[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) ·
[Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) ·
[AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) ·
[franklee16/academic-research-skills](https://github.com/franklee16/academic-research-skills) ·
[Calix-L/awesome-latex-skills](https://github.com/Calix-L/awesome-latex-skills) ·
[mronkko/claude-academic-research](https://github.com/mronkko/claude-academic-research) ·
[claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) ·
[Spark-To-Paper-Skills/paperjury](https://github.com/Spark-To-Paper-Skills/paperjury)

Check what you have: `bash ~/.claude/skills/everythingpaper/scripts/check_skills.sh --tools`.

## The tools

All plain Python 3 or bash, standard library only. Run them on their own any time.

| Script | What it does |
|---|---|
| `scripts/outline_lint.py` | Checks an outline before drafting: central claim, claims with evidence, sections with purposes, word budget against the page limit |
| `scripts/paper_lint.py` | Placeholders and `[TODO-EVIDENCE]`, undefined or unused refs and labels, cited keys missing from the bib, repeated words, undefined acronyms, overclaim and AI-tell phrases, unsupported "significant", long sentences, abstract numbers missing from the body, banned dashes |
| `scripts/citation_check.py` | Duplicate or incomplete BibTeX, bad DOIs; with `--online`, existence against Crossref and arXiv, title mismatch, retractions, DOI suggestions |
| `scripts/line_review.py` | Numbers every sentence (`L0001`), writes review chunks and an `issues.md` coverage list, re-run flags only the chunks that changed |
| `scripts/issue_register.py` | Summarises `issues.md` and gates on open FATAL or MAJOR issues and unread chunks |
| `scripts/ledger_check.py` | Grades the Requirements Ledger |
| `scripts/compile_check.sh` | Builds the LaTeX in a scratch folder; undefined references, overfull boxes, page count, page limit |
| `scripts/check_skills.sh` | Which catalog skills and programs are present |

Run the regression tests with `bash tests/run_tests.sh`.

## Honest limits

- It cannot make a weak idea strong, and it will say so rather than polish it.
- It cannot run your experiments. If evidence does not exist, the paper stays marked until it does.
- The scripts check mechanics, not truth. Whether a claim is supported is the job of the Round 2 read and the Round 3 panel, and a person (you and your co-authors) still decides.
- Venue and AI-use policies are your responsibility to confirm; the skill fetches and records them but cannot guarantee a page is current.
- No tool can promise acceptance.

## How it was built

Following the pattern of the other director skills: inventory the best public skills, read and vet them, write a catalog of what each is for and when to use it, write a director `SKILL.md` that audits, routes, executes and checks, add deterministic scripts for what a model should not eyeball, and test against seeded failures (`tests/sample/`) until the scripts catch them. The `evals/` folder holds sample requests and what a good run must show.

## Credits

The helper skills belong to their authors, linked in `catalog.md`. This repository is MIT licensed and only holds the director, catalog, references and checkers.
