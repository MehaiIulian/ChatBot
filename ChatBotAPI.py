from random import choice

import numpy
from flask import Flask, request, jsonify

import requests as req

# Import necessary data from ChatBot to use for chat
from ChatBot import model, bag_of_words, words, labels, data

import time

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return "API for delivering recipes to the user! Running now ..."


# Defining Spooncular API url's and enpoints to get data
base_url = "https://api.spoonacular.com/recipes/"
url_get_by_ingredients = "findByIngredients?apiKey="
url_get_by_vegetarian = "random?apiKey="
url_get_ingredients = "ingredientWidget.json?apiKey="
url_get_nutrition = "nutritionWidget.json?apiKey="
url_get_equipment = "equipmentWidget.json?apiKey="
url_get_instructions = "analyzedInstructions?apiKey="
api_key = "bb238c76bf8e4034829176f6fbd152ca"

# global variables
id_of_choose_recipe = -1
string_of_recipes = ""

# global arrays to contain information about recipes
id_of_recipes = []
title_of_recipes = []


def clear_last_data_of_recipes():
    id_of_recipes.clear()
    title_of_recipes.clear()


# http://127.0.0.1:5000/get-vegetarian-recipes
@app.route('/get-vegetarian-recipes', methods=['GET', 'POST'])
def send_vegetarian_recipes():
    time.sleep(2)
    print(get_vegetarian_recipes())
    return jsonify(chatBotReply=get_vegetarian_recipes())


def get_vegetarian_recipes():
    global string_of_recipes
    string_of_recipes = ""
    clear_last_data_of_recipes()

    pd = {
        'number': 15,
        'tags': "vegetarian",
        'vegan': False,
        'limitLicense': False
    }

    get_from_url = base_url + url_get_by_vegetarian + api_key

    try:
        rez = req.get(get_from_url, pd)
        json_result = rez.json()
        try:
            for i in json_result["recipes"]:
                title = i["title"]
                title_of_recipes.append(title)
                id = i["id"]
                id_of_recipes.append(id)

            i = 0
            for j in title_of_recipes:
                i = i + 1
                string_of_recipes = string_of_recipes + str(i) + "." + str(j) + '\n'
            return string_of_recipes

        except (IndexError, KeyError):
            return 0

    except ConnectionError:
        return 10


# http://127.0.0.1:5000/get-recipe-by-user-ingredients?ingredients=chicken&number=5
@app.route('/get-recipe-by-user-ingredients', methods=['GET', 'POST'])
def send_recipes_with_ingredients():
    ingredients = request.args.get('ingredients')
    number = int(request.args.get('number'))
    time.sleep(2)
    print(get_recipes_with_ingredients(ingredients, number))
    return jsonify(chatBotReply=get_recipes_with_ingredients(ingredients, number))


def get_recipes_with_ingredients(ingredients, number):
    global string_of_recipes
    string_of_recipes = ""
    clear_last_data_of_recipes()

    user_ingredients = ingredients
    user_ingredients = ",".join(user_ingredients.split(" "))

    user_number_of_recipes = number

    if 1 > user_number_of_recipes or user_number_of_recipes > 15:
        return 1

    else:

        pd = {
            'number': user_number_of_recipes,
            'ingredients': user_ingredients,
            'ranking': 1,
            'fillIngredients': False,
            'limitLicense': False
        }

        get_from_url = base_url + url_get_by_ingredients + api_key

        try:
            rez = req.get(get_from_url, pd)
            json_result = rez.json()

            counter = 0
            for i in json_result:
                try:
                    title = json_result[counter]["title"]
                    title_of_recipes.append(title)
                    id = json_result[counter]["id"]
                    id_of_recipes.append(id)
                    counter = counter + 1

                except (IndexError, KeyError):
                    return 0

            number_of_recipes = len(title_of_recipes)
            if 0 == number_of_recipes:
                return 2

            else:
                i = 0
                for j in title_of_recipes:
                    i = i + 1
                    string_of_recipes = string_of_recipes + str(i) + "." + str(j) + '\n'
                return string_of_recipes

        except ConnectionError:
            return 10


# http://127.0.0.1:5000/pick-recipe-number?number=3
@app.route('/pick-recipe-number', methods=['GET', 'POST'])
def send_choice_of_user():
    user_choice = request.args.get('number')
    user_choice = int(user_choice)
    time.sleep(2)

    global id_of_choose_recipe

    try:
        id = id_of_recipes[user_choice - 1]
        id_of_choose_recipe = id
        print(id_of_choose_recipe)
        choice_of_user = "You picked \n" + str(
            title_of_recipes[user_choice - 1]) + '.' + '\n' + " Hope you like it!!\n "
        response = choice_of_user
    except (IndexError, KeyError):
        response = 0
        response = int(response)

    return jsonify(chatBotReply=response)


# http://127.0.0.1:5000/chat-with-bot?message=hi
@app.route('/chat-with-bot', methods=['GET', 'POST'])
def send_response_from_bot():
    message = request.args.get('message')
    time.sleep(2)
    return jsonify(chatBotReply=chat_with_bot(message))


