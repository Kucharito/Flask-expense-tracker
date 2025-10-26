from main import app

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '74567f09f8aeab'
app.config['MAIL_PASSWORD'] = 'dcd799dc1d03db'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False