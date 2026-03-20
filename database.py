import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS history (username TEXT, payout INTEGER)")
conn.commit()

def register(u, p):
    c.execute("INSERT INTO users VALUES (?,?)", (u, p))
    conn.commit()

def login(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    return c.fetchone()

def add_history(u, payout):
    c.execute("INSERT INTO history VALUES (?,?)", (u, payout))
    conn.commit()

def get_history(u):
    c.execute("SELECT payout FROM history WHERE username=?", (u,))
    return [x[0] for x in c.fetchall()]