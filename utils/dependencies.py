#IMPORT STATEMENTS
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import smtplib
from email.message import EmailMessage
#CORE VARIABLES
js_dump = {
  "JSON FOR ACCESSING GOOGLE SHEETS API"
}
doc_url = 'SPEADSHEET LINK'
sheetname = 'performance'
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
dummy_acc = {
  'email': 'mararcrypt@gmail.com',
  'pass': ''
}
gsheet_url = ''
#FUNCTIONS
def get_gsheet(url):
  client = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_dict(js_dump, scope))
  spreadsheet = client.open_by_url(url)
  return spreadsheet
def save_fig(fig, name, format, width, height, scale):
  img_bytes = fig.to_image(format = format, width = width, height = height, scale = scale)
  f = open(name, 'wb')
  f.write(img_bytes)
  f.close()
def email_with_attachment(recipient, sender, subject, content, attachments):
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = sender
  msg['to'] = recipient
  msg.set_content(content)
  for attachment in attachments:
    with open(attachment, 'rb') as file:
      file_data = file.read()
      msg.add_attachment(file_data, maintype = 'application', subtype = 'png', filename = attachment)
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(dummy_acc['email'], dummy_acc['pass'])
    smtp.send_message(msg)