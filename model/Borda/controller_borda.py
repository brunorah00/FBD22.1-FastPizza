from flask import Flask,    make_response, jsonify, request, Blueprint

from FastPizza.model.Borda.borda import Bordas
from FastPizza.model.Borda.dao_borda import BordaDao

app_borda = Blueprint('borda_blueprint', __name__)
app_name = 'bordas'
dao_borda = BordaDao()

@app_borda.route(f'/{app_name}/', methods=['GET'])
def get_bordass():
    bordas = dao_borda.get_all()
    data = [borda.get_data_dict() for borda in bordas]
    return make_response(jsonify(data))

@app_borda.route(f'/{app_name}/add/', methods=['POST'])
def add_borda():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Bordas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    borda = dao_borda.get_by_placa(data.get('tipo'))

    if borda:
        return make_response('Borda já existe!', 400)

    borda = Bordas(**data)
    ambulancia = dao_borda.salvar(borda)
    return make_response({
        'id': borda.id,
        'tipo': borda.tipo,
    })

@app_borda.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_ambulancia_by_id(id):
    borda = dao_borda.get_by_id(id)
    if not borda:
        return make_response({'Erro': 'Ambulância não encontrada'}, 404)
    data = borda.get_data_dict()
    return make_response(jsonify(data))

@app_borda.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_borda(id):
    borda = dao_borda.get_by_id(id)

    if not borda:
        return make_response({'Erro': 'Id Não existe!'})
    dao_borda.delete_Borda(id)
    return make_response({'Deletado com sucesso': True})

@app_borda.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_borda(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Bordas.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': 'Este campo é obrigatório!'
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)

        oldBorda = dao_borda.get_by_id(id)
        if not oldBorda:
            return make_response({'Erro': 'Id não existe!'})
        newBorda = Bordas(**data)
        dao_borda.update_Borda(newBorda, oldBorda)
        return make_response({'id': oldBorda.id})