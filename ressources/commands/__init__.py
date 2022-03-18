__all__ = ["hello"]

import importlib
import sys

entries = {}
for i in __all__:
	name = "ressources.commands." + i
	importlib.import_module(name)
	entries[i] = getattr(sys.modules[name], i.capitalize())

from ressources.commands import help
entries["help"] = getattr(sys.modules["ressources.commands." + "help"], "Help")