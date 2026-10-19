# -*- coding: utf-8 -*-
"""测试包：把 tests/ 自身和上层（应用模块所在目录）都挂进 sys.path。

这样 `python -m unittest discover -s tests -t .` 和 `cd tests && python -m unittest` 都能跑，
tests/ 下的辅助模块（_pdf_fixture.py）也能被直接 import。
"""
import os
import atexit
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_PKGS = [os.path.join(_ROOT, "packages", _n) for _n in
         ("database", "workspace-core", "workspace-service", "connectors", "ai-runtime")]
for _p in (_ROOT, *[p for p in _PKGS if os.path.isdir(p)], _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# 测试绝不能读写用户真实的览籍智研数据目录。
_TEST_HOME = None
if not os.environ.get("LANJI_ZHIYAN_HOME"):
    _TEST_HOME = tempfile.mkdtemp(prefix="lanji-zhiyan-tests-")
    os.environ["LANJI_ZHIYAN_HOME"] = _TEST_HOME
    atexit.register(shutil.rmtree, _TEST_HOME, ignore_errors=True)
