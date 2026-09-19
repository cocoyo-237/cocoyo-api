"""Vérifie les sections minimales des docstrings handlers."""

import ast
from pathlib import Path

FEATURES_ROOT = Path(__file__).resolve().parent.parent / "features"


def _handler_functions(path: Path) -> list[ast.FunctionDef]:
    """Parse un handler.py et liste les fonctions handle_*.

    Args:
        path: Chemin vers handler.py.

    Returns:
        list: Fonctions AST nommées handle_*.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions: list[ast.AST] = []
    for node in tree.body:
        if node.name.startswith("handle_") if hasattr(node, "name") else False:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node)
    return functions


def test_handlers_have_args_and_raises_or_returns() -> None:
    """Chaque handle_* doit documenter Args et Raises ou Returns."""
    handlers = list(FEATURES_ROOT.rglob("handler.py"))
    assert handlers, "Aucun handler trouvé sous features/"

    for handler_path in handlers:
        for func in _handler_functions(handler_path):
            doc = ast.get_docstring(func) or ""
            assert "Args:" in doc, f"{handler_path}:{func.name} manque Args:"
            assert "Returns:" in doc or "Raises:" in doc, (
                f"{handler_path}:{func.name} manque Returns: ou Raises:"
            )
