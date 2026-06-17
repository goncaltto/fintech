from flask import Flask, request, jsonify
from cashback import ClienteVIP, ClientePadrao

app = Flask(__name__)


@app.route("/cashback", methods=["POST"])
def calc_cashback   ():
    """
    Recebe JSON no formato:
    {
        "tipo_cliente": "vip" | "padrao",
        "valor_compra": 600.0,
        "desconto": 0.15
    }
    Retorna o cashback calculado.
    """
    dados = request.get_json()

    valor_compra = dados.get("valor_compra")
    desconto = dados.get("desconto", 0)
    tipo_cliente = dados.get("tipo_cliente", "padrao")

    if valor_compra is None:
        return jsonify({"erro": "valor_compra é obrigatório"}), 400

    if tipo_cliente.lower() == "vip":
        cliente = ClienteVIP(valor_compra, desconto)
    else:
        cliente = ClientePadrao(valor_compra, desconto)

    resultado = cliente.calcular_cashback()

    return jsonify({
        "tipo_cliente": tipo_cliente,
        "valor_compra": valor_compra,
        "desconto": desconto,
        "cashback": resultado
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)