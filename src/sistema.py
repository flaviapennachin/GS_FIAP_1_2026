
import pandas as pd
from pathlib import Path
import time


# =====================================================================
# REQUISITO 8.2: ESTRUTURAS DE DADOS 
# =====================================================================

fila_alertas = []                       # alertas por prioridade
pilha_eventos_criticos = []             # últimos eventos analisados

# ESTRUTURA PARA ANÁLISE DE EFICIÊNCIA ENERGÉTICA
historico_baterias = []                 # monitoramento de ciclos de carga
historico_geracao_solar = []            # análise de eficiência energética
historico_geracao_eolica = []           # análise de eficiência energética    
historico_consumo = []                  # análise de eficiência energética

#DICIONÁRIO DE SISTEMAS E SUBSISTEMAS  
# hierarquia de sistemas e subsistemas para monitoramento e controle operacional

hierarquia_sistemas_colonia = {
    'suporte_vida': { 
        'oxigenio': 1,                    # mapeamento do mod_suporte_vida (1 = operacional, 0 = falha )
            'agua': 98.8,                 # percetual de reserva de água (0-100%)
            'alimentos': 99.9             # percetual de reserva de alimentos (0-100%)
    },
    'energia': { 
        'solar': 38.35,                   # geração solar em kWh
        'eolica': 24.24,                  # geração eólica em kWh
        'armazenamento': 85.57            # percentual de reserva de energia (0-100%)
    },
    'comunicacao': {
        'radio': 0.95,                     # qualidade do sinal de rádio (0-1)
        'satellite': 0.9,                  # qualidade do sinal de satélite (0-1)
        'laser': 0.96                      # qualidade do sinal de comunicação a laser (0-1)    
    },
    'habitacao': {
        'modulo_habitacional': 1,          # status do módulo habitacional (1 = operacional, 0 = falha)
        'sistema_climatizacao': 1,         # status do sistema de climatização (1 = operacional, 0 = falha)
        'temperatura_interna': 22.0        # temperatura interna do habitat em °C
    },
    'laboratorio': {
        'analise_solo': 1,                # status da estaçao de análise de solo (1 = operacional, 0 = falha)
        'analise_biologica': 1            # status da estaçao de análises biológicas (1 = operacional, 0 = falha)
    },
    'suporte_medico': {
        'monitoramento_saude': 1,         # status do monitoramento de saúde (1 = operacional, 0 = falha)  
        'estoque_medicamentos': 1         # status do estoque de medicamentos (1 = operacional, 0 = falha)
    } 
}

# =====================================================================
# REQUISITO 8.1: LEITURA E INGESTÃO DE DADOS
# =====================================================================

base_dir = Path(__file__).resolve().parent
csv_path = base_dir.parent / 'data' / 'dados_telemetria_marte.csv'


def exibir_introducao_aurora():
    print("=" * 85)
    print("      AURORA PRIME — SISTEMA INTELIGENTE DE CONTROLE OPERACIONAL MARCIANO      ")
    print("          Desenvolvimento Integrado: Desafio Global Solution 2026            ")
    print("=" * 85)
    print("\n[CONFIGURAÇÃO INICIAL]")
    print("• Localização: Colônia Primária, Planície de Marte.")
    print("• Frequência de Monitoramento: Ciclos de 4 horas planetárias (56 Sóis).")
    print("\nIniciando matriz de telemetria histórica...")
    print("-" * 85)
    time.sleep(1.8) 
    

def organizar_turno(dados_turno): 
    # mapeia os dados da linha atual do csv e atualiza a árvore de hierarquia de sistemas da colônia
    
   # 1. séries temporais (Listas)
    historico_baterias.append(dados_turno["reserva_pct"])
    historico_geracao_solar.append(dados_turno["geracao_solar_kwh"])
    historico_geracao_eolica.append(dados_turno["geracao_eolica_kwh"])
    historico_consumo.append(dados_turno["consumo_kwh"])
    
    # 2. atualização completa da árvore hierárquica de sistemas e subsistemas da colônia
    hierarquia_sistemas_colonia['suporte_vida']['oxigenio'] = dados_turno['mod_suporte_vida']
    hierarquia_sistemas_colonia['suporte_vida']['agua'] = dados_turno['reserva_agua_pct']
    hierarquia_sistemas_colonia['suporte_vida']['alimentos'] = dados_turno['reserva_alimentos_pct']
    
    hierarquia_sistemas_colonia['energia']['solar'] = dados_turno['geracao_solar_kwh']
    hierarquia_sistemas_colonia['energia']['eolica'] = dados_turno['geracao_eolica_kwh']
    hierarquia_sistemas_colonia['energia']['armazenamento'] = dados_turno['reserva_pct']
    
    hierarquia_sistemas_colonia['comunicacao']['radio'] = dados_turno['sinal_radio']
    hierarquia_sistemas_colonia['comunicacao']['satellite'] = dados_turno['mod_comunicacao']
    hierarquia_sistemas_colonia['comunicacao']['laser'] = dados_turno['sinal_laser']
    
    hierarquia_sistemas_colonia['habitacao']['modulo_habitacional'] = dados_turno['mod_habitacao']
    hierarquia_sistemas_colonia['habitacao']['sistema_climatizacao'] = dados_turno['status_climatizacao']
    hierarquia_sistemas_colonia['habitacao']['temperatura_interna'] = dados_turno['temp_interna']
    
    hierarquia_sistemas_colonia['laboratorio']['analise_solo'] = dados_turno['status_analise_solo']
    hierarquia_sistemas_colonia['laboratorio']['analise_biologica'] = dados_turno['status_analise_biologica']
    
    hierarquia_sistemas_colonia['suporte_medico']['monitoramento_saude'] = dados_turno['status_monitoramento_saude']
    hierarquia_sistemas_colonia['suporte_medico']['estoque_medicamentos'] = dados_turno['status_estoque_medicamentos']

    # 3. gerenciamento da pilha de eventos críticos
    if dados_turno["evento_externo"] != "nenhum":
        pilha_eventos_criticos.append(f"Turno {dados_turno['turno']} -> {dados_turno['evento_externo'].upper()}")

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
    print(f"Matriz de telemetria histórica carregada com sucesso. ({len(df)} registros para análise).\n")
    time.sleep(1.0)

    matriz_telemetria = df.to_dict(orient="records")

    for turno_atual in matriz_telemetria:
        organizar_turno(turno_atual)
        
       # Painel de monitoramento operacional completo
        print(f"» SOL-TURNO: {turno_atual['turno']:03d} | Horário: {turno_atual['hora']} | Cenário: {turno_atual['cenario']}")
        print(f"  Geração Solar Atual: {hierarquia_sistemas_colonia['energia']['solar']:.2f} kWh")
        print(f"  Geração Eólica Atual: {hierarquia_sistemas_colonia['energia']['eolica']:.2f} kWh")
        print(f"  Consumo de Energia: {turno_atual['consumo_kwh']:.2f} kWh")
        print(f"  Capacidade das Baterias: {hierarquia_sistemas_colonia['energia']['armazenamento']:.2f}%")
        print(f"  Alertas - Quantidade Atual: {len(fila_alertas)}")
        print(f"  Último Evento Crítico: {pilha_eventos_criticos[-1] if pilha_eventos_criticos else 'Nenhum'}")
        print("-" * 85)
        
        time.sleep(0.05) 

    print("\n[SIMULAÇÃO CONCLUÍDA] 56 Sóis marcianos processados com sucesso.")

if __name__ == "__main__":
    main()