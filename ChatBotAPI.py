from random import choice

import numpy
from flask import Flask, request, jsonify

import requests as req

from ChatBot import model, bag_of_words, words, labels, data

import time

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    global id_of_choose_recipe
    global image_of_choose_recipe
    global string_of_recipes

    id_of_choose_recipe = -1
    image_of_choose_recipe = ""
    string_of_recipes = ""

    clear_last_data_of_recipes()
    return "API for delivering recipes to the user! Running now ..."


base_url = "https://api.spoonacular.com/recipes/"
url_get_by_ingredients = "findByIngredients?apiKey="
url_get_by_vegetarian = "random?apiKey="
url_get_ingredients = "ingredientWidget.json?apiKey="
url_get_nutrition = "nutritionWidget.json?apiKey="
url_get_equipment = "equipmentWidget.json?apiKey="
url_get_instructions = "analyzedInstructions?apiKey="
api_key = "bb238c76bf8e4034829176f6fbd152ca"

id_of_choose_recipe = -1
image_of_choose_recipe: str = ""
string_of_recipes: str = ""

id_of_recipes = []
title_of_recipes = []
images_of_recipes = []


def clear_last_data_of_recipes():
    id_of_recipes.clear()
    title_of_recipes.clear()
    images_of_recipes.clear()


@app.route('/get-vegetarian-recipes', methods=['GET', 'POST'])
def send_vegetarian_recipes():
    global string_of_recipes
    clear_last_data_of_recipes()
    string_of_recipes = ""

    print(string_of_recipes)

    response = get_vegetarian_recipes()
    time.sleep(1)
    return jsonify(chatBotReply=response)


def get_vegetarian_recipes():
    global string_of_recipes

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
                image = i["image"]
                images_of_recipes.append(image)

            i = 0
            for j in title_of_recipes:
                i = i + 1
                string_of_recipes = string_of_recipes + str(i) + "." + str(j) + '\n'

            print(string_of_recipes)
            return string_of_recipes

        except (IndexError, KeyError):
            return 0

    except ConnectionError:
        return 10


@app.route('/get-recipe-by-user-ingredients', methods=['GET', 'POST'])
def send_recipes_with_ingredients():
    global string_of_recipes
    clear_last_data_of_recipes()
    string_of_recipes = ""

    print(string_of_recipes)

    ingredients = request.args.get('ingredients')
    number = int(request.args.get('number'))

    response = get_recipes_with_ingredients(ingredients, number)
    time.sleep(1)
    return jsonify(chatBotReply=response)


def get_recipes_with_ingredients(ingredients_, number_):
    global string_of_recipes

    user_ingredients = ingredients_
    user_ingredients = ",".join(user_ingredients.split(" "))

    user_number_of_recipes = number_

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
                    image = json_result[counter]["image"]
                    images_of_recipes.append(image)
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


def get_id_of_recipes():
    return id_of_recipes


def get_title_of_recipes():
    return title_of_recipes


@app.route('/pick-recipe-number', methods=['GET', 'POST'])
def send_choice_of_user():
    global id_of_choose_recipe
    global image_of_choose_recipe
    id_of_choose_recipe = -1
    image_of_choose_recipe = ""

    user_choice = request.args.get('number')

    if user_choice.lower() == "exit" or user_choice.lower() == "quit":
        return jsonify(chatBotReply=-1)

    user_choice = int(user_choice)

    try:
        print(get_id_of_recipes())
        print(get_title_of_recipes())
        print(id_of_recipes)
        id = id_of_recipes[user_choice - 1]
        image = images_of_recipes[user_choice - 1]
        id_of_choose_recipe = id
        image_of_choose_recipe = image
        print(id_of_choose_recipe)
        choice_of_user = "You picked \n" + str(
            title_of_recipes[user_choice - 1]) + '.' + '\n' + "Hope you like it!!\n "
        response = choice_of_user
    except (IndexError, KeyError):
        response = 0

    time.sleep(1)
    return jsonify(chatBotReply=response)


