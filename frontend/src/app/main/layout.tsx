import style from "@main/layout.module.css";
import Header from "@app/header";
import Sidebar from "@/app/components/sidebar";
import styles from "@/app/footer.module.css";

const footerData = [
  {
    lines: ["GPS System", "은성트래시스(주)"],
  },
  {
    lines: [
      "대표 : 양국승",
      "· 개인정보 보호책임자 : 양국승",
      "· 사업자번호 : 538 - 88 - 01948",
      "· 통신판매업 신고번호 : 2022 - 광주북구 - 0425",
    ],
  },
  {
    lines: [
      "사무실 : 62286 광주광역시 광산구 장신로 342 - 19",
      "Copyright (C) 2024 은성트래시스(주) all rights reserved.",
    ],
  },
];

function Footer() {
  return (
    <div className={styles.container}>
      <div className={styles.wrapper}>
        {footerData.map((section, index) => (
          <div key={index} className={styles.first}>
            {section.lines.map((line, idx) => (
              <span key={idx} className={styles.span}>
                {line}
              </span>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

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
      <Footer />
    </div>
  );
}
