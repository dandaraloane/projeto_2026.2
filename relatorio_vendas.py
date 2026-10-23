
class RelatorioVendas:
    def __init__(self, historico, total_vendido, meta_vendas):
        self.historico = historico
        self.total_vendido = total_vendido
        self.meta_vendas = meta_vendas

    def gerar(self):
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
        relatorio += (
            "Pedidos FUNCIONARIO: "
            + str(pedidos_funcionario) + "\n"
        )
        relatorio += "Total vendido: R$ %.2f\n" % self.total_vendido

        if self.total_vendido > self.meta_vendas:
            relatorio += "META ATINGIDA!\n"

        return relatorio
