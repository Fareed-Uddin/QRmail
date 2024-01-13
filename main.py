from email.message import EmailMessage
from password import defaultpassword
import ssl
import smtplib
import qrcode

def main():
    website = input("Enter your URL: ")
    senderEmail = input("Enter your email address: ")
    password = input("Enter your password: ")
    recieverEmail = input("Enter sender Email Address: ")
    fileName = input("What would like to name your QR Code: ")
    body = input("Enter the body of your email: ")
    pngName = fileName + ".png"
    password = defaultpassword()
    generateQRcode(website, pngName)
    sendQRcode(senderEmail, password, recieverEmail, body, pngName)

def generateQRcode(website,fileName):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(website)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(fileName)

def sendQRcode(senderEmail, password,recieverEmail, body, fileName):
    subject = "Your QR Code"
    em = EmailMessage()
    em['From'] = senderEmail
    em['To'] = recieverEmail
    em[' subject'] = subject
    em.set_content(body)

    with open(fileName, 'rb') as image_file:
        image_data = image_file.read()
        em.add_attachment(image_data, maintype='image', subtype='png', filename='qr_code.png')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL( 'smtp.gmail.com' , 465, context=context) as smtp:
        smtp.login(senderEmail, password)
        smtp.sendmail(senderEmail, recieverEmail, em.as_string())

if __name__ == "__main__":
    main()