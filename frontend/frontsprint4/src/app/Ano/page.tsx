
"use client";
import Link from "next/link";
import HamburguerMenu from "../HamburguerMenu/page";
import styles from "../Marca/Marca.module.css";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
const Ano = () => {
    const [selectedOption, setSelectedOption] = useState<string | null>(null); 
    const [selectedModel, setSelectedModel] = useState<string | null>(null); 
    const [selectedYear, setSelectedYear] = useState<string | null>(null); 
    const router = useRouter();
    useEffect(() => {
        const marca = localStorage.getItem("selectedMarca");
        const modelo = localStorage.getItem("selectedModelo");
        if (marca) {
            setSelectedOption(marca);
        } else {
            alert("Nenhuma marca selecionada. Por favor, volte para a página anterior.");
            router.push("/");
        }
        if (modelo) {
            setSelectedModel(modelo);
        } else {
            alert("Nenhum modelo selecionado. Por favor, volte para a página anterior.");
            router.push("/Modelo");
        }
    }, [router]);
    const anos = Array.from({ length: 21 }, (_, index) => 2000 + index);
    const vaiano = () => {
        if (selectedYear) {
            localStorage.setItem("selectedAno", selectedYear);
            router.push("/Diagnosticando");
        } else {
            alert("Por favor, selecione um ano.");
        }
    };
    return (
        <div className={styles.container}>
            <HamburguerMenu />
            <h1>Ano do {selectedModel} {selectedOption}</h1>
            <br />
            <div className={styles.paidedivs}>
                <div className={styles.botao1}></div>
                <div className={styles.botao2}></div>
                <div className={styles.botao2}></div>
            </div>
            <div className={styles.espaçador1}></div>
            <div className={styles.paidasdivs2}>
                <select 
                    className={styles.opsimples} 
                    onChange={(e) => setSelectedYear(e.target.value)}r
                    value={selectedYear || ""} 
                >
                    <option value="" disabled>Selecione um ano</option> {}
                    {anos.map((ano, index) => (
                        <option key={index} value={ano}>{ano}</option>
                    ))}
                </select>
                <div className={styles.espaçadorlateral1}></div>
                <div className={styles.espaçadorlateral2}></div>
                <div className={styles.espaçador2}></div>
                <div className={styles.finalizando} onClick={vaiano}>
                    <p className={styles.bots}>Confirmar</p>
                </div>
                <div className={styles.finalizando} onClick={() => router.push("/")}>
                    <p className={styles.bots}>Voltar</p>
                </div>
            </div>
        </div>
    );
};

export default Ano;
