import os, time, hashlib, telepot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler




def addFolder():
  
  while True:
    alreadyHave = False
    f_name = input("Folder name:  ")
    f_path = input("Folder path:  ")
    if f_path[-1] != '/':
      f_path = f_path + '/'

    for folder in folders_list:
      if folder.folder_name == f_name and folder.path == f_path:
        alreadyHave = True
      
    if alreadyHave == True:
      print("Already have this folder!")
      continue
    else:
      break

  while True:
    f_h_decision = input("Rename files to Hash(md5)? (on/off):  ").upper()
    if f_h_decision == 'ON' or f_h_decision == 'OFF':
      break
    else:
      print("Invalid")
      continue 
  f_chat_id = input("chat_id to send the files:  ")
  l_name = "log_" + f_name
  cls()
  print('Folder info:\n\n')
  print('name: ' + f_name + "\n")
  print(f_path + f_name + "\n")
  print('log file: ' + l_name + '.txt\n')
  print(f_path + l_name + '.txt\n')
  print("Hash Decision: " + f_h_decision + '\n')
  print("Chat to send: " + f_chat_id + '\n')
  dec2 = input("Press 'Enter' to continue or input 'cancel' to restart:  ").upper()
  if dec2 == 'CANCEL':
    print("Cancelled")
    time.sleep(2)
    return
  else:
      print("")
  if createFolder(f_path, f_name) == False:
    print("File Not created")
    time.sleep(2)
    return
  else:
    print("")
  
  createLog(f_path + l_name + '.txt')
  #append to list of classes folder - Folders
  folders_list.append(Folders(f_name, l_name, f_path, f_h_decision, f_chat_id))


def checkLog(path, folder, log_name, file):
  print("Lets search " + file)
  print("in log " + path + log_name + '.txt' + " ..")
  open_log = open(path + log_name + '.txt', 'a+')
  with open_log as log:
    log.seek(0)
    lines = log.read().splitlines()
    if file in lines:
      ("File name already exists in the log!")
      open_log.close()
      return True
    else:
      open_log.close()
      return False
    

def cls():
  os.system('cls' if os.name=='nt' else 'clear') 


def createFolder(path, folder):
  if os.path.exists(path+folder) == True:
    print("Nice! " + path+folder + " already exist :D")
    return True
  try:
    os.makedirs(path + folder)
  except OSError:
    print ("Creation of the directory %s failed.. try adding a / before the path" % folder)
    return False
  else:
    print ("Successfully created the directory %s " % folder)
    return True


def createLog(log):
  if os.path.isfile(log) == True:
    print("Log already exist")
  else:
    print("Making log..")
    making_log = open(log,"w+")
    print("Log created")
    making_log.close
    time.sleep(2)


def get_info():
  
  while True:
    cls()
    dec1 = input("Add Folder? (y/n):  ").upper()
    if dec1 == 'Y':
      addFolder()
      continue
    elif dec1 == 'N':
      cls()
      break
    else:
      print("Invalid")
      continue


def renameToMd5(path, file):
  # Get hash
  md5_hash = hashlib.md5()
  a_file = open(path + file, "rb")
  content = a_file.read()
  md5_hash.update(content)
  digest = md5_hash.hexdigest()

  #rename file
  fileName, fileExtension = os.path.splitext(file)
  newMd5Name = digest + fileExtension
  os.rename(path+file, path+digest+fileExtension)
  print(file + " new name is:" + digest + fileExtension + '\n')
  return newMd5Name


def renAllFoldFiles():
  print("Rename all files to md5")
  for folder in folders_list:
    print("\n\nHash decision for this folder - "+ folder.folder_name + ' - :  ' + folder.hashdecision)
    if folder.hashdecision == 'ON':
      pathAndFolder = folder.path + folder.folder_name + '/' #add / 
      print("Renaming files in this folder " + pathAndFolder)
      for file in os.listdir(pathAndFolder): 
        if os.path.isfile(pathAndFolder + file) == True:
          renameToMd5(pathAndFolder, file)



def sendAllToTelegram():
  print("Don't insert archives in this process!")
  print("Wait the monitoring step")
  global bot
  for folder in folders_list:
    print('Searching files in ' + folder.path + folder.folder_name + '/' + ' \n')
    for file in os.listdir(folder.path + folder.folder_name + '/'):
      print("\nLet's check if the " + file + " already exists in the log\n")
      if checkLog(folder.path, folder.folder_name, folder.log_name, file) == False:
        if sendToTelegram(folder.path, folder.folder_name, file, folder.chat_id, tokenBot) == False:
          print("File not send")
        else:
          print("We don't have the file in the log")
          writeInLog(folder.path, folder.log_name, file)
          os.remove(folder.path + folder.folder_name + '/' + file)
          time.sleep(3)


      else:
        print("Not send.. file already exist in log")
      

