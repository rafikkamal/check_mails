
import hashlib
import os
import math
import time

start_time = time.ctime(time.time())

output_file_path="tmp_non_duplicate_emails.txt"
#output_duplicate_file_path="output_duplicate__one_lakh.txt"
output_duplicate_file_path="tmp_duplicate_emails.txt"

#filename="ten_lakh.txt"
filename=""
total_lines=0
threshold=10000
iterations=0
#input_file_path="one_lakh.txt"

completed_lines_hash=set()

output_file=open(output_file_path, "w+")
output_duplicate_file=open(output_duplicate_file_path, "w+")

def getFilename():
   global filename
   return filename


def setFilename(newFilename):
   if(len(newFilename)>0):
      global filename
      filename = newFilename


def setTotalLinesExternal(lines):
   global total_lines
   total_lines = lines


def getTotalLines(filename):
   global total_lines
   #cmd="wc -l "+filename+" | cut -f1 -d' '"
   #cmd="awk 'END{print NR}' "+filename
   cmd="tail -n 1 "+filename
   last_email=os.popen(cmd).read()
   cmd="grep -n "+last_email.rstrip()+" "+filename+" | cut -f1 -d':'"
   total_lines=int(os.popen(cmd).read())
   print("Total lines : "+str(total_lines))


def getTotalIterations():
   global total_lines
   global iterations
   global threshold
   if total_lines > 0:
      iterations = math.ceil(total_lines/threshold)
   else:
      iterations = 0


def createTmpFile(index, head, tail):
   global filename
   tmp_file="temp_"+str(index)+".txt"
   cmd="head -n "+str(head)+" "+filename+" | tail -n "+str(tail)+" > "+tmp_file+"; "
   os.system(cmd)
   print("\n(2) CMD => \n"+cmd+"\n")
   return tmp_file


def removeTmpFile(filename):
   cmd="rm "+filename
   os.system(cmd)
   print("Removed {}".format(filename))

testEmailCheckCounter=0
duplicate_counter=0
def checkDuplicate(input_file_path):
   print("Checking duplicate emails in {}".format(input_file_path))
   global duplicate_counter
   global completed_lines_hash
   global testEmailCheckCounter
   try:
      for line in open(input_file_path, "r", buffering=2000000):
         testEmailCheckCounter+=1
         hashValue = hashlib.md5(line.rstrip().encode("utf-8")).hexdigest()
         if hashValue not in completed_lines_hash:
            output_file.write(line)
            completed_lines_hash.add(hashValue)
         else:
            duplicate_counter+=1
            output_duplicate_file.write(line)
      print("\n#Total Emails Checked : "+str(testEmailCheckCounter))
      testEmailCheckCounter=0
   except:
      print("Error!!! Something went wrong while working with file")


def processEmails():
   global filename
   global iterations

   global total_lines
#    print("Inside checkDuplicate.py")
#    print("Filename : {}".format(filename))
#    exit()
   print("Working Filename : "+filename)

   #getTotalLines(filename)

   print("Total lines in file for duplicate emails checking : "+str(total_lines))
   getTotalIterations()
   for i in range(1, iterations+1):
      print("\n# Iteration no #{}".format(i))
      if i > iterations:
         break
      head=i*threshold
      if i==iterations:
         tail=total_lines-((i-1)*threshold)
      else:
         tail=threshold
      print("Head : {}".format(head))
      print("Tail : {}".format(tail))
      input_file = createTmpFile(i, head, tail)
      checkDuplicate(input_file)
      time.sleep(0.2)
      removeTmpFile(input_file)

   print("Total Duplicate Emails Found : {}".format(duplicate_counter))

   output_file.close()
   output_duplicate_file.close()

   print("\n------------------------------")
   print("Started At : {}".format(start_time))
   print("Ended At : {}".format(time.ctime(time.time())))


def main():
   startTime = time.ctime(time.time())
   processEmails()
   endTime = time.ctime(time.time())
   print("Start Time : {}".format(startTime))
   print("End Time : {}".format(endTime))