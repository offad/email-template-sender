import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

IGNORE_KEY_WORD = "Glasgow"

HOST_ADDRESS = "smtp.gmail.com"
PORT = 587

MY_ADDRESS = 'ADDRESS'
APP_ASSWORD = 'APP_PASSWORD'

SUBJECT = "SUBJECT"

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        file_content = template_file.read()
    return Template(file_content)

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    names = []
    emails = []

    with open(filename, mode='r', encoding='utf-8') as contacts_file:

        ignoreContact = False
        checkingContact = False
        name = ""
        email = ""

        for line in contacts_file:
            line = line.strip()
            if IGNORE_KEY_WORD in line:
                ignoreContact = True
                continue

            if checkingContact:

                if '@' in line:
                    email = line
                    continue

                if len(line) == 0:
                    if not ignoreContact:
                        names.append(name)
                        emails.append(email)

                    checkingContact = False
                    ignoreContact = False

            else:
                if len(line) > 0:
                    name = line
                    checkingContact = True

    return names, emails

def main():
    mail_template = read_template('template.txt')
    names, emails = get_contacts('contacts.txt') # read contacts
    
    # set up the SMTP server
    s = smtplib.SMTP(host=HOST_ADDRESS, port=PORT)
    s.starttls()
    s.login(MY_ADDRESS, APP_PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = mail_template.substitute(NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = SUBJECT

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    main()