


// "use client";
// import { useState, useEffect } from 'react';
// import styles from './Dashboard.module.css';
// import { useRouter } from 'next/navigation';
// import HamburguerMenu from '../HamburguerMenu/page';

// const Dashboard = () => {
//     const [nome, setNome] = useState<string>("");
//     const [email, setEmail] = useState<string>("");
//     const [senha, setSenha] = useState<string>("");
//     const [bio, setBio] = useState<string>("");
//     const [imagem, setImagem] = useState<string | null>(null); // Estado para a imagem
//     const router = useRouter();

//     useEffect(() => {
//         const userCredentials = localStorage.getItem("userCredentials");
//         const userBio = localStorage.getItem("userBio");
//         const savedImage = localStorage.getItem("userImage"); // Carrega a imagem do localStorage

//         if (userCredentials) {
//             const { email, senha } = JSON.parse(userCredentials);
//             setNome(email.split("@")[0]);
//             setEmail(email);
//             setSenha(senha);
//         }

//         if (userBio) {
//             setBio(userBio);
//         }

//         if (savedImage) {
//             setImagem(savedImage);
//         }
//     }, []);

//     const handleSave = () => {
//         const updatedCredentials = {
//             email,
//             senha,
//         };
//         localStorage.setItem("userCredentials", JSON.stringify(updatedCredentials));
//         localStorage.setItem("userBio", bio);
//         if (imagem) localStorage.setItem("userImage", imagem); // Salva a imagem no localStorage
//         alert("Dados atualizados com sucesso!");
//         router.push('/Perfil');
//     };

//     const handleDelete = () => {
//         localStorage.removeItem("userCredentials");
//         localStorage.removeItem("userBio");
//         localStorage.removeItem("userImage");
//         alert("Usuário excluído com sucesso!");
//         router.push("/");
//     };

//     const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//         const file = e.target.files?.[0];
//         if (file) {
//             const reader = new FileReader();
//             reader.onloadend = () => {
//                 setImagem(reader.result as string); // Salva a imagem como base64
//             };
//             reader.readAsDataURL(file);
//         }
//     };

//     return (
//         <>
//         <HamburguerMenu></HamburguerMenu>
//         <div className={styles.containermaior}>
//             <div className={styles.container}>
//                 <h1 className={styles.title}>Gerenciar Usuário</h1>
//                 <div className={styles.formGroup}>
//                     <label className={styles.label}>Nome: (editável mudando email)</label>
//                     <input type="text" value={nome} onChange={(e) => setNome(e.target.value)} disabled className={styles.input} />
//                 </div>
//                 <div className={styles.formGroup}>
//                     <label className={styles.label}>Email:</label>
//                     <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className={styles.input} />
//                 </div>
//                 <div className={styles.formGroup}>
//                     <label className={styles.label}>Senha:</label>
//                     <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} className={styles.input} />
//                 </div>
//                 <div className={styles.formGroup}>
//                     <label className={styles.label}>Bio:</label>
//                     <textarea
//                         value={bio}
//                         onChange={(e) => setBio(e.target.value)}
//                         className={styles.textarea}
//                         maxLength={100}
//                     />
//                 </div>
//                 <div className={styles.formGroup}>
//                     <label className={styles.label}>Imagem do Usuário:</label>
//                     <input type="file" accept="image/*" onChange={handleImageChange} className={styles.input} />
//                     {imagem && <img src={imagem} alt="Pré-visualização da imagem" className={styles.previewImage} />}
//                 </div>
//                 <button onClick={handleSave} className={styles.botaoSalvar}>Salvar</button>
//                 <button onClick={handleDelete} className={styles.botaoExcluir}>Excluir Usuário</button>
//             </div>
//         </div>
//         </>
//     );
// };

// export default Dashboard;


// "use client";
// import { useState, useEffect } from 'react';
// import styles from './Dashboard.module.css';
// import { useRouter } from 'next/navigation';
// import HamburguerMenu from '../HamburguerMenu/page';

// const Dashboard = () => {
//     const [nome, setNome] = useState<string>("");
//     const [email, setEmail] = useState<string>("");
//     const [senha, setSenha] = useState<string>("");
//     const [bio, setBio] = useState<string>("");
//     const [imagem, setImagem] = useState<string | null>(null);
//     const [veiculos, setVeiculos] = useState<any[]>([]); // Estado para os veículos
//     const router = useRouter();
//     const cpfUsuario = "11122233344"; // Exemplo de CPF, deve ser obtido da sessão

//     useEffect(() => {
//         // Verifica se o usuário está logado
//         const isLoggedIn = localStorage.getItem("usuario");
//         if (!isLoggedIn) {
//             router.push("/login"); // Redireciona para a página de login se não estiver logado
//             return;
//         }

