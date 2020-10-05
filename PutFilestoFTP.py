import os, codecs, sys
import ftputil
import ftputil.session

host=''
username=''
password=''

# Соединяемся с FTP сервером и получаем список файлов и папок

def upload_dir(localDir, ftpDir):
    list = os.listdir(localDir)
    for fname in list:
        if os.path.isdir(localDir + fname):             
            if(ftp_host.path.exists(ftpDir + fname) != True):                   
                ftp_host.mkdir(ftpDir + fname)
                print("Директория "+ftpDir + fname + " создана")
            upload_dir(localDir + fname + "/", ftpDir + fname + "/")
        else:               
            if(ftp_host.upload_if_newer(localDir + fname, ftpDir + fname)):
                print("Файл " + ftpDir + fname + " загружен")
            else:
                print("Файл " + localDir + fname + " уже был загружен")

    
#sf = ftputil.session.session_factory(use_passive_mode=True)
local_dir= os.path.abspath(os.getcwd())+ '/Modules/Preparation_Import/ToFTP/'
ftp_dir= r'/'+sys.argv[1]+'/'
try:
    ftp_host=ftputil.FTPHost(host, username, password)
except ftputil.error.FTPOSError:
    print('Нет подключения к FTP: '+ host+'\nПроверьте подключение к интернету, либо обратитесь в поддержку ИМ')
else:
    upload_dir(local_dir, ftp_dir)
    ftp_host.close()
    print('Готово')
    
