
class GerenciadorPedidos:
    def __init__(self):
        self.itens = []
        self.estoque = {
            "CANETA": 100,
            "CADERNO": 50,
            "MOCHILA": 10,
            "CALCULADORA": 5
        }
        self.historico = []
        self.total_vendido = 0

    def _calcular_subtotal(self):
        subtotal = 0
        for item in self.itens:
            subtotal += int(item[1]) * float(item[2])
        return subtotal

    def _calcular_desconto(self, subtotal, tipo_cliente):
        if tipo_cliente == "COMUM" and subtotal > 500:
            return subtotal * 0.05
        elif tipo_cliente == "VIP":
            if subtotal > 500:
                return subtotal * 0.15
            return subtotal * 0.10
        elif tipo_cliente == "FUNCIONARIO":
            return subtotal * 0.20
        return 0

    def _validar_estoque(self):
        for item in self.itens:
            produto = item[0]
            quantidade = int(item[1])

            if produto not in self.estoque:
                return "ERRO: produto inexistente " + produto

            if self.estoque[produto] < quantidade:
                return "ERRO: estoque insuficiente " + produto

        return None

    def adicionar_item(self, produto, qtd, preco):
        self.itens.append([produto, str(qtd), str(preco)])

    def processar_pedido(
        self, nome, email, tipo_cliente, pagamento, parcelas,
        rua, numero, cidade, uf, cep
    ):
        if not nome:
            return "ERRO: cliente sem nome"

        if "@" not in email:
            return "ERRO: email invalido"

        if not self.itens:
            return "ERRO: pedido vazio"

        cep_limpo = cep.replace("-", "").replace(".", "")
        if len(cep_limpo) != 8 or not cep_limpo.isdigit():
            return "ERRO: cep invalido"

        erro_estoque = self._validar_estoque()
        if erro_estoque:
            return erro_estoque

        if tipo_cliente not in ["COMUM", "VIP", "FUNCIONARIO"]:
            return "ERRO: tipo de cliente desconhecido"

        subtotal = self._calcular_subtotal()
        desconto = self._calcular_desconto(subtotal, tipo_cliente)

        frete = 39.9
        if uf == "PE":
            frete = 12.5
        elif uf in ["PB", "AL", "RN", "BA", "SE", "CE", "PI", "MA"]:
            frete = 22.9

        if subtotal - desconto > 300 or tipo_cliente == "VIP":
            frete = 0

        total = subtotal - desconto + frete

        if pagamento == "PIX":
            total *= 0.95
        elif pagamento == "BOLETO":
            total += 2.5
        elif pagamento == "CARTAO":
            if parcelas < 1 or parcelas > 12:
                return "ERRO: parcelas invalidas"
            if parcelas > 3:
                total *= 1 + 0.0199 * parcelas
        else:
            return "ERRO: forma de pagamento invalida"

        total = round(total * 100) / 100

        for item in self.itens:
            produto = item[0]
            quantidade = int(item[1])
            self.estoque[produto] -= quantidade

        endereco = (
            rua + ", " + str(numero) + " - " + cidade + "/" + uf
        )

        try:
            with open("pedidos.csv", "a", encoding="utf-8") as arquivo:
                arquivo.write(
                    f"{nome},{email},{endereco},{total:.2f}\n"
                )
        except OSError:
            print("Erro ao gravar pedido no arquivo")

        print("Email enviado para " + email)

        self.historico.append(
            f"{nome}|{tipo_cliente}|{total:.2f}"
        )
        self.total_vendido += total
        self.itens.clear()

        return "OK: %.2f" % total

    def calcular_orcamento(self, tipo_cliente, uf):
        subtotal = self._calcular_subtotal()
        desconto = self._calcular_desconto(subtotal, tipo_cliente)

        frete = 39.9
        if uf == "PE":
            frete = 12.5
        elif uf in ["PB", "AL", "RN", "BA", "SE", "CE", "PI"]:
            frete = 22.9

        if subtotal - desconto > 300 or tipo_cliente == "VIP":
            frete = 0

        return round((subtotal - desconto + frete) * 100) / 100

    def gerar_relatorio(self):
        relatorio = "=== RELATORIO DE VENDAS ===\n"
        pedidos_vip = 0
        pedidos_comum = 0
        pedidos_funcionario = 0

        for registro in self.historico:
            partes = registro.split("|")
            nome = partes[0]
            tipo_cliente = partes[1]
            total = partes[2]

            if tipo_cliente == "VIP":
                pedidos_vip += 1
            elif tipo_cliente == "COMUM":
                pedidos_comum += 1
            elif tipo_cliente == "FUNCIONARIO":
                pedidos_funcionario += 1

            relatorio += (
                "Cliente: " + nome
                + " - Tipo: " + tipo_cliente
                + " - Total: R$ " + total + "\n"
            )

        relatorio += "===========================\n"
        relatorio += "Pedidos VIP: " + str(pedidos_vip) + "\n"
        relatorio += "Pedidos COMUM: " + str(pedidos_comum) + "\n"
        relatorio += "Pedidos FUNCIONARIO: " + str(pedidos_funcionario) + "\n"
        relatorio += "Total vendido: R$ %.2f\n" % self.total_vendido

        if self.total_vendido > 10000:
            relatorio += "META ATINGIDA!\n"

        return relatorio

    def verificar_estoque(self):
        alertas = []

        for produto, quantidade in self.estoque.items():
            if quantidade < 5:
                alerta = (
                    "ALERTA: " + produto
                    + " com estoque baixo (" + str(quantidade) + ")"
                )
                alertas.append(alerta)
                print("Email de reposição: " + alerta)

        return alertas

    def mensagem_promocional(self, tipo_cliente):
        if tipo_cliente == "VIP":
            return "Ofertas exclusivas: 15% em compras acima de R$ 500!"
        elif tipo_cliente == "COMUM":
            return "Confira nossas ofertas da semana!"
        elif tipo_cliente == "FUNCIONARIO":
            return "Aproveite seu desconto de funcionário!"
        else:
            return ""
