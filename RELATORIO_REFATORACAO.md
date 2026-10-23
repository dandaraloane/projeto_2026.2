# Relatório de Refatoração — Gerenciador de Pedidos

## Refatoração 1 — Extração dos cálculos de subtotal e desconto

**Code smell identificado:** Código duplicado (Duplicated Code).

**Problema encontrado:** Os cálculos de subtotal e desconto estavam repetidos nos métodos `processar_pedido()` e `calcular_orcamento()`, dificultando a manutenção e aumentando a possibilidade de inconsistências.

**Refatoração realizada:** Foram criados os métodos `_calcular_subtotal()` e `_calcular_desconto()`, centralizando os cálculos e permitindo que os dois métodos reutilizem a mesma lógica.

**Princípio SOLID relacionado:** SRP (Single Responsibility Principle — Princípio da Responsabilidade Única), pois os cálculos foram separados em métodos específicos.

**Testes:** Os 17 testes automatizados foram executados após a alteração e passaram com sucesso.

**Resultado:** A duplicação dos cálculos foi reduzida, facilitando a manutenção do código e preservando o comportamento esperado.

## Refatoração 2 — Extração da validação de estoque

**Code smell identificado:** Long Method (método longo).

**Problema encontrado:** O método `processar_pedido()` acumulava várias responsabilidades, incluindo a verificação da existência dos produtos e a validação da quantidade disponível no estoque.

**Refatoração realizada:** Foi criado o método `_validar_estoque()`, responsável por verificar se os produtos existem no estoque e se há quantidade suficiente para atender ao pedido.

**Princípio SOLID relacionado:** SRP (Single Responsibility Principle — Princípio da Responsabilidade Única), pois a validação de estoque passou a ter um método próprio.

**Testes:** Após a alteração, os 17 testes automatizados foram executados novamente e passaram com sucesso.

**Resultado:** O método `processar_pedido()` ficou mais organizado, e a validação de estoque tornou-se mais fácil de compreender e manter.

## Resumo dos testes

| Etapa | Testes executados | Resultado |
|---|---:|---|
| Refatoração 1 | 17 | Todos passaram |
| Refatoração 2 | 17 | Todos passaram |

## Refatoração 3 — Extração do cálculo de frete

**Code smell identificado:** Código duplicado (Duplicated Code).

**Problema encontrado:** A lógica de cálculo do frete estava repetida nos métodos `processar_pedido()` e `calcular_orcamento()`.

**Refatoração realizada:** Foi criado o método `_calcular_frete()`, centralizando as regras de cálculo do frete em um único local. O parâmetro `incluir_ma` preserva a diferença de comportamento existente para o estado do Maranhão.

**Princípio SOLID relacionado:** SRP (Single Responsibility Principle — Princípio da Responsabilidade Única), pois o cálculo do frete passou a ter um método específico.

**Testes:** Os 17 testes automatizados foram executados e passaram com sucesso.

**Resultado esperado:** Redução da duplicação e maior facilidade de manutenção, preservando o comportamento anterior.

## Refatoração 4 — Extração da validação dos dados do pedido

**Code smell identificado:** Long Method (método longo).

**Problema encontrado:** O método `processar_pedido()` realizava diretamente as validações de nome, e-mail, existência de itens e formato do CEP, acumulando responsabilidades.

**Refatoração realizada:** Foi criado o método `_validar_dados_pedido()`, responsável por essas verificações e pelo retorno das mensagens de erro correspondentes.

**Princípio SOLID relacionado:** SRP (Single Responsibility Principle — Princípio da Responsabilidade Única), pois a validação dos dados foi separada do processamento do pedido.

**Testes:** Os 17 testes automatizados foram executados e passaram com sucesso.
**Resultado esperado:** Código mais organizado, com validações centralizadas e comportamento anterior preservado.

## Refatoração 5 — Substituição de números mágicos por constantes

**Code smell identificado:** Números mágicos (*Magic Numbers*).

**Problema encontrado:** O código utilizava valores numéricos diretamente nas regras de negócio, como `500` para o limite de desconto, `0.05` para o desconto no pagamento via PIX, `0.0199` para a taxa de parcelamento e `300` para o limite de frete grátis. Esses valores dificultavam a compreensão das regras e tornavam alterações futuras menos práticas.

**Refatoração realizada:** Foram criadas constantes com nomes descritivos para representar os valores utilizados nas regras de negócio, como `LIMITE_DESCONTO`, `DESCONTO_PIX`, `TAXA_PARCELAMENTO` e `LIMITE_FRETE_GRATIS`. Os valores correspondentes foram substituídos pelas constantes nos métodos responsáveis pelos cálculos e pelas verificações.

