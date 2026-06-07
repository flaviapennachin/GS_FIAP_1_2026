import pandas as pd
from pathlib import Path
import time
import numpy as np

# =====================================================================
# REQUISITO 8.2: ESTRUTURAS DE DADOS
# =====================================================================
fila_alertas = []  # alertas por prioridade
pilha_eventos_criticos = []  # últimos eventos analisados
fila_transmissao_terra = []  # Fila FIFO para pacotes de telemetria pendentes

# ESTRUTURA PARA ANÁLISE DE EFICIÊNCIA ENERGÉTICA
historico_baterias = []  # monitoramento de ciclos de carga
historico_geracao_solar = []  # análise de eficiência energética
historico_geracao_eolica = []  # análise de eficiência energética
historico_consumo = []  # análise de eficiência energética
historico_temperatura = []  # histórico de leituras válidas de temperatura interna

# DICIONÁRIO DE SISTEMAS E SUBSISTEMAS
# hierarquia de sistemas e subsistemas para monitoramento e controle operacional
hierarquia_sistemas_colonia = {
    "suporte_vida": {
        "oxigenio": 1,  # mapeamento do mod_suporte_vida (1 = operacional, 0 = falha)
        "reserva_oxigenio": 100.0,  # percentual de reserva de oxigênio (0-100%)
        "agua": 98.8,  # percentual de reserva de água (0-100%)
        "alimentos": 99.9,  # percentual de reserva de alimentos (0-100%)
    },
    "energia": {
        "solar": 38.35,  # geração solar em kWh
        "eolica": 24.24,  # geração eólica em kWh
        "armazenamento": 85.57,  # percentual de reserva de energia (0-100%)
    },
    "comunicacao": {
        "radio": 0.95,  # qualidade do sinal de rádio (0-1)
        "satellite": 0.9,  # qualidade do sinal de satélite (0-1)
        "laser": 0.96,  # qualidade do sinal de comunicação a laser (0-1)
        "janela_contato": "aberta",  # status da janela com a Terra (aberta/fechada)
    },
    "habitacao": {
        "modulo_habitacional": 1,  # status do módulo habitacional (1 = operacional, 0 = falha)
        "sistema_climatizacao": 1,  # status do sistema de climatização (1 = operacional, 0 = falha)
        "temperatura_interna": 22.0,  # temperatura interna do habitat em °C
    },
    "laboratorio": {
        "analise_solo": 1,  # status da estaçao de análise de solo (1 = operacional, 0 = falha)
        "analise_biologica": 1,  # status da estaçao de análises biológicas (1 = operacional, 0 = falha)
    },
    "suporte_medico": {
        "monitoramento_saude": 1,  # status do monitoramento de saúde (1 = operacional, 0 = falha)
        "sinais_vitais_pct": 100.0,  # saúde geral da tripulação (0-100%)
        "estoque_medicamentos": 1,  # status do estoque de medicamentos (1 = operacional, 0 = falha)
        "nivel_medicamentos_pct": 100.0,  # quantidade física no estoque (0-100%)
    },
}

# =====================================================================
# REQUISITO 8.1: LEITURA E INGESTÃO DE DADOS
# =====================================================================
base_dir = Path(__file__).resolve().parent
# csv_path = base_dir.parent / "data" / "dados_telemetria_marte.csv"
csv_path = base_dir.parent / "data" / "GS - All Data.csv"


def exibir_introducao_aurora():
    print("=" * 85)
    print(
        "      AURORA PRIME — SISTEMA INTELIGENTE DE CONTROLE OPERACIONAL MARCIANO      "
    )
    print(
        "          Desenvolvimento Integrado: Desafio Global Solution 2026            "
    )
    print("=" * 85)
    print("\n[CONFIGURAÇÃO INICIAL]")
    print("• Localização: Colônia Primária, Planície de Marte.")
    print("• Frequência de Monitoramento: Ciclos de 4 horas planetárias (56 Sóis).")
    print("\nIniciando matriz de telemetria histórica...")
    print("-" * 85)
    time.sleep(1.8)


