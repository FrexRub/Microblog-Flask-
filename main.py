from flask import Flask

app = Flask(__file__)

if __name__ == "__main__":
  app.run(debug=True)
