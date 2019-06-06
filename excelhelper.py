#coding=utf-8
import xlwt
import sys
import tool
import time
import os
reload(sys)
sys.setdefaultencoding('utf-8')
class DAO:
      def __init__(self):
          self.cur_row = 0
          self.max_row = 2000
          self.file = ""
          self.table = ""
          
          self.style = xlwt.XFStyle()
          font = xlwt.Font()
          font.name = 'SimSun'
          self.style.font = font
          
          self.tool = tool.Tool()
          self.resultDir = "result\\"
          try:
             os.mkdir(self.resultDir)
          except OSError:
             pass

      def createTable(self):
          self.file = xlwt.Workbook(encoding = 'utf-8')
          self.table = self.file.add_sheet('sheet1')
          

      def insert(self, my_dict):
          if self.cur_row == 0 :
             self.createTable()
             col = 0
             for column_name in my_dict.keys():
                 self.table.write(self.cur_row, col, column_name, self.style)
                 col += 1
             self.cur_row += 1
          col = 0
          for dict_val in my_dict.values():
              self.table.write(self.cur_row,col, dict_val, self.style)
              col +=1
          self.cur_row += 1
          if self.cur_row > self.max_row:
             self.saveTable()

      def saveTable(self):
          if self.cur_row == 0:
             return
          filename = self.resultDir+str(time.time())+".xls"
          self.file.save(filename)
          print self.tool.getCurTime(),u"共保存%d条数据到%s中\r\n" % (self.cur_row-1, filename)
          self.cur_row = 0


if __name__ == "__main__":
   dao = DAO()
   detail = {
              'district' : "北京市本级"
              ,'area' : "0.0" 
              ,'date' : "2013年2月3日"
              ,'price' : "2.0" 
              ,'purpose' : "住宅用地"
              ,'supply' : "划拨"
              ,'location' : "三里屯"
          }
   try:
       for i in range(7):
           dao.insert(detail)
   finally:
   	   dao.saveTable()