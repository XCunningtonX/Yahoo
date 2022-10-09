import email
import imaplib
import time

my_email = "yourusername@yahoo.com"
app_generated_password = "your password goes here"

################### IMAP ########################
start = time.time()
try:
    imap = imaplib.IMAP4(host="imap.mail.yahoo.com", port=imaplib.IMAP4_SSL_PORT)
except Exception as e:
    print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
    imap = None

print("Connection Object : {}".format(imap))
print("Total Time Taken  : {:,.2f} Seconds\n".format(time.time() - start))

############### IMAP with Timeout ######################
start = time.time()
try:
    imap = imaplib.IMAP4(host="imap.mail.yahoo.com", port=imaplib.IMAP4_SSL_PORT, timeout=3)
except Exception as e:
    print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
    imap = None

print("Connection Object : {}".format(imap))
print("Total Time Taken  : {:,.2f} Seconds\n".format(time.time() - start))

################ IMAP SSL Connection ##############################

with imaplib.IMAP4_SSL(host="imap.mail.yahoo.com", port=imaplib.IMAP4_SSL_PORT) as imap_ssl:
    print("Connection Object : {}".format(imap_ssl))

    ############### Login to Mailbox ######################
    print("Logging into mailbox...")
    resp_code, response = imap_ssl.login("yourusername@yahoo.com", "your password goes here")

    print("Response Code : {}".format(resp_code))
    print("Response      : {}\n".format(response[0].decode()))
    
    ############### Set Mailbox #############
    resp_code, mail_count = imap_ssl.select(mailbox="INBOX", readonly=False)

    ############### Search and delete mails in a given Directory ############# 
    resp_code, mails = imap_ssl.search(None,'UNSEEN')

    mail_ids = mails[0].decode().split()
    
    print("Total Mail IDs : {}\n".format(len(mail_ids)))

    print("Deleting Mails...")
    for mail_id in mail_ids:
        resp_code, mail_data = imap_ssl.fetch(mail_id, '(RFC822)') ## Fetch mail data.

        message = email.message_from_bytes(mail_data[0][1]) ## Construct Message from mail data
        print("Mail ID : {}, Date : {}, Subject : {}".format(mail_id, message.get("Date"), message.get("Subject")))

        resp_code, response = imap_ssl.store(mail_id, '+FLAGS', '\\Deleted') ## Setting Deleted Flag
        print("Response Code : {}".format(resp_code))
        print("Response      : {}\n".format(response[0].decode()))

    resp_code, response = imap_ssl.expunge()
    print("Response Code : {}".format(resp_code))
    print("Response      : {}\n".format(response[0].decode() if response[0] else None))

    ############# Close Selected Mailbox #######################
    print("\nClosing selected mailbox....")
    imap_ssl.close()