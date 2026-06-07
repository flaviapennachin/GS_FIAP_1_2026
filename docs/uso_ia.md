# Relatório de Uso de Inteligência Artificial
**Projeto:** Aurora Prime - Sistema Inteligente de Controle Operacional Marciano  
**Fase:** 3 (Global Solution)

---

## 1. Escopo e Propósito do Uso

Durante o desenvolvimento do Projeto Aurora Prime, a Inteligência Artificial (LLMs) foi utilizada de forma estratégica e ética, atuando estritamente como uma ferramenta de apoio analítico e de geração de massa de dados simulados. A arquitetura do sistema, a definição das estruturas de dados, a lógica booleana e a integração do código foram integralmente idealizadas e concebidas pela nossa equipa.

O uso da IA concentrou-se em duas partes principais:
1. **Geração da Matriz de Telemetria (Data Engineering):** Criação de um dataset CSV realista de 336 linhas que respeitasse leis da física orbital, termodinâmica e consumo de energia.
2. **Apoio Estrutural (Pair Programming):** Auxílio na sintaxe de funções específicas da biblioteca NumPy para a regressão linear e nas rotinas de *Data Cleansing* do Pandas (tratamento de espaços em branco e prevenção de exceções `KeyError`).

---

## 2. Prompt Utilizado para Geração de Dados (CSV)

Para garantir que a simulação de 56 Sóis marcianos tivesse rigor técnico e causalidade (ex: painéis solares não gerarem energia à noite, ou o sinal de comunicação cair durante a conjunção solar), utilizamos o seguinte prompt de engenharia de dados:

> **Prompt:**
> "Atue como um Engenheiro de Dados Aeroespaciais especialista em simulações de telemetria. Preciso que você gere uma massa de dados em formato CSV para um sistema de monitoramento de uma colônia experimental em Marte chamada "Aurora Prime".
> 
> O arquivo CSV deve conter exatamente 336 linhas de dados, representando uma simulação contínua de 56 Sóis marcianos completos (um mês marciano real), com 6 leituras diárias por Sol (de 4 em 4 horas: 08:00, 12:00, 16:00, 20:00, 00:00, 04:00). A transição de dados entre os Sóis deve respeitar as leis da física, termodinâmica e os princípios de causa e efeito.
> 
> A estrutura de colunas do CSV DEVE ser exatamente esta:
> `turno,cenario,hora,mod_suporte_vida,reserva_agua_pct,reserva_alimentos_pct,mod_energia,geracao_solar_kwh,geracao_eolica_kwh,reserva_pct,sinal_radio,mod_comunicacao,sinal_laser,mod_habitacao,status_climatizacao,temp_interna,status_analise_solo,status_analise_biologica,status_monitoramento_saude,status_estoque_medicamentos,mod_laboratorio,mod_suporte_medico,consumo_kwh,evento_externo,sensor_falho`
> 
> *(Nota: Adicionamos posteriormente as colunas `reserva_oxigenio_pct`, `janela_comunicacao`, `sinais_vitais_tripulantes_pct` e `nivel_estoque_medicamentos_pct` para expandir a capacidade de análise do sistema).*
> 
> Regras de Variáveis, Restrições Críticas e Balanço Energético:
> - mod_suporte_vida, mod_habitacao, mod_energia: Devem obrigatoriamente ser sempre 1.
> - mod_comunicacao, mod_laboratorio, mod_suporte_medico: Status binários (1 operacional, 0 contingência).
> - geracao_solar_kwh: Float. Deve obrigatoriamente ir a 0.0 nos turnos noturnos.
> - consumo_kwh: Float. Carga dinâmica que reduz ao desligar módulos secundários.
> - reserva_pct: Float (0.0 a 100.0). Se geração > consumo, sobe; senão, desce.
> 
> Roteiro Narrativo dos 56 Sóis:
> - Quadrante 1 (Sóis 1-15): Operação Normal.
> - Quadrante 2 (Sóis 16-30): Tempestade de Areia (queda severa de geração solar).
> - Quadrante 3 (Sóis 31-40): Conjunção Solar (isolamento e impacto de micrometeoro no turno 223 com inconsistência proposital de temperatura -999.0).
> - Quadrante 4 (Sóis 41-56): Recuperação Orbital."

---

## 3. Validação Crítica e Auditoria da Equipa

Após a geração dos resultados e o apoio algorítmico da IA, a nossa equipa não aceitou o output de forma passiva. Realizámos as seguintes validações críticas:

1. **Auditoria de Balanço Energético:** Analisámos manualmente as linhas do CSV gerado para garantir que a coluna `reserva_pct` estava efetivamente a cair nos turnos onde a geração total (solar + eólica) era inferior ao consumo. Identificámos a necessidade de formatar os dados e aplicámos regras de *Data Cleansing* (`skipinitialspace=True` e `.str.strip()`) no código Python para evitar falhas de leitura.
2. **Validação da Inconsistência:** O prompt solicitou o valor `-999.0` no turno 223. Testámos a nossa função de `votar_sensor` de forma isolada para garantir que a falha era apanhada e corrigida pela média do histórico, evitando que a lógica booleana de habitação falhasse indevidamente.
3. **Calibração do NumPy (Previsão):** A IA sugeriu a sintaxe do `np.polyfit`. Nós validámos criticamente a lógica limitando o *array* aos últimos 18 turnos (3 Sóis). Percebemos que se usássemos todo o histórico (336 turnos), a predição linear ficaria distorcida e não seria reativa a crises súbitas (como a tempestade de areia). A limitação da janela de tempo foi uma decisão arquitetural nossa.
4. **Validação Matemática do Atraso de Rede:** As fórmulas de *Time of Flight* baseadas na mecânica orbital e a fila computacional FIFO (`fila_transmissao_terra.pop(0)`) foram implementadas para processar atrasos com base na degradação do sinal, provando a resiliência do sistema em simulações físicas reais.