//         const userCredentials = JSON.parse(isLoggedIn);
//         setNome(userCredentials.nomeUsuario);
//         setEmail(userCredentials.email);
//         setSenha(userCredentials.senha);
//         setBio(localStorage.getItem("userBio") || "");
//         setImagem(localStorage.getItem("userImage") || null);

//         // Obtém os veículos do usuário
//         fetch(`http://localhost:8080/sprint4-java/rest/veiculo/usuario/${cpfUsuario}`)
//             .then(response => response.json())
//             .then(data => setVeiculos(data))
//             .catch(error => console.error("Erro ao buscar veículos:", error));
//     }, [router]);

//     const handleSave = () => {
//         const updatedCredentials = {
//             email,
//             senha,
//             nome: nome, // Incluindo o nome
//             bio,
//             imagem,
//         };

//         fetch(`http://localhost:8080/sprint4-java/rest/usuario/${cpfUsuario}`, {
//             method: 'PUT',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(updatedCredentials),
//         })
//             .then(response => {
//                 if (response.ok) {
//                     localStorage.setItem("userBio", bio);
//                     if (imagem) localStorage.setItem("userImage", imagem);
//                     alert("Dados atualizados com sucesso!");
//                     router.push('/Perfil');
//                 } else {
//                     alert("Erro ao atualizar dados.");
//                 }
//             })
//             .catch(error => console.error("Erro ao atualizar dados:", error));
//     };

//     const handleDelete = () => {
//         // Lógica para excluir o usuário
//         fetch(`http://localhost:8080/sprint4-java/rest/usuario/${cpfUsuario}`, {
//             method: 'DELETE',
//         })
//             .then(response => {
//                 if (response.ok) {
//                     localStorage.removeItem("userCredentials");
//                     localStorage.removeItem("userBio");
//                     localStorage.removeItem("userImage");
//                     alert("Usuário excluído com sucesso!");
//                     router.push("/");
//                 } else {
//                     alert("Erro ao excluir usuário.");
//                 }
//             })
//             .catch(error => console.error("Erro ao excluir usuário:", error));
//     };

//     const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//         const file = e.target.files?.[0];
//         if (file) {
//             const reader = new FileReader();
//             reader.onloadend = () => {
//                 setImagem(reader.result as string);
//             };
//             reader.readAsDataURL(file);
//         }
//     };

//     return (
//         <>
//             <HamburguerMenu />
//             <div className={styles.containermaior}>
//                 <div className={styles.container}>
//                     <h1 className={styles.title}>Gerenciar Usuário</h1>
//                     <div className={styles.formGroup}>
//                         <label className={styles.label}>Nome: (editável mudando email)</label>
//                         <input type="text" value={nome} onChange={(e) => setNome(e.target.value)} disabled className={styles.input} />
//                     </div>
//                     <div className={styles.formGroup}>
//                         <label className={styles.label}>Email:</label>
//                         <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className={styles.input} />
//                     </div>
//                     <div className={styles.formGroup}>
//                         <label className={styles.label}>Senha:</label>
//                         <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} className={styles.input} />
//                     </div>
//                     <div className={styles.formGroup}>
//                         <label className={styles.label}>Bio:</label>
//                         <textarea
//                             value={bio}
//                             onChange={(e) => setBio(e.target.value)}
//                             className={styles.textarea}
//                             maxLength={100}
//                         />
//                     </div>
//                     <div className={styles.formGroup}>
//                         <label className={styles.label}>Imagem do Usuário:</label>
//                         <input type="file" accept="image/*" onChange={handleImageChange} className={styles.input} />
//                         {imagem && <img src={imagem} alt="Pré-visualização da imagem" className={styles.previewImage} />}
//                     </div>
//                     <button onClick={handleSave} className={styles.botaoSalvar}>Salvar</button>
//                     <button onClick={handleDelete} className={styles.botaoExcluir}>Excluir Usuário</button>

//                     <div className={styles.veiculosContainer}>
//                         <h2 className={styles.subTitle}>Veículos do Usuário</h2>
//                         <ul>
//                             {veiculos.map((veiculo) => (
//                                 <li key={veiculo.placa}>
//                                     {veiculo.marca} {veiculo.modelo} - Placa: {veiculo.placa} - Ano: {veiculo.ano} - Quilometragem: {veiculo.quilometragem}
//                                 </li>
//                             ))}
//                         </ul>
//                     </div>
//                 </div>
//             </div>
//         </>
//     );
// };

// export default Dashboard;

"use client";
import { useState, useEffect } from 'react';
import styles from './Dashboard.module.css';
import { useRouter } from 'next/navigation';
import HamburguerMenu from '../HamburguerMenu/page';

