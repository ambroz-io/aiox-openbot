# Instalação portátil AIOX no OpenBot

## RG e alcance
Documento genérico da integração pública, sem identidade da instalação de origem. Objetivo: permitir que outro OpenBot configure a equipe com seu próprio registro e ferramentas oficiais. Não contém resultados de exercícios pessoais nem promete instalação automática. O exportador copia arquivos; não cria agentes, tabelas, rotinas, contas ou serviços.

## Escolha da distribuição
O fork completo preserva histórico Git, licença, créditos e testes upstream. Ele também possui integrações de várias IDEs, inclusive configurações Claude herdadas: não use o clone completo como workspace do coordenador e não execute npm install, scripts de ativação ou hooks para instalar esta adaptação.

Use a exportação por allowlist abaixo em uma pasta nova. Inclui integração, testes do contrato/distribuição, licença, constituição e as doze definições upstream referenciadas pelo manifesto. Não inclui .git, AGENTS.md da raiz, .claude, .codex, configurações pessoais, .env, hooks, node_modules, rotinas, conversas, bancos, relatórios privados ou exercícios de maturidade. As definições upstream são referência de domínio inerte: seus comandos de ativação não são instalação OpenBot. Tarefas/templates adicionais são consultados no fork somente sob demanda autorizada; não há fechamento recursivo de todas as dependências upstream.

## Obter e conferir
Requisitos locais: Git para obter o fork; Python 3.10+ com biblioteca padrão para exportar e testar protocolo/distribuição. Validado em Python 3.12; não requer Node/npm. Para os testes do schema, jsonschema com Draft 2020-12 já disponível ou instalado explicitamente em ambiente virtual próprio. Nenhum comando abaixo instala dependências automaticamente.

Da pasta em que deseja guardar o clone, execute:

```bash
git -c core.hooksPath=/dev/null clone --branch openbot https://github.com/ambroz-io/aiox-openbot.git 261124-110000-fonte-aiox
cd 261124-110000-fonte-aiox
git rev-parse HEAD
python3 -B integrations/openbot/261124-110000-exportar-pacote-openbot.py --list
python3 -B integrations/openbot/261124-110000-exportar-pacote-openbot.py --output ../261124-110000-pacote-openbot
cd ../261124-110000-pacote-openbot
python3 -B -S integrations/openbot/tests/test_protocol.py
python3 -B -S integrations/openbot/tests/261124-110000-testar-pacote-openbot.py
python3 -B -m unittest discover -s integrations/openbot/tests -v
```

Use uma revisão publicada e aprovada deste fork e registre o SHA obtido antes de continuar. Para repetição exata, use git checkout --detach com o SHA revisado. Destino da exportação deve ser novo, externo ao checkout e com diretório pai existente. Saída: 0 sucesso, 1 recusa/erro de exportação, 2 uso inválido. Falha de escrita pode deixar pacote incompleto: não o instale; preserve o diagnóstico e use novo destino após resolver a causa. Não reutiliza nem apaga destino existente. Não é sandbox contra alterações hostis concorrentes no sistema de arquivos.

O manifesto prefixado na raiz exportada contém SHA-256 de cada arquivo permitido, sem caminhos absolutos nem dados da máquina. Confira antes de configurar agentes:

```python
import hashlib, json
from pathlib import Path
root = Path('.')
manifest = json.loads((root / '261124-110000-manifesto-pacote-openbot.json').read_text())
expected = manifest['sha256']
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual == set(expected) | {'261124-110000-manifesto-pacote-openbot.json'}
assert not any(p.is_symlink() for p in root.rglob('*'))
for name, digest in expected.items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
print('Integridade conferida')
```

Execute esse bloco Python na pasta exportada. Hashes verificam integridade relativa ao manifesto, não autenticidade de um manifesto adulterado. O teste de distribuição usa temporários próprios e os remove; -B evita bytecode. Testes aprovados não demonstram instalação real.

## Instrução pronta para o coordenador da nova instância
Copie o texto abaixo no OpenBot de destino, substituindo apenas o caminho pela localização do pacote nessa instância. O operador precisa autorizar criação/reutilização da equipe nessa instância; não é autorização para trocar modelos, ampliar permissões ou acessar produção alheia.

> Configure esta adaptação AIOX para este OpenBot usando o pacote local que indiquei. Leia integrations/openbot/README.md, este guia, manifest.json, agents/aiox-master.md e a skill do pacote. Preserve minhas instruções e permissões. Use somente ferramentas oficiais do OpenBot. Antes de criar ou alterar, liste agentes, leia os perfis relevantes e liste a biblioteca de skills; reutilize apenas vínculos compatíveis confirmados, sem substituir agentes existentes de outro contexto. Não copie IDs, caminhos, contas, dados, rotinas ou conversas de outra instalação. Registre papéis localmente, configure um coordenador e onze especialistas com inicialização em espera, instale a mesma revisão da skill nos doze e confira versão/enabled. Mantenha o modelo/conta herdados e não amplie acesso. Configure o registro compartilhado conforme protocolo e valide um piloto novo com dados fictícios e revisão independente. Não publique evidências. Reporte criação/configuração, contrato testado e operação observada como etapas distintas; bloqueios precisam de causa e próximo passo.

