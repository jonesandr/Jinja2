
from flask import Flask, render_template, request
import redis

app = Flask(__name__)
r = redis.Redis()

@app.route('/',methods=['GET','POST'])
def index():
  data = {}
  if request.method == 'POST':
    r.set(request.form['nombre'], request.form['significado'])
    data['mensaje'] = "Palabra ingresada"
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/eliminar/<nombre>',methods=['GET'])
def eliminar(nombre):
  r.delete(nombre)
  data = {'mensaje': 'Palabra eliminada'}
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/editar/<nombre>', methods=['GET'])
def editar(nombre):
  data = {'palabra':{'significado':r.get(nombre).decode('UTF-8'),'nombre':nombre}}
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)


def obtenerPalabras():
  palabras = []
  for i in r.keys():
    palabras.append({
      'nombre': i.decode("UTF-8"),
      'significado': r.get(i).decode('UTF-8')
    })
  return palabras

if __name__ == "__main__":
  app.run(debug=True)