"use client";
import { useEffect, useState } from 'react';
import Link from 'next/link';
import styles from './Perfil.module.css';
import "../reset.css";
import { useRouter } from 'next/navigation';
const Perfil = () => {
    const [nomeUsuario, setNomeUsuario] = useState<string | null>(null);
    const [bio, setBio] = useState<string>("");
    const [imagemUsuario, setImagemUsuario] = useState<string | null>(null);
    const [agendamentos, setAgendamentos] = useState<any[]>([]);
    const router = useRouter();
    useEffect(() => {
        const userCredentials = localStorage.getItem("usuario");
        const userBio = localStorage.getItem("userBio");
        const savedImage = localStorage.getItem("userImage");
        if (userCredentials) {
            const { nomeUsuario, cpfUsuario } = JSON.parse(userCredentials);
            setNomeUsuario(nomeUsuario);
            fetch(`http://localhost:8080/sprint4-java/rest/agendamento/usuario/${cpfUsuario}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao buscar agendamentos');
                    }
                    return response.json();
                })
                .then(data => {
                    setAgendamentos(data); 
                })
                .catch(error => {
                    console.error("Erro ao buscar os agendamentos:", error);
                });
        }

        if (userBio) {
            setBio(userBio);
        } else {
            setBio("Bem-vindo(a) ao nosso sistema! Edite sua bio para personalizar esta seção.");
        }

        if (savedImage) {
            setImagemUsuario(savedImage);
        }
    }, []);
    const editarBio = () => {
        router.push("/GerenciarUsuario");
    }
    return (
        <div className={styles.container}>
            <img src="/Imagens/CarroPerfil.png" alt="Imagem de fundo" className={styles.imagemFundo} />
            <img src={imagemUsuario || "/Imagens/imagenpadraouser.jpg"} alt="Imagem do usuário" className={styles.imagemUsuario} />
            <img src="/Imagens/Penedit.png" alt="" onClick={editarBio} className={styles.editarBio}/>
            <p className={styles.paragrafoBio}>
                Olá, sou {nomeUsuario || "Usuário"}. {bio}
            </p>
            <div className={styles.fundoAgendamentosPerfil}>
                <h2 className={styles.agendamentos}>Agendamentos</h2>
                <Link href="/Veiculos" className={styles.botaoveiculos}>Veículos</Link>
                <Link href="#" className={styles.botaoauto}>Auto+</Link>
                {agendamentos.length > 0 ? (
                    agendamentos.map((agendamento, index) => (
                        <div key={index} className={styles.agendamentoInfo}>
                            <p className={styles.componenteTextual}><strong>Descrição:</strong> {agendamento.descricao}</p>
                            <p className={styles.componenteTextual}><strong>Data:</strong> {agendamento.data}</p>
                            <p className={styles.componenteTextual}><strong>Horário:</strong> {agendamento.hora}</p>
                            <p className={styles.componenteTextual}><strong>Local:</strong> {agendamento.centro.nomeCentro}</p>
                            <p className={styles.componenteTextual}><strong>Serviço: </strong> {agendamento.servico.tipoServico}</p>
                        </div>
                    ))
                ) : (
                    <p className={styles.componenteTextual}>Nenhum agendamento encontrado</p>
                )}

                <Link href="/"><img src="/Imagens/SetaVolta.png" alt="Seta Voltar" className={styles.setaVoltar}/></Link>
            </div>
            
        </div>
    );
}

export default Perfil;
