"use client";

import React, { useState, ChangeEvent, useRef, useEffect } from "react";
import { Button, Input } from "@nextui-org/react";
import { Icon } from "@iconify/react";
import Otp from "./components/otp";
import Cookies from "js-cookie";
import style from "./page.module.css";

export default function Login() {
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => setIsVisible(!isVisible);

  // 1차 시도
  const [id, setId] = useState<string>("");
  const [pw, setPw] = useState<string>("");
  // 2차 시도
  const [otp, setOtp] = useState<boolean>(false);
  const ref = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.focus();
    }
  }, []);

  // Id, Pw 입력칸
  const onChangeEvent = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    if (name === "username") {
      setId(value);
    } else if (name === "password") {
      setPw(value);
    }
  };

  async function login(id: string, pw: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_URL}/login`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id, pw }),
      }
    );

    if (!response.ok) {
      if (response.status === 401 || response.status === 500) {
        alert("아이디와 비밀번호를 확인해주세요.");
      }
      return <div>로그인 중 오류가 발생했습니다.</div>;
    }

    setOtp(true);

    Cookies.set("id", id);
  }

  return (
    <div className={style.container}>
      <div className={style.formContainer}>
        <p className={style.title}>GPS System</p>
        <form className={style.form} onSubmit={(e) => e.preventDefault()}>
          <Input
            ref={ref}
            className={`${style.placeholder} ${style.label} ${style.input}`}
            isRequired
            label="아이디"
            labelPlacement="outside"
            name="username"
            placeholder="아이디를 입력해주세요"
            type="text"
            variant="bordered"
            value={id}
            onChange={onChangeEvent}
            color="primary"
          />
          <Input
            className={`${style.placeholder} ${style.label} ${style.input}`}
            isRequired
            endContent={
              <button type="button" onClick={toggleVisibility}>
                {isVisible ? (
                  <Icon
                    className="pointer-events-none text-2xl text-default-400"
                    icon="solar:eye-closed-linear"
                  />
                ) : (
                  <Icon
                    className="pointer-events-none text-2xl text-default-400"
                    icon="solar:eye-bold"
                  />
                )}
              </button>
            }
            label="비밀번호"
            labelPlacement="outside"
            name="password"
            placeholder="비밀번호를 입력해주세요"
            type={isVisible ? "text" : "password"}
            variant="bordered"
            value={pw}
            onChange={onChangeEvent}
            color="primary"
          />
          <Button color="primary" type="submit" onPress={() => login(id, pw)}>
            로그인
          </Button>
        </form>
      </div>
      {otp && <Otp />}
    </div>
  );
}
