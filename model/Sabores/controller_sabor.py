from flask import Flask,    make_response, jsonify, request, Blueprint

from model.Sabores.sabor import Sabores
from model.Sabores.dao_sabor import SaborDao


app_sabor = Blueprint('sabor_blueprint', __name__)
app_name = 'sabores'
dao_sabor = SaborDao()

@app_sabor.route(f'/{app_name}/', methods=['GET'])
def get_sabores():
    sabores = dao_sabor.get_all()
    data = [sabor.get_data_dict() for sabor in sabores]
    return make_response(jsonify(data))

@app_sabor.route(f'/{app_name}/add/', methods=['POST'])
def add_sabor():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Sabores.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    sabor = dao_sabor.get_by_name(data.get('name'))

    if sabor:
        return make_response('Sabor já existe!', 400)

    sabor = Sabores(**data)
    sabor = dao_sabor.salvar(sabor)
    return make_response({
        'id': sabor.id,
        'name': sabor.name,
    })

@app_sabor.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_sabor_by_id(id):
    sabor = dao_sabor.get_by_id(id)
    if not sabor:
        return make_response({'Erro': 'Sabor não encontrada'}, 404)
    data = sabor.get_data_dict()
    return make_response(jsonify(data))

@app_sabor.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_sabor(id):
    sabor = dao_sabor.get_by_id(id)

    if not sabor:
        return make_response({'Erro': 'Id Não existe!'})
    dao_sabor.delete_Sabor(id)
    return make_response({'Deletado com sucesso': True})

@app_sabor.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_sabor(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Sabores.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': 'Este campo é obrigatório!'
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)

        oldSabor = dao_sabor.get_by_id(id)
        if not oldSabor:
            return make_response({'Erro': 'Id não existe!'})
        newSabor = Sabores(**data)
        dao_sabor.update_Sabor(newSabor, oldSabor)
        return make_response({'id': oldSabor.id})