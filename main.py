from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# This line fixes it - allows Chrome to see manifest.json
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/fee/{amount}")
def calc_fee(amount: float, type: str = "send"):
    ecocash_fee = 0
    imtt = 0
    
    if type == "send":
        ecocash_fee = amount * 0.013
        imtt = amount * 0.02 if amount >= 5 else 0
    elif type == "cashout":
        ecocash_fee = amount * 0.017
        imtt = 0
    elif type == "merchant":
        ecocash_fee = amount * 0.014
        imtt = amount * 0.02 if amount >= 5 else 0
    else:
        ecocash_fee = amount * 0.013
        imtt = amount * 0.02 if amount >= 5 else 0

    fee = round(ecocash_fee + imtt, 2)
    total = round(amount + fee, 2)
    
    return {
        "amount": amount, 
        "type": type,
        "ecocash_fee": round(ecocash_fee, 2),
        "imtt_tax": round(imtt, 2),
        "fee": fee, 
        "total": total
    }

@app.get("/")
def home():
    path = os.path.join("static", "index.html")
    return FileResponse(path)