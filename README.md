# 🚀 Aurora Prime Control System (APCS)


![Pandas](https://img.shields.io/badge/Pandas-Data_Cleansing-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Linear_Regression-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Status](https://img.shields.io/badge/Status-Missão_Concluída-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)

> **Global Solution — FIAP 2026 | NEXT FIAP Festival**

A Missão Aurora Prime representa o estágio mais avançado da presença humana em Marte. Operando sob condições extremas, a colônia depende do **Aurora Prime Control System (APCS)** — um sistema inteligente, defensivo e totalmente autônomo, projetado para gerenciar recursos, prever falhas e tomar decisões vitais durante atrasos de comunicação de até 24 minutos com a Terra.

---

## 👨‍🚀 Equipe Aurora Prime (1CCOA-2026)
| Nome | RM |
| :--- | :--- |
| **Flávia Roberta Pennachin** | RM561860 |
| **Juan de Lucas Frois** | RM563260 |
| **Pedro Valente Toledo** | RM570394 |

---

## 🧠 Arquitetura do Sistema (As 5 Camadas APCS)
O código-fonte (`sistema.py`) foi desenvolvido com base em Engenharia de Software robusta, dividido em 5 motores lógicos que processam 56 Sóis marcianos (336 turnos) de forma autônoma:
<br>
<br>

  ![Imagem da camada 1](docs/camada_1.jpg)
  Utiliza `Pandas` envolto num bloco `try/except` para ler a telemetria, aspirar espaços em branco (Data Cleansing) e evitar quebras críticas caso o sensor de dados fique offline.
<br>
<br>

   ![Imagem da camada 2](docs/camada_2.jpg)
   Avalia intempéries (Tempestades Solares, Micrometeoros). Possui um sistema de **Votação de Sensores** que, ao detectar dados corrompidos (ex: `-999°C`), calcula a média histórica para evitar alarmes falsos.
<br>
<br>

  ![Imagem da camada 3](docs/camada_3.jpg)
  Avalia a árvore de sistemas em tempo real (Energia, Habitação, Medicina). Cruza variáveis para detectar o temido "Efeito Cascata" (quando a falha de um módulo compromete a sobrevivência).
<br>
<br>

  ![Imagem da camada 4](docs/camada_4.jpg)
  Aplica Regressão Linear Simples (`np.polyfit`) sobre as leituras recentes das baterias para prever matematicamente o colapso. Gera o **Score de Saúde (0-100%)**, ponderando energia, integridade dos módulos e clima.
<br>
<br>

  ![Imagem da camada 5](docs/camada_5.jpg)
  Formula um plano de ação diário (desligar módulos, distribuir kits médicos). Gerencia o protocolo **DTN (Delay-Tolerant Networking)**, calculando o *Time of Flight* da luz para enviar mensagens à Terra via Laser ou Rádio.

---

## 🛠️ Estruturas de Dados Aplicadas
O APCS é sustentado por estruturas de dados otimizadas para cada contexto da missão:

* 📖 **Dicionários (Tabelas Hash):** A estrutura `hierarquia_sistemas_colonia` usa dicionários aninhados para acesso instantâneo. Implementamos um **Menu Interativo O(1)** no final da simulação, onde o usuário escolhe um número e o sistema acessa a memória do módulo sem precisar percorrer listas.
* ⏳ **Filas (Queue / FIFO):** A estrutura `fila_transmissao_terra` armazena pacotes durante o bloqueio da Janela de Comunicação. Quando a janela abre, utiliza `pop(0)` para garantir que as mensagens mais antigas sejam enviadas primeiro para a Terra.
* 📚 **Pilhas (Stack / LIFO):** A estrutura `pilha_eventos_criticos` registra o histórico de catástrofes, permitindo ao sistema consultar rapidamente o impacto mais recente acessando o topo da pilha.
* 📈 **Listas (Séries Temporais):** Usadas para guardar o `historico_baterias`, essencial para extrair os arrays matemáticos necessários à Regressão Linear.

---

## ⚡ Lógica de Diagnóstico Principal
O cérebro do diagnóstico utiliza portas lógicas estritas (`IF/ELIF/ELSE` + `AND/OR/NOT`). A expressão booleana crítica que dita a "Emergência Máxima" (Protocolo Omega) é:

```text
SE (energia_armazenada < 20) E (oxigenio == 0 OU reserva_agua < 40) ENTÃO
    STATUS = "CASCATA: Falha no suporte à vida por colapso energético."
    AÇÃO = "Redirecionar toda a energia restante para Suporte à Vida."

```

---

## 💻 Como Executar a Simulação

O sistema não exige interfaces gráficas pesadas, operando diretamente no terminal com alta performance.

1. Instale as dependências analíticas:

```bash
pip install pandas numpy

```

2. Execute o núcleo do APCS:

```bash
python src/sistema.py

```

> 💡 *Nota:* Ao término dos 56 Sóis, o sistema exportará uma planilha de auditoria para `docs/relatorio_execucao_aurora.csv` e abrirá o Menu Interativo O(1).

---

## 📡 Exemplo de Saída no Terminal (Log de Comunicação)

Durante a tempestade de poeira marciana, o sistema apresenta a seguinte clareza operacional:

```text
» RELATÓRIO DE FECHO - SOL 32 | Turno: 187 | Cenário: 3
  SAÚDE DA MISSÃO: 🔴 [CRÍTICO] [█-------------------] 5%
  [!] Janela Fechada (MODO AUTÔNOMO).
  Baterias: 11.0%
  Eventos do Dia: Tempestade solar em curso. Radiação elevada.
  🚨 [PREVISÃO CRÍTICA] Mantendo-se a queda atual, as baterias esgotarão em 1.5 Sóis.
  [PLANO DE AÇÃO DIÁRIO]:
    -> Protocolo Economia: Desligar Laboratório e hibernar aquecimento secundário.
    -> Isolamento Tático: Manter operações 100% autônomas.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  [!] TRANSMISSÃO RETIDA: Janela fechada. Pacote guardado na fila (Pendentes: 3).
=====================================================================================

```

---

## 🎥 Pitch e Demonstração

▶️ **[Inserir aqui o link do vídeo do YouTube Não Listado]**

---

## 🎯 Conclusões e Aprendizagens

A construção do APCS elevou o desafio acadêmico para o nível de arquitetura de software real. Compreendemos que a inteligência de um sistema não está apenas no seu código final, mas em como ele se **defende** de falhas (usando tratamento de exceções no Pandas) e como lida com as **leis da física** (incorporando os atrasos da velocidade da luz na nossa Fila FIFO de rede).

A utilização da Regressão Linear com NumPy superou as expectativas de análise simples, criando um sistema verdadeiramente preditivo. As estruturas de dados deixaram de ser conceitos teóricos e tornaram-se a fundação absoluta para manter uma colônia virtual viva em Marte.
