import typing, json, logging, random, time

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_restful import Api, Resource, reqparse
import asyncio

from database import Slang, init


application = Flask(__name__)
api = Api(application)

def random_url() -> str:
    return str(time.time())


@application.route('/')
async def index():
    await init()
    
    if request.method == 'GET':
        search = request.args.get('search')
        parser = reqparse.RequestParser()
        parser.add_argument('search', type=str, location='form')
        params = parser.parse_args()

        print(search)
        posts = await Slang.all()

        for words in await Slang.all().order_by('-word'):
            from fuzzywuzzy import process
            if search != None:
                a = process.extractOne(search or '', words)

                if a[1] >= 69:   
                    print(a[0][1])

                    if await Slang.get_or_none(word=str(a[0][1]).lower()) is not None:
                        
                        slang = await Slang.filter(word=str(a[0][1]).lower()).first()
                        
                        return render_template('post_search.html', word=slang.word, description=slang.description, type=slang.type)
                    else:
                        return render_template('search2.html', posts=posts)

            if search == '':
                
                return render_template('search2.html', posts=posts)
    
    return render_template('search.html')
    


@application.route('/api', methods=['GET', 'POST'])
async def slang_translator():
    
    await init()
    
    if request.method == 'GET':
        parser = reqparse.RequestParser()
        parser.add_argument('words', type=str, location='form')
        params = parser.parse_args()

        if await Slang.get_or_none(word = str(params['words']).lower()) is not None:               
            slang = await Slang.filter(word = str(params['words']).lower()).first()

            return {"word": slang.word, "description": slang.description, "type": slang.type}
        
        return render_template('api.html')

    elif request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('words', type=str,  required=True)
        parser.add_argument('description', type=str,  required=True)
        parser.add_argument('type', type=str,  required=True)
        parser.add_argument('password', type=str,  required=True)
        params = parser.parse_args()
        
        if await Slang.get_or_none(word = str(params['words']).lower()) is not None:
            if params['password'] == 'admin':
                await Slang.create(word = str(params['words']).lower(), description = params['description'], type = params['type'])
                return {"status":"Succeful"}, 200
            else:
                return {"status": "error (password)"}
        else:
            return {"status": "error (word)}"}

    else:
        return {"status": "error"}


@application.route('/admin', methods=['GET', 'POST'])
async def admin():
    if request.method == 'POST':
        login = request.form["text1"]
        password = request.form["text2"]
        print(login, password)
        if login == "admin" and password == "admin":
            return redirect(url_for('admin_matvey'))
    return render_template('login.html')
        

@application.route(f'/admin/{random_url()}', methods=['GET', 'POST'])
async def admin_matvey():
    await init()

    if request.method == 'POST':
        Word = request.form["Word"]
        Description = request.form["Description"]
        Type = request.form["Type"]
        print(Word,Description,Type)
        if await Slang.get_or_none(word = Word.lower()) is None:
            await Slang.create(word = Word.lower(), description = Description, type = Type)
            return {"status":"Succeful"}, 200
        else:
            return {"status": "error (word)}"}

    return render_template("admin.html")


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
