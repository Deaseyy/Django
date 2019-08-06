import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders

from email.mime.text import MIMEText #创建邮件

#smtp服务器:smtp.163.com
#端口:25
#邮箱账号:13875045745@163.com
#授权码:要和邮箱账号匹配

smtp_server = 'smtp.163.com'
smtp_port = 25
from_email = '13875045745@163.com' #发送方账号
auth_code = 'Y8012427149' #163邮箱授权码
to_email = '1097724917@qq.com'  #收件人邮箱账号

# smtp_server = 'smtp.qq.com'
# smtp_port = 25
# from_email="1239573174@qq.com"#发送方
# auth_code="bypvqkwhecssgbdi"  #第三方登录授权码
# to_email="vi109772@163.com"

#创建邮箱对象
smtp = smtplib.SMTP(smtp_server,smtp_port)
smtp.login(from_email,auth_code)


content= '<html><body><h1>Hello</h1>' +'<p>send by <a href="http://www.python.org">Python</a>...</p>' +'</body></html>'
subject= '大吉大利'
#创建邮件
msg = MIMEMultipart()  #代表邮件本身
msg["Subject"] = subject #邮箱主题
msg["From"] = from_email #发件人
msg["To"] = to_email #收件人

#邮件正文是MIMEText
msg.attach(MIMEText(content,'html','utf-8')) #添加一个MIMEText作为邮件正文

#添加附件就是加上一个MIMEBase,从本地读取一个图片
with open(r"D:\Learn\H5\练习\1基本标签\img\2.jpg","rb") as f:
    #设置附件的MIME和文件名,这里是jpg类型
    mime = MIMEBase('image','jpg',filename='2.jpg')
    #加上必要的头信息
    mime.add_header('Content-Disposition', 'attachment', filename='test.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    mime.set_payload(f.read())
    #Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
#发送
smtp.sendmail(from_email,to_email,msg.as_string())
#关闭
smtp.close()
