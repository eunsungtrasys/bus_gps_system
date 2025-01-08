"use client";

import type { AccessHistory, CollectHistory, UsageHistory } from "@/@types/gps";
import style from "@app/table.module.css";
import { usePathname } from "next/navigation";

interface TableProps<T> {
  datas: T[];
}

export default function Table<
  T extends CollectHistory | AccessHistory | UsageHistory
>({ datas }: TableProps<T>) {
  const pathname = usePathname();

  return (
    <div className={style.container}>
      <div className={style.wrapper}>
        <div>
          <p className={style.p}>데이터 수 : {datas.length}개</p>
        </div>
        <div className={style.tableContainer}>
          <table className={style.table}>
            <thead className={style.thead}>
              {pathname === "/main/collect" && (
                <tr>
                  <th className={style.th}>ID</th>
                  <th className={style.th}>수집방법</th>
                  <th className={style.th}>수집 요청인</th>
                  <th className={style.th}>수집일시</th>
                </tr>
              )}
              {pathname === "/main/usage" && (
                <tr>
                  <th className={style.th}>UUID</th>
                  <th className={style.th}>취득경로</th>
                  <th className={style.th}>제공받는자</th>
                  <th className={style.th}>이용•제공일시</th>
                </tr>
              )}
              {pathname === "/main/access" && (
                <tr>
                  <th className={style.th}>UUID</th>
                  <th className={style.th}>ID</th>
                  <th className={style.th}>IP</th>
                  <th className={style.th}>접속일시</th>
                  <th className={style.th}>접속자 이름</th>
                </tr>
              )}
            </thead>
            <tbody>
              {datas.map((data) => {
                if (pathname === "/main/collect") {
                  const datas = data as CollectHistory;
                  return (
                    <tr key={datas.collect_history_id} className={style.tr}>
                      <td className={style.td}>{datas.coordinate_id}</td>
                      <td className={style.td}>{datas.collect_method}</td>
                      <td className={style.td}>{datas.collect_requester}</td>
                      <td className={style.td}>{datas.collect_time}</td>
                    </tr>
                  );
                }
                if (pathname === "/main/usage") {
                  const datas = data as UsageHistory;
                  return (
                    <tr key={datas.usage_history_id} className={style.tr}>
                      <td className={style.td}>{datas.usage_history_id}</td>
                      <td className={style.td}>{datas.collect_method}</td>
                      <td className={style.td}>{datas.recipient}</td>
                      <td className={style.td}>{datas.usage_time}</td>
                    </tr>
                  );
                }
                if (pathname === "/main/access") {
                  const datas = data as AccessHistory;
                  return (
                    <tr key={datas.access_history_id} className={style.tr}>
                      <td className={style.td}>{datas.access_history_id}</td>
                      <td className={style.td}>{datas.user_id}</td>
                      <td className={style.td}>{datas.ip}</td>
                      <td className={style.td}>{datas.access_time}</td>
                      <td className={style.td}>{datas.name}</td>
                    </tr>
                  );
                }
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
