import unittest
from unittest.mock import patch, mock_open

from gerenciador_pedidos import GerenciadorPedidos, DadosPedido


class TestGerenciadorPedidos(unittest.TestCase):

    def setUp(self):
        self.gerenciador = GerenciadorPedidos()

        # Simula a abertura do arquivo sem criar pedidos.csv de verdade.
        self.arquivo_mock = mock_open()
        self.patch_open = patch(
            "builtins.open",
            self.arquivo_mock
        )
        self.patch_open.start()
        self.addCleanup(self.patch_open.stop)

    def criar_dados_pedido(
        self,
        nome="Paulo",
        email="paulo@email.com",
        tipo_cliente="COMUM",
        pagamento="PIX",
        parcelas=1,
        rua="Rua A",
        numero=123,
        cidade="Paulista",
        uf="PE",
        cep="53401-000"
    ):
        return DadosPedido(
            nome=nome,
            email=email,
            tipo_cliente=tipo_cliente,
            pagamento=pagamento,
            parcelas=parcelas,
            rua=rua,
            numero=numero,
            cidade=cidade,
            uf=uf,
            cep=cep
        )

    def test_processar_pedido_cep_invalido(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)
        dados = self.criar_dados_pedido(cep="123")

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(resultado, "ERRO: cep invalido")

    def test_processar_pedido_forma_pagamento_invalida(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)
        dados = self.criar_dados_pedido(pagamento="DINHEIRO")

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(
            resultado,
            "ERRO: forma de pagamento invalida"
        )

    def test_processar_pedido_parcelas_invalidas(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)
        dados = self.criar_dados_pedido(
            pagamento="CARTAO",
            parcelas=13
        )

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(resultado, "ERRO: parcelas invalidas")

    def test_processar_pedido_sem_nome(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)
        dados = self.criar_dados_pedido(nome="")

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(resultado, "ERRO: cliente sem nome")

    def test_processar_pedido_email_invalido(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)
        dados = self.criar_dados_pedido(email="email-invalido")

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(resultado, "ERRO: email invalido")

    def test_processar_pedido_vazio(self):
        dados = self.criar_dados_pedido()

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(resultado, "ERRO: pedido vazio")

    def test_processar_pedido_produto_inexistente(self):
        self.gerenciador.adicionar_item("PRODUTO_INVALIDO", 1, 10)
        dados = self.criar_dados_pedido()

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(
            resultado,
            "ERRO: produto inexistente PRODUTO_INVALIDO"
        )

    def test_processar_pedido_estoque_insuficiente(self):
        self.gerenciador.adicionar_item("CANETA", 101, 10)
        dados = self.criar_dados_pedido()

        resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(
            resultado,
            "ERRO: estoque insuficiente CANETA"
        )

    def test_processar_pedido_com_sucesso(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)
        dados = self.criar_dados_pedido()

        with patch("builtins.print") as print_mock:
            resultado = self.gerenciador.processar_pedido(dados)

        self.assertEqual(resultado, "OK: 30.88")
        self.assertEqual(self.gerenciador.estoque["CANETA"], 98)
        self.assertEqual(
            self.gerenciador.historico,
            ["Paulo|COMUM|30.88"]
        )
        self.assertEqual(self.gerenciador.total_vendido, 30.88)
        self.assertEqual(self.gerenciador.itens, [])

        self.arquivo_mock.assert_called_once_with(
            "pedidos.csv",
            "a",
            encoding="utf-8"
        )
        self.arquivo_mock().write.assert_called_once_with(
            "Paulo,paulo@email.com,Rua A, 123 - Paulista/PE,30.88\n"
        )
        print_mock.assert_called_once_with(
            "Email enviado para paulo@email.com"
        )

    def test_estoque_inicial(self):
        self.assertEqual(
            self.gerenciador.estoque,
            {
                "CANETA": 100,
                "CADERNO": 50,
                "MOCHILA": 10,
                "CALCULADORA": 5
            }
        )

    def test_adicionar_item(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)

        self.assertEqual(
            self.gerenciador.itens,
            [["CANETA", "2", "10"]]
        )

    def test_orcamento_cliente_comum(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)

        resultado = self.gerenciador.calcular_orcamento(
            "COMUM",
            "PE"
        )

        self.assertEqual(resultado, 32.5)

    def test_orcamento_cliente_vip(self):
        self.gerenciador.adicionar_item("CANETA", 2, 10)

        resultado = self.gerenciador.calcular_orcamento(
            "VIP",
            "PE"
        )

        self.assertEqual(resultado, 18.0)

    def test_mensagem_promocional_vip(self):
        resultado = self.gerenciador.mensagem_promocional("VIP")

        self.assertEqual(
            resultado,
            "Ofertas exclusivas: 15% em compras acima de R$ 500!"
        )

    def test_mensagem_promocional_tipo_desconhecido(self):
        resultado = self.gerenciador.mensagem_promocional("DESCONHECIDO")

        self.assertEqual(resultado, "")

    def test_verificar_estoque_baixo(self):
        self.gerenciador.estoque["CANETA"] = 2

        with patch("builtins.print"):
            resultado = self.gerenciador.verificar_estoque()

        self.assertEqual(
            resultado,
            ["ALERTA: CANETA com estoque baixo (2)"]
        )

    def test_relatorio_sem_vendas(self):
        resultado = self.gerenciador.gerar_relatorio()

        self.assertIn("=== RELATORIO DE VENDAS ===", resultado)
        self.assertIn("Pedidos VIP: 0", resultado)
        self.assertIn("Pedidos COMUM: 0", resultado)
        self.assertIn("Pedidos FUNCIONARIO: 0", resultado)
        self.assertIn("Total vendido: R$ 0.00", resultado)
        self.assertNotIn("META ATINGIDA!", resultado)


if __name__ == "__main__":
    unittest.main()
