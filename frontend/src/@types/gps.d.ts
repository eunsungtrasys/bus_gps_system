// 계정
export type User = {
  user_id: number,
  id: string,
  // 
  password: string,
  // 사용자 이름
  name: string,
  // 관리자?
  is_admin: boolean,
  // OTP키
  otp_key: string,
};

// GPS좌표
export type Coordinate = {
  // 고유값
  id: number,
  // GPS기기 ID
  gps_id: string,
  // X 좌표
  x: number,
  // Y 좌표
  y: number,
  // 수집일시
  time: string,
};

// 위치정보 접속기록
export type AccessHistory = {
  // 고유값
  access_history_id: number,
  // 계정 고유값
  user_id: number,
  // 접속 IP
  ip: string,
  // 접속시간
  access_time: string,
  // 접속자
  name: string,
};

// 위치정보 수집기록
export type CollectHistory = {
  // 고유값
  collect_history_id: number,
  // GPS좌표 고유값
  coordinate_id: number,
  // 수집방법
  collect_method: string,
  // 수집요청인
  collect_requester: string,
  // 수집일시
  collect_time: string,
}

// 위치정보 이용•제공기록
export type UsageHistory = {
  // 고유값
  usage_history_id: number,
  // GPS좌표 고유값
  coordinate_id: number,
  // 취득방법
  collect_method: string,
  // 제공받는자
  recipient: string,
  // 이용•제공일시
  usage_time: string,
};

export type SearchParams = {
  first: string,
  last: string,
}