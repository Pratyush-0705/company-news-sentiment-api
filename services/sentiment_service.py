from transformers import pipeline

classifier = pipeline(
    task="sentiment-analysis",
    model="ProsusAI/finbert"
)

MAX_TEXT_LENGTH = 500

def get_articles_sentiment(news: list[dict]) -> list[dict]:

    for article in news:

        text = (
            str(article.get("title", "")) +
            " " +
            str(article.get("summary", ""))
        ).strip()

        if not text:
            article["sentiment"] = "neutral"
            article["confidence"] = 0
            continue

        truncated_text = text[:MAX_TEXT_LENGTH]

        try:
            result = classifier(truncated_text)

            article["sentiment"] = result[0]["label"].lower()
            article["confidence"] = result[0]["score"]

        except Exception as e:
            print(f"Sentiment analysis failed: {e}")

            article["sentiment"] = "neutral"
            article["confidence"] = 0

    return news