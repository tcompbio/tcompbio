# Transactions on Computational Biology (TCB)

Website for [Transactions on Computational Biology](https://tcompbio.org) (TCB), a peer-reviewed open-access journal for computational biology research.

## About TCB

TCB differs from [TMLR](https://jmlr.org/tmlr/), which it is modeled after, in three key ways:

1. **Not double blind**: TCB uses a single-blind review process. Reviewers know who the authors are.
2. **Novelty required**: Unlike TMLR, which focuses on correctness, TCB requires that every paper make a novel contribution to computational biology.
3. **Code required**: All submissions must include source code sufficient to reproduce the key results.

## Repository Structure

```
templates/    Jinja2 HTML templates for all pages
static/       Static assets (images, CSS)
src/          Source code for the static site generator
Makefile      Build targets
requirements.txt  Python dependencies
```

## Building the Site

```bash
pip install -r requirements.txt
make
```

The generated site is written to `output/`.

## Pages

| Page | Description |
|------|-------------|
| `index.html` | Home page |
| `acceptance-criteria.html` | Acceptance criteria (novelty + code + correctness) |
| `author-guide.html` | Author guidelines (single blind, code required) |
| `reviewer-guide.html` | Reviewer guidelines |
| `ae-guide.html` | Action Editor guidelines |
| `editorial-policies.html` | Submission guidelines and editorial policies |
| `editorial-board.html` | Editorial board |
| `submissions.html` | How to submit |
| `contact.html` | Contact information |
| `ethics.html` | Ethics guidelines |
| `code.html` | Code of conduct |
| `faq.html` | Frequently asked questions |
| `papers/index.html` | List of accepted papers |
| `news/index.html` | News |