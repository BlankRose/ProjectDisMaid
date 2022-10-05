__all__ = ["hello", "random"]

from src.commands import help
import importlib
import sys

entries = {}
__all__.append("help")
for i in __all__:
	name = "src.commands." + i
	importlib.import_module(name)
	entries[i] = getattr(sys.modules[name], i.capitalize())
