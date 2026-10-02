import mysql.connector
from mysql.connector import pooling
from flask import g, current_app

_pool = None


def init_pool(app):
    global _pool
    _pool = pooling.MySQLConnectionPool(
        pool_name="vivero_pool",
        pool_size=5,
        host=app.config["MYSQL_HOST"],
        port=app.config["MYSQL_PORT"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DB"],
        autocommit=True,
    )


def get_db():
    if "db" not in g:
        g.db = _pool.get_connection()
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, params=None, fetchone=False):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    if sql.strip().upper().startswith("SELECT"):
        result = cur.fetchone() if fetchone else cur.fetchall()
    else:
        result = cur.lastrowid
    cur.close()
    return result
