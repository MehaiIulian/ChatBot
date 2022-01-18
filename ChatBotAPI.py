from flask import Flask, request, jsonify

from main import getRecipeByIngredients, chooseRecipe, chat

import time
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return "API for delivering recipes to the user! Running now ..."


#http://127.0.0.1:5000/getRecipeByIngredients?ingr=chicken&nr=5
@app.route('/getRecipeByIngredients', methods=['GET', 'POST'])
def getRecipeByIngredientsBot():
    ingredients = request.args.get('ingr');
    number = int(request.args.get('nr'))
    time.sleep(2)
    return jsonify(chatBotReply=getRecipeByIngredients(ingredients, number));

#http://127.0.0.1:5000/chooseRecipe?nr=5
@app.route('/chooseRecipe', methods=['GET', 'POST'])
def chooseRecipeBot():
    nr = request.args.get('nr')
    number = int(nr)
    print(number)
    time.sleep(2)
    return jsonify(chatBotReply=chooseRecipe(number))


#http://127.0.0.1:5000/chat?msg=cooking steps
@app.route('/chat', methods=['GET', 'POST'])
def chatBot():
    message = request.args.get('msg')
    time.sleep(2)
    return jsonify(chatBotReply=chat(message))


if __name__ == '__main__':
    app.run()
