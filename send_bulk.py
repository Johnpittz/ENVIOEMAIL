# send_bulk.py
import csv, time, smtplib, ssl, sys
from email.message import EmailMessage
from datetime import datetime
from datetime import datetime, timezone
import smtplib


# ---------- CONFIGURE AQUI (substitua pelas credenciais do Mailtrap ou do seu ESP) ----------
SMTP_HOST = "sandbox.smtp.mailtrap.io"    # ex: smtp.mailtrap.io ou smtp.seuesp.com
SMTP_PORT = 587
SMTP_USER = "783387034f9e3c"       # do Mailtrap ou do ESP
SMTP_PASS = "48e104642f8980"      # do Mailtrap ou do ESP
# ------------------------------------------------------------------------------------------

FROM_NAME = "Sua Loja"
FROM_ADDR = SMTP_USER              # usar o mesmo do SMTP é recomendável
UNSUB_URL_BASE = "https://seudominio.com/unsubscribe?email="
SUBJECT = "Novidades e ofertas especiais"
EMAILS_PER_MIN = 60                # ajuste conforme seu provedor/limites
DELAY = 60.0 / EMAILS_PER_MIN

SUBJECT = "Novidades e ofertas especiais"

def mk_message(to_addr, nome):
    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{FROM_ADDR}>"
    msg["To"] = to_addr
    msg["Subject"] = SUBJECT
    msg["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    # header recomendado para entregabilidade
    msg["List-Unsubscribe"] = f"<{UNSUB_URL_BASE}{to_addr}>"

    text = (f"Olá {nome or ''},\n\n"
            "Preparamos uma página com ofertas e novidades para você:\n"
            "https://seudominio.com/minha-landing\n\n"
            f"Para parar de receber, acesse: {UNSUB_URL_BASE}{to_addr}\n")
    html = (f"""<html><body>
        <p>Olá {nome or ''},</p>
        <p>Preparamos uma página com ofertas e novidades para você.</p>
        <p><a href="https://seudominio.com/minha-landing">Abrir landing</a></p>
        <hr>
        <p style="font-size:12px;color:#666">
           Para parar de receber, <a href="{UNSUB_URL_BASE}{to_addr}">clique aqui</a>.
        </p>
    </body></html>""")
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")
    return msg

def load_recipients(csv_path):
    recs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            email = (row.get("email") or "").strip()
            unsub = (row.get("unsubscribed") or "").strip().lower() in ("true","1","yes")
            if email and not unsub:
                recs.append({"email": email, "nome": row.get("nome","").strip()})
    return recs

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
            except Exception as e:
                print(f"[ERRO] {to_addr} -> {e}", file=sys.stderr)
            time.sleep(DELAY)

            EMAILS_PER_MIN = 5        # antes era 60. teste com 5; se ainda limitar, use 2 ou 1
DELAY = 60.0 / EMAILS_PER_MIN

# ----- CONFIGS -----
LOGO_URL      = "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg"  # troque
LANDING_URL   = "https://seudominio.com/minha-landing?utm_source=email&utm_medium=remarketing&utm_campaign=teste"
UNSUB_URL_BASE= "https://seudominio.com/unsubscribe?email="  # mantenha

HTML_TEMPLATE = """\
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <meta name="x-apple-disable-message-reformatting">
  <title>Novidades e ofertas especiais</title>
  <!-- PREHEADER (aparece do lado do assunto) -->
  <span style="display:none!important;visibility:hidden;opacity:0;color:transparent;height:0;width:0;overflow:hidden;">
    Ofertas selecionadas para você, {nome}! Confira na nossa página. &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </span>
</head>
<body style="margin:0;padding:0;background:#f5f7fb;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f5f7fb;">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:100%;max-width:600px;background:#ffffff;border-radius:12px;overflow:hidden">
          <!-- HEADER -->
          <tr>
            <td align="center" style="padding:28px 24px 12px;">
              <img src="{logo_url}" width="56" height="56" alt="Logo" style="display:block;border:0;">
              <div style="font:700 20px/1.2 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;color:#111;margin-top:12px;">
                Novidades e ofertas especiais
              </div>
            </td>
          </tr>

          <!-- HERO -->
          <tr>
            <td style="padding:8px 24px 0;">
              <div style="font:400 16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;color:#333;">
                Olá {nome},<br><br>
                Preparamos uma seleção rápida de ofertas e lançamentos da nossa loja — tudo em uma página única
                para você comparar e decidir sem perder tempo.
              </div>
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td align="center" style="padding:24px 24px 8px;">
              <!-- botão “bulletproof” -->
              <a href="{landing_url}"
                 style="background:#1a73e8;color:#fff;text-decoration:none;
                        display:inline-block;padding:14px 24px;border-radius:8px;
                        font:600 16px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;">
                 Ver ofertas agora
              </a>
            </td>
          </tr>

          <!-- LISTA CURTA (opcional) -->
          <tr>
            <td style="padding:8px 24px 0;">
              <ul style="margin:0 0 16px 18px;padding:0;font:400 14px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial;color:#444;">
                <li>Entrega rápida e garantia oficial</li>
                <li>Pagamento facilitado</li>
                <li>Suporte pós-venda direto com a loja</li>
              </ul>
            </td>
          </tr>

          <!-- FOOTER -->
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

        <!-- fallback de link em texto simples -->
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


def mk_message(to_addr, nome):
    msg = EmailMessage()
    # ...
    msg["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")  # fix do warning
    # ...

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
                # Tratamento p/ limite de taxa ou outros 5xx
                print(f"[ERRO] {to_addr} -> ({e.smtp_code}) {e.smtp_error}")
                try:
                    s.rset()  # reseta a sessão para evitar "nested MAIL command"
                except Exception:
                    pass
                # backoff simples antes de seguir para o próximo
                time.sleep(max(DELAY, 2.0))
            except Exception as e:
                print(f"[ERRO] {to_addr} -> {e}")
                try:
                    s.rset()
                except Exception:
                    pass
                time.sleep(max(DELAY, 2.0))
            time.sleep(DELAY)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python send_bulk.py lista.csv")
        sys.exit(1)
    main(sys.argv[1])
