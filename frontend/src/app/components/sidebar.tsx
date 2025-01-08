"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import style from "@app/sidebar.module.css";

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { href: "/main/collect", label: "위치정보 수집기록" },
    { href: "/main/usage", label: "위치정보 이용•제공기록" },
    { href: "/main/access", label: "시스템 접속기록" },
  ];

  return (
    <div className={style.container}>
      <div className={style.sidebar}>
        {links.map((link) => (
          <div className={style.item} key={link.href}>
            <Link
              href={link.href}
              className={pathname === link.href ? style.activeLink : ""}
            >
              {link.label}
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
