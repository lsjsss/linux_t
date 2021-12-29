from email.header import Header
from email.mime.text import MIMEText
import smtplib
# 定义文件内容  plain: 纯文本
msg=MIMEText("python local test\n","plain","utf8")
msg["From"] = Header("From", "utf8")  # 发送人
msg["To"] = Header("Receivers", "utf8")  # 收件人
msg["Subject"] = Header("py test", "utf8")  # 主题
smtp=smtplib.SMTP("127.0.0.1")# 创建SMTP对象指明发给谁
sender = "root"  # 声明发送者的用户
receivers = ["bob", "alice"]  # 声明接受者的用户
# msg.as_bytes(): 将邮件内容转换成字节串
smtp.sendmail(sender, receivers, msg.as_bytes())
# mail -u bob