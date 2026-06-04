import pandas as pd
from pathlib import Path
import time

# =====================================================================
# REQUISITO 8.2: ESTRUTURAS DE DADOS
# =====================================================================

fila_alertas = []  # alertas por prioridade
pilha_eventos_criticos = []  # últimos eventos analisados

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
csv_path = base_dir.parent / "data" / "dados_telemetria_marte.csv"


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
    # classifica o evento externo do turno e retorna descrição do impacto operacional
    if turno["evento_externo"] == "nenhum":
        return "Sem eventos externos. Operação nominal."
    elif turno["evento_externo"] == "tempestade_areia":
        return "Tempestade de areia detectada. Geração solar comprometida e visibilidade reduzida"
    elif turno["evento_externo"] == "tempestade_solar":
        return "Tempestade solar em curso. Comunicação instável e radiação elevada."
    elif turno["evento_externo"] == "micrometeoro":
        return "Impacto de micrometeoro detectado. Possível falha de sensor."
    else:
        return "Um evento externo não identificado acaba de ocorrer"


# =====================================================================
# REQUISITO 8.3 (NEXT): PROTOCOLO DE VOTAÇÃO DE SENSORES
# =====================================================================


def votar_sensor(historico_temperatura, turno_atual):
    # detecta leitura inválida (-999) e estima valor real pela média histórica
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
        # leitura válida: registra no histórico e retorna o valor atual
        historico_temperatura.append(turno_atual["temp_interna"])
        return f"Temperatura interna: {turno_atual['temp_interna']:.1f}°C"


# =====================================================================
# REQUISITO 8.3: MOTOR DE DIAGNÓSTICO — REGRAS LÓGICAS
# =====================================================================


def diagnosticar(hierarquia_sistemas_colonia):
    # avalia cada sistema da colônia e classifica em normal, alerta ou crítico
    resultado = {}
    # extração de variáveis para legibilidade
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

    analise_solo = hierarquia_sistemas_colonia["laboratorio"]["analise_solo"]  # 0 ou 1
    analise_biologica = hierarquia_sistemas_colonia["laboratorio"][
        "analise_biologica"
    ]  # 0 ou 1

    monitoramento_saude = hierarquia_sistemas_colonia["suporte_medico"][
        "monitoramento_saude"
    ]  # 0 ou 1
    estoque_medicamentos = hierarquia_sistemas_colonia["suporte_medico"][
        "estoque_medicamentos"
    ]  # 0 ou 1

    # diagnóstico de energia: normal >= 50%, alerta >= 20%, crítico < 20%
    if energia_armazenada <= 100 and energia_armazenada >= 50:
        resultado["energia"] = "normal"
    elif energia_armazenada < 50 and energia_armazenada >= 20:
        resultado["energia"] = "alerta"
    else:
        resultado["energia"] = "crítico"
    # diagnóstico de comunicação: baseado em sinal de rádio e laser (0-100)
    if radio >= 50 and laser >= 50:
        resultado["comunicacao"] = "normal"
    elif radio >= 20 and laser >= 20:
        resultado["comunicacao"] = "alerta"
    else:
        resultado["comunicacao"] = "crítico"
    # módulo de satélite desligado força status crítico independente dos sinais
    if not sattelite == 1:
        resultado["comunicacao"] = "crítico"
    # diagnóstico de suporte à vida: baseado em reservas de água e alimentos
    if agua >= 70 and alimentos >= 70:
        resultado["suporte_vida"] = "normal"
    elif agua >= 40 and alimentos >= 40:
        resultado["suporte_vida"] = "alerta"
    else:
        resultado["suporte_vida"] = "crítico"
    # falha no oxigênio força status crítico independente das reservas
    if not oxigenio == 1:
        resultado["suporte_vida"] = "crítico"
    # diagnóstico de habitação: baseado na temperatura interna (°C)
    if temperatura_interna >= 18 and temperatura_interna <= 26:
        resultado["habitacao"] = "normal"
    elif (temperatura_interna >= 10 and temperatura_interna <= 18) or (
        temperatura_interna >= 26 and temperatura_interna <= 35
    ):
        resultado["habitacao"] = "alerta"
    elif temperatura_interna < 10 or temperatura_interna > 35:
        resultado["habitacao"] = "crítico"
    # falha no climatizador ou módulo habitacional força status crítico
    if (not sistema_climatizacao == 1) or (not modulo_habitacional == 1):
        resultado["habitacao"] = "crítico"
    # diagnóstico de laboratório: crítico se qualquer estação estiver inoperante
    if (not analise_solo == 1) or (not analise_biologica == 1):
        resultado["laboratorio"] = "crítico"
    else:
        resultado["laboratorio"] = "normal"
    # diagnóstico de suporte médico: crítico se qualquer subsistema estiver inoperante
    if (not monitoramento_saude == 1) or (not estoque_medicamentos == 1):
        resultado["suporte_medico"] = "crítico"
    else:
        resultado["laboratorio"] = "normal"

    return resultado


