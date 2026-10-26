# Craft rules for research papers

Why this file exists: the same mistakes sink papers again and again, and most of them are not about English. They are about claims that outrun evidence, missing controls, citations that do not say what is claimed, and a reader who cannot find the point. These are the floors. Read this before drafting and during the Round 2 read.

Contents: Evidence bars by paper type · Claims and how strongly to state them · Structure · Experiments and statistics · Citations · Placeholders and honest gaps · Prose floors · Figures, tables and math · Reproducibility and ethics · AI tells

## Evidence bars by paper type

What a skeptical expert expects to see before believing the central claim.

| Paper type | Minimum evidence bar | Typical rejection reasons |
|---|---|---|
| Empirical ML / AI | Strong, current baselines under equal tuning budget; ablations that isolate each component; more than one dataset or setting; several seeds with variance; compute and hyperparameters stated; failure cases | Weak or untuned baselines, one seed, cherry-picked benchmark, claim wider than tested, no ablation, leakage |
| Theory | Precise statements, all assumptions listed, complete proofs (main text or appendix), tightness or comparison to known bounds, a sanity example | Hidden assumptions, gap in a proof, bound no better than known, no discussion of when assumptions fail |
| Systems | Realistic workloads, comparison to the real state of the art, end-to-end and micro measurements, scalability, overheads, artifact | Toy workloads, unfair baselines, only best-case numbers, no cost analysis |
| Benchmark or dataset | Collection and annotation process, quality control, agreement statistics, licence and consent, baselines, known limitations | Unclear provenance, label noise, contamination, no baselines |
| HCI / user study | Research questions, participants and recruitment, design and procedure, measures, effect sizes and confidence intervals, ethics approval | Small or biased sample, no control, p-hacking, unmotivated measures |
| Clinical / biomedical | Registered protocol, inclusion and exclusion, primary outcome fixed in advance, effect sizes with intervals, reporting guideline (CONSORT, STROBE, PRISMA) | Selective outcomes, confounding, underpowered, missing guideline |
| Social science / economics | Identification strategy, assumptions and tests, robustness checks, data and code, clustered or appropriate standard errors | Causal language without identification, specification searching |
| Survey / review | Search protocol, inclusion criteria, taxonomy that adds insight, coverage of recent work, honest gaps and open problems | List of summaries with no synthesis, stale coverage, biased selection |
| Position paper | A clear thesis, the strongest counter-argument stated fairly, concrete implications | Opinion without argument, strawman opposition |

## Claims and how strongly to state them

- A paper has **one central claim** and two to four supporting claims. Write the central claim as a sentence a skeptic could disprove. If it cannot be disproved, it is not a claim.
- Every claim has an ID and appears in `EVIDENCE.md` with its evidence. A claim with no evidence is cut, softened to what the evidence supports, or stated as a limitation or future work.
- Match the verb to the evidence:

| Evidence | Verbs that fit |
|---|---|
| Controlled experiment or proof | shows, demonstrates, proves, establishes |
| Consistent results across settings, no causal test | suggests, indicates, is associated with |
| One setting, or a trend | is consistent with, we observe, in our setting |
| Speculation | may, could, we hypothesize (and say it is a hypothesis) |

- Words that need evidence next to them: "state of the art" (against what, on what), "significantly" (give the test and p or interval), "robust" (to what), "scalable" (up to what size), "first" (after a documented search), "novel" (say what is new rather than calling it new), "outperforms" (by how much, with what variance).
- Causal language ("causes", "leads to", "because") needs a causal design. Otherwise say "is associated with".
- State scope. "On three English benchmarks" is a scope. "In general" is not.
- Put the strongest honest claim in the title, abstract and first page. Do not bury it, and do not inflate it.

## Structure

**Empirical conference paper (typical):** Title, Abstract, Introduction (problem, gap, idea, contributions, results preview), Related Work, Method, Experiments (setup, baselines, results, ablations, analysis), Limitations, Conclusion, References, Appendix.

**Journal article (typical):** Title, Abstract, Introduction, Background or Related Work, Methods, Results, Discussion (interpretation, limits, implications), Conclusion, Data and code availability, References, Supplement.

- **Abstract** (write last): context in one sentence, the gap or problem, what you did, the main result with a number, why it matters. No citations, no undefined acronyms, no claim the body does not prove. Every number in the abstract appears in the body.
- **Introduction funnel:** the problem and why it matters, what is known and what is missing (the gap), your idea in one paragraph, a contributions list (3 or fewer bullets, each checkable), a pointer to the results. A reader should be able to state your contribution after page one.
- **Contributions list:** each item is a verifiable statement ("We prove X", "We release Y", "We show Z on N datasets"), not a topic ("We study robustness").
- **Related work:** organised by idea, not by author. For each group say what it does, what it cannot do, and how you differ. Credit first, contrast second. Cite the closest prior work and say plainly how you differ from it; reviewers know it.
- **Method:** enough detail to reimplement. Define every symbol before use, give an algorithm box when the procedure is not obvious, state assumptions, motivate each design choice in one sentence.
- **Results:** lead with the finding, then the evidence ("Method A beats B by 3.1 points (Table 2)"). One paragraph per question the experiments answer.
- **Discussion and limitations:** say where the method fails, which assumptions may not hold, and what you did not test. Honest limitations raise trust and are required by many venues.
- **Conclusion:** restate the finding in new words, what it changes, one concrete next step. No new results.
- **Signposting:** each section opens with its purpose; each paragraph opens with its point (the topic sentence) and could be skimmed by those sentences alone.

