from flask import Flask,request, jsonify
from pydantic import BaseModel
from typing import Optional, List
from flask_cors import CORS

from tools.login import *
from inicio.inicio import *

app = Flask(__name__)
CORS(app)

class Login(BaseModel):
  req: str
  user: Optional[str] = None
  password: Optional[str] = None
  uuid: Optional[str] = None

class Tareas(BaseModel):
  req: str
  fecha: Optional[str] = None
  prioridad: Optional[str] = None
  titulo: Optional[str] = None
  descripcion: Optional[str] = None
  uuid: Optional[str] = None


@app.post('/')

def log():
  try:
    data = request.json
    login = Login(**data)

    if login.req == 'login':
      return ingresar(login.user, login.password)
    elif login.req == 'reanudar':
      return verificar(login.uuid)
    else:
      return jsonify({'return': False})
  except Exception as e:
    return jsonify({"error": str(e)})
  
@app.post('/tareas')
def inicio():
  try:
    data = request.json
    tarea = Tareas(**data)
    if tarea.req == 'traerTareas':
      return traerTareas(tarea.uuid)
    elif tarea.req == 'subirTarea':
      return subirTarea(tarea.uuid,tarea.titulo,tarea.fecha,tarea.prioridad,tarea.descripcion)
  except Exception as e:
    return jsonify({"error": str(e)})

  

if __name__ == '__main__':
    app.run(debug=True)