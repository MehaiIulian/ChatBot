import requests as req

# Defining Spooncular API url's and enpoints to get data
base_url = "https://api.spoonacular.com/recipes/"
url_get_by_ingredients = "findByIngredients?apiKey="
url_get_by_vegetarian = "random?apiKey="
url_get_ingredients = "ingredientWidget.json?apiKey="
url_get_nutrition = "nutritionWidget.json?apiKey="
url_get_equipment = "equipmentWidget.json?apiKey="
url_get_instructions = "analyzedInstructions?apiKey="
api_key = "66574f61969e49d5b6c7d29f644b41d5"

id_of_choose_recipe = 639553
def test():
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

test()