import smtplib
import ssl
from email.message import EmailMessage
import requests

subject = "Email From Python"
sender_email = "spawacz887@gmail.com"
receiver_email = "spawacz887@gmail.com"
password = input("Enter a password: ")


def weather():
    API_KEY = "f493235022f117443717201d55ff1d93"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    city = input("Enter a city name: ")
    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = round(data["main"]["temp"] - 273.15, 2)
        body = (f"{city}\n"
                f"Weather:, {weather}.\n"
            f"Temperature: {temperature} celsius ")
        return body
    else:
        print("An error occurred.")


def sendemail():
    body = weather()
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    html = f"""
    <html>
        <body>
            <h1>{subject}</h1>
            <p>{body}</p>
        </body>
    </html>
    """

    message.add_alternative(html, subtype="html")

    context = ssl.create_default_context()

    print("Sending Email!")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Success")


if __name__ == "__main__":
    sendemail()
