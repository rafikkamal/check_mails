import os
import math
import validate_email
from validate_email import validate_email
import time

#filename="one_lakh.txt"
#filename="two_lakh.txt"
filename="five_lakh.txt"
#filename="ten_lakh.txt"

# valid_emails_filename="valid_emails_list.txt"
# invalid_emails_filename="invalid_emails_list.txt"

tmp_valid_emails_filename="tmp_valid_emails.txt"
tmp_invalid_emails_filename="tmp_invalid_emails.txt"

log_filename="log_file.txt"

total_lines=0
total_iterations=0
threshold=10000

iterator_end_head=0

# valid_emails_file=open(valid_emails_filename, 'w+')
# invalid_emails_file=open(invalid_emails_filename, 'w+')
tmp_valid_emails_file=open(tmp_valid_emails_filename, 'w+')
tmp_invalid_emails_file=open(tmp_invalid_emails_filename, 'w+')
log_file=open(log_filename, 'w+')


# Determines whether to write log or not
debug_enabled=1

# Valid Emails Counter
valid_emails_counter=0


def getFilename():
   global filename
   return filename


def setFilename(newFilename):
   if(len(newFilename)>0):
      global filename
      filename = newFilename


def writeLog(message, type="debug"):
   global debug_enabled
   if debug_enabled:
      global log_file
      if type=="error":
         message = "\n!!! Error \n"+message
      log_message = message.rstrip()
      log_file.write(log_message+"\n\n")


def getTotalLines():
   global filename
   global total_lines
   cmd="wc -l "+filename+" | cut -f1 -d' '"
   total_lines=int(os.popen(cmd).read())


def getTotalIteration():
   global total_iterations
   global total_lines
   global threshold
   getTotalLines()
   total_iterations = math.ceil(total_lines/threshold)


def emailStructureCheck(filename):
   writeLog("Checking emails under file "+filename+"\n")
   print("Checking emails under file => {}".format(filename))
   res = os.popen("wc -l "+filename).read()
   print("Result : {}".format(res))
   with open(filename, "r", buffering=2000000) as f:
      try:
         global tmp_valid_emails_file
         global tmp_invalid_emails_file
         global valid_emails_counter
         for line in f:
            if validate_email(line):
               valid_emails_counter+=1
               #valid_emails_file.write(line)
               tmp_valid_emails_file.write(line)
            else:
               writeLog("$$$ Invalid email found and writing in invalid.txt file => "+str(line))
               tmp_invalid_emails_file.write(line)
      except FileNotFoundError:
         print("Error!!! File not found\n\n")
      except NameError:
         print("Error!!! NameError\n\n")
      except:
         writeLog('Unable to process '+filename, "error")
         print('ERROR!!!\nUnable to process {}\n\nls'.format(filename))
   f.close()
   time.sleep(0.2)


def createTemporaryFile(index):
   global iterator_end_head
   global threshold
   global filename
   print("Filename : "+filename)
   tmp_file="tmp_validity_"+str(index)+".txt"
   cmd="head -n "+str(iterator_end_head)+" "+filename+" | tail -n "+str(threshold)+" > "+tmp_file+"; "
   #cmd+="chmod -R 777 "+tmp_file+"; "
   print("CMD : "+cmd)
   writeLog("Generate tmp file => "+cmd)
   os.system(cmd)
   time.sleep(0.005)
   return tmp_file


def deleteFile(filename):
   cmd="rm "+filename
   os.system(cmd)


def clearFile(filename):
   cmd="echo -n '' > "+filename
   os.system(cmd)


def checkProcessedFilesStatus():
   cmd="wc -l "+tmp_valid_emails_filename+"; "
   cmd+="wc -l "+tmp_invalid_emails_filename+"; "
   result=os.popen(cmd).read()
   print("\n------------------------------------------")
   print("Status Update")
   print("cmd : {}".format(cmd))
   print("{}".format(result))
   print("------------------------------------------")


def closeAllFiles():
#    valid_emails_file.close()
#    invalid_emails_file.close()
   log_file.close()
   tmp_valid_emails_file.close()
   tmp_invalid_emails_file.close()


def processEmails():
#    print("{}".format(getFilename()))
#    exit("testing with checkStructurePattern")

   global threshold
   global filename
   global total_iterations
   global iterator_end_head

   print("{}".format(filename))

   # Get total iterations number to be used in for loop
   getTotalIteration()
   writeLog("Total iteration for "+filename+" : "+str(total_iterations))
   writeLog("Working with file: "+filename)
   for i in range(1, total_iterations+1):
      writeLog("Working with iteration no# "+str(i))
      if i > total_lines:
         # Close all the open files
         closeAllFiles()
         break

      iterator_end_head = (i)*threshold
      if i==total_iterations:
         threshold = total_lines-(i-1)*threshold

      # make a tmp file with the mentioned range
      tmp_file = createTemporaryFile(i)

      print("Working with iteration no#{}".format(i))
      writeLog("Iteration no# "+str(i)+", working with : "+tmp_file)

      # Check Email Validity
      emailStructureCheck(tmp_file)
      writeLog("Completed iteration no# "+str(i))


def getTmpTotalValidEmailsCount():
   global valid_emails_counter
   return valid_emails_counter


def main():
   startTime = time.ctime(time.time())
   processEmails()
   endTime = time.ctime(time.time())
   print("Start Time : {}".format(startTime))
   print("End Time : {}".format(endTime))
   checkProcessedFilesStatus()
   os.system('find ./ -name "tmp_validity_*.txt" -exec rm \{\} \;')
   #exit()


if __name__ == "__main__":
   main()