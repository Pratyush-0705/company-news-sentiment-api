import yake

MAX_KEYWORD_TEXT_LENGTH = 2000

keyword_extractor = yake.KeywordExtractor(
    lan="en",
    n=2,
    dedupLim=0.7,
    top=5
)

def get_keywords(text: str) -> list[str]:

    if not text or not text.strip():
        return []
    
    text = text[:MAX_KEYWORD_TEXT_LENGTH]

    try:
        keywords = keyword_extractor.extract_keywords(text)

        return [keyword for keyword, score in keywords]
    
    except Exception as e:
        print(f"Keyword Extraction Failed : ", e)
        return []