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

**Testes:** Executar os 17 testes automatizados após a alteração e registrar o resultado.

**Resultado esperado:** Redução da duplicação e maior facilidade de manutenção, preservando o comportamento anterior.

## Refatoração 4 — Extração da validação dos dados do pedido

**Code smell identificado:** Long Method (método longo).

**Problema encontrado:** O método `processar_pedido()` realizava diretamente as validações de nome, e-mail, existência de itens e formato do CEP, acumulando responsabilidades.

**Refatoração realizada:** Foi criado o método `_validar_dados_pedido()`, responsável por essas verificações e pelo retorno das mensagens de erro correspondentes.

**Princípio SOLID relacionado:** SRP (Single Responsibility Principle — Princípio da Responsabilidade Única), pois a validação dos dados foi separada do processamento do pedido.

**Testes:** Registrar o resultado da execução dos 17 testes automatizados após a alteração.

**Resultado esperado:** Código mais organizado, com validações centralizadas e comportamento anterior preservado.
