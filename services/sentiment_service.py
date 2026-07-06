from transformers import pipeline

classifier = pipeline(
    task="sentiment-analysis",
    model="ProsusAI/finbert"
)

def get_articles_sentiment(news: list[dict]) -> list[dict]:

    for article in news:

        text = (
            str(article.get("title", "")) +
            " " + 
            str(article.get("description","")) +
            " " +
            str(article.get("summary", ""))
        ).strip()

        if not text:
            article["sentiment"] = "neutral"
            article["confidence"] = 0
            continue

        try:
            result = classifier(
                text,
                truncation= True,
                max_length=512
                                )

            article["sentiment"] = result[0]["label"].lower()
            article["confidence"] = result[0]["score"]

        except Exception as e:
            print(f"Sentiment analysis failed: {e}")

            article["sentiment"] = "neutral"
            article["confidence"] = 0

    return news