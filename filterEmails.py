import os
import time

import checkStructurePattern
import checkDuplicate
import checkDisposable


class MyClass:
   originalFilename=""
   totalTmpValidEmailsCount=0

   def __init__(self, filename):
      self.filename=filename
      global originalFilename
      originalFilename=filename


   def setOriginalFilename(self, filename):
      global originalFilename
      originalFilename=filename


   def getOriginalFilename(self):
      global originalFilename
      return originalFilename


   def setNextFileToBeProcessed(self, filename):
      self.filename = filename


   def getNextFileToBeProcessed(self):
      return self.filename


   def generateReport(filename):
      return


   def mergeToFinalResultFile(self, srcFile, destFile):
      cmd="cat "+srcFile+" >> "+destFile
      os.system(cmd)


   def removeTmpFiles(self, filename):
      cmd="rm "+filename
      os.system(cmd)


   def cleanInvalidEmails(self):
      print("cleaning started")
      checkStructurePattern.setFilename(self.getNextFileToBeProcessed())
      checkStructurePattern.main()
      global totalTmpValidEmailsCount
      totalTmpValidEmailsCount = checkStructurePattern.getTmpTotalValidEmailsCount()
      print(totalTmpValidEmailsCount)
      print("cleaning done, files generated")


   def cleanDuplicateEmails(self):
      print("2nd cleaning started")
      checkDuplicate.setFilename(self.getNextFileToBeProcessed())
      global totalTmpValidEmailsCount
      checkDuplicate.setTotalLinesExternal(totalTmpValidEmailsCount)
      checkDuplicate.main()
      print("2nd cleaning done, files generated")


   def checkDisposableEmails(self):
      print("3rd cleaning started")
      checkDisposable.setFilename(self.getNextFileToBeProcessed())
      checkDisposable.main()
      print("3rd cleaning done, files generated")


   def startCleaning(self):
      #self.cleanInvalidEmails(self.getOriginalFilename())
      finalStartTime = time.ctime(time.time())
      self.setNextFileToBeProcessed(self.getOriginalFilename())
      self.cleanInvalidEmails()
      time.sleep(2)
      self.setNextFileToBeProcessed("tmp_valid_emails.txt")
      self.cleanDuplicateEmails()
      time.sleep(2)
      self.setNextFileToBeProcessed("tmp_non_duplicate_emails.txt")
      self.checkDisposableEmails()
      self.setNextFileToBeProcessed("tmp_non_disposable_emails.txt")



      # Generate Report For Later Purpose
      #generateReport(self.originalFilename)

      # Save the temporary non disposable emails in "valid_emails.txt"
      self.mergeToFinalResultFile("tmp_non_disposable_emails.txt", "valid_emails.txt")

      # Save the temporary invalid emails in "invalid_emails.txt"
      self.mergeToFinalResultFile("tmp_invalid_emails.txt", "invalid_emails.txt")
      # Save the temporary temporary disposable emails in "disposable_emails.txt"
      self.mergeToFinalResultFile("tmp_disposable_emails.txt", "disposable_emails.txt")
      # Save the temporary duplicate emails in "duplicate_emails.txt"
      self.mergeToFinalResultFile("tmp_duplicate_emails.txt", "duplicate_emails.txt")

      # Remove the temporary files
      self.removeTmpFiles("tmp_valid_emails.txt")
      self.removeTmpFiles("tmp_non_disposable_emails.txt")
      self.removeTmpFiles("tmp_non_duplicate_emails.txt")
      self.removeTmpFiles("tmp_invalid_emails.txt")
      self.removeTmpFiles("tmp_disposable_emails.txt")
      self.removeTmpFiles("tmp_duplicate_emails.txt")
      #self.removeTmpFiles(self.originalFilename)

      finalEndTime = time.ctime(time.time())

      print("\nFinal Time Calculation")
      print("Start Time : "+finalStartTime)
      print("End Time : "+finalEndTime)
      exit("done")

      return self.filename


filename="one_lakh.txt"
#filename="two_lakh.txt"
p1=MyClass(filename)
print(p1.getOriginalFilename())
p1.setOriginalFilename(filename)
print(p1.getOriginalFilename())
p1.startCleaning()