**Princípio SOLID relacionado:** A refatoração contribui principalmente para a legibilidade e a facilidade de manutenção do código. Sua relação com o princípio SRP (*Single Responsibility Principle — Princípio da Responsabilidade Única*) é indireta, pois a extração de constantes, isoladamente, não constitui uma aplicação direta desse princípio.

**Testes:** Os 17 testes automatizados foram executados e passaram com sucesso.
**Resultado esperado:** Redução do uso de números mágicos, maior clareza nas regras de negócio e facilidade para modificar os valores no futuro, preservando o comportamento anterior.

## Refatoração 6 — Introdução do objeto DadosPedido

**Code smell identificado:** Lista longa de parâmetros (*Long Parameter List*).

**Problema encontrado:** O método `processar_pedido()` recebia dez parâmetros relacionados aos dados de um pedido. Essa quantidade de parâmetros dificultava a leitura, a chamada do método e a manutenção do código.

**Refatoração realizada:** Foi criada a classe `DadosPedido`, utilizando `dataclass`, para agrupar as informações relacionadas ao pedido em um único objeto. O método `processar_pedido()` passou a receber esse objeto, acessando seus atributos conforme necessário.

**Princípio SOLID relacionado:** A alteração contribui para a organização dos dados e facilita a manutenção. Sua relação com o princípio SRP (*Single Responsibility Principle — Princípio da Responsabilidade Única*) é indireta; a introdução de um objeto de dados, isoladamente, não garante a aplicação direta desse princípio.

**Testes:** Os 17 testes automatizados foram executados e passaram com sucesso.

**Resultado:** Redução da quantidade de parâmetros do método `processar_pedido()`, melhoria da legibilidade e manutenção do comportamento observado pelos testes.

## Code smell identificado — Large Class (classe grande)

**Problema encontrado:** A classe `GerenciadorPedidos` concentra diversas responsabilidades, incluindo processamento de pedidos, validação de dados e estoque, gravação de arquivos, geração de relatórios e mensagens promocionais. Essa concentração pode dificultar a manutenção e aumentar o acoplamento entre funcionalidades.

**Refatoração proposta:** Extrair a geração de relatórios para uma classe específica, mantendo em `GerenciadorPedidos` apenas a coordenação necessária para fornecer os dados ao relatório.

**Princípio SOLID relacionado:** SRP (*Single Responsibility Principle* — Princípio da Responsabilidade Única), pois a separação busca atribuir à geração de relatórios uma responsabilidade própria.

**Testes:** Após a extração, executar todos os testes automatizados e adicionar testes para a nova classe de relatórios, verificando que o comportamento anterior foi preservado.

## Refatoração 7 — Extração da geração de relatórios

**Code smell identificado:** Large Class (classe grande).

**Problema encontrado:** A classe `GerenciadorPedidos` concentrava o processamento de pedidos, as validações, o controle de estoque, a gravação de arquivos e a geração de relatórios, reunindo responsabilidades distintas.

**Refatoração realizada:** Foi criada a classe `RelatorioVendas`, responsável pela geração do relatório de vendas. O método `gerar_relatorio()` de `GerenciadorPedidos` passou a delegar essa tarefa à nova classe.

**Princípio SOLID relacionado:** SRP (*Single Responsibility Principle* — Princípio da Responsabilidade Única), pois a geração de relatórios foi separada em uma classe específica.

**Testes:** Registrar a quantidade e o resultado reais da execução de todos os testes após a refatoração.

**Resultado esperado:** Redução das responsabilidades concentradas em `GerenciadorPedidos`, maior organização do código e preservação do formato e do conteúdo do relatório anterior.

## Refatoração 7 — Extração da geração de relatórios

**Code smell identificado:** Large Class (classe grande).

**Problema encontrado:** A classe `GerenciadorPedidos` concentrava várias responsabilidades, incluindo processamento de pedidos, validações, controle de estoque e geração de relatórios.

**Refatoração realizada:** Foi criada a classe `RelatorioVendas`, responsável exclusivamente pela geração do relatório de vendas. O método `gerar_relatorio()` de `GerenciadorPedidos` passou a delegar essa tarefa à nova classe.

**Princípio SOLID relacionado:** SRP (*Single Responsibility Principle* — Princípio da Responsabilidade Única), pois a geração de relatórios foi separada em uma classe específica.

**Testes:** 20 testes executados com sucesso (`OK`), incluindo os testes de caracterização existentes e três novos testes para a classe `RelatorioVendas`.

**Resultado:** Redução das responsabilidades concentradas em `GerenciadorPedidos`, melhor organização do código e preservação do comportamento esperado do relatório de vendas.