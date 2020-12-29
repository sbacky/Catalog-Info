#!/usr/bin/env python3

import os, datetime, reports, emails, sys

def descriptions(dir):
    '''Returns list of supplier fruit description data.'''
    # Get list of full paths to description txt files
    fileList = os.listdir(dir)
    pathList = []
    for file in fileList:
        fullPath = os.path.join(dir, file)
        pathList.append(fullPath)
    info = []
    for path in pathList:
        txt = open(path, "r")
        name = txt.readline()
        weight = txt.readline()
        txt.close()
        info.append("name: {}".format(name))
        info.append("weight: {}".format(weight))
        info.append("<br/>")
    return info

def main():
    dir = sys.argv[1]
    # Generate PDF
    date = datetime.date.today().strftime("%B %d, %Y")
    title = "Processed Update on {}\n".format(date)
    info = descriptions(dir)
    paragraph = "<br/>".join(info)
    reports.generate_report("/tmp/processed.pdf", title, paragraph)
    # Generate email
    sender = "automation@example.com"
    receiver = "student-03-73b7907327aa@example.com"
    subject = "Upload Completed - Online Fruit store"
    body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."
    attachment = "/tmp/processed.pdf"
    message = emails.generate_email(sender, receiver, subject, body, attachment)
    emails.send_email(message)

if __name__ == "__main__":
    main()