# =====================================================================
# REQUISITO 8.3 / 8.4: MOTOR DE EVENTOS EXTERNOS
# =====================================================================
def processar_evento_externo(turno):
    if turno["evento_externo"] == "nenhum":
        return "Sem eventos externos. Operação nominal."
    elif turno["evento_externo"] == "tempestade_areia":
        return "Tempestade de areia detectada. Geração solar comprometida e visibilidade reduzida."
    elif turno["evento_externo"] == "tempestade_solar":
        return "Tempestade solar em curso. Comunicação instável e radiação elevada."
    elif turno["evento_externo"] == "micrometeoro":
        return "Impacto de micrometeoro detectado. Possível falha de sensor."
    else:
        return "Um evento externo não identificado acaba de ocorrer."


# =====================================================================
# REQUISITO 8.3 (NEXT): PROTOCOLO DE VOTAÇÃO DE SENSORES
# =====================================================================
def votar_sensor(historico_temperatura, turno_atual):
    if turno_atual["temp_interna"] == -999:
        if len(historico_temperatura) == 0:
            return "Sensor falho e sem histórico disponível para recuperação."
        else:
            soma = 0
            for temp in historico_temperatura:
                soma += temp
            media = soma / len(historico_temperatura)
            return f"[VOTAÇÃO] Sensor falho. Valor estimado por média histórica: {media:.1f}°C"
    else:
        historico_temperatura.append(turno_atual["temp_interna"])
        return f"Temperatura interna: {turno_atual['temp_interna']:.1f}°C"


# =====================================================================
# REQUISITO 8.5: ANÁLISE E PREVISÃO DE DADOS COM NUMPY
# =====================================================================
def calcular_previsao_energia(historico_baterias):
    if len(historico_baterias) < 6:
        return "[PREVISÃO] A aguardar recolha de dados suficientes..."

    dados_recentes = (
        historico_baterias[-18:]
        if len(historico_baterias) >= 18
        else historico_baterias
    )

    eixo_x = np.arange(len(dados_recentes))
    eixo_y = np.array(dados_recentes)

    coeficientes = np.polyfit(eixo_x, eixo_y, 1)
    inclinacao = coeficientes[0]
    intersecao = coeficientes[1]

    if inclinacao >= 0:
        return "[PREVISÃO] Tendência Energética Positiva/Estável. Colapso improvável a curto prazo."
    else:
        turno_zero = -intersecao / inclinacao
        turnos_restantes = turno_zero - (len(dados_recentes) - 1)

        if turnos_restantes <= 0:
            return "🚨 [PREVISÃO CRÍTICA] Baterias em colapso total iminente!"
        else:
            dias_restantes = turnos_restantes / 6.0
            return f"🚨 [PREVISÃO CRÍTICA] Mantendo-se a queda atual, as baterias esgotarão em {dias_restantes:.1f} Sóis marcianos."


# =====================================================================
# REQUISITO 8.4: MOTOR DE DECISÃO (AÇÕES AUTOMÁTICAS E RECOMENDAÇÕES)
# =====================================================================
def gerar_recomendacoes(resultado_diagnostico, cascata, dados_turno, score_atual):
    acoes = []

    if cascata:
        acoes.append(
            "[!] PROTOCOLO OMEGA: Risco de perda da colônia. Redirecionar energia para Suporte à Vida."
        )

    if resultado_diagnostico.get("energia") == "crítico":
        acoes.append(
            "-> Protocolo Economia: Desligar Laboratório e hibernar aquecimento secundário."
        )
    elif resultado_diagnostico.get("energia") == "alerta":
        acoes.append("-> Ajuste de Carga: Monitorar baterias de perto.")

    if resultado_diagnostico.get("suporte_medico") == "crítico":
        acoes.append(
            "-> Emergência Médica: Sistemas inoperantes. Realizar checagem manual da tripulação."
        )
    elif dados_turno.get("sinais_vitais_tripulantes_pct", 100) < 90:
        acoes.append(
            "-> Atenção Tripulação: Sinais vitais em queda. Distribuir kit médico."
        )

    if resultado_diagnostico.get("comunicacao") == "crítico":
        if dados_turno.get("janela_comunicacao") == "fechada":
            acoes.append("-> Isolamento Tático: Manter operações 100% autônomas.")
        else:
            acoes.append("-> Falha de Link: Reiniciar módulo de satélite.")

    if len(acoes) == 0:
        if score_atual < 75 or "alerta" in resultado_diagnostico.values():
            acoes.append(
                "-> Atenção: Desvios operacionais detectados. Nível de alerta amarelo. Revisar parâmetros."
            )
        else:
            acoes.append("-> Sistemas 100% estáveis. Manter operações de rotina.")

    return acoes


