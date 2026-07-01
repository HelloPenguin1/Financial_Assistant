from fastapi import FastAPI

app = FastAPI()

@app.get('/home')
async def load_up():
    return {'message': 'Hello'}



    