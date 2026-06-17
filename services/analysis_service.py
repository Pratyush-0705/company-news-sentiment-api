def analyze_sentiment(news: list[dict]) -> dict:

    sentiment_count = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }

    for article in news:

        sentiment = article.get("sentiment", "neutral").lower()

        sentiment_count[sentiment] += 1

    overall_sentiment = max(
        sentiment_count,
        key=sentiment_count.get
    )

    return {
        "overall_sentiment": overall_sentiment,
        "positive": sentiment_count["positive"],
        "negative": sentiment_count["negative"],
        "neutral": sentiment_count["neutral"]
    }