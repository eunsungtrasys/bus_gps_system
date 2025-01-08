import style from "@main/layout.module.css";
import Header from "@app/header";
import Sidebar from "@/app/components/sidebar";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className={style.container}>
      <div>
        <Header />
      </div>
      <div className={style.wrapper}>
        <Sidebar />
        <div className={style.content}>{children}</div>
      </div>
    </div>
  );
}
