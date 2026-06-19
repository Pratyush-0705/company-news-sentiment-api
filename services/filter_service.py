import logging
import re


logger = logging.getLogger(__name__)


STOCK_PATTERNS = [

    # Analyst recommendations
    r"\bbuy rating\b",
    r"\bsell rating\b",
    r"\bhold rating\b",
    r"\bbrokerages?\b",
    r"\bbroker ratings?\b",
    r"\btarget prices?\b",
    r"\bprice targets?\b",
    r"\bupgrade(?:d)?\b",
    r"\bdowngrade(?:d)?\b",
    r"\binitiated coverage\b",
    r"\banalysts? recommend\b",

    # Trading actions
    r"\bbuy shares?\b",
    r"\bsell shares?\b",
    r"\bbuy, sell or hold\b",
    r"\bshould you buy\b",
    r"\bshould you sell\b",
    r"\btrading sessions?\b",
    r"\bintraday\b",
    r"\bblock deals?\b",
    r"\bbulk deals?\b",
    r"\bstake sales?\b",
    r"\bofs\b",
    r"\bqip\b",

    # Market references
    r"\bnse\b",
    r"\bbse\b",
    r"\bsensex\b",
    r"\bnifty\b",
    r"\bmarket cap(?:italisation)?\b",
    r"\bvaluation\b",
    r"\bmultibagger\b",
    r"\bstocks?\b",
    r"\bstocks? in focus\b",
    r"\bstocks? gained\b",
    r"\bstocks? rose\b",
    r"\bstocks? fell\b",

    # Price movement
    r"\bshare prices?\b",
    r"\bstock prices?\b",
    r"\bshares? (?:rise|rises|rose)\b",
    r"\bshares? (?:fall|falls|fell)\b",
    r"\bshares? (?:jump|jumps|jumped)\b",
    r"\bshares? (?:gain|gains|gained)\b",
    r"\bshares? (?:drop|drops|dropped)\b",
    r"\bstock(?:s)? (?:rise|rises|fall|falls|jump|jumps|gain|gains)\b",
    r"\b52-week high\b",
    r"\b52-week low\b",
    r"\ball-time high\b",
    r"\blead gains\b",
    r"\blead losers\b",
    r"\brises? \d+(\.\d+)?%\b",
    r"\bfalls? \d+(\.\d+)?%\b",
    r"\bgains? \d+(\.\d+)?%\b",
    r"\bdrops? \d+(\.\d+)?%\b",

    # Dividends
    r"\bdividend\b",
    r"\bfinal dividend\b",
    r"\binterim dividend\b",
    r"\bdividend yield\b",
    r"\brecord date\b",
    r"\bex-dividend\b",
    r"\bpayout ratio\b",

    # Fund activity
    r"\bmutual funds?\b",
    r"\bflexi cap funds?\b",
    r"\bportfolio rebalancing\b",
    r"\bportfolio changes?\b",
    r"\badding stocks?\b",
    r"\bexiting positions?\b",
    r"\bincreasing stakes?\b",
    r"\breducing exposure\b",

    # IPOs
    r"\bipo\b",
    r"\binitial public offering\b",
    r"\bdrhp\b",
    r"\bred herring prospectus\b",
    r"\banchor investors?\b",
    r"\bgrey market premium\b",
    r"\bgmp\b",
    r"\blisting gains?\b",
    r"\bissue price\b",
    r"\bprice band\b",
    r"\bopens? for subscription\b",
    r"\bcloses? for subscription\b",

    # Shareholder terminology
    r"\bequity shares?\b",
    r"\bshareholders\b",

    # Financial metrics
    r"\beps\b",
    r"\bp\/e\b",
    r"\bpe ratio\b",
    r"\bprice-to-earnings\b",

    # Common article formats
    r"\bstock to watch\b",
    r"\bstocks to watch\b",
    r"\btop picks\b",
    r"\bmarket buzz\b"

    # Fund managers
    r"\bfund manager\b",
    r"\bholdings?\b",
    r"\basset allocation\b",
    r"\bassets under management\b",
    r"\baum\b",

    # Broker language
    r"\boutperform\b",
    r"\bunderperform\b",
    r"\boverweight\b",
    r"\bunderweight\b",
    r"\bmaintains? buy\b",
    r"\bmaintains? sell\b",
    r"\bmaintains? hold\b",
]


COMPILED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in STOCK_PATTERNS
]


def is_stock_news(article: dict) -> bool:

    text = " ".join([
        str(article.get("title", "")),
        str(article.get("description", "")),
        str(article.get("content", ""))
    ])

    for pattern in COMPILED_PATTERNS:

        if pattern.search(text):

            logger.info(
                "Filtered stock article: '%s' | matched: %s",
                article.get("title", ""),
                pattern.pattern
            )

            return True

    return False