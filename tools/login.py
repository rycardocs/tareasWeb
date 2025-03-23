from flask import jsonify
from sqlalchemy import create_engine, text
import uuid
from BD import DATABASE_URL


engine = create_engine(DATABASE_URL)

def ingresar(user, password):
  try:
    with engine.connect() as connection:
      query = (f"select uuid,user from tareas.usuarios where user = '{user}' and password = AES_ENCRYPT('{password}','Tareas.902');")
      result = connection.execute(text(query))
      datos = []
      if result is not None:
       
        for row in result:
          if row[0] is None:
              nuevo_uuid = uuid.uuid4()
              connection.execute(text(f"update tareas.usuarios set uuid = '{nuevo_uuid}' where user = '{user}';"))
              connection.commit()
              datos.append({
              'uuid': nuevo_uuid,
              'user': row[1]
            })
          else:
            datos.append({
            'uuid': row[0],
            'user': row[1]
            })
        respuesta = ({'return': True , 'data': datos})
      else:
        respuesta = ({'return': False})
  except Exception as e:
    respuesta = {"return": False, "error": str(e)}
  finally:
    engine.dispose()
  return jsonify(respuesta)

def verificar(UUID):
    try:
      with engine.connect() as connection:
        res = connection.execute(f"select user from tareas.usuarios where UUID = '{UUID}';")
        if res is not None:
          respuesta = {'return': True}
        else:
          respuesta = {'return': False}
    except Exception as e:
      respuesta = {"return": False, "error": str(e)}
    finally:
      engine.dispose()
    return respuesta