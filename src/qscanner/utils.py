import re
from bs4 import BeautifulSoup

def clean_html(html_content: str) -> str:
    """Removes script/style and returns clean text with preserved structure."""
    soup = BeautifulSoup(html_content, 'lxml')
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all("p"):
        p.append("\n")
    
    text = soup.get_text(separator=' ')
    text = text.replace('\xa0', ' ')
    
    # Remove multiple spaces while keeping newlines
    text = re.sub(r' +', ' ', text)
    
    lines = [line.strip() for line in text.splitlines()]
    return '\n'.join(line for line in lines if line)

def is_toc_entry(match, text):
    """Checks if a match is likely a TOC entry (e.g., followed by dots or a page number on the same line)."""
    # Look at the rest of the line
    start = match.end()
    line_end = text.find('\n', start)
    if line_end == -1: line_end = start + 100
    line_snippet = text[start : line_end].strip()
    
    # If line ends with a digit or contains many dots, it's TOC
    if re.search(r'\d+$', line_snippet) or '....' in line_snippet or '····' in line_snippet:
        return True
    return False

def extract_section(text: str, section_name: str, next_section_name: str) -> str:
    """
    Improved section extraction with TOC filtering.
    """
    if section_name == "Item 1":
        pattern = r"Item\s+1[.\s]+Business"
    elif section_name == "Item 7":
        pattern = r"Item\s+7[.\s]+Management"
    elif section_name == "Item 1A":
        pattern = r"Item\s+1A[.\s]+Risk\s+Factors"
    elif section_name == "Item 7A":
        pattern = r"Item\s+7A[.\s]+Quantitative"
    else:
        pattern = rf"{section_name}"

    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    if not matches:
        return ""

    # Filter out TOC entries
    actual_matches = [m for m in matches if not is_toc_entry(m, text)]
    
    if not actual_matches:
        # Fallback if filtering was too aggressive
        start_index = matches[-1].start()
    else:
        # For Item 1, prefer the one after PART I
        if section_name == "Item 1":
            part_i_match = re.search(r"PART\s+I\b", text, re.IGNORECASE)
            if part_i_match:
                for m in actual_matches:
                    if m.start() > part_i_match.start():
                        return extract_until_next(m.start(), next_section_name, text)
        
        start_index = actual_matches[-1].start()

    return extract_until_next(start_index, next_section_name, text)

def extract_until_next(start_index, next_section_name, text):
    if next_section_name == "Item 1A":
        next_pattern = r"Item\s+1A[.\s]+Risk\s+Factors"
    elif next_section_name == "Item 7A":
        next_pattern = r"Item\s+7A[.\s]+Quantitative"
    else:
        next_pattern = rf"{next_section_name}"

    # Search for next section, filtering TOC
    next_matches = list(re.finditer(next_pattern, text[start_index+50:], re.IGNORECASE))
    for nm in next_matches:
        actual_nm_start = start_index + 50 + nm.start()
        if not is_toc_entry(nm, text[start_index+50:]):
            return text[start_index : actual_nm_start]
            
    return text[start_index : start_index + 30000]
