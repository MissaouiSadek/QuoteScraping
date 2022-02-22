import copy
import os
from fastapi import FastAPI
import pymongo
import uvicorn
from scraper import Scraper

quote_scraper = Scraper()
client = None
db = None
try:
    login = os.getenv('MONGODB_USERNAME','') + ":" + os.getenv('MONGODB_PASSWORD','') + '@'
    login = '' if login == ':@' else login
    hostname = os.getenv('MONGODB_HOSTNAME','localhost')
    database = os.getenv('MONGODB_DATABASE','quotes_db')
    # Connection
    client = pymongo.MongoClient(f"mongodb://{login}{hostname}:27017/")
    db = client[database]
    print('Connection To Database Successful.')
except:
    print('Connection To Database Failed.')

app = FastAPI(title = 'Quote Scrapper')

@app.on_event("shutdown")
def shutdown_event():
    print("Selenium Driver Shutdown.")
    quote_scraper.quit_scraper()
    if client != None:
        print("Mongo Client Shutdown.")
        client.close()

@app.get('/quotes/{tag}')
async def get_quotes(tag:str):
    quotes = quote_scraper.quote_scraper(tag)
    quotes_to_insert = copy.deepcopy(quotes)
    if db != None:
        try:
            quotes_collection = db[tag+"_quotes"]
            result = quotes_collection.insert_many(quotes_to_insert)
            print('Insertion To Database Successful.')
        except:
            print('Insertion To Database Failed.')
    return quotes

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)