# =====================================================================
# REQUISITO NEXT: SCORE DE SAÚDE DA MISSÃO E COMUNICAÇÃO DE ESPAÇO PROFUNDO
# =====================================================================
def calcular_score_saude(hierarquia, evento, previsao_texto):
    score = 0.0
    reserva = hierarquia["energia"]["armazenamento"]
    score += (reserva / 100.0) * 40.0

    modulos = [
        hierarquia["habitacao"]["modulo_habitacional"],
        hierarquia["suporte_vida"]["oxigenio"],
        hierarquia["comunicacao"]["satellite"],
        hierarquia["laboratorio"]["analise_solo"],
        hierarquia["suporte_medico"]["monitoramento_saude"],
    ]
    ativos = sum(modulos)
    score += (ativos / 5.0) * 30.0

    if "Sem eventos externos" in evento:
        score += 20.0
    elif "Tempestade de areia" in evento:
        score += 10.0
    else:
        score += 0.0

    if "Positiva" in previsao_texto or "Estável" in previsao_texto:
        score += 10.0
    else:
        score += 0.0

    return max(0, min(100, int(score)))


def gerar_barra_score(score):
    tamanho_barra = 20
    preenchido = int((score / 100) * tamanho_barra)
    vazio = tamanho_barra - preenchido

    if score >= 75:
        cor = "🟢 [NOMINAL]"
    elif score >= 40:
        cor = "🟡 [ALERTA] "
    else:
        cor = "🔴 [CRÍTICO]"

    return f"{cor} [{'█' * preenchido}{'-' * vazio}] {score}%"


def calcular_atraso_total(cenario, qualidade_sinal):
    if cenario == 1:
        tempo_luz = 4.3
    elif cenario == 2:
        tempo_luz = 12.5
    elif cenario == 3:
        tempo_luz = 21.0
    else:
        tempo_luz = 10.2

    penalidade_maxima = 20.0
    atraso_rede = (1.0 - qualidade_sinal) * penalidade_maxima
    return tempo_luz + atraso_rede


def gerir_transmissao_terra(hierarquia, cenario, relatorio_atual):
    janela = hierarquia["comunicacao"]["janela_contato"]
    radio = hierarquia["comunicacao"]["radio"]
    laser = hierarquia["comunicacao"]["laser"]

    if janela == "fechada":
        fila_transmissao_terra.append(relatorio_atual)
        return f"  [!] TRANSMISSÃO RETIDA: Janela fechada. Pacote guardado na fila (Pendentes: {len(fila_transmissao_terra)})."

    if laser >= radio:
        canal_escolhido = "LASER ÓTICO"
        sinal = laser
    else:
        canal_escolhido = "ONDAS DE RÁDIO"
        sinal = radio

    atraso_minutos = calcular_atraso_total(cenario, sinal)
    qtd_antigas = len(fila_transmissao_terra)

    while len(fila_transmissao_terra) > 0:
        pacote_atrasado = fila_transmissao_terra.pop(0)

    if qtd_antigas > 0:
        msg_batch = f"  [+] TRANSMISSÃO BATCH INICIADA: {qtd_antigas} pacote(s) atrasado(s) + 1 pacote atual."
    else:
        msg_batch = f"  [+] TRANSMISSÃO INICIADA: 1 pacote atual enviado."

    logs = [
        msg_batch,
        f"  [+] Via: Rede de Espaço Profundo ({canal_escolhido}) | Força do Sinal: {sinal*100:.1f}%",
        f"  [+] Tempo de Voo Estimado (ETA na Terra): {atraso_minutos:.1f} minutos.",
    ]
    return "\n".join(logs)


