import win32com.client as win32
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = ''
mail.Subject = 'Test Message'
mail.Body = 'Hi, its test email'
mail.HTMLBody = '''<h2>Я научился отправлять почту, но пока это работает для владельцев desktop outlook
и соответсвенно в рамках локальной сети</h2>
''' #this field is optional
# To attach a file to the email (optional):
#attachment  = "Path to the attachment"
#mail.Attachments.Add(attachment)

mail.Send()
self.outlook.Application.quit()
