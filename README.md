# 🚀 Aurora Prime Control System (APCS)

> **Global Solution — FIAP 2026 | NEXT FIAP Festival**

A Missão Aurora Prime representa o estágio mais avançado da presença humana em Marte. Operando em Hellas Planitia sob condições extremas, a colônia depende do **Aurora Prime Control System (APCS)** — um sistema inteligente e totalmente autônomo projetado para gerenciar recursos, prever falhas e tomar decisões vitais durante os atrasos de comunicação de até 24 minutos com a Terra.

---

## 📋 O Desafio da Autonomia em Marte

A distância média de 225 milhões de quilômetros entre a Terra e Marte inviabiliza qualquer intervenção humana em tempo real. Uma simples falha de sensor pode evoluir para uma crise irreversível durante a janela de silêncio de comunicação.

O APCS foi desenvolvido para preencher essa lacuna: ele interpreta dados em ciclos de turnos, detecta anomalias, isola falhas em cascata e executa protocolos de decisão, priorizando a sobrevivência humana acima de qualquer outro objetivo. Tudo isso de forma transparente e auditável.

---

## ⚙️ Arquitetura do Sistema

O sistema foi estruturado em cinco camadas lógicas independentes, garantindo manutenibilidade e escalabilidade:

| Camada | Nome | Responsabilidade Principal |
| --- | --- | --- |
| **1** | **Ingestão de Dados** | Leitura de telemetria e montagem estrutural (Listas, Filas, Pilhas, Dicionários, Matrizes). |
| **2** | **Motor de Eventos** | Processamento de eventos externos (tempestades, micrometeoros). |
| **3** | **Motor de Diagnóstico** | Aplicação de regras lógicas booleanas e detecção de falhas em cascata. |
| **4** | **Motor de Decisão** | Execução de protocolos automáticos e gestão de prioridades e alertas. |
| **5** | **Previsão e Relatório** | Regressão linear da reserva de energia e emissão do boletim de turno. |

---

## 🧪 Diferenciais Técnicos e Inovações

* **Protocolo de Votação de Sensores:** Em caso de impacto ou corrupção de dados (ex: leitura impossível de -999°C), o sistema não colapsa. Ele isola o dado falho, cruza os valores dos sensores redundantes ativos e calcula a melhor estimativa operacional.
* **Previsão por Regressão Linear:** O sistema não reage apenas ao presente, ele prevê o futuro. Utilizando o método dos mínimos quadrados ($y = mx + b$), o APCS projeta o comportamento da reserva energética e utiliza o coeficiente de determinação ($R^2$) para validar a confiabilidade da tendência.
* **Score de Saúde Composto:** Um índice inteligente de 0 a 100 que cruza dados de energia, status dos módulos, eventos climáticos e tendência preditiva, servindo como gatilho quantitativo para o Motor de Decisão autorizar reativações.

---

## 🎬 Cenários Simulados

O projeto foi validado por meio de uma base de telemetria rica (`dados.csv`), que transita por quatro estágios complexos de operação:

1. **Operação Normal:** Todos os módulos operacionais, reserva saudável e Score de Saúde alto. Baseline do sistema.
2. **Falha em Cascata:** Uma tempestade de areia derruba a geração solar, forçando desligamentos hierárquicos e priorização absoluta do Suporte à Vida.
3. **Evento Externo Imprevisível:** Uma tempestade solar bloqueia a comunicação terrestre, combinada a um impacto de micrometeoro que corrompe sensores (testando o Protocolo de Votação).
4. **Recuperação Gradual (Preditiva):** Utilizando o algoritmo de regressão, o sistema coordena a retomada segura e escalonada das operações sem esgotar o pouco recurso acumulado.

---

## 📁 Estrutura do Repositório

```text
📦 GS_FIAP_1_2026
 ┣ 📂 data
 ┃ ┗ 📜 dados.csv          # Telemetria simulada dos 4 cenários
 ┣ 📂 docs
 ┃ ┣ 📜 relatorio.pdf      # Documentação técnica e visão executiva
 ┃ ┣ 📜 link_video.txt     # Link para o Pitch NEXT FIAP
 ┃ ┗ 📜 uso_ia.md          # Registro e validação do uso de IA
 ┣ 📂 src
 ┃ ┗ 📜 sistema.py         # Código-fonte Python (As 5 Camadas APCS)
 ┣ 📜 .gitignore
 ┗ 📜 README.md

```

---

## 👥 Equipe Aurora Prime

**Turma:** 1CCOA-2026

| Nome | RM | Papel no Projeto |
| --- | --- | --- |
| **Flávia Roberta Pennachin** | RM561860 | Ingestão, Estruturas de Dados e Narrativa/Modelo de Negócio |
| **Juan de Lucas Frois** | RM563260 | Diagnóstico, Falhas em Cascata e Protocolo de Votação de Sensores |
| **Pedro Valente Toledo** | RM570394 | Motor de Decisão, Score de Saúde e Regressão Linear Preditiva |