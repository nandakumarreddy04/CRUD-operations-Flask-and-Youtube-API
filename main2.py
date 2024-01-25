from flask import Flask

app = Flask(__name__) 


@app.route("/") 
def helloworld():
	return "Hello World, from Nanda-2  (Load Balancer)"

if __name__ == '__main__': 
	app.run(debug=True) 