# =====================================================================
# REQUISITO 8.3: MOTOR DE DIAGNÓSTICO — REGRAS LÓGICAS
# =====================================================================
def diagnosticar(hierarquia_sistemas_colonia):
    resultado = {}
    radio = hierarquia_sistemas_colonia["comunicacao"]["radio"] * 100
    laser = hierarquia_sistemas_colonia["comunicacao"]["laser"] * 100
    energia_armazenada = hierarquia_sistemas_colonia["energia"]["armazenamento"]
    sattelite = hierarquia_sistemas_colonia["comunicacao"]["satellite"]

    oxigenio = hierarquia_sistemas_colonia["suporte_vida"]["oxigenio"]
    agua = hierarquia_sistemas_colonia["suporte_vida"]["agua"] * 100
    alimentos = hierarquia_sistemas_colonia["suporte_vida"]["alimentos"] * 100

    modulo_habitacional = hierarquia_sistemas_colonia["habitacao"][
        "modulo_habitacional"
    ]
    sistema_climatizacao = hierarquia_sistemas_colonia["habitacao"][
        "sistema_climatizacao"
    ]
    temperatura_interna = hierarquia_sistemas_colonia["habitacao"][
        "temperatura_interna"
    ]

    analise_solo = hierarquia_sistemas_colonia["laboratorio"]["analise_solo"]
    analise_biologica = hierarquia_sistemas_colonia["laboratorio"]["analise_biologica"]

    monitoramento_saude = hierarquia_sistemas_colonia["suporte_medico"][
        "monitoramento_saude"
    ]
    estoque_medicamentos = hierarquia_sistemas_colonia["suporte_medico"][
        "estoque_medicamentos"
    ]

    if energia_armazenada <= 100 and energia_armazenada >= 50:
        resultado["energia"] = "normal"
    elif energia_armazenada < 50 and energia_armazenada >= 20:
        resultado["energia"] = "alerta"
    else:
        resultado["energia"] = "crítico"

    # EXPRESSÃO BOOLEANA: comunicação normal apenas se rádio AND laser ambos acima de 50%
    if radio >= 50 and laser >= 50:
        resultado["comunicacao"] = "normal"
    elif radio >= 20 and laser >= 20:  # degradação parcial: alerta se ambos acima de 20%
        resultado["comunicacao"] = "alerta"
    else:  # qualquer canal abaixo de 20% → crítico
        resultado["comunicacao"] = "crítico"

    # EXPRESSÃO BOOLEANA: NOT satélite — falha forçada para crítico independente dos demais canais
    if not sattelite == 1:
        resultado["comunicacao"] = "crítico"

    # EXPRESSÃO BOOLEANA: suporte_vida normal apenas se água AND alimentos acima de 70%
    if agua >= 70 and alimentos >= 70:
        resultado["suporte_vida"] = "normal"
    elif agua >= 40 and alimentos >= 40:
        resultado["suporte_vida"] = "alerta"
    else:
        resultado["suporte_vida"] = "crítico"

    # EXPRESSÃO BOOLEANA: NOT oxigenio — falha de O2 é sempre crítica, ignorando água/alimentos
    if not oxigenio == 1:
        resultado["suporte_vida"] = "crítico"

    if temperatura_interna >= 18 and temperatura_interna <= 26:
        resultado["habitacao"] = "normal"
    elif (temperatura_interna >= 10 and temperatura_interna <= 18) or (
        temperatura_interna >= 26 and temperatura_interna <= 35
    ):
        resultado["habitacao"] = "alerta"
    elif temperatura_interna < 10 or temperatura_interna > 35:
        resultado["habitacao"] = "crítico"

    if (not sistema_climatizacao == 1) or (not modulo_habitacional == 1):
        resultado["habitacao"] = "crítico"

    if (not analise_solo == 1) or (not analise_biologica == 1):
        resultado["laboratorio"] = "crítico"
    else:
        resultado["laboratorio"] = "normal"

    if (not monitoramento_saude == 1) or (not estoque_medicamentos == 1):
        resultado["suporte_medico"] = "crítico"
    else:
        resultado["suporte_medico"] = "normal"

    return resultado


