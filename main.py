from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

origins =["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/ui", StaticFiles(directory="ui", html=True), name="site")


class Item(BaseModel):
    question: str
    answer: str


@app.get("/ping/")
async def test():
    return "PONG!!!"


@app.post("/createDB/")
async def createDB():
    dropDB()
    createDB()
    return {"message": "DB created"}


@app.get("/search/")
async def search(search: str):
    return readData(search)


@app.post("/save/")
async def save(item: Item):
    saveDB(item)
    return {"item": item, "created": "Successfully"}

@app.delete("/delete/")
async def delete(id: int):
    deleteData(id)
    return {"id": id, "deleted": "Successfully"}


def createDB():
    # dropDB()
    sqliteConnection, cursor = connectDB()
    sqlite_create_table_query = '''CREATE TABLE SearchBOT (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                question TEXT NOT NULL,
                                answer text NOT NULL);'''
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()


def dropDB():
    sqliteConnection, cursor = connectDB()
    sqlite_create_table_query = '''DROP TABLE SearchBOT;'''
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table dropped")

    cursor.close()


def saveDB(item: Item):
    sqliteConnection, cursor = connectDB()

    sqlite_insert_query = 'INSERT INTO SearchBOT (question, answer)  VALUES  (?, ?)'
    cursor.execute(sqlite_insert_query, (item.question, item.answer))
    sqliteConnection.commit()
    print("Record inserted successfully into SearchBOT table ",
          cursor.rowcount)
    cursor.close()


def readData(search: str):
    sqliteConnection, cursor = connectDB()
    pattern = f"%{search}%"
    sqlite_select_query = "SELECT * from SearchBOT where question like ? or answer like ?"
    cursor.execute(sqlite_select_query, (pattern, pattern))
    totalRows = cursor.fetchall()
    cursor.close()
    return totalRows

def deleteData(idToDelete: int):
    sqliteConnection, cursor = connectDB()

    sqlite_delete_query = f"""DELETE from SearchBOT where id = {idToDelete}"""
    cursor.execute(sqlite_delete_query)
    sqliteConnection.commit()
    print(f"Record {idToDelete} deleted successfully ")
    cursor.close()
    


def connectDB():
    sqliteConnection = sqlite3.connect('SQLite_Python.db', timeout=20)
    cursor = sqliteConnection.cursor()
    return [sqliteConnection, cursor]
