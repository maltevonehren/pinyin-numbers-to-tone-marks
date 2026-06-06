from pinyin_util import pinyin_numbers_to_marks

TESTS = [
    ("", ""),
    ("xian1", "xiān"),
    ("xi1", "xī"),
    ("xi", "xi"),
    ("la4", "là"),
    ("la", "la"),
    ("la5", "la"),
    ("xi1an1", "xī'ān"),
    ("wan3an1", "wǎn'ān"),
    ("tian1e2", "tiān'é"),
    ("xian4zai4", "xiànzài"),
    ("liao3", "liǎo"),
    ("an1ba", "ānba"),
    ("an1ba1", "ānbā"),
    ("zhe4ge", "zhège"),
    ("zhe4ge5", "zhège"),
    ("lv3cheng2", "lǚchéng"),
    ("lvcheng", "lücheng"),
    ("lv3", "lǚ"),
    ("lv", "lü"),
    ("kao4lv", "kàolü"),
    ("kaolv3", "kaolǚ"),
    ("not pinyin with numbers 1", "not pinyin with numbers 1"),
    ("xiànzai4", "xiànzài"),
    ("xianzai4", "xianzài"),
]

for input, output in TESTS:
    result = pinyin_numbers_to_marks(input)
    assert result == output, f"test failed for {input}: got {result} expected {output}"
print("All checks passed")
