from flask import Flask, Response
from random import sample
import pickle as pk

app = Flask(__name__)
debug = False

with open("recommendation","rb+") as f:
    answerDict = pk.load(f)

with open("topMovies","rb+") as f:
    TopMoviesOverall = list(pk.load(f))

def predict(userID):
    if userID in answerDict:
            return answerDict[userID]
    else:
        num_samples = min(20, len(TopMoviesOverall))
        return sample(TopMoviesOverall, num_samples)

@app.route("/recommend/<string:userid>", methods=["POST","GET"])
def recommend(userid):
    userid = int(userid)
    result = predict(userid)
    return ",".join(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=False)