import os, time, hashlib


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
  os.rename(path+file, path+digest+fileExtension)
  print(file + " foi renomeado para:" + digest + fileExtension + '\n')


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


def sendToLog(path, log, file):
  print("")


def sendAllToTelegram():
  for folder in folders_list:
    for file in os.listdir(folder.path + folder.folder_name + '/'):
      print("let's check if the " + file + " already exists in the log\n")
      open_log = open(folder.path + folder.log_name + '.txt', 'r')
      with open_log as log:
        for line in log:
          if file in line:
            print("The file name already exists in the log\n\n")
            
          else:
            print("file not found in the log")
            while True:
              if sendToTelegram(folder.path, folder.folder_name, file, folder.chat_id, tokenBot) == True:
                print("File sent\n\n")
                sendToLog(folder.path, folder.log_name,  file)
                break
              else:
                print("Error! File not sent. Retrying...\n")
                continue
        open_log.close()

      


def sendToTelegram(path, folder, file, chat_id, token):
  path_file = path + folder + '/' + file
  print('Finjindo q enviado')
  return True

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


if __name__ == '__main__' :
  folders_list = []
  tokenBot = input("BotToken:  ")

  get_info()
  for folder in folders_list:
    Folders.finfo(folder)
    print("")
    
  renAllFoldFiles()

  print("\n\nSending existing files to the telegram")
  sendAllToTelegram()



  
