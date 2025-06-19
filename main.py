import numpy as np
from fastapi import FastAPI
import sqlite3 as db
from typing import List, Optional
from pydantic import BaseModel, parse_obj_as
import os
import pandas as pd

# creazione app
app = FastAPI()


# Percorso database
db_path = (os.path.join(os.getcwd(), 'Database'))

# Creiamo una classe per modellare i dati che restituiamo
class DatiAscolto(BaseModel):
    anno: int
    ascolti_radio: float
    ascolti_tv: Optional[float]


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
    # Mappiamo le etichette ai campi
    return [DatiAscolto(anno=row[0], ascolti_radio=row[1], ascolti_tv=row[2]) for row in rows]


# Volendo passare direttamente dal Dataframe e non da un database
@app.get("/dati-ascolti-csv", response_model=list[DatiAscolto])
def get_dati_ascolti():
    df_ascolti = pd.read_csv(os.path.join(os.getcwd(),'Outputs', 'ascolti_radio_tv_priv.csv'))
    # Le colonne devono matchare con il model che ho definito in precedenza
    df_ascolti.rename(columns={
        "Anno": "anno",
        "Radio (a)": "ascolti_radio",
        "TV - Uso privato": "ascolti_tv"
    }, inplace=True)
    # Dal momento che il JSON non ammette valori NA o NaN, convertiamo i valori a None
    df_ascolti = df_ascolti.replace({pd.NA : None, float("nan"): None})
    # Parsing del dizionario ottenuto dal df come Lista di modelli DatiAscolto
    return parse_obj_as(List[DatiAscolto], df_ascolti.to_dict(orient="records"))


if __name__ == "__main__":
    import uvicorn
    # all'avvio dello script main, lancia anche il web server
    # in alternativa si poteva lanciare il comando uvicorn main:app --reload
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

