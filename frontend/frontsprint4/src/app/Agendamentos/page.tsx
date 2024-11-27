"use client";
import { useEffect, useState } from 'react';
import styles from './Agendamentos.module.css';
import HamburguerMenu from '../HamburguerMenu/page';

interface Usuario {
    cpfUsuario: string;
    nomeUsuario: string;
    senha: string;
    email: string;
    telefone: string;
}

interface Centro {
    idCentro: string;
    nomeCentro: string;
    enderecoCentro: string;
    telefoneCentro: string;
    horarioFuncionamento: string;
}

interface Servico {
    idServico: string;
    tipoServico: string;
    descricaoServico: string;
    precoServico: number;
    duracaoServico: number;
}

interface Veiculo {
    marca: string;
    modelo: string;
    placa: string;
    ano: number;
    quilometragem: number; 
    usuario: Usuario;
}

interface Agendamento {
    idAgendamento: string;
    data: string;
    hora: string;
    descricao: string;
    centro: Centro;
    servico: Servico;
    veiculo: Veiculo;
}

const Agendamentos = () => {
    const [tipoManutencao, setTipoManutencao] = useState<string>("");
    const [data, setData] = useState<string>(new Date().toISOString().split('T')[0]); // Data atual
    const [horario, setHorario] = useState<string>("");
    const [centros, setCentros] = useState<Centro[]>([]);
    const [servicos, setServicos] = useState<Servico[]>([]);
    const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
    const [centroSelecionado, setCentroSelecionado] = useState<string>("");
    const [servicoSelecionado, setServicoSelecionado] = useState<string>("");
    const [veiculoSelecionado, setVeiculoSelecionado] = useState<string>("");
    const [agendamentos, setAgendamentos] = useState<Agendamento[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const centrosResponse = await fetch('http://localhost:8080/sprint4-java/rest/centro');
                const centrosData: Centro[] = await centrosResponse.json();
                setCentros(centrosData);

                const servicosResponse = await fetch('http://localhost:8080/sprint4-java/rest/servico');
                const servicosData: Servico[] = await servicosResponse.json();
                setServicos(servicosData);

                const usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
                const cpf = usuario.cpfUsuario;

                if (cpf) {
                    const veiculosResponse = await fetch(`http://localhost:8080/sprint4-java/rest/veiculo/usuario/${cpf}`);
                    const veiculosData: Veiculo[] = await veiculosResponse.json();
                    setVeiculos(veiculosData);

                    const agendamentosResponse = await fetch(`http://localhost:8080/sprint4-java/rest/agendamento/usuario/${cpf}`);
                    const agendamentosData: Agendamento[] = await agendamentosResponse.json();
                    setAgendamentos(agendamentosData);
                }
            } catch (error) {
                console.error("Erro ao buscar dados:", error);
            }
        };

        fetchData();
    }, []);

    const handleAgendar = async () => {
        // Validação do horário
        const horaParts = horario.split(":");
        const horaInt = parseInt(horaParts[0]);
        const minutoInt = parseInt(horaParts[1]);

        if (horaInt < 8 || horaInt > 22) {
            alert("O horário deve estar entre 08:00 e 22:00.");
            return;
        }

        const novoAgendamento = {
            data,
            hora: horario,
            descricao: tipoManutencao,
            centro: {
                idCentro: centroSelecionado,
            },
            servico: {
                idServico: servicoSelecionado,
            },
            veiculo: veiculos.find(veiculo => veiculo.placa === veiculoSelecionado)
        };

        try {
            const response = await fetch('http://localhost:8080/sprint4-java/rest/agendamento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(novoAgendamento),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error('Erro ao agendar: ' + errorText);
            }

            const result = await response.json();
            alert("Agendamento realizado com sucesso!");
            setAgendamentos([...agendamentos, result]);

            setTipoManutencao("");
            setData(new Date().toISOString().split('T')[0]); // Resetar para a data atual
            setHorario("");
            setCentroSelecionado("");
            setServicoSelecionado("");
            setVeiculoSelecionado(""); 
            window.location.reload()
        } catch (error) {
            console.error("Erro ao agendar:", error);
            alert("Falha ao agendar. Tente novamente.");
        }
    };

    const handleRemoverAgendamento = async (idAgendamento: string) => {
        try {
            const response = await fetch(`http://localhost:8080/sprint4-java/rest/agendamento/${idAgendamento}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error("Erro ao remover agendamento");
            }
            setAgendamentos(agendamentos.filter(agendamento => agendamento.idAgendamento !== idAgendamento));
            alert("Agendamento removido com sucesso!");
        } catch (error) {
            console.error("Erro ao remover agendamento:", error);
            alert("Falha ao remover agendamento. Tente novamente.");
        }
    };

    return (
        <>
            <HamburguerMenu></HamburguerMenu>
            <div className={styles.agendamentosContainer}>
                <h1 className={styles.agendamentosTitle}>Agendamentos</h1>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Descrição:</label>
                    <input 
                        type="text" 
                        className={styles.inputText} 
                        value={tipoManutencao} 
                        onChange={(e) => setTipoManutencao(e.target.value)} 
                    />
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Data:</label>
                    <input 
                        type="date" 
                        className={styles.inputDate} 
                        value={data} 
                        onChange={(e) => setData(e.target.value)} 
                        min={new Date().toISOString().split('T')[0]} // Impedir seleção de datas anteriores
                    />
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Horário:</label>
                    <input 
                        type="time" 
                        className={styles.inputTime} 
                        value={horario} 
                        onChange={(e) => setHorario(e.target.value)} 
                    />
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Centro:</label>
                    <select 
                        className={styles.select} 
                        value={centroSelecionado} 
                        onChange={(e) => setCentroSelecionado(e.target.value)}
                    >
                        <option value="" disabled>Selecione um centro</option>
                        {centros.map(centro => (
                            <option key={centro.idCentro} value={centro.idCentro}>
                                {centro.nomeCentro}
                            </option>
                        ))}
                    </select>
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Serviço:</label>
                    <select 
                        className={styles.select} 
                        value={servicoSelecionado} 
                        onChange={(e) => setServicoSelecionado(e.target.value)}
                    >
                        <option value="" disabled>Selecione um serviço</option>
                        {servicos.map(servico => (
                            <option key={servico.idServico} value={servico.idServico}>
                                {servico.tipoServico}
                            </option>
                        ))}
                    </select>
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Veículo:</label>
                    <select 
                        className={styles.select} 
                        value={veiculoSelecionado} 
                        onChange={(e) => setVeiculoSelecionado(e.target.value)}
                    >
                        <option value="" disabled>Selecione um veículo</option>
                        {veiculos.map(veiculo => (
                            <option key={veiculo.placa} value={veiculo.placa}>
                                {`${veiculo.marca} ${veiculo.modelo} - ${veiculo.placa} (${veiculo.ano})`}
                            </option>
                        ))}
                    </select>
                </div>
                <button onClick={handleAgendar} className={styles.agendarButton}>Agendar</button>
                <h2 className={styles.subTitle}>Lista de Agendamentos</h2>
                <ul className={styles.agendamentosList}>
                    {agendamentos.map(agendamento => (
                        <li key={agendamento.idAgendamento} className={styles.agendamentoItem}>
                            <span className={styles.agendamentoSpan}>{`Data: ${agendamento.data}`}</span>
                            <br />
                            <span className={styles.agendamentoSpan}>{`Horário: ${agendamento.hora}`}</span>
                            <br />
                            <span className={styles.agendamentoSpan}>{`Serviço: ${agendamento.servico.tipoServico}`}</span>
                            <br />
                            <span className={styles.agendamentoSpan}>{`Serviço: ${agendamento.centro.nomeCentro}`}</span>
                            <br />
                            <button 
                                onClick={() => handleRemoverAgendamento(agendamento.idAgendamento)} 
                                className={styles.buttonRemove}
                            >
                                Remover
                            </button>
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
};

export default Agendamentos;



