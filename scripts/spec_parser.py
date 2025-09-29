import os
from lark import Lark, UnexpectedInput

# ----------------------------
# Load grammar relative to this file
# ----------------------------
_here = os.path.dirname(__file__)
grammar_path = os.path.join(_here, "spec_grammar.lark")

with open(grammar_path, "r", encoding="utf-8") as f:
    _grammar = f.read()

# Build parser once
_parser = Lark(_grammar, start="start")

# ----------------------------
# Public API
# ----------------------------
def validate_spec_code(code: str) -> bool:
    """
    Parse SPEC code against grammar from manuals.
    Return True if syntax is valid, else False.
    """
    try:
        _parser.parse(code)
        return True
    except UnexpectedInput as e:
        # Print parser error for debugging
        print("SPEC parse error:", e)
        return False
