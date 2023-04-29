from flask import Flask, render_template, request
import redis

app = Flask(__name__)
r = redis.Redis()

@app.route('/',methods=['GET','POST'])
def index():
  data = {}
  if request.method == 'POST':
    r.set(request.form['word'], request.form['meaning'])
    data['message'] = "Word added successfully"
  data['words'] = getWords()
  return render_template('index.html',data=data)

@app.route('/delete/<word>',methods=['GET'])
def delete(word):
  r.delete(word)
  data = {'message': 'Word deleted successfully'}
  data['words'] = getWords()
  return render_template('index.html',data=data)

@app.route('/edit/<word>', methods=['GET'])
def edit(word):
  data = {'word':{'meaning':r.get(word).decode('UTF-8'),'name':word}}
  data['words'] = getWords()
  return render_template('index.html',data=data)

def getWords():
  words = []
  for i in r.keys():
    words.append({
      'name': i.decode("UTF-8"),
      'meaning': r.get(i).decode('UTF-8')
    })
  return words

if __name__ == "__main__":
  app.run(debug=True)
