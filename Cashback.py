"""
Regras de negocio:
1. Cashback base = 5% sobre o valor final da compra (apos desconto/cupom)
2. Cliente VIP recebe +10% de bonus SOBRE O CASHBACK BASE
3. Ordem de calculo: primeiro o cashback base, depois o bonus VIP
4. Promocao: se o valor final da compra for maior que R$ 500, o cashback e dobrado. Vale para todos os clientes, inclusive VIP

Estrutura:
    Cliente: classe base, com bonus = 0 por padrao
    ClienteVIP: extende Cliente, sobrescreve o bonus (+10%)
    ClientePadrao: extende Cliente, sem sobrescrita (herda bonus = 0)
"""


class Cliente:
#Classe base. Representa um cliente comum (sem bonus de cashback)

    def __init__(self, valor_compra: float, desconto: float):
        self.valor_compra = valor_compra
        self.desconto = desconto

    def calcular_valor_final(self) -> float:
        #Valor da compra apos aplicar o desconto do cupom
        return self.valor_compra * (1 - self.desconto)

    def calcular_cashback_base(self) -> float:
        #Cashback base: 5% sobre o valor final
        return 0.05 * self.calcular_valor_final()

    def calcular_bonus(self) -> float:
        #Bonus adicional de cashback. Cliente padrao nao tem bonus
        return 0.0

    def calcular_cashback(self) -> float:
        #Cashback final, ja considerando bonus e promocao
        base = self.calcular_cashback_base()
        total = base + self.calcular_bonus()  

        if self.calcular_valor_final() > 500:
            total *= 2  #promoção do Diretor Comercial: vale para todos

        return round(total, 2)


class ClienteVIP(Cliente):
    #Cliente VIP: recebe +10% de bonus sobre o cashback base

    def calcular_bonus(self) -> float:
        return 0.10 * self.calcular_cashback_base()


class ClientePadrao(Cliente):
    #Cliente padrao: herda o comportamento base
    pass


if __name__ == "__main__":

    # Q2: cliente VIP, R$600, cupom de 20% off
    # valor_final = 480 (<=500, sem promoção) -> base = 24 -> VIP = 24 * 1.10 = 26.40
    cliente_q2 = ClienteVIP(600, 0.20)
    resultado_q2 = cliente_q2.calcular_cashback()
    print(f"Q2 - VIP, R$600, 20% off => cashback = R$ {resultado_q2:.2f}")
    assert resultado_q2 == 26.40, f"Esperado 26.40, obtido {resultado_q2}"

    # Q3: cliente padrão, R$600, cupom de 10% off
    # valor_final = 540 (>500, dobra) -> base = 27 -> dobrado = 54.00
    cliente_q3 = ClientePadrao(600, 0.10)
    resultado_q3 = cliente_q3.calcular_cashback()
    print(f"Q3 - Padrão, R$600, 10% off => cashback = R$ {resultado_q3:.2f}")
    assert resultado_q3 == 54.00, f"Esperado 54.00, obtido {resultado_q3}"

    # Q4: cliente VIP, R$600, cupom de 15% off (caso do suporte)
    # valor_final = 510 (>500, dobra) -> base = 25.50 -> VIP = 28.05 -> dobrado = 56.10
    cliente_q4 = ClienteVIP(600, 0.15)
    resultado_q4 = cliente_q4.calcular_cashback()
    print(f"Q4 - VIP, R$600, 15% off => cashback = R$ {resultado_q4:.2f}")
    assert resultado_q4 == 56.10, f"Esperado 56.10, obtido {resultado_q4}"

    print("\nTodos os testes passaram!")