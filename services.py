import re

from db_vocabulary import REPLACEMENTS

def censor_message(text: str) -> tuple[str, bool]:
    is_modified = False

    for pattern, replacement in REPLACEMENTS.items():
        # subn повертає кортеж: (новий_текст, кількість_замін)
        text, count = re.subn(
            pattern, replacement, text, flags=re.IGNORECASE | re.UNICODE
        )
        if count > 0:
            is_modified = True

    return text, is_modified