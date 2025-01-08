import Cookies from "js-cookie";
export async function otp(otp_pw: string) {
  const id = Cookies.get("id");
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_SERVER_URL}/otp`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id, otp_pw }),
    }
  );

  if (!response.ok) {
    throw new Error("OTP시도 중 오류가 발생했습니다.");
  }

  const { access_token } = await response.json();
  console.log("OTP access_token", access_token);
  Cookies.set("access_token", access_token);
}

export const today = new Date()
  .toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    timeZone: "Asia/Seoul",
  })
  .replace(/. /g, "-")
  .replace(".", "");