## Procedimento verificável com ferramentas oficiais
1. Descubra os schemas atuais na instância de destino: list_agents, read_agent, list_local_skills, create_agent, update_profile, create_skill, install_local_skill, list_tables, query_data e execute_data. Se faltarem, pare a configuração nessa etapa; não altere o banco por shell. As ferramentas locais atuam na instância que as executa, não aceitam um endpoint remoto genérico.
2. Leia manifest.json: doze papéis únicos; aiox-master reporta ao usuário, onze especialistas a ele. Os nomes do manifesto são nomes de papéis da adaptação, não usuários ou IDs a importar. Resolva os IDs novos por respostas oficiais. Uma instalação existente deve ser reconciliada antes de criar duplicatas.
3. Use read_agent antes de alterar perfil existente. Grave as instruções de agents/<papel>.md em Instructions/AGENTS.md do agente por mecanismo suportado, preservando as regras privadas anteriores fora do pacote público. create_agent recebe name, description e initialMessage; omita provider/model/reasoningEffort para herdar os atuais. Mensagem inicial: ler somente instruções atribuídas e aguardar Orion; não iniciar instalações ou projetos espontâneos. Nenhum agente novo é criado pelo exportador.
4. A skill do pacote está em integrations/openbot/skills/aiox-openbot-team. create_skill recebe sourcePath de uma pasta dentro do workspace do agente que registra. Se necessário, copie só essa pasta para seu workspace permitido; não copie perfil ou configurações. Consulte biblioteca para reutilizar uma revisão idêntica; se divergir, revisão explícita conforme ferramentas atuais. Atribua com install_local_skill(skillId, revision, agentId) nos doze. A ferramenta preserva disabled e recusa alterações locais: não force. Confira read_agent installedVersion e enabled; resolva desativação somente com autorização adequada. Siga a skill openbot-skill-creator disponível na instância ao registrar/revisar.
5. Liste as tabelas antes de criar. O protocolo usa aiox_openbot_agents para role/agent_id/name/coordinator_id/status e aiox_openbot_tasks para task_id/natural_key/role/status/summary/evidence/updated_at/attempt. Compare schemas existentes; não apague, sobrescreva ou migre dados incompatíveis automaticamente. Crie o registro novo pelas ferramentas de dados conforme o contrato abaixo, sem publicar linhas com IDs locais.
6. Para cada tarefa use todos os campos de schemas/delegation.json: identidade, tentativa, papel, projeto, escopo, entradas, arquivos permitidos, critérios e autorização. Persista-os no registro (summary/evidence ou colunas próprias), não apenas em mensagem. Use atualização condicional por identidade/tentativa/estado e confirme uma linha afetada antes de avançar. Não aceite retorno tardio/duplicado/cancelado; só Orion consolida e encerra após QA e conferência de evidência. O módulo protocol.py valida; não persiste nem supervisiona processos.
7. Faça piloto novo e mínimo na instância de destino com diretório e dados fictícios próprios, mensagens reais e artefatos verificados. Separe revisão QA da implementação. Não use nem procure os exercícios pessoais da instalação de origem. Registre FAIL e bloqueios sem converter em PASS. Interromper turno não prova que um subprocesso terminou: confira o processo exato antes de nova tentativa e só sinalize com autorização delimitada.
8. Devolva ao operador os doze vínculos locais, revisão/enabled, teste do contrato, evidência do piloto e limites. Esses vínculos e evidências ficam privados. Se não puder executar instalação real, declare apenas pacote preparado/contrato testado.

### Schema de registro para instalação nova
Referência de schema, a executar somente pelas ferramentas oficiais de dados após list_tables e conferência de conflitos. Não é comando de shell nem migração automática.

```sql
CREATE TABLE aiox_openbot_agents (
 role TEXT PRIMARY KEY, agent_id TEXT NOT NULL UNIQUE,
 name TEXT NOT NULL, coordinator_id TEXT NOT NULL,
 status TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE aiox_openbot_tasks (
 task_id TEXT PRIMARY KEY, natural_key TEXT NOT NULL UNIQUE,
 role TEXT NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('pending','running','blocked','review','completed','cancelled')),
 summary TEXT NOT NULL, evidence TEXT,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 attempt INTEGER NOT NULL DEFAULT 1
);
```

Para o coordenador, documente o vínculo coordenador→si próprio no registro de instalação; isso não muda o reports_to=null do manifesto nem o fato de reportar ao usuário. Utilize parâmetros nas escritas e mantenha dados locais privados. Esse schema não impõe isolamento por agente e o registro não fornece supervisão automática de processos.

## Recuperação e atualização
A revisão anterior das instruções fica em backup privado no destino, nunca no fork. Para desfazer persona, restaure as instruções e desative a skill com autorização do operador; não exclua projetos/agentes/dados por consequência automática. Atualização usa novo pacote e comparação de manifesto/diffs, preserva alterações locais e requer validação antes de mudar a revisão instalada. Não há cópia de rotinas pessoais, tokens, contas ou mecanismos de login. Uma instância OpenBot limpa precisa existir e possuir sessão própria das ferramentas; este guia não provisiona VPS, Docker ou autenticação.
