# CSF Crypto Incident Database

An open, independent database of real-world crypto security incidents.

This repository documents scams, hacks, phishing campaigns, user-risk patterns, and operational failures observed across Web3 ecosystems. The goal is to create a **structured, queryable, and openly reusable dataset** that helps researchers, builders, and users better understand how crypto incidents actually happen.

---

## Scope

The database focuses on:
- Scams (phishing, pig butchering, impersonation, fake exchanges)
- Wallet compromises and key theft
- Account takeovers and session hijacking
- User mistakes with security impact
- Infrastructure and software failures affecting users

Incidents are sourced from public reports (Reddit, X, news outlets, blogs) and normalized into a consistent schema.

---

## Data Structure

Each incident entry includes:
- Incident ID
- Incident type and category
- Source platform
- Public reference link
- Short incident summary
- Root cause or user mistake (when identifiable)
- Defensive takeaway or prevention guidance

The database is designed to evolve as patterns change.

---

## Explore Summary Word Clusters

The scripts create an interactive 2D word plot from all weekly incident summaries.
Words are represented by their TF-IDF profiles across summaries, then projected
to two dimensions with SVD. Common English stopwords are excluded; each remaining
unique word appears once, and hovering over a point shows the word and its
occurrence count. Nearby points indicate similar TF-IDF patterns in this corpus,
not guaranteed semantic similarity.

Install the visualization dependencies from the repository root:

```sh
python -m pip install -r vector_embeddings_vis/requirements.txt
```

Generate the summary text file, then the interactive HTML graph:

```sh
python summary_aggregator.py
python vector_embeddings_vis/vector_embeddings.py
```

The graph is written to `vector_embeddings_vis/word_clusters.html`. Open it in a
browser to zoom, pan, and inspect clusters. Use `--input` and `--output` to select
different input and output paths.

---

## Why This Exists

Most crypto losses are not caused by novel exploits — they are caused by **repeated, well-known failure patterns**.

This project aims to:
- Reduce hindsight bias in crypto security
- Make user-risk patterns visible
- Support better wallet design, education, and prevention
- Provide an open dataset for analysis and research

---

## License

This repository is released under **Creative Commons Zero v1.0 Universal (CC0)**.

You are free to use, copy, modify, and redistribute the data for any purpose, without restriction or attribution.

---

## Disclaimer

This repository is for educational and research purposes only.  
It does not provide legal, financial, or investment advice.

---

## Contributions

Contributions, corrections, and improvements are welcome.
Schema stabilization and contribution guidelines will be added as the dataset matures.
