import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import date
import os,glob



def send_mail(send_from, password, send_to,cc, subject, text, files,server,port):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To']  = ';'.join(map(str, send_to))
    msg['Cc'] = ';'.join(map(str, cc))
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    try:
        smtp = smtplib.SMTP(server,port)
        smtp.starttls()
        smtp.login(send_from, password)
        send_to = send_to + cc
        # smtp.set_debuglevel(1)
        smtp.sendmail(send_from,send_to,msg.as_string())
        smtp.close()
        print("Mail Sent")
    except Exception as error:
        print(error)



text = '''Hello All,

Please find the attached MRN Automation Report.
Please ignore this mail. Just testing mailing to bulk recipients for mypplus automation.

Thanks & Regards,
Shivani Sajjan.'''

receivers = ['rajesh.kumar.peringathodi@cgi.com','saranya.sundara.babu@cgi.com','chandrakala.k@cgi.com','ashwini.vallampalli@cgi.com',
             'vaishnavi.vaidya@cgi.com','roopashree.basavaraju@cgi.com','mounika.chitla@cgi.com','mayank.r@cgi.com','shivani.sajjan@cgi.com']
cc = ['aravind.kolaki@cgi.com','t.hariharasubramanian@cgi.com','rakesh.kiruba@cgi.com']
# receivers = ['saranya.sundara.babu@cgi.com','chandrakala.k@cgi.com','ashwini.vallampalli@cgi.com',
#              'vaishnavi.vaidya@cgi.com','roopashree.basavaraju@cgi.com','mounika.chitla@cgi.com','mayank.r@cgi.com','shivani.sajjan@cgi.com']
# cc = []
sender = 'shivani.sajjan@cgi.com'
password = 'Secretkey@02'
subject = 'MRN_AUTOMATION_MAIL_TESTING'
server = 'smtprelay.cgi.com'
port = 587
today = date.today()
d4 = today.strftime("%d-%b-%Y")
path = "/var/vodafone/mypplus/automation/SoapUIResults/CSV Reports_" + d4
print(path)
csv_files = glob.glob(os.path.join(path, "*.csv"))
if csv_files != []:
    send_mail(sender,password,receivers,cc,subject,text,csv_files,server,port)

