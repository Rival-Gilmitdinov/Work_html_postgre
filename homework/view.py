from flask import Flask, request, render_template, flash
import psycopg2
import requests
from controller import Data, add, create_table

app = Flask(__name__)
app.secret_key = 'secret'
# <string:name>/<int:id>

@app.route('/qq')
def dsf():
    return render_template('base.html')

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')5


@app.route('/about', methods=['GET', 'POST'])
def opis():
    if request.method == 'POST':
        data = request.form.get('data')
        if str(data).strip():
            add(request.form.get('data'))
            flash('Данные успешно сохранены!', 'success')
        else:
            flash('Заполните поле символами(одни пробелы не подойдут)')
        print(request.form.get('data'))
        return render_template('index.html')
    elif request.method == 'GET':
        return render_template('about.html', table=f"{create_table()}")
    else:
        print('sdfdf')


if __name__ == '__main__':
    app.run(debug=True)
