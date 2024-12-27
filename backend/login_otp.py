import onetimepass as otp
import qrcode

secret_key = 'TRASYSABCDEFGHIJKLMNOPQRSTUVWXYZ'
# img = qrcode.make(secret_key)
# img.save("secretKey.img")
# print(type(img))
# print(img.size)

def get_code():
    print(secret_key, "++++++++++++++++++++ 999")
    rt = otp.get_totp(secret_key)
    print(rt, type(rt))
    return rt

code = get_code()
print ("서버쪽 임시 비밀번호: ", code)

#코드 유효성 검증 (code: 사용자 입력값)
result = otp.valid_totp(code, secret_key)

print(result)