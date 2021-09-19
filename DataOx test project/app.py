from flask import Flask, request, jsonify
import loader

app = Flask(__name__)


@app.route("/")
def main():
    return "<p>DataOx test project</p>"


@app.route("/load")
def load():
    company = request.args.get('company')
    loader.main_company = company
    return jsonify(loader.data_loader.load(company))


if __name__ == '__main__':
    app.run()
