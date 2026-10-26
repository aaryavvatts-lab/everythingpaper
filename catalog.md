# everythingpaper catalog

About 180 helper skills that `/everythingpaper` can bring in, grouped by the stage of a paper's life. Each row: the skill, what it does, and when to use it. Skill names are the folder names under `~/.claude/skills/`. Plugin skills (`ecc:`, `anthropic-skills:`) come from plugins, not that folder.

Run `bash scripts/check_skills.sh` to see which of these are installed. A missing skill is never a reason to stop: use the next best one in its group, or the plain rules in `references/craft.md`.

Source repositories (all public): `AR` [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) · `RS` [Alexyskoutnev/research-skills](https://github.com/Alexyskoutnev/research-skills) · `PO` [Ar9av/PaperOrchestra](https://github.com/Ar9av/PaperOrchestra) · `NP` [boom5426/nature-paper-skills](https://github.com/boom5426/nature-paper-skills) · `CS` [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) · `LZ` [lingzhi227/agent-research-skills](https://github.com/lingzhi227/agent-research-skills) · `KD` [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) · `OR` [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) · `AL` [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) · `FL` [franklee16/academic-research-skills](https://github.com/franklee16/academic-research-skills) · `CX` codex-paper-skills (inside FL) · `LX` [Calix-L/awesome-latex-skills](https://github.com/Calix-L/awesome-latex-skills) · `AG` [onireimu/ageaf](https://github.com/onireimu/ageaf) · `MK` [mronkko/claude-academic-research](https://github.com/mronkko/claude-academic-research) · `CB` [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) · `DV` [dvdsosa/scientific-writing-skills](https://github.com/dvdsosa/scientific-writing-skills) · `WY` [wenyuchiou/academic-writing-skills](https://github.com/wenyuchiou/academic-writing-skills) · `GT` [Gavin-Tao/claude-skills](https://github.com/Gavin-Tao/claude-skills) · `AH` [agustinohalim/academic-writing-skills](https://github.com/agustinohalim/academic-writing-skills) · `YL` [yunshenwuchuxun/latex-paper-skills](https://github.com/yunshenwuchuxun/latex-paper-skills) · `AW` [AlexWortega/ai-peer-review-skill](https://github.com/AlexWortega/ai-peer-review-skill) · `SP` [Spark-To-Paper-Skills/paperjury](https://github.com/Spark-To-Paper-Skills/paperjury) · `SNL` [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) · `ST` [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) · `SY` [shaowen-ye/manuscript-review-skill](https://github.com/shaowen-ye/manuscript-review-skill) · `LB` [labarba/sciwrite](https://github.com/labarba/sciwrite) · `JK` [jingkarqi/writing-in-the-sciences-skill](https://github.com/jingkarqi/writing-in-the-sciences-skill) · `FU` [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) · `AND` [andrehuang/academic-writing-agents](https://github.com/andrehuang/academic-writing-agents)

## 1. Whole-paper pipelines (pick ONE spine per job; see SKILL.md Phase 2a)

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `academic-pipeline` | AR | 10-stage orchestrator: research, write, integrity check, review, revise, re-review, finalize, with user confirmation at each stage. | Default spine for a journal-style or interdisciplinary paper from scratch, or a draft that needs the full loop. |
| `paper-orchestra` | PO | Five-agent pipeline (outline, plots, literature, sections, refinement) that turns an idea and an experiment log into a LaTeX draft. | ML/CS conference paper when the user has results (an experiment log) and a template. Its sub-agents: `outline-agent`, `plotting-agent`, `literature-review-agent`, `section-writing-agent`, `content-refinement-agent`, `paper-autoraters`. |
| `paper-assembly` | LZ | Nine checkpointed phases from literature to compiled paper, with state carried between phases. | Alternative spine when the user wants strict checkpoints, or `paper-orchestra` is unavailable. |
| `paper-from-zero` | YL | Builds a paper from a research contract with placeholder-safe results. | The idea is clear but results do not exist yet; draft the skeleton honestly. |
| `empirical-paper-writer` | YL | IEEE-style empirical ML/AI paper from a structured research contract, no fabricated evidence. | Empirical IEEE-format paper. |
| `arxiv-paper-writer` | YL | Review or survey paper for arXiv in IEEEtran with verified BibTeX. | Survey or review for arXiv. |
| `nature-paper-workflow` | NP | Nature-style workflow: claim hierarchy, evidence chain, figures, submission audit. | High-impact journal paper (Nature family and similar). |
| `paper-workflow` | NP | General paper project workflow with source-of-truth files. | A long-running manuscript project that spans many sessions. |
| `write-scientific-manuscript` | NP | Full manuscript writing procedure. | Journal manuscript drafting when no other spine fits. |
| `scientific-article-writing` | AH | Gated workflow from research question to submission and revision with an AI assistant. | Journal article with integrity gates. |
| `survey-generation` | LZ | Builds a survey paper with retrieval-backed subsections and citation validation. | The paper is a literature survey. |
| `review-article-architecture` | NP | Structure for review, survey and perspective pieces. | Review or perspective, not an empirical article. |
| `research-paper-writing` | GT | Section structure, paragraph flow and reviewer-facing presentation for ML/CV/NLP papers. | Quick overall quality lift on an ML paper. |
| `academic-paper-writing` | GT | Style rules for journal papers (Elsevier, IEEE, ACM) plus cover letters, response letters and reference checks. | Journal paper in any field with submission artefacts. |
| `academic-writing-skills` | WY | Plan, draft, review, revise and proofread manuscripts; claim-to-evidence checks, overclaim detection, readiness checklist. | Any manuscript needing integrity-focused editing. |
| `paper-writing` | SNL | Editorial principles and voice for systems-style papers. | CS systems papers; strong on structure. |
| `academic` | AND | Orchestrator of specialist writing agents for `.tex` projects. | LaTeX project needing parallel review, polish and bibliography audit. |

## 2. Ideas, novelty and literature

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `deep-research` | AR | 13-agent research team with literature-review, systematic-review, fact-check and Socratic modes. | The topic needs real background work before writing. |
| `literature-search` | LZ | Semantic Scholar, arXiv and OpenAlex search returning structured results. | Finding candidate papers; every hit still needs verification. |
| `paper-lookup` | KD | Searches 18 scholarly APIs (PubMed, arXiv, OpenAlex, Crossref and more). | Look up a specific paper or a metadata record. |
| `research-lookup` | KD | Compiles current scholarly evidence for a manuscript question. | Needs fresh evidence with sources. Uses an external API key if configured. |
| `literature-review` | LZ | Multi-perspective literature review. | Drafting a related-work map. |
| `kd-literature-review` | KD | Systematic, scoping and narrative reviews with database search. | Formal literature review section or paper. |
| `related-work-writing` | LZ | Related Work organised by theme, compare and contrast. | Writing the related-work section. |
| `novelty-assessment` | LZ | Multi-round search to judge whether an idea is new. | Before committing to a claim of novelty. |
| `research-ideation` | CS | 5W1H brainstorming and gap finding. | The user has a topic but no contribution yet. |
| `idea-refine` | | Divergent then convergent thinking on a raw idea. | Fuzzy idea, no clear question. |
| `sr-screener` | AR | Protocol-driven screening for systematic and scoping reviews. | Systematic review with a protocol. |
| `ecc:scientific-thinking-literature-review` | plugin | Literature-review method guidance. | Backup for the literature steps. |
| `ecc:scientific-db-pubmed-database` | plugin | PubMed querying. | Biomedical literature. |
| `ecc:exa-search` | plugin | Web and research search. | Needs fresh web sources. |

## 3. Venue, template and fit

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `cs-ai-conference-workflow` | FL | Router that picks the right CS/AI conference skill. | Venue undecided for a CS/AI paper. |
| `neural-information-processing-systems`, `international-conference-on-machine-learning`, `international-conference-on-learning-representations`, `aaai-conference-on-artificial-intelligence`, `international-joint-conference-on-artificial-intelligence`, `artificial-intelligence-and-statistics`, `conference-on-learning-theory` | FL | Venue fit, framing, evidence bar, desk-reject risks, rebuttal posture. | Target is that AI/ML venue. They tell you to check the live call for papers; do that. |
| `computer-vision-and-pattern-recognition`, `international-conference-on-computer-vision`, `european-conference-on-computer-vision` | FL | Same, for vision. | Vision venue. |
| `annual-meeting-of-the-association-for-computational-linguistics`, `conference-on-empirical-methods-in-natural-language-processing`, `north-american-chapter-of-the-association-for-computational-linguistics` | FL | Same, for NLP. | NLP venue. |
| `acm-sigkdd-conference-on-knowledge-discovery-and-data-mining`, `the-web-conference`, `acm-sigir-conference-on-research-and-development-in-information-retrieval`, `international-conference-on-very-large-data-bases`, `acm-sigmod-international-conference-on-management-of-data` | FL | Same, for data mining, web, IR and databases. | Those venues. |
| `international-conference-on-software-engineering`, `usenix-security-symposium`, `ieee-symposium-on-security-and-privacy`, `conference-on-robot-learning`, `robotics-science-and-systems`, `acm-chi-conference-on-human-factors-in-computing-systems` | FL | Same, for SE, security, robotics and HCI. | Those venues. |
| `ml-paper-writing` | AG | NeurIPS, ICML, ICLR, ACL, AAAI, COLM writing guide with LaTeX templates and citation workflow. | ML conference paper. Also installed as `cs-ml-paper-writing` and `or-ml-paper-writing` (other authors, same idea). |
| `conference-paper-writing` | NP | Conference-first workflow with templates. | ML/AI conference when the journal style does not fit. |
| `systems-paper-writing` | OR | OSDI, SOSP, ASPLOS, NSDI, EuroSys guide. | Systems venue. |
| `venue-templates` | KD | Journal, conference, poster and grant templates. | Needs the venue's formatting rules. |
| `venue-compliance` | AG | Checks a paper against venue rules. | Pre-submission format check. |
| `latex-fmt` | LX | Reformat LaTeX for a venue, year, track and submission stage. | Switching template or preparing camera-ready. |
| `latex-formatting` | LZ | Conference templates (ICML, ICLR, NeurIPS, AAAI, ACL) and pre-submission checks. | Setting up a conference template. |
| `latex-conference-template-organizer` | CS | Cleans a messy template zip into an Overleaf-ready tree. | The user pasted a template zip. |
| `journal-targeting` | AH | Picks a target journal ladder (Scopus, Web of Science). | Journal undecided. |
| `journal-adapt` | WT | Adapts writing to a target journal's own papers. | User supplies sample papers from the journal. |
| `paper-journal-style` | CX | Checks a draft against target-journal style. | Journal named. |
| `nature-portfolio-playbook` | NP | Chooses among Nature, Nature Methods, Nature Biotechnology. | Life-science high-impact target. |

## 4. Planning, story and claims

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `good-story` | FL | Finds and sharpens the story and significance of a result. | The paper has results but no clear "why it matters". |
| `nature-story` | FL | Turns early research into an evidence-grounded story. | Early-stage idea heading to a high-impact journal. |
| `manuscript-optimizer` | NP | Audits and restructures the question, claim hierarchy, evidence chain and section logic. | Draft exists but the argument wanders. |
| `paper-plan` | CX | Structured outline from results. | Making the outline after experiments. |
| `experiment-result-to-claim` | CX | Judges what claims results support and what is missing. | Right after experiments finish, before writing. |
| `results-analysis` | NP | Validates comparisons and turns results into paper-ready text. | Analysing experimental results. Also `cs-results-analysis` (strict stats bundle). |
| `statistical-analysis` | KD | Test selection, assumptions, effect sizes, power. | The analysis plan or reporting is weak. |
| `figure-planner` | NP | One claim per figure, panel roles, main vs supplement. | Planning figures. |
| `paper-taste` | FL | Judges research taste and contribution level. | Honest check of how strong the contribution is. |
| `scientific-critical-thinking` | KD | Evaluates design validity, bias, confounds and evidence quality. | Stress-testing the science itself. |
| `research-integrity` | AH | No numbers without source, no citations from memory. | Always on for AI-assisted writing. |
| `draft-marker-discipline` | NP | Tracks open questions with in-source markers. | Drafting across many sessions. |

## 5. Drafting by section

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `abstract-writing` | RS | Three recipes and a mechanical checklist for abstracts. | Writing or fixing the abstract (write it last). |
| `intro-related-writing` | RS | Seven-question funnel for the Introduction and credit-then-contrast related work. | Introduction and related work. |
| `method-writing` | RS | Method section recipes. | Method section. |
| `results-writing` | RS | Experimental results recipes. | Results section. |
| `conclusion-writing` | RS | Three-paragraph conclusion shape. | Conclusion. |
| `caption-writing` | RS | Self-contained figure, table and algorithm captions. | Any caption. |
| `supplement-writing` | RS | Appendix method distilled from strong appendices. | Supplement or appendix. |
| `paper-writing-section` | LZ | One section at a time with two-pass refinement. | Generic section drafting. |
| `section-writing-agent` | PO | Drafts the remaining sections in one multimodal call. | Inside the `paper-orchestra` spine. |
| `paper-write` | CX | Section-by-section drafting from a paper plan. | Plan exists, drafting now. |
| `stat-writing` | FU | End-to-end statistical writing for LaTeX. | Statistics papers. |
| `nature-writing` | CS | Drafts Nature-style sections from claims and figures. | Nature-family. |
| `scientific-writing` | NP | Full-paragraph prose for manuscripts (also `kd-scientific-writing`). | Journal prose. |
| `sciwrite-manuscript`, `sciwrite-prose`, `sciwrite-process`, `sciwrite-publish` | DV | Manuscript, prose, process and publishing guidance. | Extra craft for journal writing. |
| `writing-in-the-sciences` | JK | Stanford "Writing in the Sciences" workflow. | Clear scientific prose and editing method. |
| `academic-style` | MK | Topic sentences, paragraph structure, hedging, tense. | Prose-level drafting. |
| `academic-paper` | AR | 12-agent drafting pipeline with 11 modes (plan, outline, abstract, lit-review, citation-check, format-convert, disclosure). | Drafting or revising with its modes. |
| `paper-style-calibration` | CX | Matches the user's own prior papers or reference papers. | User supplies samples of their style. |
| `results-backfill` | YL | Fills placeholder results once real results exist. | Skeleton drafted earlier. |
| `table-generation` | LZ | Booktabs LaTeX tables from data. | Results tables. |
| `proof-writer`, `proof-checker` | CX | Write and verify mathematical proofs. | Theory papers. |

## 6. Figures and tables

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `figure-creation` | RS | Design and export decisions for ML-venue figures. | Any new figure. |
| `academic-plotting` | OR | Publication figures for ML papers (matplotlib/seaborn, diagrams). | Plots from experiment data. |
| `figure-generation` | LZ | Three-phase plotting with visual feedback. | Many plots. |
| `figure-style` | NP | Legibility and correctness rules for figures that ship. | Final figure pass. |
| `nature-figure` | NP | Submission-grade figures for Nature-family and similar. | High-impact journals. |
| `publication-chart-skill` | CS | Publication-quality charts and tables. | Charts. |
| `paper-figure`, `paper-figures-advise` | CX | Figures from results, chart-type advice. | Choosing chart types and making figures from results. |
| `scientific-schematics` | KD | AI-drafted scientific diagrams. | Conceptual diagrams; needs an API key. |
| `plotting-agent` | PO | Plots inside `paper-orchestra`. | That spine. |
| `dataviz` | plugin | Chart design rules (color, axes, accessibility). | Any chart. |

## 7. Editing and polishing prose

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `sentence-audit` | RS | Sentence-by-sentence precision pass against a first-time-reader defect list. | Core of the line-by-line review. |
| `paper-refine` | CX | Paragraph-level refinement. | Paragraph polish. |
| `paper-polish-workflow` | CX | Checkpointed interactive polishing. | User wants control over each change. |
| `latex-polish` | LX | Edits LaTeX prose at light, moderate or strict intensity. | Prose polish inside `.tex`. |
| `latex-rhythm-refiner` | YL | Sentence rhythm in LaTeX. | Readability. |
| `prose-revision` | FL | Finds the best structure for ideas the user already has. | Muddled passages. |
| `nature-polishing` | CS | Concise, Nature-leaning English. | High-impact journals, non-native writers. |
| `anti-defensive-writing` | NP | Removes audit-voice, self-critique and README tone from manuscripts. | Draft sounds timid or like a report. |
| `scientific-prose-style` | NP | Prose rules for abstract, intro, results, discussion. | Style pass. |
| `results-section-revision` | NP | Revises Results flow when figures and claims are fixed. | Results read badly. |
| `writing-anti-ai`, `deslop`, `no-ai-slop`, `humanizer-writing-skill` | CS, ST | Remove AI-sounding patterns. | Last prose pass; keep scientific hedging and passive Methods. |
| `manuscript-revision`, `critic-loop` | MK | Parallel critics until no major issue remains. | Revising a finished draft. |
| `paper-revision` | LZ | Applies reviewer feedback section by section. | Revising after review. |
| `science-editor` | | Copy-editing for scientific text. | General edit. |

## 8. Citations, references and integrity

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `alterlab-citation-verifier` | AL | Checks each bibliography entry exists via Crossref, OpenAlex, Semantic Scholar, arXiv; flags retractions. | Every bibliography before submission. |
| `citation-verifier` | NP | DOI, PMID, placeholder and BibTeX hygiene. | Bibliography cleanup. |
| `claim-source-verification` | NP | Checks each claim against its cited source. | Does the source say what we claim? |
| `citation-audit` | CX | Zero-context audit of every reference, including wrong-context citations. | Pre-submission integrity. |
| `experiment-claim-audit` | CX | Every number and scope claim matches raw result files. | Before submission. |
| `reference-checker`, `reference-audit-guide` | FL, NP | Exhaustive reference verification. | Reference lists. |
| `crossref` | FL | Matches pasted references to Crossref and returns DOIs. | A raw reference list. |
| `citation-management` | AG | Search, metadata and BibTeX. Also `kd-citation-management`, `lz-citation-management` (harvests missing citations). | Building or repairing `.bib`. |
| `citation-verification` | CS | Guidance on preventing fake citations. | Reference reading. |
| `empirical-integrity` | MK | Every number comes from a pipeline file. | Numbers in prose. |
| `stats-reporting-audit` | NP | Audits statistical reporting. | Stats in results. |
| `data-availability` | NP | Data Availability statements and repository plans. | Journals that require them. |
| `alterlab-ai-use-disclosure` | AL | AI-use disclosure statements by venue policy. | Any submission; check the venue's AI rules. |
| `alterlab-research-workflows` | AL | Packaged multi-agent audits and panels. | Citation audit or claim stress-test at scale. |

## 9. Review, grading and finding mistakes

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `academic-paper-reviewer` | AR | 5-seat role-separated panel (journal fit, methods, domain, devil's advocate). | Round 3 panel, journals. |
| `paperjury` | SP | Review for CS conferences (CVPR, ACL, NeurIPS families); direct-edit mode. | Round 3 panel, CS venues. |
| `self-review` | LZ | NeurIPS-form review with three personas. | Round 3 for ML papers. |
| `paper-self-review` | CS | Audits structure, logic, claims, citations, compliance. | Quick self-audit. |
| `review-paper` | CB | 8-agent referee report for a target journal. | Round 3 for economics and social science. |
| `review-paper-checks`, `review-paper-light` | CB | Fast mechanical checks; contribution and identification. | Cheap extra passes. |
| `review-paper-code` | CB | Reviews research code against paper claims. | Code accompanies the paper. |
| `paper-review` | AW | N independent reviews plus a meta-review. | Strong independent review. |
| `peer-review` | KD | Structured evidence-bounded review. | Reviewing a manuscript. |
| `ag-paper-reviewer`, `paper-reviewer`, `wy-paper-review`, `cpx-paper-review`, `sy-manuscript-review`, `manuscript-review` | various | More reviewer styles (AG, NP, WY, CX, SY, AH). | Need a different reviewer voice. |
| `paper-autoraters` | PO | Four paper-quality autoraters. | Scores for the paper-orchestra spine. |
| `content-refinement-agent` | PO | Simulated review plus targeted revision with revert rules. | Iterative refinement. |
| `submission-audit` | NP | Preflight on claim support, figure coverage and compliance. | Close to submission. |
| `manuscript-writing-review` | LB | Five audit passes on manuscript writing. | Writing audit. |
| `scholar-evaluation` | KD | Qualitative evaluation of scholarly work. | Developmental feedback. |
| `paper-analyzer`, `paper-read` | NP, LX | Deep analysis of a single paper. | Reading prior work or a paper under review. |

## 10. Rebuttal, revision and post-acceptance

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `rebuttal-writing` | RS | Two-stage triage then writing. | Conference rebuttal. |
| `rebuttal-pipeline`, `rebuttal-writer`, `rebuttal-review` | CX | Parse reviews, draft letter, review letter. | Full rebuttal workflow. |
| `lz-rebuttal-writing` | LZ | Point-by-point with evidence. | Alternative drafter. |
| `rebuttal-response` | NP | Response letters and rebuttals. | Journal response. |
| `review-response`, `cs-review-response`, `nature-response` | GT, CS | Response-to-reviewers letters. | Journal revision. |
| `post-acceptance` | CS | Presentation and poster after acceptance. | Accepted paper. |
| `paper-version` | CB | Policy brief or short summaries from a paper. | Audience-specific version. |
| `presenting-conference-talks`, `academic-slides`, `beamer-academic` | | Talk and slides from a paper. | After the paper, or hand off to `/everythingslideshow`. |

## 11. LaTeX, build and conversion

| Skill | Src | What it does | Use it when |
|---|---|---|---|
| `paper-compilation` | LZ | pdflatex and bibtex loop with error repair. | Compile and fix. |
| `paper-compile` | CX | Compile and verify output. | Same. |
| `latex-rescue` | LX | Diagnoses and repairs build failures with minimal changes. | A build fails. |
| `pdf2tex` | LX | Rebuilds editable LaTeX from a PDF. | Only a PDF exists. |
| `paper-bootstrap` | NP | Standard project structure. | Starting a new manuscript folder. |
| `anthropic-skills:pdf`, `anthropic-skills:docx` | plugin | Read and write PDF and Word files. | Inputs or outputs in those formats. |

## Deliberately not recommended

- Design and website-scoring skills (for example `jury`): they judge websites, not papers.
- Any skill that downloads papers from shadow libraries. Use publisher, arXiv or open-access copies.
- Skills that write whole papers with no evidence in hand. `everythingpaper` never invents results; use the placeholder rules in `references/craft.md`.
