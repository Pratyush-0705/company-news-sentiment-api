from datetime import datetime, timedelta, timezone

import requests
from fastapi import HTTPException

from config.settings import (
    GNEWS_API_KEY,
    REQUEST_TIMEOUT,
    MAX_ARTICLES
)

from services.filter_service import is_stock_news
from services.relevance_service import is_relevant_article
from services.normalize_service import normalize_company_query

MAX_PAGES = 5

def get_company_news(
    company: str,
    days: int
) -> list[dict]:

    query = normalize_company_query(company)

    url = "https://gnews.io/api/v4/search"

    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)

    articles = []
    seen_titles = set()
    page = 1

    while len(articles) < MAX_ARTICLES and page <= MAX_PAGES:

        params = {
            "q": query,
            "apikey": GNEWS_API_KEY,
            "max": 10,
            "page": page,
            "lang": "en",
            "from": start_date.isoformat()
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=504,
                detail="News service timed out."
            )

        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=503,
                detail="Unable to connect to news service."
            )

        except requests.exceptions.HTTPError:

            status_code = response.status_code

            if status_code == 400:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid request sent to news provider."
                )

            elif status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or missing GNews API key."
                )

            elif status_code == 429:
                raise HTTPException(
                    status_code=429,
                    detail="GNews API rate limit exceeded."
                )

            else:
                raise HTTPException(
                    status_code=502,
                    detail=f"News provider returned status code {status_code}."
                )

        except ValueError:
            raise HTTPException(
                status_code=502,
                detail="Invalid JSON received from news provider."
            )

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=503,
                detail=f"News request failed: {str(e)}"
            )

        articles_from_api = data.get("articles", [])

        if not articles_from_api:
            break

        for article in articles_from_api:

            if len(articles) >= MAX_ARTICLES:
                break

            article_title = article.get("title","").strip()

            if article_title in seen_titles:
                continue
            
            if(is_relevant_article(article,company) and not is_stock_news(article)):

                seen_titles.add(article_title)

                articles.append({
                    "title": article.get("title",""),
                    "description": article.get("description",""),
                    "url": article.get("url",""),
                    "content": article.get("content",""),
                    "source": article.get("source",""),
                    "publishedAt": article.get("publishedAt","")
                })

        if len(articles_from_api) == 0:
            break

        page += 1

    return articles[:MAX_ARTICLES]