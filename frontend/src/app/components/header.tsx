import style from "@app/header.module.css";

export default function Header() {
  return (
    <>
      <div className={style.container}>
        <p className={style.p}>GPS 조회 시스템</p>
      </div>
    </>
  );
}
