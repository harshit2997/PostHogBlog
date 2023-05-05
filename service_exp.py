from flask import Flask, Response
from random import sample
import pickle as pk

from posthog import Posthog

posthog = Posthog(project_api_key='<API KEY HERE>', host='https://app.posthog.com')

app = Flask(__name__)
debug = False

with open("recommendation","rb+") as f:
    answerDict = pk.load(f)

with open("recommendation_exp","rb+") as f:
    answerDictExp = pk.load(f)

with open("topMovies","rb+") as f:
    TopMoviesOverall = list(pk.load(f))

def predict(userID):
    variant = posthog.get_feature_flag('IsNMFEnabled', str(userID))

    if variant == 'test':
        if userID in answerDictExp:
            return answerDictExp[userID]
        else:
            num_samples = min(20, len(TopMoviesOverall))
            return sample(TopMoviesOverall, num_samples)
    else:
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