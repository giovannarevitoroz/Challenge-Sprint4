// import Link from 'next/link'; 

// export default function NotFound() {
//     return (
//         <div>
//             <h1>404</h1>
//             <p>Oops! Uma pena não ser isso que você procura :( </p>
//             <Link href="/">
//                 <button> Voltar para a página inicial</button>
//             </Link>
//         </div>
//     );
// }

// app/not-found.tsx
import Link from 'next/link';
import styles from './not-found.module.css';

export default function NotFound() {
    return (
        <div className={styles.notFoundContainer}>
            <h1 className={styles.errorCode}>404</h1>
            <p className={styles.message}>Oops! Uma pena não ser isso que você procura :(</p>
            <Link href="/">
                <button className={styles.homeButton}>Voltar para a página inicial</button>
            </Link>
        </div>
    );
}
