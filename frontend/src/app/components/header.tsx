import style from "@app/header.module.css";
import Image from "next/image";

export default async function Header() {
  return (
    <>
      <div className={style.container}>
        <Image
          className={style.image}
          priority
          src="/gps.trasys_logo.webp"
          alt="logo"
          width={75}
          height={5}
        />
        <p className={style.p}>GPS 조회 시스템</p>
      </div>
    </>
  );
}
