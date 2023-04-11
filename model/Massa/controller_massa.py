from flask import Flask,    make_response, jsonify, request, Blueprint

from FastPizza.model.Massa.massa import Massas
from FastPizza.model.Massa.dao_massa import MassaDao

app_massa = Blueprint('massa_blueprint', __name__)
app_name = 'massas'
dao_massa = MassaDao()

@app_massa.route(f'/{app_name}/', methods=['GET'])
def get_massas():
    massas = dao_massa.get_all()
    data = [massa.get_data_dict() for massa in massas]
    return make_response(jsonify(data))

@app_massa.route(f'/{app_name}/add/', methods=['POST'])
def add_massa():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Massas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    massa = dao_massa.get_by_tipo(data.get('tipo'))

    if massa:
        return make_response('Massa já existe!', 400)

    massa = Massas(**data)
    massa = dao_massa.salvar(massa)
    return make_response({
        'id': massa.id,
        'tipo': massa.tipo,
    })

@app_massa.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_massa_by_id(id):
    massa = dao_massa.get_by_id(id)
    if not massa:
        return make_response({'Erro': 'Massa não encontrada'}, 404)
    data = massa.get_data_dict()
    return make_response(jsonify(data))

@app_massa.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_massa(id):
    massa = dao_massa.get_by_id(id)

    if not massa:
        return make_response({'Erro': 'Id Não existe!'})
    dao_massa.delete_Massa(id)
    return make_response({'Deletado com sucesso': True})

@app_massa.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_massa(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Massas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': 'Este campo é obrigatório!'
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)

        oldMassa = dao_massa.get_by_id(id)
        if not oldMassa:
            return make_response({'Erro': 'Id não existe!'})
        newMassa = Massas(**data)
        dao_massa.update_Massa(newMassa, oldMassa)
        return make_response({'id': oldMassa.id})