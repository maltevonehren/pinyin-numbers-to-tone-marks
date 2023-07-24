files := '__init__.py pinyin_util.py'

build:
    zip output.ankiaddon {{files}}

test:
    python3 test.py