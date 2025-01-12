import style from "@app/dateInput.module.css";

interface DateInputProps {
  value: string;
  name: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function DateInput({ value, name, onChange }: DateInputProps) {
  return (
    <input
      className={style.input}
      type="date"
      value={value}
      name={name}
      onChange={onChange}
    />
  );
}
