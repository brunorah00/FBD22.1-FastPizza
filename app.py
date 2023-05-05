from flask import Flask

from model.Pedido.controller_pedido import app_pedido
from model.Sabores.controller_sabor import app_sabor
from model.Massa.controller_massa import app_massa
from model.Pizzas.controller_pizza import app_pizza
from model.Status.controller_status import app_statu
from model.Borda.controller_borda import app_borda

app = Flask(__name__)

app.register_blueprint(app_pedido)
app.register_blueprint(app_sabor)
app.register_blueprint(app_massa)
app.register_blueprint(app_pizza)
app.register_blueprint(app_statu)
app.register_blueprint(app_borda)

if __name__ == '__main__':
    app.run(debug=True)