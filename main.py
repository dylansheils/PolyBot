import imaplib
import email
from email.header import decode_header
import webbrowser
import os

import pip

# Pretend these are not outwardly visible...
username = "thebest.polybot@gmail.com"
password = "thePolyBot2000"

log = ""
sender = ""
# Credit for Gmail Parser: https://www.thepythoncode.com/article/reading-emails-in-python
def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)

status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 1
# total number of emails
messages = int(messages[0])

resulting_message = []

try:
    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            resulting_message = body.split(' ')
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        resulting_message = body.split(' ')
                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    folder_name = clean(subject)
                    if not os.path.isdir(folder_name):
                      # make a folder for this email (named after the subject)
                      os.mkdir(folder_name)
                    filename = "index.html"
                    filepath = os.path.join(folder_name, filename)
                    # write the file
                    open(filepath, "w").write(body)
                    # open in the default browser
        sender = msg['From']
except:
    print("Error: No new emails to read in...")
    # close the connection and logout
    imap.close()
    imap.logout()

if(sender != ""):
    resulting_message = [x.replace("\r\n"," ") for x in resulting_message]
    grammar_msg = resulting_message
    resulting_message = [x.replace(","," ") for x in resulting_message]
    resulting_message = [x.replace("."," ") for x in resulting_message]

    parsed_msg = []
    for x in resulting_message:
        if(x != ' ' and x != ''):
            tmp_array = []
            if(' ' in x):
                tmp_array = x.split(' ')
            else:
                tmp_array.append(x)
            for k in tmp_array:
                parsed_msg.append(k)

    # Credit for removing spaces: https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
    while("" in parsed_msg):
        parsed_msg.remove("")

    #Basic Spell Checking on Uncapitalized Verbiage
    from autocorrect import Speller
    spell = Speller(lang='en')
    i = 0

    whyAreTheseCorrections = ['iterated', 'codebase']
    for x in parsed_msg:
        if((not x.islower() and not x.isupper()) or x.isupper()):
            i += 1
        else:
            before = parsed_msg[i]
            parsed_msg[i] = spell(parsed_msg[i])
            for j in whyAreTheseCorrections:
                if(before == j):
                    parsed_msg[i] = before
            if(before != parsed_msg[i]):
                print("Basic Spelling Check: Possible Correction: " + before + " to " + parsed_msg[i])
                log += "Basic Spelling Check: Possible Correction: " + before + " to " + parsed_msg[i] + "\n"
            i += 1

    # Parse Sender Information
    sender = sender.split(" ")
    nameOfSender = ""
    emailOfSender = ""
    i = 0
    for x in sender:
        if "@" in x:
            emailOfSender = x
        else:
            nameOfSender += x + " "

    nameOfSender = nameOfSender.rstrip()
    emailOfSender = emailOfSender.replace('<', '')
    emailOfSender = emailOfSender.replace('>', '')

    # # To delete emails...
    status, messages = imap.search(None, "ALL")
    # # convert messages to a list of email IDs
    messages = messages[0].split(b' ')
    for mail in messages:
        _, msg = imap.fetch(mail, "(RFC822)")
        # you can delete the for loop for performance if you have a long list of emails
        # because it is only for printing the SUBJECT of target email to delete
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                     # if it's a bytes type, decode to str
                     subject = subject.decode()
        # mark the mail as deleted
        imap.store(mail, "+FLAGS", "\\Deleted")
     #permanently remove mails that are marked as deleted
     #from the selected mailbox (in this case, INBOX)
    imap.expunge()
     # close the connection and logout
    imap.close()
    imap.logout()


    from subprocess import call
    call(["python", "advanceCorrection.py", '#'.join(parsed_msg), nameOfSender, emailOfSender, log, '#'.join(grammar_msg)])