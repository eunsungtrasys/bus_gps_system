"use client";

import { useEffect, useState } from "react";
import style from "@collect/page.module.css";
import type { CollectHistory } from "@/@types/gps";
import Cookies from "js-cookie";
import { today } from "@/utils";
import DateInput from "@/app/components/dateInput";
import Button from "@/app/components/button";
import Table from "@/app/components/table";

export default function Page() {
  const [startDate, setStartDate] = useState<string>("");
  const [lastDate, setLastDate] = useState<string>("");
  const [collectDatas, setCollectDatas] = useState<CollectHistory[]>([]);

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
      `${process.env.NEXT_PUBLIC_API_SERVER_URL}/collect?first=${first}&last=${last}`,
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
      setCollectDatas(data.result);
    } else {
      console.error("응답 데이터가 배열이 아닙니다.");
    }
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const access_token = Cookies.get("access_token");

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_URL}/collect?first=${startDate}&last=${lastDate}`,
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
      setCollectDatas(data.result);
    } else {
      console.error("응답 데이터가 배열이 아닙니다.");
    }
  };

  useEffect(() => {
    setStartDate(today);
    setLastDate(today);
    fetchData(today, today);
  }, []);

  return (
    <div className={style.container}>
      <div>
        <div className={style.title}>위치정보 수집기록</div>
      </div>
      <form onSubmit={onSubmit} className={style.datePicker}>
        <DateInput name="start" value={startDate} onChange={selectDates} />
        <DateInput name="last" value={lastDate} onChange={selectDates} />
        <Button />
      </form>
      <Table datas={collectDatas} />
    </div>
  );
}
