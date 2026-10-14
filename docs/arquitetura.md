Arquitetura do Sistema

1. Visão geral

O sistema tem como objetivo auxiliar os estudantes universitários na organização de suas rotinas acadêmicas, permitindo visualizar aulas, cadastrar lembretes, acompanhar prazos importantes e receber notificações sobre compromissos próximos.

A arquitetura foi definida considerando os requisitos funcionais e não funcionais identificados nas entregas anteriores, buscando garantir que o sistema seja simples de utilizar, rápido, seguro e confiável.

2. Atributos de qualidade

Foram definidos cinco atributos de qualidade considerados importantes para o funcionamento do sistema, considerando as necessidades dos estudantes e os requisitos não funcionais já documentados.

Atributo de qualidade

Justificativa

Métrica verificável

Desempenho

O estudante precisa acessar rapidamente as informações das aulas e dos lembretes.

A tela principal deve carregar em até 3 segundos em conexões 4G/Wi-Fi, conforme o RNF-01.

Usabilidade

O sistema deve permitir que o estudante cadastre seus compromissos sem dificuldades.

O cadastro de um lembrete deve ser concluído em até 1 minuto, sem treinamento prévio, conforme o RNF-02.

Disponibilidade

O sistema deve permanecer disponível durante o semestre acadêmico.

Manter disponibilidade mínima de 99% durante o semestre, conforme o RNF-03.

Segurança e privacidade

Os dados dos estudantes devem ser protegidos contra acessos indevidos.

Utilizar TLS 1.3 em 100% das comunicações e armazenar senhas com hash bcrypt de 10 rounds, conforme o RNF-04.

Confiabilidade das notificações

O estudante precisa ser alertado sobre seus compromissos para evitar o esquecimento de prazos.

Verificar, por meio de registros de execução, se as notificações programadas são encaminhadas corretamente ao serviço externo.

As métricas de desempenho, usabilidade, disponibilidade e segurança foram retiradas dos requisitos não funcionais da primeira entrega. Para a confiabilidade das notificações, a equipe deverá definir uma meta numérica após escolher o serviço externo e verificar os recursos disponíveis para acompanhar os envios.

3. Diagrama C4 de contexto

O diagrama de contexto apresenta o sistema e os principais atores e serviços externos que se relacionam com ele.

flowchart TB
    Estudante["Estudante"]
    Coordenacao["Coordenação acadêmica"]
    Suporte["Equipe de suporte / Operação"]
    Sistema["Sistema de Organização Acadêmica"]
    Notificacoes["Serviço de notificações"]

    Estudante -->|"Consulta aulas e gerencia lembretes"| Sistema
    Sistema -->|"Exibe aulas, prazos e compromissos"| Estudante

    Coordenacao -->|"Fornece informações acadêmicas"| Sistema

    Suporte -->|"Realiza monitoramento e manutenção"| Sistema

    Sistema -->|"Solicita envio de notificações"| Notificacoes
    Notificacoes -->|"Retorna informações sobre o envio"| Sistema

Descrição do diagrama de contexto

O estudante é o usuário principal do sistema e poderá visualizar as aulas programadas, cadastrar lembretes e acompanhar prazos acadêmicos.

A coordenação acadêmica está relacionada às informações sobre aulas e prazos importantes. A equipe de suporte será responsável pelas atividades de monitoramento e manutenção do sistema.

O serviço de notificações será responsável pelo envio dos alertas solicitados pela aplicação.

A forma de acesso da coordenação acadêmica às informações ainda deverá ser definida durante a modelagem.

4. Diagrama C4 de contêineres

O diagrama de contêineres apresenta uma proposta de organização dos principais componentes do sistema e de suas responsabilidades.

Como o projeto ainda está na fase de documentação e modelagem, os componentes são apresentados de forma conceitual, sem definir linguagens de programação ou tecnologias.
flowchart TB
    Estudante["Estudante"]

    subgraph Sistema["Sistema de Organização Acadêmica"]
        Interface["Interface do usuário"]
        Aplicacao["Aplicação e regras de negócio"]
        Banco[("Banco de dados")]
        Agendador["Componente de agendamento de notificações"]
    end

    Servico["Serviço externo de notificações"]

    Estudante -->|"Acessa"| Interface
    Interface -->|"Solicita operações"| Aplicacao
    Aplicacao -->|"Consulta e armazena dados"| Banco
    Aplicacao -->|"Disponibiliza compromissos"| Agendador
    Agendador -->|"Solicita envio de alertas"| Servico
    Servico -->|"Retorna status do envio"| Agendador

Descrição dos contêineres

Interface do usuário: permitirá que o estudante visualize as aulas programadas, cadastre e gerencie lembretes e acompanhe os prazos acadêmicos.

Aplicação e regras de negócio: será responsável pelo processamento das solicitações, validação dos dados e aplicação das regras definidas para os compromissos acadêmicos.

Banco de dados: armazenará as informações necessárias para o funcionamento do sistema, como usuários, aulas, lembretes e prazos acadêmicos.

Componente de agendamento de notificações: verificará os compromissos que precisam gerar alertas e solicitará o envio ao serviço externo.

Serviço externo de notificações: receberá as solicitações de envio e retornará as informações disponibilizadas pelo provedor.

A tecnologia utilizada em cada componente será definida posteriormente, conforme as necessidades do projeto.

5. Estilo arquitetural escolhido

Arquitetura em camadas

O estilo arquitetural proposto para o sistema é a arquitetura em camadas, separando as responsabilidades da interface, das regras de negócio e do acesso aos dados.

A interface será responsável pela interação com o estudante. A camada de aplicação ficará responsável pelas regras de negócio, como o cadastro de lembretes e a validação dos prazos. O acesso aos dados será responsável pelo armazenamento e pela consulta das informações.

A comunicação com o serviço de notificações será organizada em um componente específico, facilitando o tratamento de falhas e uma possível substituição do serviço utilizado.

Justificativa

A arquitetura em camadas foi escolhida por facilitar a organização do sistema e a manutenção das funcionalidades.

Essa organização permite separar as responsabilidades, facilitando a realização de testes e a identificação de problemas.

O desempenho poderá ser acompanhado pelo tempo de carregamento da tela principal. A segurança será considerada na proteção dos dados e no controle de acesso. A disponibilidade dependerá do monitoramento e da infraestrutura utilizada.

A separação do componente de notificações também permitirá acompanhar os resultados dos envios e identificar falhas de comunicação com o serviço externo.

Esse estilo foi considerado adequado ao escopo inicial do projeto por permitir uma organização simples, sem exigir a complexidade de vários serviços independentes.

6. Considerações finais

A arquitetura proposta foi definida com base nos requisitos e nas necessidades identificados nas entregas anteriores do Projeto Integrador.

Os diagramas C4 apresentam a relação do sistema com seus usuários e serviços externos, além de uma proposta de organização dos principais componentes.

Os atributos de qualidade estabelecem critérios para avaliar o funcionamento do sistema durante o desenvolvimento e os testes.

As tecnologias de implementação, o banco de dados e o serviço externo de notificações serão definidos posteriormente, conforme as decisões da equipe.
