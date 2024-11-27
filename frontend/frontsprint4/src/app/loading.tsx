// app/loading.tsx
import styles from "./loading.module.css";

export default function Loading() {
  return (
    <div className={styles.loadingOverlay}>
      <div className={styles.spinner}></div>
      <div className={styles.smile}>≧◠‿◠≦</div>
    </div>
  );
}
