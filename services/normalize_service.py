import re


def normalize_company_query(company: str) -> str:
    company = re.sub(r"\s*&\s*", " and ", company)

    company = re.sub(r"\s+", " ", company)

    return company.strip()