@app.route('/chat-with-bot', methods=['GET', 'POST'])
def send_response_from_bot():
    message = request.args.get('message')

    if message.lower() == "exit" or message.lower() == "quit":
        return jsonify(chatBotReply=-1)
    time.sleep(1)
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
    elif response == "Here is the image!" or response == "Here is the picture!" or response == "Here is the look!":
        return 11
    elif response == "Bye!":
        return -1
    else:
        return 100


def get_specified_info_for_recipe(specific_url):
    global id_of_choose_recipe

    pd = {
        'id': str(id_of_choose_recipe)
    }

    id_r = str(id_of_choose_recipe)

    get_from_url = base_url + id_r + '/' + specific_url + api_key

    rez = req.get(get_from_url, pd)
    json_result = rez.json()

    return json_result


def chat_with_bot(message):
    global string_of_recipes
    global image_of_choose_recipe

    message = str(message)

    res = model.predict([bag_of_words(message, words)])[0]
    results_index = numpy.argmax(res)
    tag = labels[results_index]

    if res[results_index] > 0.80:

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        response = choice(responses)
        option = response_from_bot(response)
        if option == 1 or option == 2 or option == 7:
            return response

        elif option == -1:
            return -1

        elif option == 3:

            try:

                json_result = get_specified_info_for_recipe(url_get_ingredients)
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
                    for j in range(len(ingredients_name)):
                        recipe_ingredients = recipe_ingredients + str(ingredients_weight[i]) + " "
                        recipe_ingredients = recipe_ingredients + " " + str(ingredients_unit[i]) + " "
                        recipe_ingredients = recipe_ingredients + " " + str(ingredients_name[i]) + '\n'
                        i = i + 1

                    print(recipe_ingredients)
                    return recipe_ingredients

                except (KeyError, IndexError):
                    return 0
            except ConnectionError:
                return 10

        elif option == 4:

            try:

                json_result = get_specified_info_for_recipe(url_get_instructions)

                try:
                    i = 0
                    list_of_instructions = ""

                    for j in json_result:
                        instructions = ""
                        step = str(i + 1) + ".Step " + str(json_result[i]["name"])
                        list_of_instructions = list_of_instructions + step + '\n'
                        for k in json_result[i]['steps']:
                            steps = k['step']
                            instruction_to = steps.split(".")

                            for l in instruction_to:
                                if not l:
                                    continue

                                l = l.strip(' ')

                                s_step = " > " + l + "."
                                instructions = instructions + s_step + '\n'

                        list_of_instructions = list_of_instructions + instructions + '\n'
                        i = i + 1

                    print(list_of_instructions)
                    return list_of_instructions
                except (KeyError, IndexError):
                    return 0

            except ConnectionError:
                return 10

        elif option == 5:

            try:
                json_result = get_specified_info_for_recipe(url_get_nutrition)

                try:
                    calories_r = str(json_result["calories"])
                    calories = "calories:" + calories_r + '\n'
                    carbs_r = str(json_result["carbs"])
                    carbs = "carbs:" + carbs_r + '\n'
                    fat_r = str(json_result["fat"])
                    fat = "fat:" + fat_r + '\n'
                    protein_r = str(json_result["protein"])
                    protein = "protein:" + protein_r + '\n'
                    nutrition = calories + carbs + fat + protein
                    print(nutrition)
                    return nutrition
                except (IndexError, KeyError):
                    return 0

            except ConnectionError:
                return 10

        elif option == 6:

            try:
                json_result = get_specified_info_for_recipe(url_get_equipment)

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

        elif option == 8:
            clear_last_data_of_recipes()
            global string_of_recipes
            global id_of_choose_recipe
            global image_of_choose_recipe
            string_of_recipes = ""
            image_of_choose_recipe = ""
            id_of_choose_recipe = -1
            return 1

        elif option == 9:
            string = "Welcome (back) to the overview:"
            string_of_recipes = ""
            i = 0
            for j in title_of_recipes:
                i = i + 1
                string_of_recipes = string_of_recipes + str(i) + "." + str(j) + '\n'

            if string_of_recipes == "":
                return 0
            overview_message = string + '\n' + string_of_recipes

            print(string_of_recipes)

            print(overview_message)
            return overview_message

        elif option == 11:

            return image_of_choose_recipe

    else:
        response = "I am not sure what you want to do. Can you rephrase your question?"
        return response


if __name__ == '__main__':
    app.run()
