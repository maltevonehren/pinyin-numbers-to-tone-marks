from pinyin_util import *

TESTS = [
    ("", ""),
    ("xian1", "xiān"),
    ("xi1", "xī"),
    ("xi1an1", "xī'ān"),
    ("wan3an1", "wǎn'ān"),
    ("tian1e2", "tiān'é"),
    ("xian4zai4", "xiànzài"),
    ("liao3", "liǎo"),
    ("not pinyin with numbers 1", "not pinyin with numbers 1"),
    ("an1ba", "ānba"),
    ("an1ba1", "ānbā"),
]

for (input, output) in TESTS:
    result = pinyin_numbers_to_marks(input)
    assert result == output, \
        f"test failed for {input}: got {result} expected {output}"
print('All checks passed')