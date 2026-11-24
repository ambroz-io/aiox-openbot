# Integração AIOX/OpenBot — primeira versão

## Pedido
Adaptar os papéis do AIOX a agentes permanentes do OpenBot em um fork público, preservando créditos e sem dados pessoais. Orion é o único ponto de contato e chefe direto dos onze especialistas.

## Critérios de aceitação
- [x] Pacote adicional com doze definições e fontes originais preservadas.
- [x] Protocolo de delegação e ciclo mediado exclusivamente por Orion.
- [x] Skill portável e documentação de instalação e recuperação.
- [x] Testes locais de hierarquia, tentativas, duplicatas, cancelamento e evidências.
- [ ] Prova operacional por mensagens e revisão independente na instalação.
- [ ] Publicação conferida da branch openbot no fork.

## Arquivos
README.md, UPSTREAM.md, manifest.json, protocol.py, agents/, skills/aiox-openbot-team/, workflows/, schemas/, tests/.

## Verificação
`python3 -B -m unittest discover -s integrations/openbot/tests -v` na raiz. Requer Python 3 e `jsonschema` para os testes do schema; consulte o README para preparação e execução. A suíte completa upstream não foi executada nesta etapa.

Esta story pública não contém IDs locais, caminhos privados nem dados da instalação.
