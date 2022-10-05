__all__ = ["hello", "random"]

import importlib
import sys

entries = {}
for i in __all__:
	name = "src.commands." + i
	importlib.import_module(name)
	entries[i] = getattr(sys.modules[name], i.capitalize())

from src.commands import help
entries["help"] = getattr(sys.modules["src.commands." + "help"], "Help")