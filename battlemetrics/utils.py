import re


def remove_html_tags(text: str) -> str:
    """Remove HTML tags from a string."""
    return re.compile(r"<[^>]+>").sub("", text)
