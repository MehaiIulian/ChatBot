from flask import Flask, request, jsonify

from main import getRecipeByIngredients, chooseRecipe, chat

import time

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return "API for delivering recipes to the user! Running now ..."

# http://127.0.0.1:5000/getVegetarianRecipes
@app.route('/getRecipeByIngredients', methods=['GET', 'POST'])
def getVegetarianRecipes():
    time.sleep(2)
    print(getVegetarianRecipes())
    return jsonify(chatBotReply=getVegetarianRecipes())


# http://127.0.0.1:5000/getRecipeByIngredients?ingr=chicken&nr=5
@app.route('/getRecipeByIngredients', methods=['GET', 'POST'])
def getRecipeByIngredientsBot():
    ingredients = request.args.get('ingr');
    number = int(request.args.get('nr'))
    time.sleep(2)
    print(getRecipeByIngredients(ingredients, number))
    return jsonify(chatBotReply=getRecipeByIngredients(ingredients, number))


# http://127.0.0.1:5000/chooseRecipe?nr=5
@app.route('/chooseRecipe', methods=['GET', 'POST'])
def chooseRecipeBot():
    nr = request.args.get('nr')
    number = int(nr)
    print(number)
    time.sleep(2)
    print(chooseRecipe(number))
    return jsonify(chatBotReply=chooseRecipe(number))


# http://127.0.0.1:5000/chat?msg=ingredients
@app.route('/chat', methods=['GET', 'POST'])
def chatBot():
    message = request.args.get('msg')
    time.sleep(2)
    print(chat(message))
    return jsonify(chatBotReply=chat(message))


if __name__ == '__main__':
    app.run()
