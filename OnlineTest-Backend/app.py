from flask import Flask,request,json,jsonify
import flask
from evaluation import extract,totalMarks

def add_cors_header(response):
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'HEAD,OPTIONS,GET,POST,PUT,DELETE'
  response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
  response.headers['Access-Control-Expose-Headers'] = 'content-range'
  response.headers['Access-Control-Allow-Credentials'] = 'true'
  response.headers['Content-Type'] = 'application/json; charset=utf-8'
  response.headers['content-range'] = 'review 1-10/10'
  return response

app=Flask(__name__)
app.after_request(add_cors_header)

data={}
@app.route("/",methods=['POST'])
def putdata():
  data=request.get_json()
  extract(data)
  return flask.jsonify(data)

@app.route("/",methods=['GET'])
def getScore():
  data=totalMarks
  print(data)
  return flask.jsonify(data)

app.secret_key="abcd"
app.run(debug=True)