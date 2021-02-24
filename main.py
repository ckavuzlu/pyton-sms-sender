import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import schedule
import time
import datetime
import base64


class Person:
    def __init__(self, name: str, emailAddress: str, dayOfMonth: int, lastEmail: int):
        self.name = name
        self.emailAddress = emailAddress
        self.dayOfMonth = dayOfMonth
        self.lastEmail = lastEmail


berk = Person("Berk", "berkarademir@gmail.com", 12, -1)
burak = Person("Burak", "bemlik1@gmail.com", 21, -1)
can = Person("Can", "ckavuzlu@gmail.com", 5, -1)
izzet = Person("İzzet", "fatmanesil@hotmail.com", 15, -1)
mert = Person("Mert", "mert-erem@hotmail.com", 23, -1)

personArray = [berk, burak, can, izzet, mert]

sender_email = "ckavuzlu@gmail.com"
subject = "Patyum Odeme Hatirlatmasi"
encodedPassword = "ZmVuZXJiYWhjZTEyM3F3ZQ=="
password = base64.b64decode(encodedPassword).decode("utf-8")


def sendMail():
    for person in personArray:
        if (person.dayOfMonth - 1 == datetime.datetime.now().date()) and person.lastEmail != datetime.datetime.now().date():
            body = """
                   Sevgili {name} ,

                   Yarın günlerden {day} , patyum ödeme günü geldi. Asağıda ödeme bilgileri ve toplam kasadaki miktarın da yer 
                   aldığı ödeme sheet linki yer alıyor. İşCep Kullanıyorsan Karekodu da ekledim. 

                   Oğulcan Kavuzlu
                   Iban : TR640006400000111400981012

                   Sheet Link : https://docs.google.com/spreadsheets/d/1vYLtfuWREKKbAoSRD4B7MgZUMsx8sEmEYPK4lqoMB5s/edit?usp=sharing

                   Bu mesaj otomatiktir, ödeme yaptıysan lütfen dikkate alma :) .
            """.format(name=person.name, day=person.dayOfMonth)

            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = subject
            msgRoot['From'] = sender_email
            msgRoot['To'] = person.emailAddress

            msgText = MIMEText(body)
            msgRoot.attach(msgText)

            fp = open(r'C:\\Users\Can Kavuzlu\Desktop\Python\test.jpeg', 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            msgImage.add_header('content-disposition', 'attachment', filename=('utf-8', '', 'İşCep Qr Kod'))
            msgRoot.attach(msgImage)

            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(sender_email, password)
            send_it = session.sendmail(sender_email, person.emailAddress, msgRoot.as_string())
            person.lastEmail = datetime.datetime.now().date()
            session.quit()
            print('Message sent to ' + person.emailAddress)
        else:
            print(str(person.name) + ' Ödeme günü : ' + str(person.dayOfMonth) + ' Bugun : ' + str(
                datetime.datetime.now().day))
            print(str(person.name) + ' Last Mail Tarihi : ' + str(person.lastEmail) + '\n')


schedule.every().day.at("12:00").do(sendMail)

while True:
    schedule.run_pending()
    time.sleep(1)
