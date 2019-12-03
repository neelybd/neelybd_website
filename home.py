from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators

DEBUG = True

# ReCaptcha
# Keys for localhost

app = Flask(__name__, template_folder='templates')
app.config.from_object(__name__)

app.secret_key = 'YourSuperSecreteKey'


### Mail ###
class ContactForm(FlaskForm):
    name = StringField('Your Name:', [validators.DataRequired()])
    email = StringField('Your e-mail address:', [validators.DataRequired(), validators.Email('your@email.com')])
    subject = StringField('Subject:', [validators.DataRequired()])
    message = TextAreaField('Your message:', [validators.DataRequired()])
    submit = SubmitField('Send Message')


# add mail server config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'Email'
app.config['MAIL_PASSWORD'] = 'Password'

mail = Mail(app)
### End Mail ###

@app.route('/', methods=('GET', 'POST'))
def home():
    form = ContactForm()
    return render_template('index.html/', form=form)


@app.route('/submit/', methods=('GET', 'POST'))
def contact_submit():
    form = ContactForm()
    if request.method == 'POST':
        msg = Message("Message from your visitor" + form.name.data,
                      sender='YourUser@NameHere',
                      recipients=['Email'])
        msg.body = """
        From: %s <%s>, Subject: <%s>
        %s
        """ % (form.name.data, form.email.data, form.subject.data, form.message.data)
        mail.send(msg)
        flash('Successfully sent message!')
        return render_template('index.html', form=form)
    if request.method == 'GET':
        return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)