# =====================================================================
# REQUISITO 8.4: DETECÇÃO DE FALHAS EM CASCATA
# =====================================================================


def detectar_cascata(resultado):
    # verifica combinações de falhas simultâneas que indicam encadeamento crítico
    if resultado["energia"] == "crítico" and resultado["comunicacao"] == "crítico":
        return "CASCATA DETECTADA: Energia crítica comprometeu a comunicação."
    if resultado["energia"] == "crítico" and resultado["suporte_vida"] == "crítico":
        return "CASCATA DETECTADA: Energia crítica comprometeu o suporte à vida."
    if resultado["energia"] == "crítico" and resultado["habitacao"] == "crítico":
        return "CASCATA: Colapso energético comprometeu o sistema de climatização."
    if resultado["comunicacao"] == "crítico" and resultado["suporte_vida"] == "crítico":
        return "CASCATA: Sem contato com a Terra e suporte à vida em risco. Emergência máxima."
    if (
        resultado["suporte_vida"] == "crítico"
        and resultado["suporte_medico"] == "crítico"
    ):
        return "CASCATA: Falha simultânea no suporte à vida e no atendimento médico. Vidas em perigo."
    if resultado["energia"] == "alerta" and resultado["comunicacao"] == "crítico":
        return "CASCATA: Energia baixa acelerou a degradação da comunicação."
    if (
        resultado["laboratorio"] == "crítico"
        and resultado["suporte_medico"] == "crítico"
    ):
        return "CASCATA: Colapso total dos sistemas científicos e médicos."
    return None  # nenhuma cascata detectada


def organizar_turno(dados_turno):
    # mapeia os dados da linha atual do csv e atualiza a árvore de hierarquia de sistemas da colônia
    # 1. séries temporais (Listas)
    historico_baterias.append(dados_turno["reserva_pct"])
    historico_geracao_solar.append(dados_turno["geracao_solar_kwh"])
    historico_geracao_eolica.append(dados_turno["geracao_eolica_kwh"])
    historico_consumo.append(dados_turno["consumo_kwh"])

    # 2. atualização completa da árvore hierárquica de sistemas e subsistemas da colônia
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

    # 3. gerenciamento da pilha de eventos críticos
    if dados_turno["evento_externo"] != "nenhum":
        pilha_eventos_criticos.append(
            f"Turno {dados_turno['turno']} -> {dados_turno['evento_externo'].upper()}"
        )

    # 4. fila de alertas baseada em qualquer módulo secundário que vá para 0
    modulos_secundarios = ["mod_comunicacao", "mod_laboratorio", "mod_suporte_medico"]
    for mod in modulos_secundarios:
        if dados_turno[mod] == 0:
            alerta = f"🚨 [FILA] Módulo Secundário {mod.upper()} desativado para gerenciamento de carga!"
            if alerta not in fila_alertas:
                fila_alertas.append(alerta)


# =====================================================================
# PIPELINE PRINCIPAL (Execução)
# =====================================================================
def main():
    exibir_introducao_aurora()

    df = pd.read_csv(csv_path)
    print(
        f"Matriz de telemetria histórica carregada com sucesso. ({len(df)} registros para análise).\n"
    )
    time.sleep(1.0)

    matriz_telemetria = df.to_dict(orient="records")

    for turno_atual in matriz_telemetria:
        organizar_turno(turno_atual)

        evento = processar_evento_externo(turno_atual)
        sensor = votar_sensor(historico_temperatura, turno_atual)
        resultado = diagnosticar(hierarquia_sistemas_colonia)
        cascata = detectar_cascata(resultado)

        # Painel de monitoramento operacional completo
        print(
            f"» SOL-TURNO: {turno_atual['turno']:03d} | Horário: {turno_atual['hora']} | Cenário: {turno_atual['cenario']}"
        )
        print(
            f"  Geração Solar Atual: {hierarquia_sistemas_colonia['energia']['solar']:.2f} kWh"
        )
        print(
            f"  Geração Eólica Atual: {hierarquia_sistemas_colonia['energia']['eolica']:.2f} kWh"
        )
        print(f"  Consumo de Energia: {turno_atual['consumo_kwh']:.2f} kWh")
        print(
            f"  Capacidade das Baterias: {hierarquia_sistemas_colonia['energia']['armazenamento']:.2f}%"
        )
        print(f"  Alertas - Quantidade Atual: {len(fila_alertas)}")
        print(
            f"  Último Evento Crítico: {pilha_eventos_criticos[-1] if pilha_eventos_criticos else 'Nenhum'}"
        )
        print("-" * 85)
        print(f"  Evento Externo: {evento}")
        print(f"  Sensor Temperatura: {sensor}")
        print(f"  Diagnóstico: {resultado}")
        if cascata:
            print(f"  Alerta de cascata!: {cascata}")
        time.sleep(0.05)

    print("\n[SIMULAÇÃO CONCLUÍDA] 56 Sóis marcianos processados com sucesso.")


if __name__ == "__main__":
    main()
