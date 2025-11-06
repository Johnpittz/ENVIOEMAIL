# send_bulk.py (VERSÃO LIMPA • SANDBOX MAILTRAP)
import csv, time, smtplib, ssl, sys
from email.message import EmailMessage
from datetime import datetime, timezone

# =============== SMTP (SANDBOX MAILTRAP) ===============
SMTP_HOST = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 587
SMTP_USER = "783387034f9e3c"   # <-- troque pelo seu (Integration > SMTP)
SMTP_PASS = "48e104642f8980"  # <-- troque pelo seu
# =======================================================

# Remetente (use um e-mail válido, mesmo que fictício para sandbox)
FROM_NAME = "Sua Loja"
FROM_ADDR = "no-reply@exemplo.com"  # NÃO use o USER aqui

# Throttling
EMAILS_PER_MIN = 5
DELAY = 60.0 / EMAILS_PER_MIN

# Links
LANDING_URL    = "https://seudominio.com/minha-landing?utm_source=email&utm_medium=remarketing&utm_campaign=teste"
UNSUB_URL_BASE = "https://seudominio.com/unsubscribe?email="
LOGO_URL       = "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg"

# Template HTML (inline)
HTML_TEMPLATE = """\
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <meta name="x-apple-disable-message-reformatting">
  <title>Novidades e ofertas especiais</title>
  <span style="display:none!important;visibility:hidden;opacity:0;height:0;width:0;overflow:hidden;">
    Ofertas selecionadas para você, {nome}! Confira na nossa página. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </span>
</head>
<body style="margin:0;padding:0;background:#f5f7fb;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f5f7fb;">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:100%;max-width:600px;background:#ffffff;border-radius:12px;overflow:hidden">
          <tr>
            <td align="center" style="padding:28px 24px 12px;">
              <img src="{logo_url}" width="56" height="56" alt="Logo" style="display:block;border:0;">
              <div style="font:700 20px/1.2 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;color:#111;margin-top:12px;">
                Novidades e ofertas especiais
              </div>
            </td>
          </tr>
          <tr>
            <td style="padding:8px 24px 0;">
              <div style="font:400 16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;color:#333;">
                Olá {nome},<br><br>
                Preparamos uma seleção rápida de ofertas e lançamentos da nossa loja — tudo em uma página única
                para você comparar e decidir sem perder tempo.
              </div>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:24px 24px 8px;">
              <a href="{landing_url}"
                 style="background:#1a73e8;color:#fff;text-decoration:none;
                        display:inline-block;padding:14px 24px;border-radius:8px;
                        font:600 16px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;">
                 Ver ofertas agora
              </a>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 24px 28px;">
              <div style="height:1px;background:#e9eef5;margin:0 0 16px 0;"></div>
              <div style="font:400 12px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;color:#6b7280;">
                Você está recebendo este e-mail por ser nosso cliente. Se não quiser mais receber,
                <a href="{unsubscribe_url}" style="color:#1a73e8;">clique aqui para descadastrar</a>.
                <br>
                © {ano} Sua Loja — Todos os direitos reservados.
              </div>
            </td>
          </tr>
        </table>
        <div style="font:400 12px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;color:#777;margin-top:12px;">
          Problemas com o botão? Acesse: <br>
          <a href="{landing_url}" style="color:#1a73e8;word-break:break-all;">{landing_url}</a>
        </div>
      </td>
    </tr>
  </table>
</body>
</html>
"""

def load_recipients(csv_path):
    recs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            email = (row.get("email") or "").strip()
            unsub = (row.get("unsubscribed") or "").strip().lower() in ("true","1","yes")
            if email and not unsub:
                recs.append({"email": email, "nome": (row.get("nome") or "").strip()})
    return recs

def mk_message(to_addr, nome):
    # Corpo texto + HTML
    text = (
        f"Olá {nome or ''},\n\n"
        f"Acesse nossas ofertas: {LANDING_URL}\n"
        f"Descadastro: {UNSUB_URL_BASE}{to_addr}\n"
        "© Sua Loja"
    )
    html = HTML_TEMPLATE.format(
        nome=(nome or "").strip() or "tudo bem",
        logo_url=LOGO_URL,
        landing_url=LANDING_URL,
        unsubscribe_url=f"{UNSUB_URL_BASE}{to_addr}",
        ano=datetime.now().year
    )

    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"] = to_addr
    msg["Subject"] = f"Novidades e ofertas — {datetime.now().strftime('%H:%M:%S')}"
    msg["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    msg["List-Unsubscribe"] = f"<{UNSUB_URL_BASE}{to_addr}>"
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")
    return msg

def main(csv_path):
    recipients = load_recipients(csv_path)
    print(f"[INFO] Válidos para envio: {len(recipients)}")

    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as s:
        s.starttls(context=ctx)
        s.login(SMTP_USER, SMTP_PASS)

        for i, r in enumerate(recipients, start=1):
            to_addr = r["email"]
            try:
                msg = mk_message(to_addr, r.get("nome"))
                s.send_message(msg)
                print(f"[OK] {i}/{len(recipients)} -> {to_addr}")
            except smtplib.SMTPResponseException as e:
                print(f"[ERRO] {to_addr} -> ({e.smtp_code}) {e.smtp_error}")
                try: s.rset()
                except Exception: pass
                time.sleep(max(DELAY, 2.0))
            except Exception as e:
                print(f"[ERRO] {to_addr} -> {e}")
                try: s.rset()
                except Exception: pass
                time.sleep(max(DELAY, 2.0))
            time.sleep(DELAY)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python send_bulk.py lista.csv")
        sys.exit(1)
    main(sys.argv[1])
