
export interface Predicoes {
    temperatura_alta: number;
    sons_estranhos: number;
    luz_painel: number;
    alto_consumo_combustivel: number;
    dificuldade_partida: number;
    carro_vibrando: number;
    problemas_freio: number;
    problemas_direcao: number;
    fumaca_escapamento: number;
    cheiros_incomuns: number;
    bateria_fraca: number;
    ar_nao_gelando: number;
    vazamento: number;
    fumaca_capo: number;
    perda_potencia: number;
    problemas_eletricos: number;
    motor_falhando: number;
    volante_desalinhado: number;
    nivel_oleo: number;
  }
  
  export interface PredicoesResultado {
    diagnostico: string;
    sintomas: string[];
    solucao: string;
  }
  
  export async function useFetchApi(data: Predicoes): Promise<PredicoesResultado | null> {
    try {
      const sanitizedData = Object.fromEntries(
        Object.entries(data).map(([key, value]) => [key, Number(value)])
      );
  
      console.log('Dados enviados:', sanitizedData);
  
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sanitizedData),
      });
  
      if (!response.ok) {
        throw new Error('Erro na requisição!');
      }
  
      const result: PredicoesResultado = await response.json();
      return result;
    } catch (error) {
      console.error('Erro ao fazer a predição:', error);
      return null;
    }
  }