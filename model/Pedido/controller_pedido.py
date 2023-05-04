from flask import Flask, make_response, jsonify, request, Blueprint
from model.Pedido.pedido import Pedido
from model.Pedido.dao_pedido import PedidoDao

app_pedido = Blueprint('pedido_blueprint', __name__)
app_name = 'pedidos'
dao_pedido = PedidoDao()

@app_pedido.route(f'/{app_name}/', methods=['GET'])
def get_pedidos():
    pedidos = dao_pedido.get_all()
    data = [pedido.get_data_dict() for pedido in pedidos]
    return make_response(jsonify(data))

@app_pedido.route(f'/{app_name}/add/', methods=['POST'])
def add_pedido():
    data = request.form.to_dict(flat=True)

    erros = []
    for key in Pedido.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': "Este campo é obrigatório"
            })

    if erros:
        return make_response({
            'erros': erros
        }, 400)

    pedido = Pedido(**data)
    pedido = dao_pedido.salvar(pedido)
    return make_response({
        'id': pedido.id,
        'pizza_id': pedido.pizza_id,
    })

@app_pedido.route(f'/{app_name}/<int:id>', methods=['GET'])
def get_pedido_by_id(id):
    pedido = dao_pedido.get_by_id(id)
    if not pedido:
        return make_response({'Erro': 'Pedido não encontrado'}, 404)
    data = pedido.get_data_dict()
    return make_response(jsonify(data))

@app_pedido.route(f'/{app_name}/delete/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    pedido = dao_pedido.get_by_id(id)

    if not pedido:
        return make_response({'Erro': 'ID não existe!'})
    dao_pedido.delete_pedido(id)
    return make_response({'Deletado com sucesso': True})

@app_pedido.route(f'/{app_name}/update/<int:id>', methods=['PUT'])
def update_pedido(id):
    data = request.form.to_dict(flat=True)
    erros = []

    for key in Pedido.campos_validacao:
        if key not in data.keys():
            erros.append({
                'coluna': key,
                'message': 'Este campo é obrigatório!'
            })
    if erros:
        return make_response({
            'erros': erros
        }, 400)

    oldPedido = dao_pedido.get_by_id(id)
    if not oldPedido:
        return make_response({'Erro': 'ID não existe!'})
    newPedido = Pedido(**data)
    dao_pedido.update_pedido(newPedido, oldPedido)
    return make_response({'id': oldPedido.id})
