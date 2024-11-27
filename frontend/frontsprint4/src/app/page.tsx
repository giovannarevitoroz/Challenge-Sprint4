import Link from "next/link";
// import styles from "./app/home_estilo/Home.module.css";
import styles from "../app/home_estilo/Home.module.css";
import Header from "./Header/Header";
import HamburgerMenu from "./HamburguerMenu/page";
import Head from "./Head";


export default function Home() {
  return (
   <>
    <Head></Head>
      <Header></Header>
      <HamburgerMenu></HamburgerMenu>

      <div className={styles.containerpropaganda}>    
        <img src="/imagens/mulherprops.jpg" alt="Mulher" className={styles.imagempropaganda}/>
      </div>
      <div className={styles.container2}>
         <h2>Seu carro novo onde <br></br>quer que esteja</h2>
         <img src="/imagens/CarroNovo.png" alt="Propaganda"></img>
         <Link href={'/Cadastro'} className={styles.conferir}>Confira</Link>
      </div>
      <div className={styles.containerazul}>
        <p>Venha conhecer umas das nossas 22 unidades</p>
        <Link href={'/Cadastro'} className={styles.ir}>IR</Link>
      </div>
      
      <div className={styles.containerazul2}>
        <p>Já pensou em ter diversos serviços para seu veiculo na palma de suas maos?</p>
        <img src="/imagens/DonoMoco.png" alt="" />
      </div>
   </>
  );
}


