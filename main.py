from fastapi import FastAPI, HTTPException

from models.request_models import CompanyRequest

from services.news_service import get_company_news
from services.scraper_service import scrape_article
from services.summary_service import generate_summary
from services.sentiment_service import get_articles_sentiment
from services.keywords_service import get_keywords
from services.analysis_service import analyze_sentiment


app = FastAPI(
    title="Company News Sentiment API",
    version="2.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Company News Sentiment API is running"
    }


@app.post("/company-sentiment")
def company_sentiment(request: CompanyRequest):

    news = get_company_news(
        company=request.company,
        days=request.days
    )

    if not news:
        raise HTTPException(
            status_code=404,
            detail="No articles found."
        )

    for article in news:

        url = article.get("url","")
        description = article.get("description","")
        content = article.get("content","")

        scraped_content = scrape_article(url)

        combined_text = description + content + scraped_content

        article["summary"] = generate_summary(
            scraped_content
        )

        article['keywords'] = get_keywords(combined_text)

    news = get_articles_sentiment(news)

    sentiment = analyze_sentiment(news)

    return {
        "company": request.company,
        "articles_analyzed": len(news),
        "overall_sentiment": sentiment["overall_sentiment"],
        "positive": sentiment["positive"],
        "negative": sentiment["negative"],
        "neutral": sentiment["neutral"],
        "articles": news
    }