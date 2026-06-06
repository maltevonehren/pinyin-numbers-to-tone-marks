import re


MARK_ON_FIRST = [
    "a",
    "ai",
    "ao",
    "e",
    "ei",
    "i",
    "o",
    "ou",
    "u",
    "ü",
]
MARK_ON_SECOND = [
    "ia",
    "iao",
    "ie",
    "io",
    "iu",
    "ua",
    "uai",
    "ue",
    "ui",
    "uo",
    "üe",
]
VOWELS = ["a", "e", "i", "o", "u", "ü", "v"]
TONES = {
    "a": "āáǎàa",
    "e": "ēéěèe",
    "i": "īíǐìi",
    "o": "ōóǒòo",
    "u": "ūúǔùu",
    "ü": "ǖǘǚǜü",
}
V2Ü = {
    "v": "ü",
    "ve": "üe",
}

PROTECTED_PATTERNS = [
    # HTML comments
    r"<!--.*?-->",  # For example: <!-- note -->
    # HTML blocks that should remain untouched
    r"<script\b[^>]*>.*?</script>",  # For example: <script>...</script>
    r"<style\b[^>]*>.*?</style>",  # For example: <style>...</style>
    r"<[^>]+>",  # For example: <a href="..."> or </div>
    # Anki field syntax
    r"\{\{[#^][^}]+\}\}.*?\{\{/[^}]+\}\}",  # For example: {{#Field}}...{{/Field}}
    r"\{\{c\d+::.*?\}\}",  # For example: {{c1::text}}
    r"\{\{[^}]+\}\}",  # For example: {{FieldName}}
    # Anki media
    r"\[sound:[^\]]+\]",  # For example: [sound:file.mp3]
    # LaTeX / MathJax
    r"\\\(.*?\\\)",  # For example: \( x^2 + y^2 \)
    r"\\\[.*?\\\]",  # For example: \[ x^2 + y^2 \]
    r"\[\$\].*?\[/\$\]",  # For example: [$] x^2 + y^2 [/$]
    # HTML entities and URLs
    r"&[A-Za-z0-9#]+;",  # For example: &nbsp;
    r"https?://[^\s<>'\"]+",  # For example: https://example.com
]

PROTECTED_PATTERN = re.compile(
    "|".join(PROTECTED_PATTERNS),
    re.IGNORECASE | re.DOTALL,
)


def add_tone(word: str, position: int, tone: int) -> str:
    """return a str where the character at `position` is replaced
    with the same character but with a tone mark corresponding to the `tone`"""
    return word[:position] + TONES[word[position]][tone - 1] + word[position + 1 :]


def v2ü(word: str) -> str:
    if word in V2Ü:
        return V2Ü[word]
    else:
        return word


def next_character_is_vowel(input: str, position: int) -> bool:
    return position + 1 < len(input) and input[position + 1] in VOWELS


def next_character_is_digit(input: str, position: int) -> bool:
    return position + 1 < len(input) and input[position + 1].isdigit()


def _pinyin_numbers_to_marks_plain(input: str) -> str:
    cluster_start = 0
    cluster_end = 0
    seen_cluster = False
    output = ""
    for i, c in enumerate(input):
        if not seen_cluster:
            if c in VOWELS:
                cluster_start = i
                seen_cluster = True
                cluster_end = i + 1
            else:
                output += c

        else:
            cluster = input[cluster_start:cluster_end]

            if c in VOWELS:
                if cluster_end < i:
                    output += v2ü(cluster) + input[cluster_end:i]
                    cluster_start = i
                cluster_end = i + 1

            elif c in ["1", "2", "3", "4", "5"]:
                cluster = v2ü(cluster)
                separator = input[cluster_end:i]
                if any(
                    not (character.isalpha() or character == "'")
                    for character in separator
                ) or next_character_is_digit(input, i):
                    output += input[cluster_start : i + 1]
                elif cluster in MARK_ON_FIRST:
                    output += add_tone(cluster, 0, int(c)) + input[cluster_end:i]
                    if next_character_is_vowel(input, i):
                        output += "'"
                elif cluster in MARK_ON_SECOND:
                    output += add_tone(cluster, 1, int(c)) + input[cluster_end:i]
                    if next_character_is_vowel(input, i):
                        output += "'"
                else:
                    output += input[cluster_start : i + 1]
                seen_cluster = False

            elif c == " ":
                output += v2ü(cluster) + input[cluster_end : i + 1]
                seen_cluster = False

        i += 1
    if seen_cluster:
        cluster = input[cluster_start:]
        output += v2ü(cluster)
    return output


def pinyin_numbers_to_marks(input: str) -> str:
    output = ""
    last_end = 0
    for match in PROTECTED_PATTERN.finditer(input):
        output += _pinyin_numbers_to_marks_plain(input[last_end : match.start()])
        output += match.group(0)
        last_end = match.end()
    output += _pinyin_numbers_to_marks_plain(input[last_end:])
    return output
