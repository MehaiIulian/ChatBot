
import requests as req

id_of_choose_recipe= 776505

base_url = "https://api.spoonacular.com/recipes/"
url_get_by_ingredients = "findByIngredients?apiKey="
url_get_by_vegetarian = "random?apiKey="
url_get_ingredients = "ingredientWidget.json?apiKey="
url_get_nutrition = "nutritionWidget.json?apiKey="
url_get_equipment = "equipmentWidget.json?apiKey="
url_get_instructions = "analyzedInstructions?apiKey="
api_key = "bb238c76bf8e4034829176f6fbd152ca"

def get_specified_info_for_recipe(specific_url):
    pd = {
        'id': str(id_of_choose_recipe)
    }

    id_r = str(id_of_choose_recipe)

    get_from_url = base_url + id_r + '/' + specific_url + api_key

    rez = req.get(get_from_url, pd)
    json_result = rez.json()

    return json_result


def test():
    url = url_get_instructions

    json_result = get_specified_info_for_recipe(url)

    i = 0
    list_of_instructions = ""

    for j in json_result:
        instructions = ""
        step = str(json_result[i]["name"])
        list_of_instructions = "too cook it ..." + list_of_instructions + step + '\n'
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
    return list_of_instructions

print(test())
