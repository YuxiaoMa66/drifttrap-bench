import textwrap
from pathlib import Path


def make_pkg(tmp_path):
    pkg = tmp_path / "demo_pkg"
    (pkg / "sub").mkdir(parents=True)
    (pkg / "__init__.py").write_text("class A:\n    pass\n")
    (pkg / "sub" / "__init__.py").write_text("")
    (pkg / "sub" / "m.py").write_text(textwrap.dedent("""
        class B:
            pass


        class C:
            def f(self):
                return 1
    """))
    return pkg
from griffe_helpers import count_classes


def test_count_classes(tmp_path):
    assert count_classes(make_pkg(tmp_path)) == 3
