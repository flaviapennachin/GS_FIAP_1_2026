PROMPT IA - GERANDO DADOS CSV
# =====================================================================
# PROMPT IA - GERANDO DADOS CSV
# =====================================================================
Atue como um Engenheiro de Dados Aeroespaciais especialista em simulações de telemetria. Preciso que você gere uma massa de dados em formato CSV para um sistema de monitoramento de uma colônia experimental em Marte chamada "Aurora Prime".

O arquivo CSV deve conter exatamente 336 linhas de dados, representando uma simulação contínua de 56 Sóis marcianos completos (um mês marciano real), com 6 leituras diárias por Sol (de 4 em 4 horas: 08:00, 12:00, 16:00, 20:00, 00:00, 04:00). A transição de dados entre os Sóis deve respeitar as leis da física, termodinâmica e os princípios de causa e efeito.

A estrutura de colunas do CSV DEVE ser exatamente esta (respeitando a nomenclatura das chaves que uso no meu script Python):
turno,cenario,hora,mod_suporte_vida,reserva_agua_pct,reserva_alimentos_pct,mod_energia,geracao_solar_kwh,geracao_eolica_kwh,reserva_pct,sinal_radio,mod_comunicacao,sinal_laser,mod_habitacao,status_climatizacao,temp_interna,status_analise_solo,status_analise_biologica,status_monitoramento_saude,status_estoque_medicamentos,mod_laboratorio,mod_suporte_medico,consumo_kwh,evento_externo,sensor_falho

Regras de Variáveis, Restrições Críticas e Balanço Energético:
- turno: Inteiro sequencial de 1 a 336.
- cenario: Inteiro de 1 a 4, indicando o quadrante macro da história.
- hora: Strings cíclicas (08:00, 12:00, 16:00, 20:00, 00:00, 04:00).
- mod_suporte_vida, mod_habitacao, mod_energia: Devem obrigatoriamente ser sempre 1 em todos os 336 turnos da simulação, representando sistemas vitais que nunca desligam.
- mod_comunicacao, mod_laboratorio, mod_suporte_medico: Status binários (1 operacional, 0 desligado para contingência energética).
- status_ (climatizacao, analise_solo, analise_biologica, monitoramento_saude, estoque_medicamentos): Seguem o comportamento de ativação do seu respectivo módulo pai. Se o módulo estiver em 1, o status é 1; se o módulo for desligado (0), o status vai para 0.
- reserva_agua_pct e reserva_alimentos_pct: Floats. Começam em 100.0 no turno 1 e sofrem um consumo sutil e linear de 0.05% por turno ao longo da simulação.
- geracao_solar_kwh: Float. Deve obrigatoriamente ir a 0.0 nos turnos noturnos de 20:00, 00:00 e 04:00. Nos turnos diurnos (08:00, 12:00, 16:00), varia de forma realista entre 30.0 e 50.0 kWh (em condições normais).
- geracao_eolica_kwh: Float. Flutua senoidalmente entre 5.0 e 40.0 kWh, independente da hora do dia.
- sinal_radio, sinal_laser: Floats de 0.0 a 1.0 representando a qualidade do canal de transmissão. Eles flutuam junto com a linha de base da mecânica celeste de afastamento dos planetas.
- consumo_kwh: Float. Carga dinâmica. Todos os módulos ligados = ~35 kWh. Quando os módulos secundários (comunicação, laboratório ou suporte médico) são desligados, o consumo cai proporcionalmente (-5.0 kWh por módulo desligado), gerando uma economia visível.
- reserva_pct: Float (0.0 a 100.0). Representa o nível das baterias. Se (geracao_solar + geracao_eolica > consumo), a reserva sobe; se for menor, a reserva desce de forma causal.
- temp_interna: Float. Temperatura interna estável em torno de 22.0°C (flutuação normal de +/- 0.5°C).
- evento_externo: String ('nenhum', 'tempestade_areia', 'tempestade_solar', 'micrometeoro').
- sensor_falho: Binário (0 ou 1).

Roteiro Narrativo dos 56 Sóis (336 linhas) e Dinâmica Orbital:

Quadrante 1: Operação Normal e Proximidade Orbital (Sóis 1 a 15 | Turnos 1 a 90) - cenario = 1
Terra e Marte em rota de aproximação máxima (Oposição). Os sinais de rádio e laser mantêm-se altos (> 0.85). A colônia opera em total estabilidade. Reserva de energia flutua de forma saudável entre 75% e 95%. Todos os módulos operam em 1. O evento_externo é 'nenhum' e sensor_falho é 0.

Quadrante 2: Afastamento Planetário e Crise Prolongada - Tempestade de Areia (Sóis 16 a 30 | Turnos 91 a 180) - cenario = 2
Os planetas se afastam na órbita. Cumulativamente, o evento_externo passa a ser 'tempestade_areia'. A poeira em suspensão derruba a geração solar diurna em 85% (fica entre 2.0 e 7.0 kWh). A reserva_pct começa a minguar consistentemente dia após dia. Quando a reserva cruzar < 50%, mude o 'mod_laboratorio' para 0 (e seus status para 0). Se a reserva continuar caindo e cruzar < 30%, mude o 'mod_suporte_medico' para 0 (e seus status para 0). O consumo_kwh deve cair visivelmente após esses desligamentos.

Quadrante 3: Conjunção e Eventos Críticos Imprevisíveis (Sóis 31 a 40 | Turnos 181 a 240) - cenario = 3
A tempestade de areia cessa. Contudo, os planetas entram em Conjunção Solar (lados opostos do Sol), empurrando o atraso de transmissão para o limite físico. No Sol 32 inicia-se uma 'tempestade_solar' que dura 4 Sóis: a radiação dispara, o sinal_laser cai para 0.0, e 'mod_comunicacao' vai para 0 (isolamento autônomo total). A reserva de energia atinge o mínimo histórico de 10%.
No Sol 38 (exatamente no Turno 223, às 00:00), ocorre um impacto de 'micrometeoro'. Insira a INCONSISTÊNCIA PROPOSITAL: a coluna temp_interna deve registrar o valor impossível de -999.0 e a coluna sensor_falho deve virar 1. Nos turnos seguintes, a temperatura volta ao normal (~22.0°C) e sensor_falho volta para 0.

Quadrante 4: Recuperação Orbital e Preditiva NEXT (Sóis 41 a 56 | Turnos 241 a 336) - cenario = 4
A geometria orbital inicia fase de reaproximação. Os eventos voltam para 'nenhum'. A geração solar normaliza. O 'mod_comunicacao' volta imediatamente para 1. A reserva_pct começa a subir progressivamente Sol após Sol. Quando a reserva ultrapassar 45%, o 'mod_suporte_medico' (e seus status) volta para 1. Quando a reserva consolidar acima de 70%, o 'mod_laboratorio' finalmente é reativado (volta para 1), terminando a simulação com a colônia 100% recuperada e estável.

Retorne APENAS as linhas de texto do CSV estruturado, incluindo a linha de cabeçalho exata fornecida. Não inclua blocos de código com formatação markdown, textos explicativos, resumos ou notas. Forneça o arquivo bruto de 336 linhas pronto para ser salvo em um arquivo .csv.
# ============================================================================