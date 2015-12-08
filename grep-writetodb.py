import sqlite3


def write_to_db(*args, db_name):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	for datum in *args:
		c.executemany("INSERT INTO keywords")

