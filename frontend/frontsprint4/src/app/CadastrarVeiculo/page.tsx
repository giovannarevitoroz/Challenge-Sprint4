"use client";
import { useState, useEffect } from 'react';
import styles from './CadastrarVeiculo.module.css';
import { useRouter } from 'next/navigation';
import HamburguerMenu from '../HamburguerMenu/page';

const CadastrarVeiculo = () => {
    const [marca, setMarca] = useState<string>("");
    const [modelo, setModelo] = useState<string>("");
    const [ano, setAno] = useState<string>("");
    const [placa, setPlaca] = useState<string>("");
    const [quilometragem, setQuilometragem] = useState<string>("");
    const [usuario, setUsuario] = useState(null);  
    
    const router = useRouter();

    useEffect(() => {
        // Carrega os dados do usuário do localStorage
        const storedUsuario = localStorage.getItem("usuario");
        if (storedUsuario) {
            setUsuario(JSON.parse(storedUsuario));
        } else {
            alert("Usuário não encontrado. Por favor, faça login.");
            router.push("/login"); 
        }
    }, [router]);

    const handleSave = async () => {
        if (!usuario) {
            alert("Usuário não encontrado.");
            return;
        }

        const vehicleData = {
            marca,
            modelo,
            placa,
            ano: parseInt(ano),
            quilometragem: parseFloat(quilometragem),
            usuario,  
        };

        try {
            const response = await fetch(`http://localhost:8080/sprint4-java/rest/veiculo`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(vehicleData),
            });

            if (response.ok) {
                alert("Veículo cadastrado com sucesso!");
                router.push("/Veiculos");
            } else {
                alert("Erro ao cadastrar o veículo. Tente novamente.");
            }
        } catch (error) {
            console.error("Erro ao cadastrar o veículo:", error);
            alert("Ocorreu um erro ao tentar cadastrar o veículo.");
        }
    };

    const handleAnoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (!/^\d*$/.test(value)) {
            alert("O ano deve conter apenas dígitos.");
            return;
        }
        if (value.length <= 4) {
            setAno(value);
        }
    };

    const handlePlacaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value.toUpperCase();
        setPlaca(value);
        if (value.length >= 7) {
            const padraoPlaca = /^[A-Z]{3}-?\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$/;
            if (!padraoPlaca.test(value)) {
                alert("A placa deve estar no formato AAA-1234 ou AAA1A23.");
                setPlaca("");
            }
        }
    };

    return (
        <>
        <HamburguerMenu></HamburguerMenu>
        <div className={styles.containermaior}>
            <div className={styles.container}>
                <h1 className={styles.title}>Cadastrar Veículo</h1>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Marca:</label>
                    <input type="text" value={marca} onChange={(e) => setMarca(e.target.value)} className={styles.input} placeholder='Chevrolet'/>
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Modelo:</label>
                    <input type="text" value={modelo} onChange={(e) => setModelo(e.target.value)} className={styles.input} placeholder='Onix'/>
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Ano:</label>
                    <input type="text" value={ano} onChange={handleAnoChange} className={styles.input} maxLength={4} placeholder='2024'/>
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Placa:</label>
                    <input type="text" value={placa} onChange={handlePlacaChange} className={styles.input} maxLength={7} placeholder='AAA-1234'/>
                </div>
                <div className={styles.formGroup}>
                    <label className={styles.label}>Quilometragem:</label>
                    <input type="number" value={quilometragem} onChange={(e) => setQuilometragem(e.target.value)} className={styles.input} maxLength={9} placeholder='10000.00'/>
                </div>
                <button onClick={handleSave} className={styles.botaoSalvar}>Salvar</button>
            </div>
        </div>
        </>
    );
};

export default CadastrarVeiculo;
