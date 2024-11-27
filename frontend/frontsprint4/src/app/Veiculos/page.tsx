"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import styles from './Veiculos.module.css';
import HamburguerMenu from '../HamburguerMenu/page';

const ExibirVeiculo = () => {
    const [veiculoData, setveiculoData] = useState<{ id: string; marca: string; modelo: string; ano: number; placa: string; quilometragem: string }[]>([]);
    const [userCpf, setUserCpf] = useState<string | null>(null);

    useEffect(() => {
        const storedUserData = localStorage.getItem("usuario");
        
        if (storedUserData) {
            const userData = JSON.parse(storedUserData);
            setUserCpf(userData.cpfUsuario);

            // Fazer o fetch dos veículos do usuário
            fetch(`http://localhost:8080/sprint4-java/rest/veiculo/usuario/${userData.cpfUsuario}`)
                .then(response => response.json())
                .then(data => setveiculoData(data))
                .catch(error => console.error("Erro ao buscar veículos:", error));
        }
    }, []);

    return (
        <>
            <HamburguerMenu />
            <div className={styles.container}>
                <h1 className={styles.title}>Dados do(s) Veículo(s)</h1>
                {veiculoData.length > 0 ? (
                    veiculoData.map((veiculo, index) => (
                        <div key={index} className={styles.veiculoInfo}>
                            <p><strong>Marca:</strong> {veiculo.marca}</p>
                            <p><strong>Modelo:</strong> {veiculo.modelo}</p>
                            <p><strong>Ano:</strong> {veiculo.ano}</p>
                            <p><strong>Placa:</strong> {veiculo.placa}</p>
                            <p><strong>Quilometragem:</strong> {veiculo.quilometragem} km</p>
                            {/* Link para a página de gerenciamento do veículo */}
                            <Link href={`/GerenciarVeiculo/${veiculo.placa}`}>
                                <button className={styles.botaoAlterar}>Alterar Dados do Veículo</button>
                            </Link>
                        </div>
                    ))
                ) : (
                    <p className={styles.noData}>Nenhum dado de veículo encontrado.</p>
                )}
            </div>
        </>
    );
};

export default ExibirVeiculo;