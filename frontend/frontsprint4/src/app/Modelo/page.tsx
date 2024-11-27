"use client";
import Link from "next/link";
import HamburguerMenu from "../HamburguerMenu/page";
import styles from "../Marca/Marca.module.css";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
const Modelo = () => {
    const [selectedOption, setSelectedOption] = useState<string | null>(null); 
    const [selectedModel, setSelectedModel] = useState<string | null>(null); 
    const router = useRouter();
    useEffect(() => {
        const marca = localStorage.getItem("selectedMarca");
        if (marca) {
            setSelectedOption(marca);
        } else {
            alert("Nenhuma marca selecionada. Por favor, volte para a página anterior.");
            router.push("/")
        }
    }, [router]);
    const modelosPorMarca: { [key: string]: string[] } = {
        Chevrolet: ["Onix", "Camaro", "Tracker", "Outros"],
        Honda: ["Civic", "HR-V", "Fit", "Outros"],
        Volkswagen: ["Gol", "Jetta", "T-Cross", "Outros"],
        Outro: ["Outros"]
    };

    const vaimodelo = () => {
        if (selectedModel) {
            localStorage.setItem("selectedModelo", selectedModel);
            router.push("/Ano");
        } else {
            alert("Por favor, selecione um modelo.");
        }
    };
    return (
        <div className={styles.container}>
            <HamburguerMenu />
            <h1>Modelos de {selectedOption}</h1>
            <br />
            <div className={styles.paidedivs}>
                <div className={styles.botao1}></div>
                <div className={styles.botao2}></div>
                <div className={styles.botao2}></div>
            </div>
            <div className={styles.espaçador1}></div>
            <div className={styles.paidasdivs2}>
                {selectedOption && modelosPorMarca[selectedOption]?.map((modelo: string, index: number) => (
                    <div
                        key={index}
                        className={`${styles.opsimples} ${selectedModel === modelo ? styles.selected : ""}`} 
                        onClick={() => setSelectedModel(modelo)} 
                    >
                        {modelo}
                    </div>
                ))}
                <div className={styles.espaçadorlateral1}></div>
                <div className={styles.espaçadorlateral2}></div>
                <div className={styles.espaçador2}></div>

                <div className={styles.finalizando} onClick={vaimodelo}>
                    <p className={styles.bots}>Confirmar</p>
                </div>

                <div className={styles.finalizando} onClick={() => router.push("/")}>
                    <p className={styles.bots}>Voltar</p>
                </div>
            </div>
        </div>
    );
};

export default Modelo;
