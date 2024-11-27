"use client";
import Link from "next/link";
import HamburguerMenu from "../HamburguerMenu/page";
import styles from "./Marca.module.css";
import { useState } from "react";
import { useRouter } from "next/navigation";
const Marca = () => {
    const [selectedOption, setSelectedOption] = useState(null);
    const router = useRouter();
    const handleOptionClick = (option) => {
        setSelectedOption(option);
    };
    const vaimodelo = () => {
        if (selectedOption) {
            localStorage.setItem("selectedMarca", selectedOption);
            router.push("/Modelo");
        } else {
            alert("Por favor, selecione uma marca.");
        }
    };
    const voltabase = () => {
        router.push("/");
    };
    return (
        <div className={styles.container}>
            <HamburguerMenu />
            <h1>Marca</h1>
            <br />
            <div className={styles.paidedivs}>
                <div className={styles.botao1}></div>
                <div className={styles.botao2}></div>
                <div className={styles.botao2}></div>
            </div>
            <div className={styles.espaçador1}></div>
            <div className={styles.paidasdivs2}>
                {["Chevrolet", "Honda", "Volkswagen", "Outro"].map((marca, index) => (
                    <div
                        key={index}
                        className={`${styles.opsimples} ${selectedOption === marca ? styles.selected : ""}`}
                        onClick={() => handleOptionClick(marca)}
                    >
                        {marca}
                    </div>
                ))}
                <div className={styles.espaçadorlateral1}></div>
                <div className={styles.espaçadorlateral2}></div>
                <div className={styles.espaçador2}></div>
                <div className={styles.finalizando} onClick={vaimodelo}>
                    <p className={styles.bots}>Confirmar</p>
                </div>
                <div className={styles.finalizando} onClick={voltabase}>
                    <p className={styles.bots}>Voltar</p>
                </div>
            </div>
        </div>
    );
};

export default Marca;
