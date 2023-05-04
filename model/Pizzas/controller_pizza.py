from flask import Flask, make_response, jsonify, request, Blueprint
from model.Pizzas.pizza import Pizzas
from model.Pizzas.dao_pizza import PizzaDao

app_pizza = Blueprint('pizza_blueprint', __name__)
app_name = 'pizzas'
dao_pizza = PizzaDao()

@app_pizza.route(f'/{app_name}/', methods=['GET'])
def get_pizzas():
    pizzas = dao_pizza.get_all()
    data = [pizza.get_data_dict() for pizza in pizzas]
    return make_response(jsonify(data))

@app_pizza.route(f'/{app_name}/add/', methods=['POST'])
def add_pizza():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Pizzas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

    if erros:
        return make_response({
            'erros': erros
        }, 400)

    pizza = dao_pizza.get_by_id(data.get('id'))

    if pizza:
        return make_response('Pizza já existe!', 400)

    pizza = Pizzas(**data)
    pizza = dao_pizza.salvar(pizza)
    return make_response({
        'id': pizza.id,
        'bordas_id': pizza.bordas_id,
        'massas_id': pizza.massas_id
    })

@app_pizza.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_pizza_by_id(id):
    pizza = dao_pizza.get_by_id(id)
    if not pizza:
        return make_response({'Erro': 'Pizza não encontrada'}, 404)
    data = pizza.get_data_dict()
    return make_response(jsonify(data))

@app_pizza.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_pizza(id):
    pizza = dao_pizza.get_by_id(id)

    if not pizza:
        return make_response({'Erro': 'Id não existe!'})
    dao_pizza.delete_pizza(id)
    return make_response({'Deletado com sucesso': True})

@app_pizza.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_pizza(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Pizzas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': 'Este campo é obrigatório!'
            })
    if erros:
        return make_response({
            'erros': erros
        }, 400)

    oldPizza = dao_pizza.get_by_id(id)
    if not oldPizza:
        return make_response({'Erro': 'Id não existe!'})

    newPizza = Pizzas(**data)
    dao_pizza.update_pizza(newPizza, oldPizza)
    return make_response({'id': oldPizza.id})
