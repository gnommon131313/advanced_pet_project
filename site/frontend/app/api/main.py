import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import re


# ВАЖНО: тут лишь пример, всь фронтенд должен быть сделан через соответствующие фреймворки, а не через FastApi и генератор шаблонов Jinja2

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")  # Раздаем статические файлы (например, ваш HTML, CSS, JS)
templates = Jinja2Templates(directory="templates")  # Jinja2 получает доступ к шаблонам html (этот способ ориентирован на фреймворки типа FastAPI или Starlette)

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join('static', 'favicon.ico'))

@app.get("/", tags=['root']) 
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/catalog", tags=['products'])
async def read_catalog_html(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request,})
    
@app.get("/cart", tags=['products'])
async def read_cart_html(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request,})