# =====================================================================
# REQUISITO 8.4: DETECÇÃO DE FALHAS EM CASCATA
# =====================================================================
def detectar_cascata(resultado):
    if resultado["energia"] == "crítico" and resultado.get("comunicacao") == "crítico":
        return "CASCATA DETECTADA: Energia crítica comprometeu a comunicação."
    if resultado["energia"] == "crítico" and resultado.get("suporte_vida") == "crítico":
        return "CASCATA DETECTADA: Energia crítica comprometeu o suporte à vida."
    if resultado["energia"] == "crítico" and resultado.get("habitacao") == "crítico":
        return "CASCATA: Colapso energético comprometeu o sistema de climatização."
    if (
        resultado.get("comunicacao") == "crítico"
        and resultado.get("suporte_vida") == "crítico"
    ):
        return "CASCATA: Sem contato com a Terra e suporte à vida em risco. Emergência máxima."
    if (
        resultado.get("suporte_vida") == "crítico"
        and resultado.get("suporte_medico") == "crítico"
    ):
        return "CASCATA: Falha simultânea no suporte à vida e no atendimento médico. Vidas em perigo."
    if resultado["energia"] == "alerta" and resultado.get("comunicacao") == "crítico":
        return "CASCATA: Energia baixa acelerou a degradação da comunicação."
    if (
        resultado.get("laboratorio") == "crítico"
        and resultado.get("suporte_medico") == "crítico"
    ):
        return "CASCATA: Colapso total dos sistemas científicos e médicos."
    return None


def organizar_turno(dados_turno):
    historico_baterias.append(dados_turno["reserva_pct"])
    historico_geracao_solar.append(dados_turno["geracao_solar_kwh"])
    historico_geracao_eolica.append(dados_turno["geracao_eolica_kwh"])
    historico_consumo.append(dados_turno["consumo_kwh"])

    hierarquia_sistemas_colonia["suporte_vida"]["oxigenio"] = dados_turno[
        "mod_suporte_vida"
    ]
    hierarquia_sistemas_colonia["suporte_vida"]["reserva_oxigenio"] = dados_turno[
        "reserva_oxigenio_pct"
    ]
    hierarquia_sistemas_colonia["suporte_vida"]["agua"] = dados_turno[
        "reserva_agua_pct"
    ]
    hierarquia_sistemas_colonia["suporte_vida"]["alimentos"] = dados_turno[
        "reserva_alimentos_pct"
    ]

    hierarquia_sistemas_colonia["energia"]["solar"] = dados_turno["geracao_solar_kwh"]
    hierarquia_sistemas_colonia["energia"]["eolica"] = dados_turno["geracao_eolica_kwh"]
    hierarquia_sistemas_colonia["energia"]["armazenamento"] = dados_turno["reserva_pct"]

    hierarquia_sistemas_colonia["comunicacao"]["radio"] = dados_turno["sinal_radio"]
    hierarquia_sistemas_colonia["comunicacao"]["satellite"] = dados_turno[
        "mod_comunicacao"
    ]
    hierarquia_sistemas_colonia["comunicacao"]["laser"] = dados_turno["sinal_laser"]
    hierarquia_sistemas_colonia["comunicacao"]["janela_contato"] = dados_turno[
        "janela_comunicacao"
    ]

    hierarquia_sistemas_colonia["habitacao"]["modulo_habitacional"] = dados_turno[
        "mod_habitacao"
    ]
    hierarquia_sistemas_colonia["habitacao"]["sistema_climatizacao"] = dados_turno[
        "status_climatizacao"
    ]
    hierarquia_sistemas_colonia["habitacao"]["temperatura_interna"] = dados_turno[
        "temp_interna"
    ]

    hierarquia_sistemas_colonia["laboratorio"]["analise_solo"] = dados_turno[
        "status_analise_solo"
    ]
    hierarquia_sistemas_colonia["laboratorio"]["analise_biologica"] = dados_turno[
        "status_analise_biologica"
    ]

    hierarquia_sistemas_colonia["suporte_medico"]["monitoramento_saude"] = dados_turno[
        "status_monitoramento_saude"
    ]
    hierarquia_sistemas_colonia["suporte_medico"]["sinais_vitais_pct"] = dados_turno[
        "sinais_vitais_tripulantes_pct"
    ]
    hierarquia_sistemas_colonia["suporte_medico"]["estoque_medicamentos"] = dados_turno[
        "status_estoque_medicamentos"
    ]
    hierarquia_sistemas_colonia["suporte_medico"]["nivel_medicamentos_pct"] = (
        dados_turno["nivel_estoque_medicamentos_pct"]
    )

    if dados_turno["evento_externo"] != "nenhum":
        pilha_eventos_criticos.append(
            f"Turno {dados_turno['turno']} -> {dados_turno['evento_externo'].upper()}"
        )

    modulos_secundarios = ["mod_comunicacao", "mod_laboratorio", "mod_suporte_medico"]
    for mod in modulos_secundarios:
        if dados_turno[mod] == 0:
            alerta = f"🚨 [FILA] Módulo Secundário {mod.upper()} desativado para gerenciamento de carga!"
            if alerta not in fila_alertas:
                fila_alertas.append(alerta)


