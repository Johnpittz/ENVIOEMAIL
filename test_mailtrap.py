import smtplib, ssl
from email.message import EmailMessage

SMTP_HOST = "sandbox.smtp.mailtrap.io"   # ATENÇÃO: é "sandbox.smtp..."
SMTP_PORT = 587
SMTP_USER = "783387034f9e3c"
SMTP_PASS = "48e104642f8980"

msg = EmailMessage()
msg["From"] = "Loja Teste <teste@exemplo.com>"
msg["To"] = "dest@exemplo.com"
msg["Subject"] = "Teste simples"
msg.set_content("Corpo em texto puro.")

with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as s:
    s.starttls(context=ssl.create_default_context())
    s.login(SMTP_USER, SMTP_PASS)
    s.send_message(msg)
print("OK - enviado para a sandbox")