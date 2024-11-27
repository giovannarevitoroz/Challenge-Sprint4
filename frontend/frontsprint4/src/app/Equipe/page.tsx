import React from 'react';
import styles from './Equipe.module.css';
import HamburguerMenu from '../HamburguerMenu/page';
import Link from 'next/link';
import '../reset.css';
const Equipe = () => {
  return (
    <>
      <div className={styles.menuContainer}>
        <HamburguerMenu />
      </div>
      <div className={styles.voltando}>
        <Link href={"/"} className={styles.voltarbotao}>Voltar</Link>
      </div>
      <h1 className={styles.titulo}>Equipe</h1>
      <img className={styles.imagem} src="./Imagens/Revito.png" alt="Giovanna Revito" />
      <h2 className={styles.tituloDireita}>Giovanna Revito</h2>
      <p className={styles.paragrafoRmDireita}>Rm 558981</p>
      <p className={styles.paragrafoDireito}>Uma jovem desenvolvedora que realiza seu trabalho com excelência</p>
      <h2 className={styles.tituloEsquerda}>Kaian Gustavo</h2>
      <p className={styles.paragrafoRmEsquerdo}>Rm 558986</p>
      <p className={styles.paragrafoEsquerdo}>Um jovem desenvolvedor que realiza seu trabalho com excelência</p>
      <img className={styles.imagem2} src="./Imagens/Kaian.png" alt="Kaian Gustavo" />
      <img className={styles.imagem} src="./Imagens/Kenji.png" alt="Lucas Kenji" />
      <h2 className={`${styles.titulo} ${styles.tituloDireita}`}>Lucas Kenji</h2>
      <p className={styles.paragrafoRmDireita}>Rm 554424</p>
      <p className={styles.paragrafoDireito}>Um jovem desenvolvedor que realiza seu trabalho com excelência</p>
    </>
  );
};
export default Equipe;


