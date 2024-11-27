"use client";
import { useState, useEffect } from 'react';
import styles from './GerenciarVeiculo.module.css';
import { useRouter } from 'next/navigation';
import HamburguerMenu from '../HamburguerMenu/page';
const GerenciarVeiculo = () => {
    const [marca, setMarca] = useState<string>("");
    const [modelo, setModelo] = useState<string>("");
    const [ano, setAno] = useState<string>("");
    const [placa, setPlaca] = useState<string>("");
    const router = useRouter();
    useEffect(() => {
        const vehicleData = localStorage.getItem("vehicleData");
        if (vehicleData) {
            const { marca, modelo, ano, placa } = JSON.parse(vehicleData);
            setMarca(marca);
            setModelo(modelo);
            setAno(ano);
            setPlaca(placa);
        }
    }, []);
    const handleSave = () => {
        const updatedVehicleData = {
            marca,
            modelo,
            ano,
            placa,
        };
        localStorage.setItem("vehicleData", JSON.stringify(updatedVehicleData));
        alert("Dados do veículo atualizados com sucesso!");
    };
    const handleDelete = () => {
        localStorage.removeItem("vehicleData");
        alert("Veículo excluído com sucesso!");
        router.push("/");
    };
    const handleSaveAndGoBack = () => {
        handleSave();
        router.push("/Veiculos");
    };
    const handleAnoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (!/^\d*$/.test(value)) {
            alert("O ano deve conter apenas dígitos.");
            return;
        }
        if (value.length <= 4) {
            setAno(value);
            if (value.length === 4 && !/^\d{4}$/.test(value)) {
                alert("O ano deve conter 4 dígitos numéricos.");
                setAno("");
            }
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
                <h1 className={styles.title}>Gerenciar Veículo</h1>
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
                <div className={styles.escapamento}></div>
                <button onClick={handleSaveAndGoBack} className={styles.botaoSalvar}>Salvar</button>
                <button onClick={handleDelete} className={styles.botaoExcluir}>Excluir Veículo</button>
            </div>
        </div>
        </>
    );
};
export default GerenciarVeiculo;
