import resend

class MailUtil:

  @staticmethod
  def send(subject: str, body_html: str):

    resend.api_key = "re_HKdsuvmk_5QDSNgSUJ6CLtRtUi2F1GAgX"

    resend.Emails.send({
      "from": "Tennis@resend.dev",
      "to": "heciying@gmail.com",
      "subject": subject,
      "html": body_html
      # "html": "<p>Congrats on sending your <strong>first email</strong>!</p>"
    })