def response_from_bot(response):
    if response == "Hello!" or response == "Good to see you again!" or response == "Hi there!":
        return 1
    elif response == "I am fine!" or response == "I am good!" or response == "I'm here to help you!":
        return 2
    elif response == "These are the ingredients:" or response == "Here are the ingredients:" or response == "Here is the full list of ingredients":
        return 3
    elif response == "These are the instructions:" or response == "There are the cooking steps:" or response == "This is how you make it:":
        return 4
    elif response == "See the recipe's nutrition information:":
        return 5
    elif response == "Here are the tools you need:" or response == "Here is the equipment you need:":
        return 6
    elif response == "You are welcome!":
        return 7
    elif response == "Here, you can start again with new ingredients:" or response == "Here, you can start again:":
        return 8
    elif response == "Welcome (back) to the overview:" or response == "Welcome (back) to the menu:":
        return 9


def chat_with_bot(message):
    message = str(message)
    if message.lower() == "quit":
        return "quit"
    res = model.predict([bag_of_words(message, words)])[0]
    results_index = numpy.argmax(res)
    tag = labels[results_index]

    # If confidence level is higher 75%, open up the json file, find specific tag and spit out response
    if res[results_index] > 0.75:

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        response = choice(responses)
        option = response_from_bot(response)

        if option == 1:
            return response

        elif option == 2:
            return response

        elif option == 3:

            pd = {
                'id': str(id_of_choose_recipe)
            }

            id = str(id_of_choose_recipe)

            get_from_url = base_url + id + '/' + url_get_ingredients + api_key

            try:
                rez = req.get(get_from_url, pd)
                json_result = rez.json()

                try:
                    ingredients_name = []
                    ingredients_weight = []
                    ingredients_unit = []

                    i = 0
                    for j in json_result["ingredients"]:
                        name = json_result["ingredients"][i]["name"]
                        ingredients_name.append(name)
                        weight = json_result["ingredients"][i]["amount"]["metric"]["value"]
                        ingredients_weight.append(weight)
                        quantity = json_result["ingredients"][i]["amount"]["metric"]["unit"]
                        ingredients_unit.append(quantity)
                        i = i + 1

                    i = 0
                    recipe_ingredients = ""
                    for ingredient in range(len(ingredients_name)):
                        recipe_ingredients = recipe_ingredients + str(ingredients_weight[i]) + " "
                        recipe_ingredients = recipe_ingredients + " " + str(ingredients_unit[i]) + " "
                        recipe_ingredients = recipe_ingredients + " " + str(ingredients_name[i]) + '\n'
                        i = i + 1

                    return recipe_ingredients

                except (KeyError, IndexError):
                    return 0
            except ConnectionError:
                return 10  # Spooncular api error


        elif option == 4:
            pd = {
                'id': str(id_of_choose_recipe)
            }

            id = str(id_of_choose_recipe)

            get_from_url = base_url + id + '/' + url_get_instructions + api_key

            try:
                rez = req.get(get_from_url, pd)
                json_result = rez.json()

                try:
                    i = 0
                    list_of_instructions = ""

                    for j in json_result:
                        instructions = ""
                        step = "Steps " + ":" + str(json_result[i]["name"])
                        list_of_instructions = list_of_instructions + step + '\n'

                        for k in json_result[i]['steps']:
                            steps = k['step']
                            instruction_to = steps.split(".")

                            for l in instruction_to:
                                if not l:
                                    continue
                                if l[0] == " ":
                                    a = l.replace(" ", "", 1)
                                    if a[0] == " ":
                                        b = a.replace(" ", "", 1)
                                        s_step = " - " + str(b) + "."
                                        instructions = instructions + s_step + '\n'
                                    else:
                                        s_step = " - " + str(a) + "."
                                        instructions = instructions + s_step + '\n'
                                else:
                                    s_step = " – " + l + "."
                                    instructions = instructions + s_step + '\n'

                        list_of_instructions = list_of_instructions + instructions + '\n'
                        i = i + 1
                    return list_of_instructions
                except (KeyError, IndexError):
                    return 0


            except ConnectionError:
                return 10  # Spooncular api error

        elif option == 5:
            pd = {
                'id': str(id_of_choose_recipe)
            }

            id = str(id_of_choose_recipe)

            get_from_url = base_url + id + '/' + url_get_nutrition + api_key

            try:
                rez = req.get(get_from_url, pd)
                json_result = rez.json()

                try:
                    calories = "calories:" + str(json_result["calories"]) + '\n'
                    carbs = "carbs:" + str(json_result["carbs"]) + '\n'
                    fat = "fat:" + str(json_result["fat"]) + '\n'
                    protein = "protein:" + str(json_result["protein"]) + '\n'
                    nutrition = calories + carbs + fat + protein
                    return nutrition
                except (IndexError, KeyError):
                    return 0

            except ConnectionError:
                return 10

        elif option == 6:
            pd = {
                'id': str(id_of_choose_recipe)
            }

            id = str(id_of_choose_recipe)

            get_from_url = base_url + id + '/' + url_get_equipment + api_key

            try:
                rez = req.get(get_from_url, pd)
                json_result = rez.json()

                try:
                    equipment = ""
                    for i in json_result["equipment"]:
                        equipment = equipment + str(i.get('name')) + ","

                    equipment_to_use = str(equipment[:-1])
                    print(equipment_to_use)

                    return equipment_to_use

                except (IndexError, KeyError):
                    return 0


            except ConnectionError:
                return 10

        elif option == 7:
            return response

        elif option == 8:
            return 1  # For new ingredients

        elif option == 9:
            string = "Welcome (back) to the overview:"
            return string + '\n' + string_of_recipes
        else:
            return "I am not sure what you want to do. Can you rephrase your question?"


if __name__ == '__main__':
    app.run()
