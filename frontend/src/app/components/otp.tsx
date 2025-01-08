import React, { useState } from "react";
import { InputOtp } from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { otp } from "@/utils";
import style from "@app/otp.module.css";

export default function Otp() {
  const [value, setValue] = useState<string>("");
  const router = useRouter();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await otp(value);
      router.push("/main/collect");
    } catch (error) {
      console.error("OTP 인증 시도 중 오류 발생", error);
    }
  };

  return (
    <div className={style.container}>
      <div className={style.modal_box}>
        <div>
          <p className={style.title}>OTP번호 6자리를 입력해주세요</p>
        </div>
        <form onSubmit={submit}>
          <InputOtp
            className={style.input}
            length={6}
            value={value}
            onValueChange={setValue}
            variant="bordered"
            color="default"
          />
          <div className={style.button_box}>
            <button className={style.button} type="submit">
              로그인
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
