
MARK_ON_FIRST = [
    "a", "ai", "ao", "e", "ei", "i", "o", "ou", "u", "ü",
]
MARK_ON_SECOND = [
    "ia", "iao", "ie", "io", "iu", "ua", "uai", "ue", "ui", "uo", "üe",
]
TONES = {
    "a": "āáǎà",
    "e": "ēéěè",
    "i": "īíǐì",
    "o": "ōóǒò",
    "u": "ūúǔù",
    "ü": "ǖǘǚǜ",
}


def add_tone(word: str, position: int, tone: int) -> str:
    """return a str where the character at `position` is replaced
    with the same charater but with a tone mark corresponding to the `tone`"""
    return word[:position] + TONES[word[position]][tone-1] + word[position+1:]


def next_character_is_vowel(input: str, position: int) -> bool:
    return position+1 < len(input) and input[position+1] in TONES


def pinyin_numbers_to_marks(input: str) -> str:
    i = 0
    cluster_start = 0
    cluster_end = 0
    seen_cluster = False
    output = ""
    for (i, c) in enumerate(input):
        if not seen_cluster:
            if c in TONES:
                cluster_start = i
                seen_cluster = True
                cluster_end = i + 1
            else:
                output += c
        else:
            if c in TONES:
                if cluster_end < i:
                    output += input[cluster_start:i]
                    cluster_start = i
                cluster_end = i + 1
            elif c in ["1", "2", "3", "4"]:
                cluster = input[cluster_start:cluster_end]
                if cluster in MARK_ON_FIRST:
                    output += add_tone(cluster, 0, int(c)) + input[cluster_end:i]
                    if next_character_is_vowel(input, i):
                        output += "'"
                elif cluster in MARK_ON_SECOND:
                    output += add_tone(cluster, 1, int(c)) + input[cluster_end:i]
                    if next_character_is_vowel(input, i):
                        output += "'"
                else:
                    output += input[cluster_start:i+1]
                seen_cluster = False
            elif c == " ":
                output += input[cluster_start:i+1]
                seen_cluster = False
        i += 1
    if seen_cluster:
        output += input[cluster_start:]
    return output
