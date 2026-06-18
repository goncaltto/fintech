from flask import Flask, request, jsonify
from flask_cors import CORS
from cashback import ClienteVIP, ClientePadrao
from db import get_connection

app = Flask(__name__)
CORS(app)


def salvar_consulta(ip, tipo_cliente, valor_compra, desconto, cashback):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO consultas (ip, tipo_cliente, valor_compra, desconto, cashback)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (ip, tipo_cliente, valor_compra, desconto, cashback),
    )
    conn.commit()
    cursor.close()
    conn.close()


@app.route("/cashback", methods=["POST"])
def calc_cashback():
    """
    Recebe JSON no formato:
    {
        "tipo_cliente": "vip" | "padrao",
        "valor_compra": 600.0,
        "desconto": 0.15
    }
    Retorna o cashback calculado e salva a consulta no banco.
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

    ip_usuario = request.remote_addr
    salvar_consulta(ip_usuario, tipo_cliente, valor_compra, desconto, resultado)

    return jsonify({
        "tipo_cliente": tipo_cliente,
        "valor_compra": valor_compra,
        "desconto": desconto,
        "cashback": resultado,
    })


@app.route("/historico", methods=["GET"])
def historico():
    ip_usuario = request.remote_addr

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT tipo_cliente, valor_compra, desconto, cashback, criado_em
        FROM consultas
        WHERE ip = %s
        ORDER BY criado_em DESC
        """,
        (ip_usuario,),
    )
    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    for r in registros:
        r["criado_em"] = r["criado_em"].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(registros)


if __name__ == "__main__":
    app.run(debug=True, port=5000)