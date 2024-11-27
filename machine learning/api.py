from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from pycaret.classification import load_model

# Criação do app Flask
app = Flask(__name__)
CORS(app)

# Carregar o modelo PyCaret
model = load_model('nb_pipeline')

# Rota principal para verificar o status do serviço
@app.route("/", methods=['GET'])
def home():
    return jsonify({"message": "API está rodando."}), 200

# Rota de predição
@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Obter os dados JSON do corpo da requisição
        data = request.get_json()

        print(data)

        # Extrair os valores das características
        features = [
            data.get('temperatura_alta', 0),
            data.get('sons_estranhos', 0),
            data.get('luz_painel', 0),
            data.get('alto_consumo_combustivel', 0),
            data.get('dificuldade_partida', 0),
            data.get('carro_vibrando', 0),
            data.get('problemas_freio', 0),
            data.get('problemas_direcao', 0),
            data.get('fumaca_escapamento', 0),
            data.get('cheiros_incomuns', 0),
            data.get('bateria_fraca', 0),
            data.get('ar_nao_gelando', 0),
            data.get('vazamento', 0),
            data.get('fumaca_capo', 0),
            data.get('perda_potencia', 0),
            data.get('problemas_eletricos', 0),
            data.get('motor_falhando', 0),
            data.get('volante_desalinhado', 0),
            data.get('nivel_oleo', 0)
        ]

        # Criar um DataFrame para ser usado no modelo
        features_df = pd.DataFrame([features], columns=[
            'temperatura_alta', 'sons_estranhos', 'luz_painel', 'alto_consumo_combustivel',
            'dificuldade_partida', 'carro_vibrando', 'problemas_freio', 'problemas_direcao',
            'fumaca_escapamento', 'cheiros_incomuns', 'bateria_fraca', 'ar_nao_gelando',
            'vazamento', 'fumaca_capo', 'perda_potencia', 'problemas_eletricos', 
            'motor_falhando', 'volante_desalinhado', 'nivel_oleo'
        ])

        problemas_carro = {
            "Superaquecimento": {
                "sintomas": [
                    'Temperatura Alta', 
                    'Sons Estranhos', 
                    'Fumaça no Escapamento', 
                    'Cheiro Incomum', 
                    'Vazamento de líquido', 
                    'Fumaça no Capô'
                ],
                "solucao": "Reparar ou substituir o radiador e completar o fluido de arrefecimento para evitar o superaquecimento do motor."
            },
            "Problema no Motor": {
                "sintomas": [
                    'Sons Estranhos', 
                    'Luz no Painel', 
                    'Alto Consumo de Combustível', 
                    'Dificuldade de Dar Partida', 
                    'Perda da Potência', 
                    'Motor Falhando'
                ],
                "solucao": "Inclui troca de óleo, verificação do sistema de injeção, substituição da correia dentada, limpeza do sistema de arrefecimento e ajuste das válvulas. Ideal para garantir a performance e a durabilidade do motor."
            },
            "Problema no sistema de combustível": {
                "sintomas": [
                    'Luz no Painel', 
                    'Alto Consumo de Combustível', 
                    'Dificuldade de Dar Partida', 
                    'Fumaça no Escapamento', 
                    'Cheiro Incomum', 
                    'Motor Falhando'
                ],
                "solucao": "Verificar e substituir o filtro de combustível para garantir o fluxo de combustível adequado para o motor."
            },
            "Problema nos freios": {
                "sintomas": [
                    'Sons Estranhos', 
                    'Carro Vibrando', 
                    'Freios com Problema'
                ],
                "solucao": "Substituir os discos de freio e as pastilhas se necessário para garantir a eficiência dos freios."
            },
            "Problema no alinhamento": {
                "sintomas": [
                    'Sons Estranhos', 
                    'Carro Vibrando', 
                    'Volante Desalinhado', 
                    'Direção com Problema'
                ],
                "solucao": "Verificar e ajustar o alinhamento e a geometria das rodas para garantir uma direção estável e uniforme. Se necessário, substituir componentes desgastados."
            },
            "Problema na bateria": {
                "sintomas": [
                    'Luz no Painel', 
                    'Dificuldade de Dar Partida', 
                    'Bateria Fraca', 
                    'Cheiro Incomum', 
                    'Perda da Potência', 
                    'Problemas Elétricos'
                ],
                "solucao": "Verificar e substituir a bateria se necessário, verificar o sistema de carregamento."
            },
            "Problema no Ar-condicionado": {
                "sintomas": [
                    'Sons Estranhos', 
                    'Cheiro Incomum', 
                    'Ar não Gelando'
                ],
                "solucao": "Verificar e reparar o sistema de ar condicionado, incluindo checagem de vazamentos, substituição de filtros e manutenção dos componentes do sistema."
            },
            "Vazamento de óleo": {
                "sintomas": [
                    'Luz no Painel', 
                    'Fumaça no Escapamento', 
                    'Vazamento de líquido', 
                    'Cheiro Incomum', 
                    'Nível de Óleo Baixo'
                ],
                "solucao": "Identificar e reparar o vazamento de óleo, completar o nível de óleo para evitar danos ao motor."
            },
            "Sistema de arrefecimento": {
                "sintomas": [
                    'Temperatura Alta', 
                    'Sons Estranhos', 
                    'Luz no Painel', 
                    'Fumaça no Escapamento', 
                    'Cheiro Incomum', 
                    'Vazamento de Líquido'
                ],
                "solucao": "Verificar e reparar o sistema de arrefecimento, substituir componentes defeituosos para evitar o superaquecimento do motor."
            }
}
        
        # Fazer a predição usando o modelo carregado
        prediction = model.predict(features_df)

        print(prediction)

         # Verificar se o problema identificado está em `problemas_carro`
        problema_identificado = prediction[0]
        if problema_identificado in problemas_carro:
            # Se o problema for identificado no dicionário, retornar a solução e sintomas correspondentes
            dict_problema = {
                "diagnostico": problema_identificado,
                "sintomas": problemas_carro[problema_identificado]['sintomas'],
                "solucao": problemas_carro[problema_identificado]['solucao']
            }
        else:
            # Caso contrário, retorne um diagnóstico padrão
            dict_problema = {
                "diagnostico": "Problema não identificado",
                "sintomas": [],
                "solucao": "Nenhuma ação específica identificada. Consulte um mecânico para diagnóstico mais detalhado."
            }


        # Retornar a resposta como JSON
        print(dict_problema)
        return jsonify(dict_problema), 200
    except Exception as e:
        # Caso ocorra um erro, retornar a mensagem de erro
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)