from open_webui.retrieval.web.playwright_content import select_playwright_content


def test_uses_rendered_text_when_extraction_is_empty():
    rendered_text = 'Rendered page content'

    assert select_playwright_content('', rendered_text) == rendered_text


def test_uses_rendered_text_when_extraction_collapses_to_page_chrome():
    navigation = 'UniFi\n\nUISP\n\nBranding\n\nCloud Gateways'
    specifications = '25G SFP28: 2\nTotal PoE Availability: 720W\nSwitching Capacity: 460 Gbps\n'
    rendered_text = f'{navigation}\n\n{specifications * 12}'

    assert select_playwright_content(navigation, rendered_text) == rendered_text


def test_keeps_structured_text_when_it_is_not_part_of_rendered_body():
    extracted_text = 'A clean structured summary that includes generated labels'
    rendered_text = 'Rendered body text ' * 100

    assert select_playwright_content(extracted_text, rendered_text) == extracted_text


def test_keeps_structured_text_for_short_pages():
    extracted_text = 'Navigation'
    rendered_text = f'{extracted_text}\nA short page body'

    assert select_playwright_content(extracted_text, rendered_text) == extracted_text


def test_keeps_structured_text_when_rendered_body_is_empty():
    extracted_text = 'Extracted document content'

    assert select_playwright_content(extracted_text, ' \n ') == extracted_text


def test_subset_comparison_ignores_whitespace_differences():
    extracted_text = 'UniFi\n\nUISP\nBranding'
    rendered_text = f'UniFi UISP    Branding\n{"Specification data " * 40}'

    assert select_playwright_content(extracted_text, rendered_text) == rendered_text
