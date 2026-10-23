
from dataclasses import dataclass
from relatorio_vendas import RelatorioVendas


@dataclass
class DadosPedido:
    nome: str
    email: str
    tipo_cliente: str
    pagamento: str
    parcelas: int
    rua: str
    numero: int
    cidade: str
    uf: str
    cep: str


class GerenciadorPedidos:
  
    LIMITE_DESCONTO = 500
    DESCONTO_COMUM = 0.05
    DESCONTO_VIP = 0.15
    DESCONTO_VIP_PADRAO = 0.10
    DESCONTO_FUNCIONARIO = 0.20

    DESCONTO_PIX = 0.05
    TAXA_PARCELAMENTO = 0.0199
    TAXA_BOLETO = 2.5

    LIMITE_FRETE_GRATIS = 300
    FRETE_PADRAO = 39.9
    FRETE_PERNAMBUCO = 12.5
    FRETE_REGIONAL = 22.9

    PARCELAS_MINIMAS = 1
    PARCELAS_SEM_TAXA = 3
    PARCELAS_MAXIMAS = 12

    LIMITE_ESTOQUE_BAIXO = 5
    META_VENDAS = 10000

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
        if (
            tipo_cliente == "COMUM"
            and subtotal > self.LIMITE_DESCONTO
        ):
            return subtotal * self.DESCONTO_COMUM

        elif tipo_cliente == "VIP":
            if subtotal > self.LIMITE_DESCONTO:
                return subtotal * self.DESCONTO_VIP

            return subtotal * self.DESCONTO_VIP_PADRAO

        elif tipo_cliente == "FUNCIONARIO":
            return subtotal * self.DESCONTO_FUNCIONARIO

        return 0

    def _validar_dados_pedido(self, nome, email, cep):
        if not nome:
            return "ERRO: cliente sem nome"

        if "@" not in email:
            return "ERRO: email invalido"

        if not self.itens:
            return "ERRO: pedido vazio"

        cep_limpo = cep.replace("-", "").replace(".", "")

        if len(cep_limpo) != 8 or not cep_limpo.isdigit():
            return "ERRO: cep invalido"

        return None

    def _validar_estoque(self):
        for item in self.itens:
            produto = item[0]
            quantidade = int(item[1])

            if produto not in self.estoque:
                return "ERRO: produto inexistente " + produto

            if self.estoque[produto] < quantidade:
                return "ERRO: estoque insuficiente " + produto

        return None

    def _calcular_frete(self, uf, incluir_ma=False):
        frete = self.FRETE_PADRAO

        if uf == "PE":
            frete = self.FRETE_PERNAMBUCO

        elif incluir_ma and uf == "MA":
            frete = self.FRETE_REGIONAL

        elif uf in ["PB", "AL", "RN", "BA", "SE", "CE", "PI"]:
            frete = self.FRETE_REGIONAL

        return frete

    def adicionar_item(self, produto, qtd, preco):
        self.itens.append([produto, str(qtd), str(preco)])

    def processar_pedido(self, dados: DadosPedido):
        erro_dados = self._validar_dados_pedido(
            dados.nome,
            dados.email,
            dados.cep
        )

        if erro_dados:
            return erro_dados

        erro_estoque = self._validar_estoque()

        if erro_estoque:
            return erro_estoque

        if dados.tipo_cliente not in [
            "COMUM", "VIP", "FUNCIONARIO"
        ]:
            return "ERRO: tipo de cliente desconhecido"

        subtotal = self._calcular_subtotal()

        desconto = self._calcular_desconto(
            subtotal,
            dados.tipo_cliente
        )

        frete = self._calcular_frete(
            dados.uf,
            incluir_ma=True
        )

        if (
            subtotal - desconto > self.LIMITE_FRETE_GRATIS
            or dados.tipo_cliente == "VIP"
        ):
            frete = 0

        total = subtotal - desconto + frete

        if dados.pagamento == "PIX":
            total *= 1 - self.DESCONTO_PIX

        elif dados.pagamento == "BOLETO":
            total += self.TAXA_BOLETO

        elif dados.pagamento == "CARTAO":
            if (
                dados.parcelas < self.PARCELAS_MINIMAS
                or dados.parcelas > self.PARCELAS_MAXIMAS
            ):
                return "ERRO: parcelas invalidas"

            if dados.parcelas > self.PARCELAS_SEM_TAXA:
                total *= (
                    1 + self.TAXA_PARCELAMENTO * dados.parcelas
                )

        else:
            return "ERRO: forma de pagamento invalida"

        total = round(total * 100) / 100

        for item in self.itens:
            produto = item[0]
            quantidade = int(item[1])
            self.estoque[produto] -= quantidade

        endereco = (
            dados.rua + ", " + str(dados.numero)
            + " - " + dados.cidade + "/" + dados.uf
        )

        try:
            with open("pedidos.csv", "a", encoding="utf-8") as arquivo:
                arquivo.write(
                    f"{dados.nome},{dados.email},{endereco},{total:.2f}\n"
                )

        except OSError:
            print("Erro ao gravar pedido no arquivo")

        print("Email enviado para " + dados.email)

        self.historico.append(
            f"{dados.nome}|{dados.tipo_cliente}|{total:.2f}"
        )

        self.total_vendido += total
        self.itens.clear()

        return "OK: %.2f" % total

    def calcular_orcamento(self, tipo_cliente, uf):
        subtotal = self._calcular_subtotal()

        desconto = self._calcular_desconto(
            subtotal,
            tipo_cliente
        )

        frete = self._calcular_frete(uf)

        if (
            subtotal - desconto > self.LIMITE_FRETE_GRATIS
            or tipo_cliente == "VIP"
        ):
            frete = 0

        return round((subtotal - desconto + frete) * 100) / 100

    def gerar_relatorio(self):
        relatorio = RelatorioVendas(
            historico=self.historico,
            total_vendido=self.total_vendido,
            meta_vendas=self.META_VENDAS
        )

        return relatorio.gerar()

    def verificar_estoque(self):
        alertas = []

        for produto, quantidade in self.estoque.items():
            if quantidade < self.LIMITE_ESTOQUE_BAIXO:
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
