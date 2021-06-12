import email.message
import smtplib


def send_mail(account: str, msg_text: list):
    # 建立訊息物件
    msg = email.message.EmailMessage()
    from_a = 'pythonjobsystem@gmail.com'
    password = 'pythonjobsystem'
    to_b = account
    msg["From"] = from_a
    msg["To"] = to_b
    msg["Subject"] = "Job System 忘記密碼通知"
    msg.set_content("帳號: " + msg_text[0] + " 密碼: " + msg_text[1])  # 內容
    # msg.add_alternative("<h3>HTML內容</h3>我是駿凱，寄送郵件測試，我用python寄的，你看看有沒有收到！！！", subtype="html")  # HTML信件內容
    # 連線到SMTP Sevver
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 建立gmail連驗
    server.login(from_a, password)
    server.send_message(msg)
    server.close()  # 發送完成後關閉連線
    # print("send")

# send_mail("你好")
