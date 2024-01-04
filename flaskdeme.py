
from flask import *
from helloworld import HelloWorld
#model = (r'E:\')

app = Flask(__name__)

result = dict()
result["results"] = ""


@app.route('/hello', methods=('GET', 'POST'))
def hello_reponse():

    a = HelloWorld()

    return a


@app.route('/identity', methods=('GET', 'POST'))
def hello_reponse():

    a = HelloWorld()

    return a

@app.route('/')




@app.route('/hello', methods=('GET', 'POST'))
def hello_reponse():
    a = HelloWorld()

    return a

if __name__ == '__main__':
    app.run(port=11252)

