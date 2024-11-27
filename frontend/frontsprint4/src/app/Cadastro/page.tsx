"use client";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as Yup from "yup";
import { useRouter } from "next/navigation";
import styles from './cadastro.module.css';
import HamburguerMenu from '../HamburguerMenu/page';
import Link from 'next/link';
import { useEffect } from "react";
import '../reset.css';

const validationSchema = Yup.object().shape({
    cpfUsuario: Yup.string()
        .matches(/^\d{11}$/, "CPF deve conter 11 dígitos.")
        .required("CPF é obrigatório."),
    nomeUsuario: Yup.string()
        .min(3, "Nome deve ter ao menos 3 caracteres.")
        .required("Nome é obrigatório."),
    senha: Yup.string()
        .min(6, "Senha deve ter ao menos 6 caracteres.")
        .required("Senha é obrigatória."),
    email: Yup.string()
        .email("Email inválido.")
        .required("Email é obrigatório."),
    telefone: Yup.string()
        .matches(/^\d{11}$/, "Telefone deve conter 11 dígitos (ex: 11987654321).")
        .required("Telefone é obrigatório."),
});
const Cadastro = () => {
    const router = useRouter();
    const { register, handleSubmit, formState: { errors } } = useForm({
        resolver: yupResolver(validationSchema),
    });
    const onSubmit = async (data : any) => {
        try {
            const response = await fetch("http://localhost:8080/sprint4-java/rest/usuario", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorMessage = await response.text();
                console.error("Erro da API:", errorMessage);
                throw new Error(`Erro: ${errorMessage}`);
            }
            alert('Cadastro realizado com sucesso!'); 
            router.push("/Login");
        } catch (error) {
            console.error("Erro ao salvar o usuário: ", error);
        }
    };
    useEffect(() => {
        const usuario = localStorage.getItem('usuario');
        if (usuario) {
            router.push('/'); 
        }
    }, [router]);
    return (
        <>
        <div className={styles.container}>
            <HamburguerMenu />
            <h1 className={styles.titulo}>Cadastre-se</h1>
            <form onSubmit={handleSubmit(onSubmit)}>
                <div className={styles.formulario}>
                    <input
                        type="text"
                        id="cpfUsuario"
                        {...register("cpfUsuario")}
                        placeholder={errors.cpfUsuario ? errors.cpfUsuario.message : 'CPF'}
                        className={errors.cpfUsuario ? styles.inputError : ''}
                    />
                </div>
                <div className={styles.formulario}>
                    <input
                        type="text"
                        id="nomeUsuario"
                        {...register("nomeUsuario")}
                        placeholder={errors.nomeUsuario ? errors.nomeUsuario.message : 'Nome'}
                        className={errors.nomeUsuario ? styles.inputError : ''}
                    />
                </div>
                <div className={styles.formulario}>
                    <input
                        type="password"
                        id="senha"
                        {...register("senha")}
                        placeholder={errors.senha ? errors.senha.message : 'Senha'}
                        className={errors.senha ? styles.inputError : ''}
                    />
                </div>
                <div className={styles.formulario}>
                    <input
                        type="email"
                        id="email"
                        {...register("email")}
                        placeholder={errors.email ? errors.email.message : 'Email'}
                        className={errors.email ? styles.inputError : ''}
                    />
                </div>
                <div className={styles.formulario}>
                    <input
                        type="text"
                        id="telefone"
                        {...register("telefone")}
                        placeholder={errors.telefone ? errors.telefone.message : 'Telefone'}
                        className={errors.telefone ? styles.inputError : ''}
                    />
                </div>
                <div className={styles.divisor}></div>
                <button className={styles.botao} type="submit">Cadastrar</button>
                <div className={styles.desistirbotao}>
                    <Link className={styles.voltabotao} href={"/"}>Voltar</Link>
                </div>
            </form>
            <div className={styles.espacadorfinal}></div>
        </div>
        </>
    );
};
export default Cadastro;
