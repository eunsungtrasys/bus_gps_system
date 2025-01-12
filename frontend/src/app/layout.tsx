import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import style from "@/app/footer.module.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "GPS Data Management",
  description: "Generated by EUNSUNG",
};

const footerData = [
  {
    lines: ["GPS System", "은성트래시스(주)"],
  },
  {
    lines: [
      "대표 : 양국승",
      "· 개인정보처리관리자 : 양국승",
      "· 사업자번호 : 538 - 88 - 01948",
      "· 통신판매업 신고번호 : 2022 - 광주북구 - 0425",
    ],
  },
  {
    lines: [
      "사무실 : 62286 광주광역시 광산구 장신로 342 - 19",
      "Copyright (C) 2024 은성트래시스(주),&ensp;(주)카라멜라 all rights reserved.",
    ],
  },
];

export function Footer() {
  return (
    <div className={style.container}>
      <div className={style.wrapper}>
        {footerData.map((section, index) => (
          <div key={index} className={style.first}>
            {section.lines.map((line, idx) => (
              <span key={idx} className={style.span}>
                {line}
              </span>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="kr">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
        <Footer />
      </body>
    </html>
  );
}
