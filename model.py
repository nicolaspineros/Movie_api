from pydantic import BaseModel, Field
import datetime
from typing import Optional


class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15)
    overview: str
    year: int = Field(le=datetime.date.today().year)
    rating: float = Field(ge=1, le=10)
    category: str

    class Config:
        schema_extra = {
            "example":{
                'id': 1,
                'title':'Mi pelicula',
                'overview':'Descripción de la pelicula',
                'year':2022,
                'rating':7.9,
                'category':'Acción'
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]
