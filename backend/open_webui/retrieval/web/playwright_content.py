MIN_RENDERED_TEXT_LENGTH = 500
MIN_RENDERED_TO_EXTRACTED_RATIO = 3


def _normalize_whitespace(text: str) -> str:
    return ' '.join(text.split())


def select_playwright_content(extracted_text: str, rendered_text: str) -> str:
    """Prefer rendered text when structured extraction clearly collapsed.

    The structured result remains the default because it usually removes page chrome
    and produces cleaner documents. The rendered body is only used when the structured
    result is empty, or when it is demonstrably a small subset of a substantial body.
    """
    normalized_extracted = _normalize_whitespace(extracted_text)
    normalized_rendered = _normalize_whitespace(rendered_text)

    if not normalized_rendered:
        return extracted_text
    if not normalized_extracted:
        return rendered_text

    extraction_collapsed = (
        len(normalized_rendered) >= MIN_RENDERED_TEXT_LENGTH
        and len(normalized_rendered) >= len(normalized_extracted) * MIN_RENDERED_TO_EXTRACTED_RATIO
        and normalized_extracted in normalized_rendered
    )
    return rendered_text if extraction_collapsed else extracted_text
