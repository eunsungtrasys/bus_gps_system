import style from "@app/button.module.css";

export default function Button() {
  return (
    <div>
      <button className={style.button} type="submit">
        검색
      </button>
    </div>
  );
}
