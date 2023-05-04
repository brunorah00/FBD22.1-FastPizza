from flask import Flask,    make_response, jsonify, request, Blueprint

from model.Status.status import Status
from model.Status.dao_status import StatuDao

app_statu = Blueprint('status_blueprint', __name__)
app_name = 'status'
dao_statu = StatuDao()

@app_statu.route(f'/{app_name}/', methods=['GET'])
def get_status():
    status = dao_statu.get_all()
    data = [statu.get_data_dict() for statu in status]
    return make_response(jsonify(data))

@app_statu.route(f'/{app_name}/add/', methods=['POST'])
def add_statu():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Status.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

        if erros:
            return make_response({
                'erros': erros
            }, 400)

    statu = dao_statu.get_by_tipo(data.get('tipo'))

    if statu:
        return make_response('Status já existe!', 400)

    statu = Status(**data)
    statu = dao_statu.salvar(statu)
    return make_response({
        'id': statu.id,
        'tipo': statu.tipo,
    })

@app_statu.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_statu_by_id(id):
    statu = dao_statu.get_by_id(id)
    if not statu:
        return make_response({'Erro': 'Status não encontrada'}, 404)
    data = statu.get_data_dict()
    return make_response(jsonify(data))

@app_statu.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_statu(id):
    statu = dao_statu.get_by_id(id)

    if not statu:
        return make_response({'Erro': 'Id Não existe!'})
    dao_statu.delete_Statu(id)
    return make_response({'Deletado com sucesso': True})

@app_statu.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_statu(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Status.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': 'Este campo é obrigatório!'
            })
        if erros:
            return make_response({
                'erros': erros
            }, 400)

        oldStatu = dao_statu.get_by_id(id)
        if not oldStatu:
            return make_response({'Erro': 'Id não existe!'})
        newStatu = Status(**data)
        dao_statu.update_Statu(newStatu, oldStatu)
        return make_response({'id': oldStatu.id})