## Experiments and statistics

- Baselines: the strongest published, run or reported under comparable budget; say which numbers you re-ran and which you copied from papers.
- Ablations: remove or replace each claimed component; show each matters.
- Variance: several seeds or folds; report mean and spread (state whether standard deviation or standard error); do not hide the spread.
- Significance: use an appropriate test and report effect size with an interval, not only p. Do not claim a difference inside the noise. Correct for multiple comparisons when you test many.
- Splits and leakage: tuning on validation, one-time test; state how data were split and rule out train-test overlap.
- Report negative and null results that bear on the claim.
- State compute, hardware, run time and hyperparameter search budget.
- Never report a number you cannot trace to a log or script. `experiment-claim-audit` checks this.

## Citations

- Cite for: prior results you build on, methods you use, datasets, claims of fact that are not common knowledge. Do not cite to decorate.
- Verify every entry exists (DOI, arXiv id, publisher page) and read the passage that supports the claim. Use the published version over the preprint when both exist.
- Cite the original source for a result, not a review that mentions it, unless the review is the point.
- Self-citation: when it is the closest prior work, cite it; do not pad.
- No "et al." in bib entries where a venue demands full author lists; consistent style; no duplicate keys; capitalisation protected with braces for proper nouns and acronyms in titles.
- Quote sparingly, with the page. Paraphrase and cite; never copy sentences.

## Placeholders and honest gaps

When evidence does not exist yet:
- Write `[TODO-EVIDENCE: what is needed, e.g. "accuracy of baseline B on dataset D, 3 seeds"]` where the number or claim would go.
- Keep the claim out of the abstract and contributions until the evidence exists, or phrase it as a plan ("we will evaluate").
- Do not fill a table cell with a plausible number. Leave `--` and a marker.
- `paper_lint.py` fails any paper that contains a marker, so a gap cannot ship unnoticed. List every marker in the report.
- A skeleton with honest gaps is a good deliverable. A finished-looking paper with a made-up result is a fraud risk for the user.

## Prose floors

- One idea per sentence. Typical length 15 to 30 words; beyond 40 split unless it is a list.
- Subject and verb close together; the actor in the subject; active voice by default, passive where the actor does not matter (Methods).
- Define a term at first use and keep that name for that thing for the whole paper. Do not vary terms for style: a reader will think they are different things.
- Define every acronym once, at first use in the body (and again in the abstract if used there).
- Numbers: units, sample sizes, intervals. "Improves by 4.2 points (95% CI 3.1 to 5.3)" beats "greatly improves".
- Hedge in proportion: hedge a claim once, where it applies, not every sentence.
- Tense: past for what you did and found; present for what the paper does and for general truths.
- Cut: "it is worth noting that", "in order to", "plays a crucial role", "a wide range of", and any sentence that only announces what the next one says.
- Keep the user's voice and the field's conventions: passive Methods, technical terms, standard hedges are fine. Do not "humanize" them away.
- Respect saved punctuation rules (for example no em dashes).

## Figures, tables and math

- One claim per exhibit. The caption states the takeaway, not only the content, and stands alone: a reader who sees only the figure and caption understands it.
- Label axes with units; legends readable at print size; fonts not smaller than the body caption; vector output; colour-blind safe palettes and a non-colour cue (marker or line style); consistent colours for the same method across figures.
- Tables: bold the best result only if the difference is meaningful; align decimals; units in headers; state whether higher or lower is better; show variance.
- Refer to every figure and table in the text, and discuss what the reader should see.
- Math: define every symbol on first use, keep one notation throughout, number only equations you reference, say what each equation means in words.

## Reproducibility and ethics

- State data sources, licences, preprocessing, splits, hyperparameters, seeds, compute, code and model availability. Give a link or say why not.
- Ethics: human subjects approval, consent, privacy, dual-use, bias and fairness analysis where relevant, and the venue's required statements (broader impact, limitations, checklist).
- Data and code statements follow the venue's template; `data-availability` helps.
- AI-assistance disclosure follows the venue's policy; check it live.

## AI tells and report-voice

Patterns that mark text as machine-made or padded: stacked adjectives, "delve", "tapestry", "landscape", "underscore", "pivotal", "in the realm of", rule-of-three lists everywhere, "not only X but also Y" repetition, a summary sentence ending every paragraph, vague attributions ("studies show"), over-neat structure. Remove them, but keep legitimate scientific hedging and domain vocabulary. Report-voice (audit language, "we verified that", developer file names, self-critique in the main text) belongs in logs and the appendix, not the argument (`anti-defensive-writing`).
