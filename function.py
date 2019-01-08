import smtplib, os, time
import traceback
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import io
import logging
def logfile():
    # fp = io.StringIO()
    # traceback.print_stack(file=fp)
    # message = fp.getvalue()

    tim = time.strftime("%Y%m%d%H%M%S")
    logging.basicConfig(level=logging.DEBUG,            # 定义输出到文件的log级别，大于此级别的都被输出
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',# 定义输出log的格式
                        datefmt='%a, %d %b %Y %H:%M:%S',         # 时间
                        filename='../Logfile/'+tim+'.log',       # log文件名
                        filemode='w')                        # 写入模式“w”或“a”

    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning message')
    logging.error('error message')
    logging.critical('critical message')



def send_mail(n,report):
    """用于将测试报告发送到邮箱
      n== 1 时 添加附件
    :param
    smtp_dict = {
        "smtp_server": "发送邮件的smtp ex:smtp.126.com",
        "send_user": "发送邮件的邮箱 ex:am1122@126.com",
        "send_pwd": "发送邮件的邮箱密码 ex:mima",
        "sender": "发件人邮箱用于显示收到邮件中的发件人 ex:am1122@126.com",
        "receiver": "收件人邮箱 ex:zhangmin@hidtest.cn",多个收件人可以写成list
        "subject": "邮件主题 ex:自动化测试报告"
    }
    """
    smtp_dict = {
        "smtp_server": "smtp.163.com",  # 发送邮件服务器
        "send_user": "shaoxinlin5519@163.com",  # 发送邮件的邮箱账号
        "send_pwd": "159369sxl",  # 发送邮件的账号密码
        "sender": "shaoxinlin5519@163.com",
        "receiver": ['1260510655@qq.com','shaoxinlin@ajgs.cn'], # 收件邮箱地址
        "subject": "接口自动化测试报告\n"  # 邮件主题
    }

    # 获取测试报告的内容
    file = open(report, "rb")
    mail_body = file.read()
    print(mail_body)
    file.close()
    # 组装邮件内容
    msg=MIMEMultipart()
    # msg = MIMEText(mail_body, 'html', 'utf-8')
    msg['Subject'] = Header(smtp_dict["subject"], 'utf-8')
    msg['From'] = smtp_dict["send_user"]
    msg['to']=";".join(smtp_dict["receiver"])
    print(msg['to'])
    if n==1:
    #添加附件
        part = MIMEText(mail_body,'html',"utf-8")
        part.add_header('Content-Disposition', 'attachment', filename="接口自动化测试报告.html")
        msg.attach(part)
        msg.attach(MIMEText(mail_body, 'html', 'utf-8'))  ###将数据放到正文
    else:
        msg.attach(MIMEText(mail_body, 'html', 'utf-8'))###将数据放到正文
    # 发送邮件
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtp_dict["smtp_server"])
        smtp.login(smtp_dict["send_user"], smtp_dict["send_pwd"])
        smtp.sendmail(msg['From'],msg['to'], msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as se:
        print("邮件发送失败！！")
        print(se)
        raise se

def screen_shot(driver):
    """用于测试用例执行过程中的截图
    :param
    第一个当然是driver对象，
    第二个是保存的图片文件名，不用输.png"""

    top_dir = "../report/image/"
    times = time.strftime("%Y%m%d%H%M%S")
    image_file = top_dir + times + ".png"
    driver.get_screenshot_as_file(image_file)