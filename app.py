from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    intro = db.Column(db.String(300), unique=True, nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    date = db.Column(db.DateTime, unique=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return  redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")



@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    bmi = ''
    if request.method == 'POST' and 'weight' in request.form and 'height' in request.form:
        Weight = float(request.form.get('weight'))
        Height = float(request.form.get('height'))
        bmi = round(Weight/((Height/100)**2), 2)
    return render_template("calculate.html", bmi=bmi)


if __name__ == "__main__":
    app.run(debug=True)
