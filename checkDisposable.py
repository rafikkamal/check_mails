import hashlib
import math
import os
import time

start_time = time.ctime(time.time())

output_file_path="tmp_non_disposable_emails.txt"
output_disposable_file_path="tmp_disposable_emails.txt"

filename="ten_lakh.txt"
total_lines=0
iterations=0
threshold=10000

disposable_lines_hash=set()

output_file=open(output_file_path, "w+")
output_disposable_file=open(output_disposable_file_path, "w+")

def getFilename():
   global filename
   return filename


def setFilename(newFilename):
   if(len(newFilename)>0):
      global filename
      filename = newFilename


def getDisposableDomains():
   try:
      disposable_domains_list = "disposable_domains.txt"
      global disposable_lines_hash
      with open(disposable_domains_list, 'r') as f:
         for line in f:
            #disposable_lines_hash.add(line.rstrip())
            disposable_lines_hash.add(hashlib.md5(line.rstrip().encode("utf-8")).hexdigest())
      #disposable_lines_hash = set(lines)
   except FileNotFoundError:
      print("File \"{}\" not found.".format(disposable_domains_list))
      exit("Exiting Code")


def getTotalLines(filename):
   global total_lines
   cmd="wc -l "+filename+" | cut -f1 -d' '"
   total_lines=int(os.popen(cmd).read())


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
   tmp_file="temp_disposable_"+str(index)+".txt"
   cmd="head -n "+str(head)+" "+filename+" | tail -n "+str(tail)+" > "+tmp_file
   os.system(cmd)
   return tmp_file


def removeTmpFile(filename):
   cmd="rm "+filename
   os.system(cmd)
   print("Removed {}".format(filename))


def getEmailDomain(email):
   email_split = email.rstrip().split("@")
   if len(email_split) != 2:
      return ""
   return email_split[1]


disposable_counter=0
def checkDisposable(input_file_path):
   print("Checking disposable emails in {}".format(input_file_path))
   global disposable_counter
   global disposable_lines_hash
   for line in open(input_file_path, "r", buffering=2000000):
      domain = getEmailDomain(line)
      if len(domain) != 0:
         hashValue = hashlib.md5(domain.encode("utf-8")).hexdigest()
         if hashValue not in disposable_lines_hash:
            #print(line+"is not disposable")
            output_file.write(line)
            #disposable_lines_hash.add(hashValue)
         else:
#             print(line+" is disposable")
            disposable_counter+=1
            output_disposable_file.write(line)
      else:
         #print(line+" is disposable")
         disposable_counter+=1
         output_disposable_file.write(line)


def main():
   global filename
   global threshold
   global iterations
   global total_lines

   getTotalLines(filename)
   getTotalIterations()
   getDisposableDomains()

   print("\n----------------------------------")
   print("Checking Disposable Emails")
   print("----------------------------------")
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
      checkDisposable(input_file)
      time.sleep(0.1)
      removeTmpFile(input_file)
      #exit()


   print("\n----------------------------------")
   global disposable_counter
   print("Total Disposable Emails Found : {}".format(disposable_counter))

   output_file.close()
   output_disposable_file.close()

   print("\n------------------------------")
   print("Started At : {}".format(start_time))
   print("Ended At : {}".format(time.ctime(time.time())))