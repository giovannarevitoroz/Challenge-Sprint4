'use client'
import { useState, useEffect } from 'react';
import { useFetchApi } from '../../../components/useFetchApi';
import Link from 'next/link';
import HamburguerMenu from '../HamburguerMenu/page';
import styles from "./Diagnostico.module.css";

const Diagnosticando = () => {
  const formatoInicialFormulario = {
    temperatura_alta: null,
    sons_estranhos: null,
    luz_painel: null,
    alto_consumo_combustivel: null,
    dificuldade_partida: null,
    carro_vibrando: null,
    problemas_freio: null,
    problemas_direcao: null,
    fumaca_escapamento: null,
    cheiros_incomuns: null,
    bateria_fraca: null,
    ar_nao_gelando: null,
    vazamento: null,
    fumaca_capo: null,
    perda_potencia: null,
    problemas_eletricos: null,
    motor_falhando: null,
    volante_desalinhado: null,
    nivel_oleo: null,
  };

  const [formDados, setFormDados] = useState(formatoInicialFormulario);
  const [result, setResult] = useState(null);
  const [formularioEnviado, setFormularioEnviado] = useState(false);
  const [veiculos, setVeiculos] = useState([]); 
  const [veiculoSelecionado, setVeiculoSelecionado] = useState(null); 
  const [usuarioLogado, setUsuarioLogado] = useState(false); // Variável para controlar se o usuário está logado

  const sintomas = [
    { id: 'temperatura_alta', label: 'Carro está com a temperatura alta?' },
    { id: 'sons_estranhos', label: 'Carro está fazendo sons estranhos?' },
    { id: 'luz_painel', label: 'Carro está com alguma luz no painel?' },
    { id: 'alto_consumo_combustivel', label: 'Carro está consumindo muita gasolina?' },
    { id: 'dificuldade_partida', label: 'Carro está com dificuldade de dar partida?' },
    { id: 'carro_vibrando', label: 'Carro está vibrando muito?' },
    { id: 'problemas_freio', label: 'Carro está com algum problema na hora de frear?' },
    { id: 'problemas_direcao', label: 'Carro está com algum problema na direção?' },
    { id: 'fumaca_escapamento', label: 'Carro está soltando muita fumaça pelo escapamento?' },
    { id: 'cheiros_incomuns', label: 'Carro está com algum cheiro incomum/ruim?' },
    { id: 'bateria_fraca', label: 'Carro está com a bateria fraca?' },
    { id: 'ar_nao_gelando', label: 'O ar-condicionado está com problema ao esfriar o carro?' },
    { id: 'vazamento', label: 'Carro está com vazamento de algum líquido?' },
    { id: 'fumaca_capo', label: 'Carro está soltando vapor/fumaça pelo capô?' },
    { id: 'perda_potencia', label: 'Carro está perdendo potência?' },
    { id: 'problemas_eletricos', label: 'Carro está com algum problema elétrico?' },
    { id: 'motor_falhando', label: 'Carro está com o motor falhando?' },
    { id: 'volante_desalinhado', label: 'Carro está com o volante desalinhado?' },
    { id: 'nivel_oleo', label: 'Carro está com o nível de óleo baixo no painel?' },
  ];

  useEffect(() => {
    const storedUserData = localStorage.getItem("usuario");

    if (storedUserData) {
      const userData = JSON.parse(storedUserData);
      setUsuarioLogado(true); // Define que o usuário está logado

      // Fazer o fetch dos veículos do usuário
      fetch(`http://localhost:8080/sprint4-java/rest/veiculo/usuario/${userData.cpfUsuario}`)
        .then(response => response.json())
        .then(data => setVeiculos(data))
        .catch(error => console.error("Erro ao buscar veículos:", error));
    }
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormDados({
      ...formDados,
      [name]: value === 'null' ? null : Number(value),
    });
  };

  const handleVeiculoChange = (e) => {
    const placaSelecionada = e.target.value;
    const veiculoSelecionadoAtual = veiculos.find(veiculo => veiculo.placa === placaSelecionada);
    setVeiculoSelecionado(veiculoSelecionadoAtual); // Armazena o objeto do veículo completo
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const algumSintomaMarcado = Object.values(formDados).some((valor) => valor === 1);
    if (!algumSintomaMarcado) {
      alert("Por favor, selecione pelo menos uma opção 'Sim' para os sintomas.");
      return;
    }

    try {
      const prediction = await useFetchApi(formDados);
      console.log('Retorno da API:', prediction);
      setResult(prediction);
      setFormularioEnviado(true);

      if (usuarioLogado) {
        const dadosParaEnviar = {
          idDiagnostico: "",
          veiculo: veiculoSelecionado, // Inclui o veículo apenas se o usuário estiver logado
          descricaoSintomas: prediction.sintomas.join(', '), 
          solucao: prediction.solucao || "Nenhuma solução fornecida.",
          orcamento: null,
          servico: null,
          categoria: prediction.diagnostico || "Categoria não especificada",
          status: ""
        };

        console.log('Dados a serem enviados:', dadosParaEnviar);

        // Enviar os dados para a API Java apenas se o usuário estiver logado
        const response = await fetch('http://localhost:8080/sprint4-java/rest/diagnostico', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(dadosParaEnviar),
        });

        if (!response.ok) {
          const errorResponseText = await response.text();
          console.error('Erro ao enviar os dados:', errorResponseText);
          alert(`Erro ao enviar os dados: ${errorResponseText}`);
          return;
        }

        const responseData = await response; 
        console.log('Dados enviados com sucesso:', responseData);
      }
    } catch (error) {
      console.error('Erro ao enviar os dados:', error);
    }
  };

  return (
    <>
      <HamburguerMenu />
      <div className={styles.textContainer}>
        <p className={styles.instructionText}>Responda às perguntas abaixo para que possamos identificar o possível problema no seu veículo</p>
      </div>

      <form onSubmit={handleSubmit} className={styles.formulario}>
        {usuarioLogado && (
          <div className={styles.veiculoContainer}>
            <label className={styles.sintomaLabel}>Selecione o veículo:</label>
            <select
              name="veiculo_id"
              value={veiculoSelecionado ? veiculoSelecionado.placa : ''}
              onChange={handleVeiculoChange}
              disabled={formularioEnviado}
              required
            >
              <option value="" disabled>Escolha um veículo</option>
              {veiculos.map((veiculo) => (
                <option key={veiculo.placa} value={veiculo.placa}>{veiculo.modelo}, {veiculo.marca} - {veiculo.placa}</option>
              ))}
            </select>
          </div>
        )}
        <hr className={styles.divisor} />

        {sintomas.map((sintoma) => (
          <div key={sintoma.id} className={styles.sintomaContainer}>
            <label className={styles.sintomaLabel}>{sintoma.label}</label>
            <div className={styles.radioContainer}>
              <label>
                <input
                  type="radio"
                  name={sintoma.id}
                  value="1"
                  checked={formDados[sintoma.id] === 1}
                  onChange={handleChange}
                  disabled={formularioEnviado}
                />
                Sim
              </label>
              <label>
                <input
                  type="radio"
                  name={sintoma.id}
                  value="0"
                  checked={formDados[sintoma.id] === 0}
                  onChange={handleChange}
                  disabled={formularioEnviado}
                />
                Não
              </label>
            </div>
            <hr className={styles.divisor} />
          </div>
        ))}
        <button type="submit" className={styles.botao} disabled={formularioEnviado}>Enviar Diagnóstico</button>
      </form>

      {formularioEnviado && result && (
        <div className={styles.resultado}>
          <h3>Resultado do Diagnóstico</h3>
          <p><strong>Diagnóstico:</strong> {result.diagnostico || "Nenhum diagnóstico encontrado."}</p>
          <p><strong>Sintomas:</strong> {result.sintomas.join(', ') || "Nenhum sintoma encontrado."}</p>
          <p><strong>Solução:</strong> {result.solucao || "Nenhuma solução fornecida."}</p>
        </div>
      )}

  <Link href="/" className={styles.voltaBotao}>Home</Link>

    </>
  );
};

export default Diagnosticando;





