from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # must match the folder's name

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
