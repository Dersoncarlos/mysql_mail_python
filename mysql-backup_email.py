#!/usr/bin/python
# -*- coding: utf-8 -*-
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Anderson Carlos dos Santos Santana
# Website: http://dersoncarlos.com.br
# Tested with : Python 2.7.15 & PHP 5.6
# Script Revision: 1.1
#
##########################################################
 
# Import required python libraries
 
import os
import time
import datetime
import pipes
import subprocess
import smtplib
import zipfile

from email import encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.mime.base import MIMEBase 

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.
 
DB_HOST = 'endereco_servidor.com.br' 
DB_USER = 'username_bd'
DB_USER_PASSWORD = 'password_bd'
DB_NAME = 'bd'
BACKUP_PATH = 'path_completo'
SMTP_SERVER = 'endereco_smtp_servidor'


# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME
 
# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)
 
# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print ("checking for databases names file.")
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print ("Databases file found...")
    print ("Starting backup of all dbs listed in file " + DB_NAME)
else:
    print ("Databases file not found...")
    print ("Starting backup of database " + DB_NAME)
    multi = 0
 
# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")
 
   while p <= flength:
        db = dbfile.readline()   # reading database name from file
        db = db[:-1]         # deletes extra line
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        os.system(dumpcmd)
        # descomentar as linhas abaixo caso queira fazer compressao(gzip)   
        # gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
        # os.system(gzipcmd)
        p = p + 1
    dbfile.close()
else:
    db = DB_NAME
    print ("Iniciando backup de 1 banco")
    dumpcmd = "mysqldump  -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + DB_NAME + ".sql"
    
    os.system(dumpcmd)
    # descomentar as linhas abaixo caso queira fazer compressao(gzip)
    # gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + DB_NAME + ".sql"
    # os.system(gzipcmd)
 
print ("")
print ("Backup script completed")
print ("backups criado em '" + TODAYBACKUPPATH + "' diretorio")

print ("enviando email...")

gmail_user = "email_remetente"
gmail_password = 'senha' # env_var
# Create Email
mail_from = gmail_user
mail_to = "email_destino"
mail_subject = 'Backup'

arquivo = pipes.quote(TODAYBACKUPPATH) + "/" + DB_NAME + ".sql"

print ("anexando arquivo: '" + arquivo + "' ")

msg = MIMEMultipart()
message = "segue link de backup"

f = file(arquivo)

msg.attach(MIMEText(message, 'plain'))
msg['Subject'] = 'Backup banco de dados'
msg['From'], msg['To'] = gmail_user, mail_to

attachment = MIMEText(f.read())
attachment.add_header('Content-Disposition', 'attachment',   filename=arquivo)
msg.attach(attachment)

print ("enviando email...")

# Sent Email
server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
server.login(gmail_user, gmail_password)
server.sendmail(mail_from, mail_to, msg.as_string())
server.close()
print ("email enviado...")
