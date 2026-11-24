# AIOX para OpenBot

Integração independente, experimental, em fork público de SynkraAI/aiox-core. Preserva licença MIT, créditos e arquivos originais. Consulte [UPSTREAM.md](UPSTREAM.md).

## Organização
Orion é o ponto de contato do usuário e chefe direto dos onze agentes permanentes. Todos os retornos passam por Orion. Consulte [manifest.json](manifest.json) e [agents/](agents/).

## Instalação em outro OpenBot
Para distribuição sem configurações de IDE, use primeiro o [guia portátil](261124-110000-instalacao-portatil-openbot.md) e o exportador por allowlist. Não instale a partir do clone completo nem execute hooks upstream. O guia inclui bootstrap, registro local, verificação e limites.

1. Obtenha este fork na branch openbot e leia estas instruções.
2. Preserve as instruções e configurações anteriores do coordenador em backup privado.
3. Leia o manifesto e as instruções adaptadas. Configure o coordenador com a definição aiox-master, preservando regras locais de segurança e VPS.
4. Use as ferramentas oficiais de leitura/criação de agentes. Reutilize somente agentes compatíveis; não substitua agentes preexistentes. Crie os onze especialistas com as definições adaptadas e inicialização em espera. Mantenha modelo e conta do coordenador salvo escolha explícita do usuário.
5. Grave instruções duráveis em cada AGENTS.md/Instructions e registre o vínculo entre papel e agente somente na instalação local. Nunca publique IDs, caminhos privados, histórico ou credenciais.
6. Registre a skill de skills/aiox-openbot-team pela ferramenta create_skill e instale a revisão exata em cada agente pela install_local_skill. Consulte antes a biblioteca para evitar duplicação.
7. Prepare o registro compartilhado de tarefas com as ferramentas de dados do OpenBot. Não manipule seu banco pelo shell.
8. Execute o piloto isolado e a revisão antes de usar projetos reais. Não há instalador automático nem serviço adicional.

## Teste local do contrato
Requisitos: Python 3 e o pacote `jsonschema` com suporte a Draft 2020-12 para os testes do schema. Em ambiente virtual próprio, instale-o com `python3 -m pip install jsonschema` se necessário. Execute `python3 -B -m unittest discover -s integrations/openbot/tests -v` na raiz do checkout. Os testes de protocolo isolados usam apenas a biblioteca padrão: `python3 -B -S integrations/openbot/tests/test_protocol.py`. Nenhum teste instala dependências automaticamente.

Esses testes validam o contrato, não executam agentes. Uma instalação só tem prova operacional após mensagens reais, artefatos no disco, comandos executados e revisão independente. Evidências operacionais locais não são publicadas automaticamente.

## Uso
Fale com Orion: "Implemente esta tarefa usando a equipe e me devolva código, testes e revisão". Você não precisa acionar especialistas. Orion mantém o progresso e consolida os retornos. Dúvidas dos especialistas também passam por Orion. Os retornos distinguem execução, revisão e bloqueios; implementação concluída não significa revisão aprovada.

## Compatibilidade e limites
- Papéis e responsabilidades: adaptados; tarefas/templates originais carregados sob demanda.
- Delegação: mensagens assíncronas do OpenBot; não usa Task/AskUserQuestion do Claude.
- Comandos básicos: protocolo interpretado pelo coordenador; não são extensões de slash commands da interface.
- Hooks Claude, estado de sessão original, CodeRabbit e Pro: não instalados; disponibilidade precisa ser verificada por projeto. Não apresentar verificação ausente como aprovada.
- Permissões: as da plataforma. Subordinação é instrução operacional, não isolamento de segurança.
- Requisitos do framework original não foram removidos. A integração pode ser testada sem npm install; a suíte completa upstream precisa de suas dependências e não deve ser declarada aprovada sem execução.

## Retomada, cancelamento e recuperação
Registre tentativas e autorizações antes de delegar; aceite apenas retorno da tentativa ativa. Não avance tarefa cancelada ou concluída por resposta tardia. Para cancelamento, interrompa agentes ativos, feche esperas e confira processos iniciados. Para desfazer a migração, restaure instruções privadas e desative a skill; excluir agentes/dados exige autorização apropriada. Nunca apague projetos para reverter uma persona.
