from flask import jsonify
from sqlalchemy import create_engine, text
from BD import DATABASE_URL
from datetime import datetime


engine = create_engine(DATABASE_URL)

def traerTareas (UUID):
  try:
    with engine.connect() as connection:
      query = f"select tareas.titulo, tareas.descripcion, tareas.prioridad, tareas.estado, tareas.fecha_creacion, tareas.fecha_vencimiento, tareas.id_usuario, tareas.id from tareas.usuarios left join tareas.tareas on tareas.id_usuario = usuarios.id where usuarios.uuid = '{UUID}';"
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
            'idTarea': row[7]
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
      res = conn.execute(text(f"select usuarios.id from tareas.usuarios where uuid = '{uuid}';"))
      for user in res:
        ide = user[0]
      query = f"INSERT INTO tareas.tareas (titulo, descripcion, prioridad, estado, fecha_creacion, fecha_vencimiento, id_usuario) VALUES ('{titulo}', '{descripcion}', '{prioridad}', 0, Date(now()), '{fecha}', {ide});"
      insertar = conn.execute(text(query))
      conn.commit()
      if insertar.rowcount > 0:
        respuesta = {'return': True, 'id': ide}
      else:
        respuesta = {'return': False, 'error': 'Error al insertar la tarea'}
  except Exception as e:
    respuesta = {'return': False, 'error': str(e)}
  return respuesta

def filtrarTareas(uuid,prioridad):
  try:
    with engine.connect() as conn:
      if prioridad == '10':
        query = f"select tareas.titulo, tareas.descripcion, tareas.prioridad, tareas.estado, tareas.fecha_creacion, tareas.fecha_vencimiento, tareas.id_usuario, tareas.id from tareas.usuarios left join tareas.tareas on tareas.id_usuario = usuarios.id where usuarios.uuid = '{uuid}';"
      elif prioridad < '5': 
        query = f"select tareas.titulo, tareas.descripcion, tareas.prioridad, tareas.estado, tareas.fecha_creacion, tareas.fecha_vencimiento, tareas.id_usuario, tareas.id from tareas.usuarios left join tareas.tareas on tareas.id_usuario = usuarios.id where usuarios.uuid = '{uuid}' and tareas.prioridad = '{prioridad}';"
      else:
        query = f"select tareas.titulo, tareas.descripcion, tareas.prioridad, tareas.estado, tareas.fecha_creacion, tareas.fecha_vencimiento, tareas.id_usuario, tareas.id from tareas.usuarios left join tareas.tareas on tareas.id_usuario = usuarios.id where usuarios.uuid = '{uuid}' and tareas.estado = '{prioridad}';"
      res = conn.execute(text(query))
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
            'idTarea': row[7]
          })
        respuesta = {'return': True, 'respuesta': datos}
      else:
        respuesta = {'return': False}
  except Exception as e:
     respuesta = {'return': False, 'error': str(e)}
  finally:
    engine.dispose()
  return respuesta

def eliminarTarea(uuid,idTarea):
  try:
    with engine.connect() as conn:
      query = f"delete from tareas.tareas where tareas.id = '{idTarea}';"
      res = conn.execute(text(query))
      conn.commit()
      if res.rowcount > 0:
        respuesta = {'return': True}
  except Exception as e:
    respuesta = {'return': False, 'error': str(e)}
  finally:
    engine.dispose()
  return respuesta

def editarTarea(idTarea,titulo,fecha,prioridad,descripcion,estado):
  try:
    with engine.connect() as conn:
      query = f"UPDATE tareas.tareas SET tareas.titulo = '{titulo}', tareas.descripcion = '{descripcion}', tareas.prioridad = {prioridad}, tareas.estado = '{estado}', tareas.fecha_vencimiento = '{fecha}' WHERE tareas.id = '{idTarea}';"
      print(query)
      res = conn.execute(text(query))
      conn.commit()
      if res.rowcount > 0:
        respuesta = {'return': True}
  except Exception as e:
    respuesta = {'return': False, 'error': str(e)}
  finally:
    engine.dispose()
  return respuesta

def buscar(uuid,titulo):
  try:
    with engine.connect() as connection:
      query = f"select tareas.titulo, tareas.descripcion, tareas.prioridad, tareas.estado, tareas.fecha_creacion, tareas.fecha_vencimiento, tareas.id_usuario, tareas.id from tareas.usuarios left join tareas.tareas on tareas.id_usuario = usuarios.id where usuarios.uuid = '{uuid}' and (tareas.titulo like '%{titulo}%' or tareas.descripcion like '%{titulo}%')";
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
            'vencimiento': [5],
            'usuario': row[6],
            'idTarea': row[7]
          })
        respuesta = {'return': True, 'respuesta': datos}
      else:
        respuesta = {'return': False}
  except Exception as e:
      respuesta = {"return": False, "error": str(e)}
  return respuesta