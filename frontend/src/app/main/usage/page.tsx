"use client";

import style from "@collect/page.module.css";
import { useEffect, useState } from "react";
import type { CollectHistory } from "@/@types/gps";
import Cookies from "js-cookie";
import Table from "@/app/components/table";
import { today } from "@/utils";

export default function Page() {
  const [startDate, setStartDate] = useState<string>("");
  const [lastDate, setLastDate] = useState<string>("");
  const [usageDatas, setusageDatas] = useState<CollectHistory[]>([]);

  const selectDates = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name === "start") {
      setStartDate(value);
    } else if (name === "last") {
      setLastDate(value);
    }
  };

  const fetchData = async (first: string, last: string) => {
    const access_token = Cookies.get("access_token");

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_URL}/usage?first=${first}&last=${last}`,
      {
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          Authorization: `Bearer ${access_token}`,
        },
        cache: "force-cache",
      }
    );

    const data = await response.json();
    if (Array.isArray(data.result)) {
      setusageDatas(data.result);
    } else {
      console.error("응답 데이터가 배열이 아닙니다.");
    }
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const access_token = Cookies.get("access_token");

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_URL}/usage?first=${startDate}&last=${lastDate}`,
      {
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          Authorization: `Bearer ${access_token}`,
        },
        cache: "force-cache",
      }
    );

    const data = await response.json();
    if (Array.isArray(data.result)) {
      setusageDatas(data.result);
    } else {
      console.error("응답 데이터가 배열이 아닙니다.");
    }
  };

  useEffect(() => {
    // const today = new Date().toISOString().split("T")[0];
    // setStartDate(today);
    // setLastDate(today);
    setStartDate(today);
    setLastDate(today);
    fetchData(today, today);
  }, []);

  return (
    <div className={style.container}>
      <div>
        <div className={style.title}>위치정보 이용•제공기록</div>
      </div>
      <form onSubmit={onSubmit} className={style.datePicker}>
        <input
          className={style.input}
          type="date"
          value={startDate}
          name="start"
          onChange={selectDates}
        />
        <input
          className={style.input}
          type="date"
          value={lastDate}
          name="last"
          onChange={selectDates}
        />
        <button type="submit" className={style.button}>
          검색
        </button>
      </form>
      <Table datas={usageDatas} />
    </div>
  );
}
