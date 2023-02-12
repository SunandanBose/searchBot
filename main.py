from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui", html=True), name="site")


class Item(BaseModel):
    question: str
    answer: str


@app.get("/ping/")
async def test():
    return "PONG!!!"


@app.post("/createDB/")
async def createDB():
    createDB()
    return {"message": "DB created"}


@app.get("/search/")
async def search(search: str):
    return readData(search)


@app.post("/save/")
async def save(item: Item):
    saveDB(item)
    return {"item": item, "created": "Successfully"}


def createDB():
    dropDB()
    sqliteConnection, cursor = connectDB()
    sqlite_create_table_query = '''CREATE TABLE SearchBOT (
                                question TEXT NOT NULL UNIQUE,
                                amswer text NOT NULL);'''
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

    sqlite_insert_query = f"""INSERT INTO SearchBOT
                          (question, amswer)  VALUES  ('{item.question}', '{item.answer}')"""
    print(sqlite_insert_query)
    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    print("Record inserted successfully into SearchBOT table ",
          cursor.rowcount)
    cursor.close()


def readData(search: str):
    sqliteConnection, cursor = connectDB()

    sqlite_select_query = f"""SELECT * from SearchBOT where question like '%{search}%'"""
    cursor.execute(sqlite_select_query)
    totalRows = cursor.fetchall()
    cursor.close()
    return totalRows


def connectDB():
    sqliteConnection = sqlite3.connect('SQLite_Python.db', timeout=20)
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    return [sqliteConnection, cursor]
