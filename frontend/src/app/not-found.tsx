"use client";

import React from "react";
import style from "./not-found.module.css";
import { useRouter } from "next/navigation";

export default function NotFound() {
  const router = useRouter();

  return (
    <div className={style.container}>
      <title className={style.title}>404 - Page Not Found</title>
      <div className={style.description}>
        죄송합니다. 페이지 정보를 찾을 수 없습니다.
        <br />
        URL 주소를 확인해주세요.
      </div>
      <button className={style.back} onClick={() => router.back()}>
        돌아가기
      </button>
    </div>
  );
}