# =====================================================================
# REQUISITO 8.2: BUSCA RÁPIDA EM DICIONÁRIO / TABELA HASH (Acesso O(1))
# =====================================================================
def menu_busca_rapida(hierarquia):
    """
    Exibe um menu interativo permitindo acessar os dados finais dos módulos
    instantaneamente através de busca por chaves de dicionário.
    """
    print("\n" + "=" * 85)
    print("  SISTEMA DE CONSULTA RÁPIDA (ACESSO DIRETO) - STATUS FINAL DOS MÓDULOS  ")
    print("=" * 85)

    # Mapeamento numérico das opções para as chaves da hierarquia
    opcoes = {
        "1": ("Suporte à Vida", "suporte_vida"),
        "2": ("Energia", "energia"),
        "3": ("Comunicação", "comunicacao"),
        "4": ("Habitação", "habitacao"),
        "5": ("Laboratório", "laboratorio"),
        "6": ("Suporte Médico", "suporte_medico"),
    }

    # REQUISITO PILHA (LIFO): exibir o último evento crítico registrado ao entrar no menu
    # .pop() remove e retorna o elemento do TOPO da pilha (Last In, First Out)
    if pilha_eventos_criticos:
        ultimo_evento = pilha_eventos_criticos.pop()
        print(f"\n  [PILHA LIFO] Último evento crítico registrado: {ultimo_evento}")
        print("  (Removido do topo da pilha para consulta — comportamento LIFO)")

    while True:
        print("\nSelecione o módulo para consultar o status:")
        for numero, (nome_exibicao, _) in opcoes.items():
            print(f"  [{numero}] - {nome_exibicao}")
        print("  [0] - Desligar Terminal e Encerrar")

        escolha = input("\nDigite o número da opção desejada: ").strip()

        if escolha == "0":
            print("\n[!] Desligando terminais da Colônia Aurora Prime... Até logo!\n")
            time.sleep(1.0)
            break
        elif escolha in opcoes:
            chave_do_dicionario = opcoes[escolha][1]
            nome_do_modulo = opcoes[escolha][0]

            # Acesso direto O(1)
            dados_modulo = hierarquia[chave_do_dicionario]

            print(f"\n--- DADOS DE STATUS: {nome_do_modulo.upper()} ---")
            for metrica, valor in dados_modulo.items():
                metrica_formatada = metrica.replace("_", " ").title()
                print(f"  > {metrica_formatada}: {valor}")
            print("-" * 45)
            time.sleep(0.5)
        else:
            print("\n[!] Opção inválida. Por favor, escolha um número válido do menu.")


