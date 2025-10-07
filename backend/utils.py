import re

ENTITY_KEYWORDS = {
    "Counterparty": ["Counterparty"],
    "Initial Valuation Date": ["Initial Valuation Date"],
    "Notional": ["Notional", "Notional Amount", "Notional Amount (N)", "Amount"],
    "Valuation Date": ["Valuation Date"],
    "Maturity": ["Maturity", "Termination Date", "Expiry Date", "Tenor", "Duration"],
    "Underlying": ["Underlying", "Instrument", "Asset"],
    "Coupon": ["Coupon", "Coupon (C)", "Interest Rate"],
    "Barrier": ["Barrier", "Barrier (B)"],
    "Calendar": ["Calendar", "Business Day", "Schedule"]
}

ALL_KEYWORDS = sorted({k for kws in ENTITY_KEYWORDS.values() for k in kws}, key=len, reverse=True)


def next_non_empty_index(lines, start_index):
    j = start_index + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    return j if j < len(lines) else None

def is_label_like(s):
    for kw in ALL_KEYWORDS:
        if re.match(rf"^\s*{re.escape(kw)}\b", s, re.IGNORECASE):
            return True
    if re.match(r"^\s*Party\s+[AB]\b", s, re.IGNORECASE):
        return True
    return False

def post_process_candidate(candidate, entity_name=None):
    """Clean candidate and try to pick useful substring (currency/number/date/percent) intelligently."""
    if candidate is None:
        return None
    candidate = candidate.strip()
    if '\t' in candidate:
        candidate = candidate.split('\t')[-1].strip()
    # ignore tiny abbreviations like N), C)
    if re.match(r'^[A-Za-z0-9]{1,3}\)$', candidate):
        return None

    # NEW FIX: if this is the 'Underlying' entity, or text includes 'ISIN'/'Reuters', keep the full string
    if (entity_name and entity_name.lower() == "underlying") or re.search(r'\b(ISIN|Reuters|Bloomberg|Corp|Ltd|SE)\b', candidate, re.I):
        return candidate.strip()

    # if it contains digits/currency/%/date → keep from first useful token
    if re.search(r'\d', candidate) or re.search(r'\b(EUR|USD|GBP|INR|JPY)\b', candidate, re.I) or '%' in candidate or re.search(r'\d{1,2}\s+[A-Za-z]+', candidate):
        candidate = re.sub(r'[\.;,]+$', '', candidate).strip()
        m = re.search(r'(\b(EUR|USD|GBP|INR|JPY|\$|€|£|₹)\b|\d{1,3}[,\d]*(?:\.\d+)?\s*(?:million|bn|billion|m|k)?|\d+%|\d{1,2}\s+[A-Za-z]+)', candidate, re.I)
        if m:
            return candidate[m.start():].strip()
        return candidate

    if len(candidate) <= 3:
        return None
    return candidate