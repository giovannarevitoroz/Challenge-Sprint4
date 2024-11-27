'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation'; 
import HamburguerMenu from '../../HamburguerMenu/page'; 
import styles from '../GerenciarVeiculo.module.css'; 

interface Vehicle {
    marca: string;
    modelo: string;
    ano: number;
    placa: string;
    quilometragem: string; 
}

const GerenciarVeiculo = () => {
    const { placa } = useParams(); // Acessando a placa diretamente dos parâmetros da URL
    const [vehicle, setVehicle] = useState<Vehicle | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (placa) {
            setLoading(true); // Começa o carregamento
            fetch(`http://localhost:8080/sprint4-java/rest/veiculo/${placa}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao buscar veículo');
                    }
                    return response.json();
                })
                .then(data => {
                    setVehicle(data);
                    setLoading(false); // Finaliza o carregamento
                })
                .catch(error => {
                    setError(error.message);
                    setLoading(false); // Finaliza o carregamento mesmo em caso de erro
                });
        }
    }, [placa]); 

    const handleSaveAndGoBack = () => {
        if (!vehicle) return; 

        fetch(`http://localhost:8080/sprint4-java/rest/veiculo/${placa}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(vehicle),
        })
        .then(response => {
            if (response.ok) {
                alert('Veículo atualizado com sucesso!');
                window.location.href = '/Veiculos';
            } else {
                throw new Error('Erro ao atualizar veículo');
            }
        })
        .catch(error => alert(error.message));
    };

    const handleDelete = () => {
        if (!vehicle) return;

        fetch(`http://localhost:8080/sprint4-java/rest/veiculo/${placa}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                alert('Veículo excluído com sucesso!');
                window.location.href = '/Veiculos'; 
            } else {
                throw new Error('Erro ao excluir veículo');
            }
        })
        .catch(error => alert(error.message));
    };

    const handleAnoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        // Validação ou manipulação do ano pode ser feita aqui
        setVehicle(prev => prev ? { ...prev, ano: Number(value) } : null);
    };

    const handleQuilometragemChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        // Validação para permitir 9 dígitos inteiros e 2 decimais
        if (/^\d{0,9}(\.\d{0,2})?$/.test(value)) {
            setVehicle(prev => prev ? { ...prev, quilometragem: value } : null);
        }
    };

    if (loading) return <p>Carregando dados do veículo...</p>;
    if (error) return <p>Erro: {error}</p>;

    return (
        <>
            <HamburguerMenu />
            <div className={styles.containermaior}>
                <div className={styles.container}>
                    <h1 className={styles.title}>Gerenciar Veículo</h1>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Marca:</label>
                        <input 
                            type="text" 
                            value={vehicle?.marca || ''} 
                            onChange={(e) => setVehicle(prev => prev ? { ...prev, marca: e.target.value } : null)} 
                            className={styles.input} 
                            placeholder='Chevrolet'
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Modelo:</label>
                        <input 
                            type="text" 
                            value={vehicle?.modelo || ''} 
                            onChange={(e) => setVehicle(prev => prev ? { ...prev, modelo: e.target.value } : null)} 
                            className={styles.input} 
                            placeholder='Onix'
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Ano:</label>
                        <input 
                            type="text" 
                            value={vehicle?.ano.toString() || ''} 
                            onChange={handleAnoChange} 
                            className={styles.input} 
                            maxLength={4} 
                            placeholder='2024'
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Placa:</label>
                        <input 
                            type="text" 
                            value={vehicle?.placa || ''} 
                            readOnly 
                            disabled
                            className={styles.input} 
                            placeholder='AAA-1234'
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Quilometragem:</label>
                        <input 
                            type="text" 
                            value={vehicle?.quilometragem || ''} 
                            onChange={handleQuilometragemChange} 
                            className={styles.input} 
                            maxLength={12} 
                            placeholder='123456789.99'
                        />
                    </div>
                    <div className={styles.escapamento}></div>
                    <button onClick={handleSaveAndGoBack} className={styles.botaoSalvar}>Salvar</button>
                    <button onClick={handleDelete} className={styles.botaoExcluir}>Excluir Veículo</button>
                </div>
            </div>
        </>
    );
};

export default GerenciarVeiculo;






