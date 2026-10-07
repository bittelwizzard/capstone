from __future__ import annotations

from html import escape
from pathlib import Path
from tempfile import gettempdir

import numpy as np
import pymupdf

from propose_week11_queries import parse_round_inputs, parse_round_outputs


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "bbo_capstone_presentation.pdf"


def paragraph(text: str) -> str:
    return f"<p>{escape(text)}</p>"


def section(title: str, text: str) -> str:
    return f"<h3>{escape(title)}</h3>{paragraph(text)}"


def build_presentation() -> None:
    history_inputs = parse_round_inputs(ROOT / "week 14" / "inputs.txt")
    history_outputs = parse_round_outputs(ROOT / "week 14" / "outputs.txt")
    if len(history_inputs) != 13 or len(history_outputs) != 13:
        raise ValueError("Presentation requires thirteen completed rounds")
    if any(len(values) != 8 for values in history_inputs + history_outputs):
        raise ValueError("Each round must contain eight inputs and outputs")
    proposal = (ROOT / "week 13" / "proposed_queries_round13.txt").read_text().splitlines()
    for function_index, line in enumerate(proposal):
        submitted = np.array([float(value) for value in line.split("-")])
        if not np.allclose(submitted, history_inputs[-1][function_index], atol=1e-9, rtol=0):
            raise ValueError("Latest history does not match round-13 proposals")

    rows = []
    initial_count = 0
    for function_index in range(1, 9):
        initial = np.load(ROOT / f"function_{function_index}" / "initial_outputs.npy")
        initial_count += len(initial)
        values = [round_values[function_index - 1] for round_values in history_outputs]
        initial_best = float(np.max(initial))
        best = max(initial_best, max(values))
        final_output = values[-1]
        formatted = ["~0" if abs(value) < 1e-12 else f"{value:,.5f}" for value in (initial_best, best, final_output)]
        rows.append(f"<tr><td>F{function_index}</td>" + "".join(f"<td>{value}</td>" for value in formatted) + "</tr>")

    table = (
        "<table><tr><th>Function</th><th>Initial best</th><th>Best observed</th><th>Final round 13</th></tr>"
        + "".join(rows) + "</table>"
    )
    pages = [
        section("My objective", "I am trying to find high-value inputs for eight unknown functions without knowing their formulas. Each function has between two and eight input variables, and I can submit only one point per function in each round.")
        + section("My approach", "I start with the supplied observations, add the results from each round and use a Gaussian process model to estimate which new points might be useful. I balance promising areas with areas where the model is less certain.")
        + section("The process", "Review the data, compare possible points, submit one query per function, record the returned values and update the model. From round 11, I also group similar inputs and give a small preference to the group with the best average result.")
        + section("How I judge progress", "I compare the best output found for each function with its initial best, while also checking the latest result. A good prediction or one successful query is not proof that I have found the best possible input.")
        + paragraph(f"Current evidence: {initial_count} initial observations plus 104 query records across thirteen completed rounds, for {initial_count + 104} input-output records."),

        section("Starting point", "The initial Function 1 script compared several model settings using expected improvement: choosing a point for its potential to beat the best known result. By Week 2, I used GP-UCB, which also gives weight to uncertainty.")
        + section("More systematic searching", "From round 3, I made small exploration adjustments when recent results improved or worsened. Candidate budgets were larger for functions with more variables. Fixed seeds and saved query files made the process easier to repeat.")
        + section("Comparing alternatives", "I tested small neural networks on Functions 5, 7 and 8 as a separate exercise. Their performance varied with the settings and limited data. The submitted-query scripts continued using Gaussian processes; the network experiment was not a replacement query policy.")
        + section("Rounds 11 and 12", "I added input-space clustering to favour promising local groups while retaining uncertainty-driven search. The current cluster-aware code uses dimension-based exploration rather than the earlier recent-result adjustment.")
        + section("What guides me now", "Build on all available evidence, compare results within each function, refine promising regions and avoid treating one high value as a reliable pattern. Model warnings and uneven outcomes remind me that more computation does not replace better coverage."),

        paragraph("Results through round 13. Higher is better within each function; output scales differ, so values should not be compared across functions.")
        + table
        + section("Meaningful patterns", "The best observed value improved over the initial best for seven functions; F3 did not improve. F5 rose from about 1089 initially to 8662.41. F2 reached 0.64245 in round 12, while the final F2 result was lower at 0.61859. F4 recovered from poor boundary results and finished at 0.57686.")
        + section("What seems to matter", "Location and combinations of inputs appear important. Because I usually change several variables together, I cannot isolate individual causes. F1's tiny outputs give little useful signal, and the larger input spaces remain sparsely covered.")
        + section("What I have learned", "I need to look at both improvement and setbacks, not just the largest score. Grouping and PCA-style thinking can help summarise patterns, but PCA has not been applied here and input variation alone does not establish which variables drive high outputs."),

        section("Balancing the search", "Exploration tests uncertain areas; exploitation tests near promising results. My model uses both, with a small bonus for a promising input group. The same balance is not equally useful for every function.")
        + section("What worked: Function 5", "The best observed value rose from about 1089 initially to 6814 in round 12, then to 8662.41 in the final round. These results came from points near the upper input bounds. This is a strong observed pattern, but it does not prove the global optimum or isolate which input caused the gain.")
        + section("What worked: Function 4", "Two earlier boundary queries returned below -34. Moving back near the central observations produced positive results, including 0.57686 in the final round. This was a useful correction after the model's boundary predictions performed poorly.")
        + section("Mixed evidence and uncertainty", "The final result was below the previous best for Functions 2, 3, 4 and 7, although F4 remained positive. A promising query can still fall short of the best result. Identical repeated inputs also differed for Functions 2, 3 and 6, so observed variability and record uncertainty deserve attention."),

        section("Project close-out", "The final query round is complete. The next steps are to preserve the raw records, verify repeated-query provenance and report the best observed result separately for each function. The search did not establish global optima.")
        + section("What I would improve", "Record prediction and uncertainty diagnostics consistently, compare clustered and non-clustered policies under the same query budget, and reserve some queries for deliberate space coverage. Repeated inputs should be interpreted only after their source is confirmed.")
        + section("Connection to wider ML", "This project shares the challenge of active learning: deciding which new observation is worth its cost. Like other ML work, its results depend on data coverage and model assumptions, not just model complexity. PCA highlights the value of finding patterns and reducing redundancy, but a low-variation variable can still be important to the objective.")
        + section("Explaining the results", "For a non-technical stakeholder, I would say: 'I used each result to make the next experiment more informed. Some functions improved, others remained uncertain, and the best values found are not guaranteed to be the best possible.'")
        + paragraph("Evidence: repository scripts, initial arrays, weekly logs, cluster diagnostics and reflections through the final round. The datasheet and model card document the data and method limits."),
    ]

    document = pymupdf.open(ROOT / "BBO capstone project presentation template.pdf")
    if len(document) != len(pages):
        raise ValueError("Expected a five-page presentation template")
    css = """
        body { font-family: sans-serif; font-size: 11pt; color: #202020; }
        h3 { font-size: 13pt; color: #242052; margin: 10pt 0 4pt; }
        p { margin: 0 0 9pt; line-height: 1.3; }
        table { width: 100%; border-collapse: collapse; margin: 12pt 0; font-size: 10pt; }
        th { background: #efeff4; text-align: left; }
        th, td { padding: 6pt 4pt; border-bottom: 1px solid #d2d2d2; }
    """
    for page_index, (page, content) in enumerate(zip(document, pages)):
        boxes = [drawing["rect"] for drawing in page.get_drawings()
                 if drawing["rect"].width > 350 and 300 < drawing["rect"].height < 650]
        if not boxes:
            raise ValueError(f"Cannot locate answer box on template page {page_index + 1}")
        box = min(boxes, key=lambda rectangle: rectangle.get_area())
        inset = pymupdf.Rect(box.x0 + 15, box.y0 + 12, box.x1 - 15, box.y1 - 12)
        spare_height, scale = page.insert_htmlbox(inset, content, css=css, scale_low=1)
        if spare_height < 0 or scale != 1:
            raise ValueError(f"Presentation content does not fit page {page_index + 1}")
    document.set_metadata({"title": "BBO Capstone: Approach, Evidence and Next Steps", "subject": "Thirteen-round optimisation study"})
    OUTPUT.parent.mkdir(exist_ok=True)
    document.save(OUTPUT, deflate=True)
    document.close()
    preview_directory = Path(gettempdir()) / "capstone_presentation_previews"
    preview_directory.mkdir(exist_ok=True)
    with pymupdf.open(OUTPUT) as completed:
        for page_index, page in enumerate(completed):
            page.get_pixmap(matrix=pymupdf.Matrix(1, 1)).save(preview_directory / f"presentation_preview_{page_index + 1}.png")
            if pages[page_index].count("<h3>") < 3 or len(page.get_text()) < 1000:
                raise ValueError("Missing presentation content")
    print(f"Created and rendered five pages: {OUTPUT}")


if __name__ == "__main__":
    build_presentation()