def sendToTelegram(path, folder, file, chat, token):
  
  fileName, fEx = os.path.splitext(file)
  path_file = path + folder + '/' + file

  if fEx != '.gif':
    doc = open(path_file, 'rb')
    
    try:
      bot.sendDocument(chat, doc, caption=file)
    except telepot.exception.TelegramError as teleerror:
      print(teleerror)
      return False
    else:
      print('file send')

  if fEx == '.gif':
    doc = open(path_file, 'rb')
    
    try:
      bot.sendDocument(chat, doc, caption=file)
    except telepot.exception.TelegramError as teleerror:
      print(teleerror)
      return False
    else:
      print('Gif send')

  elif fEx == '.png' or fEx == '.jpeg' or fEx == '.jpg':
    doc = open(path_file, 'rb')
    
    try:
      bot.sendPhoto(chat, doc, caption=file)
    except telepot.exception.TelegramError as teleerror:
      print(teleerror)
      return False
    else:
      print('file send')

  elif fEx == '.mp4' or fEx == '.webm' or fEx == '.avi' or fEx == '.flv' or fEx == '.wmv ' or fEx == '.mkv':
    doc = open(path_file, 'rb')
    
    try:
      bot.sendVideo(chat, doc, caption=file)
    except telepot.exception.TelegramError as teleerror:
      print(teleerror)
      return False
    else:
      print('file send')


def writeInLog(path, log_name, file):
  log = log_name + '.txt'
  print("Writing the file in " + path + log)
  with open(path + log, "a+") as log:
    log.seek(0)
    lines = log.read().splitlines()
    log.write(file + "\n")
    log.close()
  print("Saved in log")


class Folders:
  def __init__(self, f_name, l_name, f_path, f_h_decision, f_chat_id):
    self.folder_name = f_name
    self.log_name = l_name
    self.path = f_path
    self.hashdecision = f_h_decision
    self.chat_id = f_chat_id


  def finfo(self):
    print("-Folder: " + self.path + self.folder_name)
    print("-Log: " + self.path + self.log_name + '.txt')
    print("-Hash decision: " + self.hashdecision)
    print("-Chat_id: " + self.chat_id)


class MyFileHandler(FileSystemEventHandler):
  def on_created(self, event):
      print(f'event type: {event.event_type}  path : {event.src_path}')
      file = os.path.basename(event.src_path)
      path = os.path.dirname(event.src_path)
        
      print('file: ' + file)   
      print('path: ' + path)
      if os.path.isfile(path + '/' + file) == True:
        if folder.hashdecision == 'ON':
          print("convert " + file + " to md5")
          file = renameToMd5(path + '/', file)
          time.sleep(1)
          print("New name is:" + file)
        else:
          print("Hash decision off")
        print("\nLet's check if the " + file + " already exists in the log\n")
        if checkLog(folder.path, folder.folder_name, folder.log_name, file) == False:
          print("It's a new file!")
          sendToTelegram(folder.path, folder.folder_name, file, folder.chat_id, tokenBot)
        
          print("We don't have the file in the log")
          writeInLog(folder.path, folder.log_name, file)
          os.remove(folder.path + folder.folder_name + '/' + file)
          time.sleep(3)
        else:
          print("Not send.. file already exist in log")
      else:
        print("Event isn't a file...")
      





if __name__ == '__main__' :
  #declaration
  folders_list = []
  paths = []
  observers = []
  event_handler = MyFileHandler()
  observer = Observer()

  """
  Add folder manually
  folders_list.append(Folders(f_name, l_name, f_path, f_h_decision, f_chat_id))  
  
  """
  tokenBot = input("BotToken:  ")
  bot = telepot.Bot(tokenBot)


  get_info()
  for folder in folders_list:
    Folders.finfo(folder)
    print("")
    
  renAllFoldFiles()

  print("\n\nSending existing files to the telegram")
  sendAllToTelegram()

  
  
  for folder in folders_list:
    infolder = folder.path + folder.folder_name
    targetPath = str(infolder).rstrip()
    observer.schedule(event_handler, targetPath)
    observers.append(observer)
  
  for i in observers:
    print(i)
  print("monitoring Folders with watchdog, now you can add more files to folders")
  observer.start()

  

  try:
      while True:
          # poll every second
          time.sleep(1)
  except KeyboardInterrupt:
      for o in observers:
          o.unschedule_all()
          # stop observer if interrupted
          o.stop()
  for o in observers:
      # Wait until the thread terminates before exit
      o.join()





  