const Dashboard = () => {
    const [cpfUsuario, setCpfUsuario] = useState<string>("");
    const [nomeUsuario, setNomeUsuario] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [senha, setSenha] = useState<string>("");
    const [telefone, setTelefone] = useState<string>(""); 
    const [bio, setBio] = useState<string>("");
    const [imagem, setImagem] = useState<string | null>(null);
    const [veiculos, setVeiculos] = useState<any[]>([]);
    const router = useRouter();

    useEffect(() => {
        const isLoggedIn = localStorage.getItem("usuario");
        if (!isLoggedIn) {
            router.push("/login");
            return;
        }

        const userCredentials = JSON.parse(isLoggedIn);
        setCpfUsuario(userCredentials.cpfUsuario);
        setNomeUsuario(userCredentials.nomeUsuario);
        setEmail(userCredentials.email);
        setSenha(userCredentials.senha);
        setTelefone(userCredentials.telefone); 
        setBio(localStorage.getItem("userBio") || "");
        setImagem(localStorage.getItem("userImage") || null);
    }, [router]);

    // Novo useEffect para buscar os veículos apenas quando cpfUsuario é atualizado
    useEffect(() => {
        if (cpfUsuario) {
            fetch(`http://localhost:8080/sprint4-java/rest/veiculo/usuario/${cpfUsuario}`)
                .then(response => response.json())
                .then(data => setVeiculos(data))
                .catch(error => console.error("Erro ao buscar veículos:", error));
        }
    }, [cpfUsuario]);

    const handleSave = () => {
        const updatedCredentials = {
            cpfUsuario,
            nomeUsuario,
            email,
            senha,
            telefone,
        };
    
        fetch(`http://localhost:8080/sprint4-java/rest/usuario/${cpfUsuario}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedCredentials),
        })
            .then(response => {
                if (response.ok) {
                    localStorage.setItem("usuario", JSON.stringify({
                        cpfUsuario: cpfUsuario, 
                        nomeUsuario: nomeUsuario,
                        senha,
                        email,
                        telefone, 
                    }));
                    localStorage.setItem("userBio", bio);
                    if (imagem) localStorage.setItem("userImage", imagem);
                    alert("Dados atualizados com sucesso!");
                    router.push('/Perfil');
                } else {
                    alert("Erro ao atualizar dados.");
                }
            })
            .catch(error => console.error("Erro ao atualizar dados:", error));
    };

    const handleDelete = () => {
        fetch(`http://localhost:8080/sprint4-java/rest/usuario/${cpfUsuario}`, {
            method: 'DELETE',
        })
            .then(response => {
                if (response.ok) {
                    localStorage.removeItem("usuario");
                    localStorage.removeItem("userBio");
                    localStorage.removeItem("userImage");
                    alert("Usuário excluído com sucesso!");
                    router.push("/");
                } else {
                    alert("Erro ao excluir usuário.");
                }
            })
            .catch(error => console.error("Erro ao excluir usuário:", error));
    };

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagem(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <>
            <HamburguerMenu />
            <div className={styles.containermaior}>
                <div className={styles.container}>
                    <h1 className={styles.title}>Gerenciar Usuário</h1>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Nome: (editável mudando email)</label>
                        <input type="text" value={nomeUsuario} onChange={(e) => setNomeUsuario(e.target.value)} disabled className={styles.input} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Email:</label>
                        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className={styles.input} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Senha:</label>
                        <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} className={styles.input} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Telefone:</label>
                        <input type="text" value={telefone} onChange={(e) => setTelefone(e.target.value)} className={styles.input} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Bio:</label>
                        <textarea
                            value={bio}
                            onChange={(e) => setBio(e.target.value)}
                            className={styles.textarea}
                            maxLength={100}
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Imagem do Usuário:</label>
                        <input type="file" accept="image/*" onChange={handleImageChange} className={styles.input} />
                        {imagem && <img src={imagem} alt="Pré-visualização da imagem" className={styles.previewImage} />}
                    </div>
                    <button onClick={handleSave} className={styles.botaoSalvar}>Salvar</button>
                    <button onClick={handleDelete} className={styles.botaoExcluir}>Excluir Usuário</button>

                    <div className={styles.veiculosContainer}>
                        <h2 className={styles.subTitle}>Veículos do Usuário</h2>
                        <ul>
                            {veiculos.map((veiculo) => (
                                <li key={veiculo.placa}>
                                    {veiculo.marca} {veiculo.modelo} - Placa: {veiculo.placa} - Ano: {veiculo.ano} - Quilometragem: {veiculo.quilometragem}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Dashboard;