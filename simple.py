from flask import Flask, render_template

app = Flask(__name__, template_folder='frontend/templates')


@app.route('/')
def home():
    print(app.template_folder)
    return render_template('items/index.html')


if __name__ == '__main__':
    app.run(debug=True)
