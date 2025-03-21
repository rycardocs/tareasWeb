from flask import jsonify
from sqlalchemy import create_engine, text
from BD import DATABASE_URL


engine = create_engine(DATABASE_URL)

def traerTareas (UUID):
  try:
    with engine.connect() as connection:
      query = f"select tareas.titulo, tareas.descripcion, tareas.prioridad, tareas.estado, tareas.fecha_creacion, tareas.fecha_vencimiento, tareas.id_usuario from tareas.usuarios left join tareas.tareas on tareas.id_usuario = usuarios.id where usuarios.uuid = '{UUID}';"
      res = connection.execute(text(query))
      if res is not None:
        datos = []
        for row in res:
          datos.append({
            'titulo': row[0],
            'descripcion': row[1],
            'prioridad': row[2],
            'estado': row[3],
            'creacion': row[4],
            'vencimiento': row[5],
            'usuario': row[6],
          })
        respuesta = {'return': True, 'respuesta': datos}
      else:
        respuesta = {'return': False}
  except Exception as e:
      respuesta = {"return": False, "error": str(e)}
  return respuesta

def subirTarea(uuid,titulo,fecha,prioridad,descripcion):
  try:
    with engine.connect() as conn:
      res = conn.execute(f"select user from tareas.usuarios where UUID = '{uuid}';")
      print(res[0][0])
      query = f"INSERT INTO tareas.tareas (titulo, descripcion, prioridad, estado, fecha_creacion, fecha_vencimiento, id_usuario) VALUES ('{titulo}', '{descripcion}', '{prioridad}', 0, '{fecha}', '{fecha}', 't');"
  except Exception as e:
    respuesta = {'return': False, 'error': str(e)}
  return respuesta