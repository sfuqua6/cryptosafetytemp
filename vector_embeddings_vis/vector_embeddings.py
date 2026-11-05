#!/usr/bin/env python3
"""Project summary-word TF-IDF vectors into an interactive 2D plot."""

import argparse
import sys
from collections import Counter
from pathlib import Path

try:
    import plotly.graph_objects as go
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
except ImportError as error:
    missing_package = error.name or "a required package"
    print(
        f"Missing dependency: {missing_package}. "
        "Install dependencies with "
        "'python -m pip install -r vector_embeddings_vis/requirements.txt'.",
        file=sys.stderr,
    )
    raise SystemExit(1) from error


def main() -> int:
    repository_dir = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description=(
            "Plot unique words from weekly incident summaries using their "
            "TF-IDF profiles across summaries."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=repository_dir / "weekly_summaries.txt",
        help="one-summary-per-line input text file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "word_clusters.html",
        help="path for the interactive HTML plot",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(
            f"input file not found: {args.input}. "
            "Generate it first with 'python summary_aggregator.py'."
        )

    try:
        documents = [
            line.strip()
            for line in args.input.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        if len(documents) < 3:
            raise ValueError("At least three non-empty summaries are required.")

        vectorizer = TfidfVectorizer(stop_words="english")
        document_vectors = vectorizer.fit_transform(documents)
        words = vectorizer.get_feature_names_out()
        if len(words) < 2:
            raise ValueError("At least two non-stopword terms are required.")

        word_vectors = document_vectors.T
        coordinates = TruncatedSVD(n_components=2, random_state=42).fit_transform(
            word_vectors
        )
        analyzer = vectorizer.build_analyzer()
        word_counts = Counter(
            term for document in documents for term in analyzer(document)
        )

        counts = [word_counts[word] for word in words]
        size_reference = 2 * max(counts) / (20**2)
        figure = go.Figure(
            data=[
                go.Scatter(
                    x=coordinates[:, 0],
                    y=coordinates[:, 1],
                    mode="markers",
                    customdata=list(zip(words, counts)),
                    marker={
                        "size": counts,
                        "sizemode": "area",
                        "sizeref": size_reference,
                        "sizemin": 4,
                        "opacity": 0.72,
                    },
                    hovertemplate=(
                        "<b>%{customdata[0]}</b><br>"
                        "Occurrences: %{customdata[1]}<extra></extra>"
                    ),
                )
            ]
        )
        figure.update_layout(
            title="Incident Summary Word Clusters (TF-IDF + SVD)",
            template="plotly_white",
            hovermode="closest",
            dragmode="pan",
            xaxis_title="SVD component 1",
            yaxis_title="SVD component 2",
        )

        args.output.parent.mkdir(parents=True, exist_ok=True)
        figure.write_html(args.output, include_plotlyjs=True, full_html=True)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Plotted {len(words)} unique words from {len(documents)} summaries.")
    print(f"Interactive graph saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
