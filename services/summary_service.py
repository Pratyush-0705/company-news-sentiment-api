from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import logging


logger = logging.getLogger(__name__)


summarizer = LsaSummarizer()


def generate_summary(text: str, sentence_count: int = 3) -> str:
    """
    Generate a short summary from article text.

    Args:
        text (str): Full article content
        sentence_count (int): Number of summary sentences

    Returns:
        str: Summarized text
    """

    if not text or len(text.split()) < 50:
        return text

    try:
        parser = PlaintextParser.from_string(
            text,
            Tokenizer("english")
        )

        summary = summarizer(
            parser.document,
            sentence_count
        )

        return " ".join(str(sentence) for sentence in summary)

    except Exception as e:
        logger.warning(f"Summary generation failed: {e}")

        return text[:500]