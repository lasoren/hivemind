from flask import Flask
from flask import Response
app = Flask(__name__)

@app.route("/sentiment")
def sentiment():
    return flask.jsonify(sentiment=0.5)

@app.route("/articles")
def articles():
    json = {"sentiment" : 0.5,
            "articles" : [
                {"title": "Obama Eats Children",
                 "snippet": "Obama seen eating children."}
                ]}
    return Response(json.dump(json), mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
