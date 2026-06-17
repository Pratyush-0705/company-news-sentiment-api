from newspaper import Config
from newspaper import Article
import logging
from config.settings import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


config = Config()

config.browser_user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/137.0 Safari/537.36"
)

config.request_timeout = REQUEST_TIMEOUT


def scrape_article(url: str) -> str:

    if not url:
        return ""

    try:
        article = Article(url=url, config=config)

        article.download()
        article.parse()

        return article.text.strip()

    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {e}")

        return ""