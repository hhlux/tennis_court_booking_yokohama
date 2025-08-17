import resend

resend.api_key = "re_HKdsuvmk_5QDSNgSUJ6CLtRtUi2F1GAgX"

r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": "heciying@gmail.com",
  "subject": "Hello World",
  "html": "<p>Congrats on sending your <strong>first email</strong>!</p>"
})
