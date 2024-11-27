
// "use client";
// import { useState, useEffect, useRef } from "react";
// import Link from "next/link";
// import styles from "./HamburguerMenu.module.css";

// const HamburguerMenu = () => {
//   const [menuAberto, setMenuAberto] = useState(false);
//   const [cliente, setCliente] = useState<string | null>(null);
//   const menuRef = useRef<HTMLDivElement>(null);

//   useEffect(() => {
//     // Recupera os dados do usuário do local storage
//     const userCredentials = localStorage.getItem("usuario");
//     if (userCredentials) {
//       const { email } = JSON.parse(userCredentials); // Extraímos o email do objeto
//       setCliente(email.split("@")[0]); // Pegamos o nome antes do "@" do email
//     }
//   }, []);

//   const MudaMenu = () => setMenuAberto((prevState) => !prevState);

//   const sairPagina = () => {
//     // Limpa o local storage ao sair e redireciona para a página inicial
//     localStorage.removeItem("userCredentials");
//     setCliente(null); // Atualiza o estado do cliente
//     window.location.href = "/";
//   };

//   useEffect(() => {
//     const fecharMenuFora = (event: MouseEvent) => {
//       if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
//         setMenuAberto(false);
//       }
//     };
//     document.addEventListener("mousedown", fecharMenuFora);
//     return () => {
//       document.removeEventListener("mousedown", fecharMenuFora);
//     };
//   }, []);

//   return (
//     <>
//       <div className={styles.Hamburgao}>
//         <div
//           className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
//           onClick={MudaMenu}
//         ></div>
//         <div
//           className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
//           onClick={MudaMenu}
//         ></div>
//         <div
//           className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
//           onClick={MudaMenu}
//         ></div>
//         <div
//           ref={menuRef}
//           className={`${styles.hanburguerMenu} ${
//             menuAberto ? styles.menuAberto : styles.menuFechado
//           }`}
//         >
//           <h2 className={styles.formH2}>
//             Olá,<br></br> {cliente || "Usuário"}
//           </h2>
//           <nav>
//             <ul className={styles.listaUL}>
//               <li className={styles.listaLI}>
//                 <Link href="/" className={styles.linkdomenu}>Início</Link>
//               </li>
//               <li className={styles.listaLI}>
//                 <Link href="/Marca" className={styles.linkdomenu}>Diagnósticos</Link>
//               </li>
//               {/* Exibe a opção "Perfil" apenas se o cliente estiver logado */}
//               {cliente && (
//                 <li className={styles.listaLI}>
//                   <Link href="/Perfil" className={styles.linkdomenu}>Perfil</Link>
//                 </li>
//               )}
//               <li className={styles.listaLI}>
//                 <Link href="/Equipe" className={styles.linkdomenu}>Equipe</Link>
//               </li>
//               {/* O botão de sair só aparece se o cliente estiver logado */}
//               {cliente && (
//                 <li className={styles.listaLI}>
//                   <button onClick={sairPagina} className={styles.linkdomenu}>
//                     Sair
//                   </button>
//                 </li>
//               )}
//             </ul>
//           </nav>
//         </div>
//       </div>
//     </>
//   );
// };

// export default HamburguerMenu;

//codigo antigo


"use client";
import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import styles from "./HamburguerMenu.module.css";

const HamburguerMenu = () => {
  const [menuAberto, setMenuAberto] = useState(false);
  const [cliente, setCliente] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Recupera os dados do usuário do local storage
    const userCredentials = localStorage.getItem("usuario");
    if (userCredentials) {
      const { email } = JSON.parse(userCredentials); // Extraímos o email do objeto
      setCliente(email.split("@")[0]); // Pegamos o nome antes do "@" do email
    }
  }, []);

  const MudaMenu = () => setMenuAberto((prevState) => !prevState);

  const sairPagina = () => {
    // Limpa o local storage ao sair e redireciona para a página inicial
    localStorage.removeItem("usuario");
    localStorage.removeItem("userBio");
    setCliente(null); // Atualiza o estado do cliente
    window.location.href = "/";
  };

  useEffect(() => {
    const fecharMenuFora = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuAberto(false);
      }
    };
    document.addEventListener("mousedown", fecharMenuFora);
    return () => {
      document.removeEventListener("mousedown", fecharMenuFora);
    };
  }, []);

  const redirecionarDiagnosticos = () => {
    if (cliente) {
      window.location.href = "/Diagnosticando"; 
    } else {
      window.location.href = "/Marca"; 
    }
  };


  return (
    <>
      <div className={styles.Hamburgao}>
        <div
          className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
          onClick={MudaMenu}
        ></div>
        <div
          className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
          onClick={MudaMenu}
        ></div>
        <div
          className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
          onClick={MudaMenu}
        ></div>
        <div
          ref={menuRef}
          className={`${styles.hanburguerMenu} ${
            menuAberto ? styles.menuAberto : styles.menuFechado
          }`}
        >
          <h2 className={styles.formH2}>
            Olá,<br></br> {cliente || "Usuário"}
          </h2>
          <nav>
            <ul className={styles.listaUL}>
              <li className={styles.listaLI}>
                <Link href="/" className={styles.linkdomenu}>Início</Link>
              </li>
              <li className={styles.listaLI}>
              <button onClick={redirecionarDiagnosticos} className={`${styles.linkdomenu} ${styles.botaoSair}`}>
                  Diagnósticos
                </button>
              </li>
              {/* Exibe a opção "Perfil" apenas se o cliente estiver logado */}
              {cliente && (
                <li className={styles.listaLI}>
                  <Link href="/Perfil" className={styles.linkdomenu}>Perfil</Link>
                </li>
              )}
              <li className={styles.listaLI}>
                <Link href="/Equipe" className={styles.linkdomenu}>Equipe</Link>
              </li>
              {/* Exibe as novas opções apenas se o cliente estiver logado */}
              {cliente && (
                <>
                  <li className={styles.listaLI}>
                    <Link href="/CadastrarVeiculo" className={styles.linkdomenu}>Cadastrar um Veículo</Link>
                  </li>
                  <li className={styles.listaLI}>
                    <Link href="/Agendamentos" className={styles.linkdomenu}>Fazer um Agendamento</Link>
                  </li>
                </>
              )}
              {/* O botão de sair só aparece se o cliente estiver logado */}
              {cliente && (
                <li className={styles.listaLI}>
                  <button onClick={sairPagina} className={`${styles.linkdomenu} ${styles.botaoSair}`}>
                    Sair
                  </button>
                </li>
              )}
            </ul>
          </nav>
        </div>
      </div>
    </>
  );
};

