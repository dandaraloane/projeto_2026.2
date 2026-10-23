
import unittest
from relatorio_vendas import RelatorioVendas


class TestRelatorioVendas(unittest.TestCase):

    def test_gerar_relatorio_sem_vendas(self):
        relatorio = RelatorioVendas(
            historico=[],
            total_vendido=0,
            meta_vendas=10000
        )

        resultado = relatorio.gerar()

        self.assertIn("Pedidos VIP: 0", resultado)
        self.assertIn("Pedidos COMUM: 0", resultado)
        self.assertIn("Pedidos FUNCIONARIO: 0", resultado)
        self.assertIn("Total vendido: R$ 0.00", resultado)
        self.assertNotIn("META ATINGIDA!", resultado)

    def test_contar_pedidos_por_tipo_de_cliente(self):
        historico = [
            "Ana|VIP|150.00",
            "Bruno|COMUM|80.00",
            "Carlos|FUNCIONARIO|50.00",
            "Diana|VIP|200.00"
        ]

        relatorio = RelatorioVendas(
            historico=historico,
            total_vendido=480,
            meta_vendas=10000
        )

        resultado = relatorio.gerar()

        self.assertIn("Pedidos VIP: 2", resultado)
        self.assertIn("Pedidos COMUM: 1", resultado)
        self.assertIn("Pedidos FUNCIONARIO: 1", resultado)
        self.assertIn("Cliente: Ana - Tipo: VIP - Total: R$ 150.00", resultado)

    def test_exibir_mensagem_quando_meta_for_atingida(self):
        relatorio = RelatorioVendas(
            historico=[],
            total_vendido=10000.01,
            meta_vendas=10000
        )

        resultado = relatorio.gerar()

        self.assertIn("META ATINGIDA!", resultado)


if __name__ == "__main__":
    unittest.main()
