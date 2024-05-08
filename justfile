files := '__init__.py pinyin_util.py'

build:
    zip output.ankiaddon {{files}}
    
build-dev:
    zip dev.ankiaddon {{files}} manifest.json

test:
    python3 test.py
