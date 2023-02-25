                                        
import string
import json
import psycopg2
import numpy as np
from psycopg2 import sql, extras
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    matrix = np.random.rand(3,2)
    return str(matrix)


@app.route("/hello")
def hello():
    return "hello"


# route only prints data to console
@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
      pg_connection_dict = {
  'dbname': 'lab0',
  'user': 'postgres',
  'password': 'postgres',
  'port': '5432',
  'host': '35.232.191.92'
  }


  conn = psycopg2.connect(**pg_connection_dict)

  # Create json cursor
  cur = conn.cursor(cursor_factory = extras.RealDictCursor)

  # Get the example
  cmd = """SELECT json_build_object(
  'type', 'FeatureCollection',
  'features', json_agg(ST_AsGeoJSON(example.*)::json)
  ) FROM example;"""

  # If want with CRS 'crs', json_build_object('type', 'name', properties', json_build_object( 'name', ST_SRID(>

  cur.execute(cmd)
  #  cur.execute('SELECT ST_ASGeoJSON(geom) FROM example')

  conn.commit() # Committ command

  geojson = json.loads(json.dumps(cur.fetchall()))[0]["json_build_object"]

  # Close connection
  cur.close()
  conn.close()

  return geojson



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
