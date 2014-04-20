import sqlite3
conn = sqlite3.connect('baza.db')
cur = conn.cursor()

try: cur.execute("DROP TABLE uporabniki");
except: pass
try: cur.execute("DROP TABLE ankete");
except: pass
try: cur.execute("DROP TABLE vprasanja");
except: pass
try: cur.execute("DROP TABLE odgovori");
except: pass

cur.execute("""CREATE TABLE uporabniki (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    email TEXT
                    );""")

cur.execute("""CREATE TABLE ankete (
                    id INTEGER PRIMARY KEY,
                    naslov TEXT,
                    uvod TEXT,
                    uporabnik TEXT,
                    FOREIGN KEY(uporabnik) REFERENCES uporabniki(username));""")

cur.execute("""CREATE TABLE vprasanja (
                    id INTEGER PRIMARY KEY,
                    naslov TEXT,
                    vprasanja TEXT,
                    tip TEXT,
                    vrstni_red INTEGER,
                    anketa INTEGER,
                    FOREIGN KEY(anketa) REFERENCES ankete(id));""")

cur.execute("""CREATE TABLE odgovori (
                    id INTEGER PRIMARY KEY,
                    skupina INTEGER,
                    text TEXT,
                    vprasanje INTEGER,
                    FOREIGN KEY(vprasanje) REFERENCES vprasanja(id));""")

cur.execute("INSERT INTO uporabniki VALUES ('jureslak','jureslak', 'mail')")

cur.execute("INSERT INTO ankete VALUES (NULL, 'Moja anketa', 'bla bla', 'jureslak')")

cur.execute("INSERT INTO vprasanja VALUES (NULL, 'Starost?', '10\n20', 'radiobutton', 1, 1)")
cur.execute("INSERT INTO vprasanja VALUES (NULL, 'Visina?', '', 'text', 2, 1)")
cur.execute("INSERT INTO vprasanja VALUES (NULL, 'Teza?', '', 'text', 3, 1)")

cur.execute("INSERT INTO odgovori VALUES (NULL, 0, '20', 0)")
cur.execute("INSERT INTO odgovori VALUES (NULL, 0, '180', 1)")
cur.execute("INSERT INTO odgovori VALUES (NULL, 0, '70', 2)")

cur.execute("INSERT INTO odgovori VALUES (NULL, 1, '25', 0)")
cur.execute("INSERT INTO odgovori VALUES (NULL, 1, '140', 1)")
cur.execute("INSERT INTO odgovori VALUES (NULL, 1, '30', 2)")

for line in cur.execute("SELECT * FROM uporabniki"):
    print(line)
for line in cur.execute("SELECT * FROM vprasanja"):
    print(line)
for line in cur.execute("SELECT * FROM ankete"):
    print(line)
for line in cur.execute("SELECT * FROM odgovori"):
    print(line)

conn.commit()   
