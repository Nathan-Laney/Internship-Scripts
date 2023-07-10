import win32com.client
import os
import zipfile
from pathlib import Path
from datetime import datetime

zipped_path = 'C:/temp/zipped'
unzipped_path = 'C:/temp/unzipped'
text_log_path = 'C:/temp/logs'

date = datetime.today().strftime('%Y-%m-%d')

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6) # "6" refers to the index of a folder - in this case the inbox. You can change that number to reference
preArchiveFolder = inbox.Folders("LogManager").Folders("PreArchive")
postArchiveFolder = inbox.Folders("LogManager").Folders("Archive")
messages = preArchiveFolder.Items


def downloadLogZipFile(m):
    if "Report Domain: alexandercountync.gov Submitter: reports.emailsrvr.com" in m.Subject:
        # print (m)
        attachments = m.Attachments
        # print(len(attachments))
        # num_attach = len([x for x in attachments])
        for x in attachments:
            attachment = x
            # print ("attachment: " + attachment)
            attachment.SaveASFile(os.path.join(zipped_path,attachment.FileName))
    # else:
    #     print("This is not a report email.")

def extractZipFile(file):
    # Unzip the .zip file
    working_directory = zipped_path
    os.chdir(working_directory)
    # print("file:")
    # print(file)
    if zipfile.is_zipfile(file): # if it is a zipfile, 
        # print("is zip")
        with zipfile.ZipFile(file) as item: # treat the file as a zip
            item.extractall(unzipped_path)  # extract it into the unzip path

def convertXMLtoTXT(file):
    working_directory = unzipped_path
    os.chdir(working_directory)
    # print(file)
    if ".xml" in file:
        filename = os.path.splitext(file)[0] + ".txt"
        # print(filename)
        if not os.path.isfile(filename):
            # print('file doesnt exist, creating it now') 
            os.rename(file,filename)
        # else:
        #     print("file already exists, no need to convert")
    return os.path.splitext(file)[0] + ".txt"
        # os.remove(working_directory + '/' + file)

def appendContentsToLogfile(file):
    working_directory = text_log_path
    os.chdir(working_directory)
    with open(date + '.txt', "a") as logFile:
        if '.txt' in file:
            with open(unzipped_path + '/'+ file, 'r') as inputfile:
                logFile.write("\n---------------------------------------------------------------\n" + inputfile.name + "\n---------------------------------------------------------------\n")
                logFile.write(inputfile.read())

def clearTempFolders():
    working_directory = unzipped_path
    os.chdir(working_directory)
    for file in os.listdir(working_directory):
        # print(file)
        os.remove(file)

    working_directory = zipped_path
    os.chdir(working_directory)
    for file in os.listdir(working_directory):
        # print(file)
        os.remove(file)

    # os.rmdir(zipped_path)
    # os.rmdir(unzipped_path)

def createTempFolders():
    if not os.path.exists(zipped_path):
        os.makedirs(zipped_path)
    if not os.path.exists(unzipped_path):
        os.makedirs(unzipped_path)
    if not os.path.exists(text_log_path):
        os.makedirs(text_log_path)
    


if __name__ == '__main__':
    createTempFolders()
    # Download all message attachments

    print("Downloading Attachments")

    for message in messages:
        downloadLogZipFile(message)
        message.Move(postArchiveFolder)

    print("Unzipping")
    
    for file in os.listdir(zipped_path):
        extractZipFile(file)

    print("Converting and Appending")
    
    for file in os.listdir(unzipped_path):
        if '.xml' in file:
            txtFile = convertXMLtoTXT(file)
            # print (txtFile)
    
    # has to be two loops or the "for each file" is messed up as a result of directory operation

    for file in os.listdir(unzipped_path):
        if '.txt' in file:
            appendContentsToLogfile(txtFile)
    
    clearTempFolders()


    print("DONE")