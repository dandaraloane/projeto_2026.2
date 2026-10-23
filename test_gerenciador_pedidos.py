
import unittest
from gerenciador_pedidos import GerenciadorPedidos
from unittest.mock import mock_open, patch
from contextlib import redirect_stdout
import io

class TestGerenciadorPedidos(unittest.TestCase):

    
    def test_processar_pedido_cep_invalido(self):
        self.gerenciador.adicionar_item("CANETA", 1, 10)

        resultado = self.gerenciador.processar_pedido(
            "Paulo", "teste@email.com", "COMUM", "PIX", 1,
            "Rua A", "10", "Paulista", "PE", "123"
        )

        self.assertEqual(resultado, "ERRO: cep invalido")

    def test_processar_pedido_forma_pagamento_invalida(self):
        self.gerenciador.adicionar_item("CANETA", 1, 10)

        resultado = self.gerenciador.processar_pedido(
            "Paulo", "teste@email.com", "COMUM", "DINHEIRO", 1,
            "Rua A", "10", "Paulista", "PE", "53401-000"
        )

        self.assertEqual(
            resultado, "ERRO: forma de pagamento invalida"
        )

    def test_processar_pedido_parcelas_invalidas(self):
        self.gerenciador.adicionar_item("CANETA", 1, 10)

        resultado = self.gerenciador.processar_pedido(
            "Paulo", "teste@email.com", "COMUM", "CARTAO", 13,
            "Rua A", "10", "Paulista", "PE", "53401-000"
        )

        self.assertEqual(resultado, "ERRO: parcelas invalidas")


    def test_processar_pedido_sem_nome(self):
        resultado = self.gerenciador.processar_pedido(
            "", "teste@email.com", "COMUM", "PIX", 1,
            "Rua A", "10", "Paulista", "PE", "53401-000"
        )

        self.assertEqual(resultado, "ERRO: cliente sem nome")

    def test_processar_pedido_email_invalido(self):
        resultado = self.gerenciador.processar_pedido(
            "Paulo", "emailinvalido", "COMUM", "PIX", 1,
            "Rua A", "10", "Paulista", "PE", "53401-000"
        )

        self.assertEqual(resultado, "ERRO: email invalido")

    def test_processar_pedido_vazio(self):
        resultado = self.gerenciador.processar_pedido(
            "Paulo", "teste@email.com", "COMUM", "PIX", 1,
            "Rua A", "10", "Paulista", "PE", "53401-000"
        )

        self.assertEqual(resultado, "ERRO: pedido vazio")

    def test_processar_pedido_produto_inexistente(self):
        self.gerenciador.adicionar_item("TECLADO", 1, 50)

        resultado = self.gerenciador.processar_pedido(
            "Paulo", "teste@email.com", "COMUM", "PIX", 1,
            "Rua A", "10", "Paulista", "PE", "53401-000"
        )

        self.assertEqual(
            resultado, "ERRO: produto inexistente TECLADO"
        )

    def test_processar_pedido_estoque_insuficiente(self):
        self.gerenciador.adicionar_item("CANETA", 101, 2)

        resultado = self.gerenciador.processar_pedido(
            "Paulo", "teste@email.com", "COMUM", "PIX", 1,
            "Rua A", "10", "Paulista", "PE", "53401-000"
        )

        self.assertEqual(
            resultado, "ERRO: estoque insuficiente CANETA"

        )
        
    def test_processar_pedido_com_sucesso(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)

        with patch("builtins.open", mock_open()):
            with redirect_stdout(io.StringIO()):
                resultado = self.gerenciador.processar_pedido(
                    "Paulo", "teste@email.com", "COMUM", "PIX", 1,
                    "Rua A", "10", "Paulista", "PE", "53401-000"
                )

        self.assertEqual(resultado, "OK: 30.88")
        self.assertEqual(self.gerenciador.estoque["CANETA"], 98)
        self.assertEqual(
            self.gerenciador.historico,
            ["Paulo|COMUM|30.88"]
        )
        self.assertEqual(self.gerenciador.total_vendido, 30.88)
        self.assertEqual(self.gerenciador.itens, [])


    def setUp(self):
        self.gerenciador = GerenciadorPedidos()

    def test_estoque_inicial(self):
        self.assertEqual(self.gerenciador.estoque["CANETA"], 100)
        self.assertEqual(self.gerenciador.estoque["CADERNO"], 50)
        self.assertEqual(self.gerenciador.estoque["MOCHILA"], 10)
        self.assertEqual(self.gerenciador.estoque["CALCULADORA"], 5)

    def test_adicionar_item(self):
        self.gerenciador.adicionar_item("CANETA", 2, 3.50)

        self.assertEqual(
            self.gerenciador.itens,
            [["CANETA", "2", "3.5"]]
        )

    def test_orcamento_cliente_comum(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)

        resultado = self.gerenciador.calcular_orcamento(
            "COMUM", "PE"
        )

        self.assertEqual(resultado, 32.5)

    def test_orcamento_cliente_vip(self):
        self.gerenciador.adicionar_item("CANETA", 10, 10)

        resultado = self.gerenciador.calcular_orcamento(
        "VIP", "PE"
     )

        self.assertEqual(resultado, 90.0)

    def test_mensagem_promocional_vip(self):
        resultado = self.gerenciador.mensagem_promocional("VIP")

        self.assertEqual(
            resultado,
            "Ofertas exclusivas: 15% em compras acima de R$ 500!"
        )

    def test_mensagem_promocional_tipo_desconhecido(self):
        resultado = self.gerenciador.mensagem_promocional("OUTRO")

        self.assertEqual(resultado, "")

    def test_verificar_estoque_baixo(self):
        self.gerenciador.estoque["CANETA"] = 4

        resultado = self.gerenciador.verificar_estoque()

        self.assertIn(
            "ALERTA: CANETA com estoque baixo (4)",
            resultado
        )

    def test_relatorio_sem_vendas(self):
        resultado = self.gerenciador.gerar_relatorio()

        self.assertIn("=== RELATORIO DE VENDAS ===", resultado)
        self.assertIn("Pedidos VIP: 0", resultado)
        self.assertIn("Pedidos COMUM: 0", resultado)
        self.assertIn("Pedidos FUNCIONARIO: 0", resultado)
        self.assertIn("Total vendido: R$ 0.00", resultado)


if __name__ == "__main__":
    unittest.main()
