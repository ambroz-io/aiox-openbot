# Ciclo de tarefa no OpenBot

Cada seta é uma delegação feita por Orion, nunca de especialista para especialista.

1. River recebe requisitos e grava uma tarefa com critérios testáveis.
2. Pax valida; se rejeitar, Orion devolve a River com achados.
3. Dex implementa no checkout autorizado e executa testes.
4. Quinn revisa do disco; se FAIL, Orion devolve a Dex com achados e nova tentativa.
5. Gage confere a entrega e publica somente o escopo autorizado.
6. Orion verifica evidências e apresenta a entrega ao usuário.

Registre estado após cada retorno e use o identificador original da tarefa, tentativa e papel. Limite tentativas de correção pelo briefing; ao esgotar, reporte bloqueio. Não publique até a revisão passar. Toda decisão não resolvida volta a Orion.