# =====================================================================
# PIPELINE PRINCIPAL (Execução e Exportação)
# =====================================================================
def main():
    exibir_introducao_aurora()

    # TRATAMENTO DE EXCEÇÃO E DATA CLEANSING
    try:
        # 1. Lê o ficheiro ignorando os espaços logo após a vírgula
        df = pd.read_csv(csv_path, skipinitialspace=True)

        # 2. Limpa quaisquer espaços perdidos no início ou fim dos nomes das colunas
        df.columns = df.columns.str.strip()

        # 3. Limpa os espaços extra nos dados de texto (ex: "aberta   " vira "aberta")
        for col in df.select_dtypes(["object"]).columns:
            df[col] = df[col].str.strip()

        print(
            f"Matriz de telemetria carregada. ({len(df)} registros limpos e prontos para análise).\n"
        )
        time.sleep(1.0)

    except FileNotFoundError:
        print(
            "\n[!] FALHA CRÍTICA: Link de dados da telemetria (CSV) corrompido ou offline."
        )
        print(f"    Caminho procurado: {csv_path}")
        print(
            "    Verifique se o arquivo está na pasta 'data/'. Abortando simulação.\n"
        )
        return
    except Exception as e:
        print(f"\n[!] FALHA CRÍTICA INESPERADA: Ocorreu um erro ao ler os dados -> {e}")
        return

    matriz_telemetria = df.to_dict(orient="records")

    # REQUISITO MATRIZ/LISTA DE LISTAS: estrutura 2D explícita com leituras por horário e variável
    # Formato: matriz_horarios[indice_turno][indice_variavel] → valor da variável no turno
    # Colunas selecionadas para a matriz 2D:
    VARIAVEIS_MATRIZ = ["hora", "reserva_pct", "geracao_solar_kwh", "geracao_eolica_kwh", "consumo_kwh", "temp_interna"]
    # lista[horario][variavel]: cada linha = 1 turno; cada coluna = 1 variável
    matriz_horarios = [
        [turno.get(var, None) for var in VARIAVEIS_MATRIZ]
        for turno in matriz_telemetria
    ]
    # Exemplo de acesso: matriz_horarios[0][1] → reserva_pct do turno 1
    dados_exportacao = []

    for turno_atual in matriz_telemetria:
        organizar_turno(turno_atual)

        evento = processar_evento_externo(turno_atual)
        sensor = votar_sensor(historico_temperatura, turno_atual)
        resultado = diagnosticar(hierarquia_sistemas_colonia)
        cascata = detectar_cascata(resultado)
        previsao_energia = calcular_previsao_energia(historico_baterias)
        score_atual = calcular_score_saude(
            hierarquia_sistemas_colonia, evento, previsao_energia
        )
        lista_acoes = gerar_recomendacoes(resultado, cascata, turno_atual, score_atual)

        sol_marciano = ((turno_atual["turno"] - 1) // 6) + 1
        dados_exportacao.append(
            {
                "Turno": turno_atual["turno"],
                "Sol": sol_marciano,
                "Hora": turno_atual["hora"],
                "Cenário": turno_atual["cenario"],
                "Score Saúde (%)": score_atual,
                "Baterias (%)": round(
                    hierarquia_sistemas_colonia["energia"]["armazenamento"], 1
                ),
                "Evento": turno_atual["evento_externo"],
                "Diagnóstico": str(resultado),
                "Ações Recomendadas": " | ".join(lista_acoes),
            }
        )

        if turno_atual["hora"] == "04:00" or cascata or score_atual < 40:
            barra_visual = gerar_barra_score(score_atual)
            print(
                f"» RELATÓRIO DE FECHO - SOL {sol_marciano:02d} | Turno: {turno_atual['turno']:03d} | Cenário: {turno_atual['cenario']}"
            )
            print(f"  SAÚDE DA MISSÃO: {barra_visual}")

            if (
                hierarquia_sistemas_colonia["comunicacao"]["janela_contato"]
                == "fechada"
            ):
                print("  [!] Janela Fechada (MODO AUTÔNOMO).")

            print(
                f"  Baterias: {hierarquia_sistemas_colonia['energia']['armazenamento']:.1f}%"
            )
            print(f"  Eventos do Dia: {evento}")
            print(f"  {previsao_energia}")

            if cascata:
                print(f"  Alerta Crítico!: {cascata}")

            print("  [PLANO DE AÇÃO DIÁRIO]:")
            for acao in lista_acoes:
                print(f"    {acao}")

            # --- INTEGRAÇÃO DA COMUNICAÇÃO FIFO E DELAY ---
            print("  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            resumo_pacote = f"SOL {sol_marciano} | Saúde: {score_atual}% | Bateria: {hierarquia_sistemas_colonia['energia']['armazenamento']:.1f}%"
            log_comunicacao = gerir_transmissao_terra(
                hierarquia_sistemas_colonia, turno_atual["cenario"], resumo_pacote
            )
            print(log_comunicacao)

            print("=" * 85)
            time.sleep(0.1)

    print("\n[SIMULAÇÃO CONCLUÍDA] 56 Sóis marcianos processados.")

    docs_dir = base_dir.parent / "docs"
    docs_dir.mkdir(exist_ok=True)

    caminho_exportacao = docs_dir / "relatorio_execucao_aurora.csv"
    df_exportacao = pd.DataFrame(dados_exportacao)
    df_exportacao.to_csv(caminho_exportacao, index=False)

    print(f"[EXTRAÇÃO] Tabela de auditoria salva com sucesso em: {caminho_exportacao}")

    # --- INÍCIO DO MENU DE CONSULTA O(1) ---
    menu_busca_rapida(hierarquia_sistemas_colonia)


if __name__ == "__main__":
    main()