export default HamburguerMenu;

//codigo q aparece as novas opcoes se logado

//codigo q nao precisa de login/ fiz por nao conseguir a api
// "use client";
// import { useState, useEffect, useRef } from "react";
// import Link from "next/link";
// import styles from "./HamburguerMenu.module.css";

// const HamburguerMenu = () => {
//   const [menuAberto, setMenuAberto] = useState(false);
//   const [cliente, setCliente] = useState<string | null>(null);
//   const menuRef = useRef<HTMLDivElement>(null);

//   useEffect(() => {
//     // Recupera os dados do usuário do local storage
//     const userCredentials = localStorage.getItem("usuario");
//     if (userCredentials) {
//       const { email } = JSON.parse(userCredentials); // Extraímos o email do objeto
//       setCliente(email.split("@")[0]); // Pegamos o nome antes do "@" do email
//     }
//   }, []);

//   const MudaMenu = () => setMenuAberto((prevState) => !prevState);

//   const sairPagina = () => {
//     // Limpa o local storage ao sair e redireciona para a página inicial
//     localStorage.removeItem("userCredentials");
//     setCliente(null); // Atualiza o estado do cliente
//     window.location.href = "/";
//   };

//   useEffect(() => {
//     const fecharMenuFora = (event: MouseEvent) => {
//       if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
//         setMenuAberto(false);
//       }
//     };
//     document.addEventListener("mousedown", fecharMenuFora);
//     return () => {
//       document.removeEventListener("mousedown", fecharMenuFora);
//     };
//   }, []);

//   return (
//     <>
//       <div className={styles.Hamburgao}>
//         <div
//           className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
//           onClick={MudaMenu}
//         ></div>
//         <div
//           className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
//           onClick={MudaMenu}
//         ></div>
//         <div
//           className={`${styles.hanburguerBotao} ${styles.hanburguerBotaoSmall}`}
//           onClick={MudaMenu}
//         ></div>
//         <div
//           ref={menuRef}
//           className={`${styles.hanburguerMenu} ${
//             menuAberto ? styles.menuAberto : styles.menuFechado
//           }`}
//         >
//           <h2 className={styles.formH2}>
//             Olá,<br></br> {cliente || "Usuário"}
//           </h2>
//           <nav>
//             <ul className={styles.listaUL}>
//               <li className={styles.listaLI}>
//                 <Link href="/" className={styles.linkdomenu}>Início</Link>
//               </li>
//               <li className={styles.listaLI}>
//                 <Link href="/Marca" className={styles.linkdomenu}>Diagnósticos</Link>
//               </li>
//               {/* Exibe a opção "Perfil" apenas se o cliente estiver logado */}
//               {cliente && (
//                 <li className={styles.listaLI}>
//                   <Link href="/Perfil" className={styles.linkdomenu}>Perfil</Link>
//                 </li>
//               )}
//               <li className={styles.listaLI}>
//                 <Link href="/Equipe" className={styles.linkdomenu}>Equipe</Link>
//               </li>
//               {/* Exibe as novas opções para todos, independente de estarem logados */}
//               <li className={styles.listaLI}>
//                 <Link href="/CadastrarVeiculo" className={styles.linkdomenu}>Cadastrar um Veículo</Link>
//               </li>
//               <li className={styles.listaLI}>
//                 <Link href="/Agendamento" className={styles.linkdomenu}>Fazer um Agendamento</Link>
//               </li>
//               {/* O botão de sair só aparece se o cliente estiver logado */}
//               {cliente && (
//                 <li className={styles.listaLI}>
//                   <button onClick={sairPagina} className={styles.linkdomenu}>
//                     Sair
//                   </button>
//                 </li>
//               )}
//             </ul>
//           </nav>
//         </div>
//       </div>
//     </>
//   );
// };

// export default HamburguerMenu;
