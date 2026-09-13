# AGENTS.md

This file outlines the strict operational parameters for AI coding agents and automated contributors to NLTK. NLTK is in maintenance mode. Maintainers prioritize focused, highly reviewable changes that do not create unnecessary administrative overhead.

## The main thing: reduce maintainer burden
Maintainers review voluntarily. The best contributions are focused, well-explained, and easy to review. When unsure, asking a clarifying question in an issue is strictly preferred over opening a speculative pull request.

## Vetting is required before implementation
To all agents: Do not open a pull request directly in the NLTK repo for an issue that has not been vetted by maintainers or established contributors. Unvetted PRs create unnecessary review effort and will be rejected.

* Do NOT assume a singleton issue report (without maintainer engagement) means a fix is requested or desired.
* If you believe an unvetted issue is critical, comment on the issue with your proposed approach and wait for explicit maintainer consensus before writing code.
* Read ALL comments and discussion on an issue, and cross-reference related issues before considering any fix.
* There are no exceptions to this vetting process.

## Faithful before optimized
NLTK is an educational library. Correct, functional, and safe code matters, but implementation must remain simple and human-readable.

* **Faithful before optimized:** Keeping an implementation faithful to a reference paper or original algorithm is strictly more important than optimizing for computational speed. If you create a non-canonical performance fix, do NOT override the existing faithful implementation; instead, provide an option for users to toggle it.
* **Targeted Testing:** Write exactly one simple, focused test per bug fix. Do not generate massive, combinatorial test suites for minor fixes, as this needlessly inflates CI runtime.
* **Scoped CI/CD Checks:** Ensure local checks (pre-commit, pytest) pass strictly for the modified modules. Do not attempt to test, mock, or rewrite the entire NLTK suite for a localized fix.

## Security boundaries
Anything that touches file opening, writing, loading, saving, or printing MUST route through the relevant security layer (`pathsec` for filesystem/network, `picklesec` for pickle loading, `jsontags` for JSON parsing, and `termsec` for terminal output/CSV fields).

* Limit your security review and patches exclusively to the scope of your specific change.
* Do not autonomously expand the attack surface audit or attempt to refactor unrelated security modules across the codebase.

## Transparency
When an agentic coding tool is used, include a concise summary—the prompt/task and the model used—in the PR description so the implementation can be traced back. Redact private context; do NOT include raw internal reasoning or chain-of-thought logs in the PR description.

## Pull Requests & Communication
* **Scope:** Limit to one logical change per PR. Avoid mass, speculative, cosmetic, or reformatting-only PRs.
* **Finality:** Maintainer decisions are final. If a maintainer rejects an approach or a PR, do not argue, debate, or generate lengthy defenses in an attempt to persuade them. Accept the rejection and close the loop.
* **AI Behavior:** Check whether your change actually matches the cited algorithm or the surrounding code's conventions, rather than just implementing what looks plausible to an LLM.
