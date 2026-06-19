import re

def is_relevant_article(
    article: dict,
    company: str
) -> bool:

    if not company:
        return False

    text = " ".join([
        str(article.get("title", "")),
        str(article.get("description", "")),
        str(article.get("content", ""))
    ]).lower()

    company = company.lower().strip()

    pattern = rf"\b{re.escape(company)}\b"

    return bool(re.search(pattern, text))