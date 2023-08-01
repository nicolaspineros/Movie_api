from fastapi import Depends, FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import  List
from model import Movie, User, movies
from fastapi.encoders import jsonable_encoder

from starlette.requests import Request
from jwt_manager import JWTBearer, create_token, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

jwt_bearer = JWTBearer()

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world!</h1>')

@app.post('/login', tags=['auth'],response_model=dict, status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(jwt_bearer)])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Categoria no encontrada"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()    
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    result.title = movie.title
    result.category = movie.overview
    result.overview = movie.overview
    result.rating = movie.rating
    result.year = movie.year  
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Updated done"})    
        
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})

        
