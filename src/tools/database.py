import sqlite3 as db
import logging

_folder = "data/"
_default = "global"

def _open(name: str, table: str = None) -> db.Connection | None:
	c = db.connect(name)
	if not c:
		logging.error(f"Failed to open the database {name}!")
		return
	if table:
		t = c.cursor()
		t.execute(f"""
			SELECT * FROM sqlite_master
			WHERE type='table' AND name='{table}'
		""")
		if t.fetchone()[0]:
			logging.warn(f"{table} doesnt exists!")
			return
	return c

def _close(con: db.Connection) -> None:
	con.commit()
	con.close()

def insert(table: str, values: tuple, database: str = _default):
	path = _folder + database + ".db"
	c = _open(path, table)
	if not c: return

	t = c.cursor()
	t.execute(f"""
		SELECT * FROM {table}
		WHERE 
	""")

	_close(c)