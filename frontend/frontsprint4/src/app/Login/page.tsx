"use client";
import React, { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useRouter } from 'next/navigation';
import styles from './login.module.css';
import Link from 'next/link';
import HamburguerMenu from '../HamburguerMenu/page';
import '../reset.css';
interface LoginData {
    nomeUsuario: string;
    senha: string;
}
const schema = yup.object().shape({
    nomeUsuario: yup.string().required('Nome é obrigatório'), 
    senha: yup.string().min(6, 'A senha deve ter pelo menos 6 caracteres').required('Senha é obrigatória'),
});
const Login: React.FC = () => {
    const { control, handleSubmit, formState: { errors } } = useForm<LoginData>({
        resolver: yupResolver(schema),
    });
    const [errorMessage, setErrorMessage] = useState('');
    const router = useRouter();
    const onSubmit = async (data: LoginData) => {
        try {
            const response = await fetch('http://localhost:8080/sprint4-java/rest/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                const result = await response.json();
                const usuarioData = {
                    cpfUsuario: result.cpfUsuario,
                    nomeUsuario: result.nomeUsuario,
                    email: result.email,
                    senha: data.senha,
                    telefone: result.telefone,
                };
                localStorage.setItem('usuario', JSON.stringify(usuarioData));

                alert('Login realizado com sucesso!');
                router.push('/');
            } else {
                const errorData = await response.json();
                setErrorMessage(errorData.message || 'Erro no login. Verifique suas credenciais.');
            }
        } catch (error) {
            setErrorMessage('Erro ao tentar conectar à API.');
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
            <HamburguerMenu />
            <div className={styles.container}>
                <h1 className={styles.titulo}>Login</h1>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className={styles.formulario}>
                        <Controller
                            name="nomeUsuario" 
                            control={control}
                            defaultValue=""
                            render={({ field }) => (
                                <input
                                    {...field}
                                    placeholder={errors.nomeUsuario ? errors.nomeUsuario.message : 'Nome'} 
                                    className={errors.nomeUsuario ? styles.inputError : ''}
                                />
                            )}
                        />
                    </div>
                    <div className={styles.formulario}>
                        <Controller
                            name="senha"
                            control={control}
                            defaultValue=""
                            render={({ field }) => (
                                <input
                                    type="password"
                                    {...field}
                                    placeholder={errors.senha ? errors.senha.message : 'Senha'}
                                    className={errors.senha ? styles.inputError : ''}
                                />
                            )}
                        />
                    </div>
                    <div className={styles.divisao}></div>

                    <button className={styles.botao} type="submit">Entrar</button>
                    {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}

                    <div className={styles.desistirbotao}>
                        <Link className={styles.voltabotao} href={"/"}>Voltar</Link>
                    </div>
                </form>
                <div className={styles.qualquer}></div>
            </div>
        </>
    );
};
export default Login;
