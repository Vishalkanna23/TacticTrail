
import pymupdf

from app.ingestion.pdf_parser import extract_pdf_pages


def test_pdf_parser_preserves_page_numbers(tmp_path):
    pdf_path = tmp_path / "security_report.pdf"

    document = pymupdf.open()

    page1 = document.new_page()
    page1.insert_text((72, 72), "Brute force attacks")

    page2 = document.new_page()
    page2.insert_text((72, 72), "Credential dumping")

    document.save(pdf_path)
    document.close()

    results = extract_pdf_pages(pdf_path)

    assert len(results) == 2
    assert results[0]["document"] == "security_report.pdf"
    assert results[0]["page"] == 1
    assert "Brute force attacks" in results[0]["text"]
    assert results[1]["page"] == 2
    assert "Credential dumping" in results[1]["text"]

def test_pdf_parser_detects_large_heading(tmp_path):
    pdf_path = tmp_path / "security_heading.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Credential Access",
        fontsize=18,
    )

    page.insert_text(
        (72, 110),
        "Attackers may attempt to obtain passwords.",
        fontsize=11,
    )

    document.save(pdf_path)
    document.close()

    results = extract_pdf_pages(pdf_path)

    assert len(results) == 1
    assert results[0]["heading"] == "Credential Access"
    assert "Attackers may attempt" in results[0]["text"]
