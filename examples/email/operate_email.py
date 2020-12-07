'''
一、说明
1.1 程序说明
（1）smtp是邮件发送协议；pop和imap都是邮件接收协议，两者的区别通常的说法是imap的操作会同步到邮箱服务器而pop不会，表现上我也不是很清楚

（2）本程序实现使用smtplib标准库实现邮件发送、使用poplib标准库和imaplib标准库实现邮件收取

（3）具体到代码上，三个功能依次对应程序中的send_email_by_smtp()、recv_email_by_pop3()、recv_email_by_imap4()三个函数，这三个函数相互独立没有调用关系

（4）由于还没弄清楚要怎么能很好地解码邮件，所以这里的pop和imap都只是直接将最新的一封邮件读取后直接打印出来，并没有进行解码。

（5）在贴上代码时，代码中的邮箱已全部替换，使用时记得修改这些信息；注释中已都有较详细说明，不多辍述。

（6）对于自己邮箱的smtp服端器、pop服务器、imap服务器地址如果不知道则自己百度一下，一般都是“协议+邮箱后辍”的形式（比如pop.qq.com），这种形式如果能ping通一般就是了；端口则可能多变，如果查不到就直接nmap等工具扫一下。比如下面：
'''

import smtplib
import poplib
import imaplib
from email.mime.text import MIMEText
from email.header import Header


class operate_email:
    # 此函数通过使用smtplib实现发送邮件
    def send_email_by_smtp(self):
        # 用于发送邮件的邮箱。修改成自己的邮箱
        sender_email_address = "your_email@qq.com"
        # 用于发送邮件的邮箱的密码。修改成自己的邮箱的密码
        sender_email_password = "your_email_password"
        # 用于发送邮件的邮箱的smtp服务器，也可以直接是IP地址
        # 修改成自己邮箱的sntp服务器地址；qq邮箱不需要修改此值
        smtp_server_host = "smtp.qq.com"
        # 修改成自己邮箱的sntp服务器监听的端口；qq邮箱不需要修改此值
        smtp_server_port = 465
        # 要发往的邮箱
        receiver_email = "your_dest_email@qq.com"
        # 要发送的邮件主题
        message_subject = "Python smtp测试邮件"
        # 要发送的邮件内容
        message_context = "这是一封通过Python smtp发送的测试邮件..."

        # 邮件对象，用于构建邮件
        # 如果要发送html，请将plain改为html
        message = MIMEText(message_context, 'plain', 'utf-8')
        # 设置发件人（声称的）
        message["From"] = Header(sender_email_address, "utf-8")
        # 设置收件人（声称的）
        message["To"] = Header(receiver_email, "utf-8")
        # 设置邮件主题
        message["Subject"] = Header(message_subject, "utf-8")

        # 连接smtp服务器。如果没有使用SSL，将SMTP_SSL()改成SMTP()即可其他都不需要做改动
        email_client = smtplib.SMTP_SSL(smtp_server_host, smtp_server_port)
        try:
            # 验证邮箱及密码是否正确
            email_client.login(sender_email_address, sender_email_password)
            print(
                "smtp----login success, now will send an email to {receiver_email}"
            )
        except:
            print(
                "smtp----sorry, username or password not correct or another problem occur"
            )
        else:
            # 发送邮件
            email_client.sendmail(sender_email_address, receiver_email,
                                  message.as_string())
            print(f"smtp----send email to {receiver_email} finish")
        finally:
            # 关闭连接
            email_client.close()

    # 此函数通过使用poplib实现接收邮件
    def recv_email_by_pop3(self):
        # 要进行邮件接收的邮箱。改成自己的邮箱
        email_address = "your_email@qq.com"
        # 要进行邮件接收的邮箱的密码。改成自己的邮箱的密码
        email_password = "your_email_password"
        # 邮箱对应的pop服务器，也可以直接是IP地址
        # 改成自己邮箱的pop服务器；qq邮箱不需要修改此值
        pop_server_host = "pop.qq.com"
        # 邮箱对应的pop服务器的监听端口。改成自己邮箱的pop服务器的端口；qq邮箱不需要修改此值
        pop_server_port = 995

        try:
            # 连接pop服务器。如果没有使用SSL，将POP3_SSL()改成POP3()即可其他都不需要做改动
            email_server = poplib.POP3_SSL(host=pop_server_host,
                                           port=pop_server_port,
                                           timeout=10)
            print("pop3----connect server success, now will check username")
        except:
            print(
                "pop3----sorry the given email server address connect time out"
            )
            exit(1)
        try:
            # 验证邮箱是否存在
            email_server.user(email_address)
            print("pop3----username exist, now will check password")
        except:
            print("pop3----sorry the given email address seem do not exist")
            exit(1)
        try:
            # 验证邮箱密码是否正确
            email_server.pass_(email_password)
            print("pop3----password correct,now will list email")
        except:
            print("pop3----sorry the given username seem do not correct")
            exit(1)

        # 邮箱中其收到的邮件的数量
        email_count = len(email_server.list()[1])
        # 通过retr(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
        resp, lines, octets = email_server.retr(email_count)
        # lines是邮件内容，列表形式使用join拼成一个byte变量
        email_content = b'\r\n'.join(lines)
        # 再将邮件内容由byte转成str类型
        email_content = email_content.decode()
        print(email_content)

        # 关闭连接
        email_server.close()

    # 此函数通过使用imaplib实现接收邮件
    def recv_email_by_imap4(self):
        # 要进行邮件接收的邮箱。改成自己的邮箱
        email_address = "your_email@qq.com"
        # 要进行邮件接收的邮箱的密码。改成自己的邮箱的密码
        email_password = "your_email_password"
        # 邮箱对应的imap服务器，也可以直接是IP地址
        # 改成自己邮箱的imap服务器；qq邮箱不需要修改此值
        imap_server_host = "imap.qq.com"
        # 邮箱对应的pop服务器的监听端口。改成自己邮箱的pop服务器的端口；qq邮箱不需要修改此值
        imap_server_port = 993

        try:
            # 连接imap服务器。如果没有使用SSL，将IMAP4_SSL()改成IMAP4()即可其他都不需要做改动
            email_server = imaplib.IMAP4_SSL(host=imap_server_host,
                                             port=imap_server_port)
            print("imap4----connect server success, now will check username")
        except:
            print(
                "imap4----sorry the given email server address connect time out"
            )
            exit(1)
        try:
            # 验证邮箱及密码是否正确
            email_server.login(email_address, email_password)
            print("imap4----username exist, now will check password")
        except:
            print(
                "imap4----sorry the given email address or password seem do not correct"
            )
            exit(1)

        # 邮箱中其收到的邮件的数量
        email_server.select()
        email_count = len(email_server.search(None, 'ALL')[1][0].split())
        # 通过fetch(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
        typ, email_content = email_server.fetch(f'{email_count}'.encode(),
                                                '(RFC822)')
        # 将邮件内存由byte转成str
        email_content = email_content[0][1].decode()
        print(email_content)
        # 关闭select
        email_server.close()
        # 关闭连接
        email_server.logout()


if __name__ == "__main__":
    # 实例化
    email_client = operate_email()
    # 调用通过smtp发送邮件的发送函数
    email_client.send_email_by_smtp()
    # 调用通过pop3接收邮件的接收函数
    email_client.recv_email_by_pop3()
    # 调用通过imap4接收邮件的接收函数
    email_client.recv_email_by_imap4()