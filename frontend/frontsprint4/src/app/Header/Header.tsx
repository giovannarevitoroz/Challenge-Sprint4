
"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import styles from "./header.module.css";
import "../reset.css";
const Header = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");
  useEffect(() => {
    const userCredentials = JSON.parse(localStorage.getItem("usuario"));
    if (userCredentials && userCredentials.email) {
      setIsLoggedIn(true);
      setUserName(userCredentials.email.split("@")[0]);
    }
  }, []);
  const handleLogout = () => {
    localStorage.removeItem("usuario");
    localStorage.removeItem("userBio");
    setIsLoggedIn(false);
    alert("Usuário desconectado");
    window.location.reload()
  };
  return (
    <header className={styles.header}>
      {isLoggedIn ? (
        <>
          <h1 className={styles.titulo}>Bem-vindo, {userName}!</h1>
          <img 
            src="/imagens/PortaSair.png"
            alt="Sair"
            onClick={handleLogout}
            className={styles.logoutImage}
          />
        </>
      ) : (
        <div className={styles.authLinks}>
          <Link href="/Cadastro" className={styles.cadastrar}>Cadastre-se </Link>
          <Link href="/Login" className={styles.cadastrar}>/ Login</Link>
        </div>
      )}
    </header>
  );
};
export default Header;
