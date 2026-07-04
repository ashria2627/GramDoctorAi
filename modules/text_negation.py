import re

CLAUSE_SPLIT_PATTERN = r"[,،;।\n]+"


def is_symptom_negated(text, phrase):
    escaped = re.escape(str(phrase).lower().strip()).replace(r"\ ", r"\s+")
    if not escaped:
        return False

    lowered = str(text).lower()

    clauses = re.split(CLAUSE_SPLIT_PATTERN, lowered)
    relevant_clauses = [c for c in clauses if re.search(escaped, c)]
    if not relevant_clauses:
        return False

    before_pattern = rf"(?<![a-z0-9])(?:no|without|deny|denies|denied|never|absent)\s+(?:any\s+|a\s+|an\s+)?{escaped}(?![a-z0-9])"
    not_before_pattern = rf"(?<![a-z0-9])not\s+(?:present\s+|having\s+|have\s+|has\s+|any\s+|a\s+|an\s+)?{escaped}(?![a-z0-9])"
    after_pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])\s+(?:is\s+|are\s+|was\s+|were\s+)?(?:not\s+present|absent|not\s+there|not\s+seen|not\s+found)"
    bangla_before_pattern = rf"(?:না|নেই|নাই)\s+(?:কোনো\s+)?{escaped}"
    bangla_after_pattern = rf"{escaped}\s*(?:না|নেই|নাই)"

    patterns = [before_pattern, not_before_pattern, after_pattern, bangla_before_pattern, bangla_after_pattern]

    return any(
        re.search(pattern, clause) is not None
        for clause in relevant_clauses
        for pattern in patterns
    )