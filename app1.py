from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app1)
app1.app_context().push()


class ToDo(db.Model):
    __tablename__ = "ToDo"
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
#    date_created = db.Column(db.Date, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}"

@app1.route('/', methods=['GET', 'POST'])
def hello():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']        
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit() 
    allToDo = ToDo.query.all()
    print(allToDo)
    return render_template('index.html', allToDo=allToDo)

@app1.route('/show')
def about():
    allToDo = ToDo.query.all()
    print(allToDo)   
    name = 'Faisal'
    return render_template('about.html', NAME=name)  #The term "NAME" reads from the html file and "name" reads from pyton variable file.

@app1.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update(Sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(Sno=Sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo = ToDo.query.filter_by(Sno=Sno).first()
    return render_template('update.html', Todo=todo)

@app1.route('/delete/<int:Sno>')
def delete(Sno):
    todo = ToDo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
    
                    

if __name__ == "__main__":
    app1.run(debug=True, port=8000)
    