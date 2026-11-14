
import re

CITATION_PATTERN = re.compile(
    r"\[([^\[\]\n]+?),\s*page\s+(\d+)\]"
)


def find_unverified_citations(
    answer: str,
    sources: list[dict],
) -> list[str]:
    """Find citations not present in retrieved evidence."""

    allowed = {
        (source["document"], int(source["page"]))
        for source in sources
    }

    unverified = set()

    for match in CITATION_PATTERN.finditer(answer):
        document = match.group(1).strip()
        page = int(match.group(2))

        if (document, page) not in allowed:
            unverified.add(
                f"[{document}, page {page}]"
            )

    return sorted(unverified)
