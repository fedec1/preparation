from fastapi import FastAPI
import sqlite3 as db
import os

# creazione app
app = FastAPI()


# Percorso database
db_path = (os.path.join(os.getcwd(), 'Database'))


# Creazione della prima route
@app.get("/dati-ascolti")
def get_utenti():
    # Connessione al db
    conn = db.connect(os.path.join(db_path, 'database.db'))
    cursor = conn.cursor()
    # Esecuzione della query
    cursor.execute("SELECT * FROM ascolti_radio")
    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    import uvicorn
    # all'avvio dello script main, lancia anche il web server
    # in alternativa si poteva lanciare il comando uvicorn main:app --reload
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

