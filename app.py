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
  estado: Optional[int] = None
  titulo: Optional[str] = None
  descripcion: Optional[str] = None
  uuid: Optional[str] = None
  idTarea: Optional[int] = None
  creacion: Optional[str] = None
  Vencimiento: Optional[datetime] = None



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
    data = request.json
    tarea = Tareas(**data)
    if tarea.req == 'traerTareas':
      return traerTareas(tarea.uuid)
    elif tarea.req == 'subirTarea':
      return subirTarea(tarea.uuid,tarea.titulo,tarea.fecha,tarea.prioridad,tarea.descripcion)
    elif tarea.req == 'filtrar':
      return filtrarTareas(tarea.uuid,tarea.prioridad)
    elif tarea.req == 'eliminar':
      return eliminarTarea(tarea.uuid,tarea.idTarea)
    elif tarea.req == 'editar':
      return editarTarea(tarea.idTarea,tarea.titulo,tarea.fecha,tarea.prioridad,tarea.descripcion,tarea.estado)
    elif tarea.req == 'buscar':
      return buscar(tarea.uuid,tarea.titulo)
    else:
      return jsonify({"error": 'No valido'})

if __name__ == '__main__':
    app.run(debug=True)