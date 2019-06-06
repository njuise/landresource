# coding:utf-8
import MySQLdb
import tool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class DAO:
      def __init__(self,ip):    
          self.tool = tool.Tool()
          try:
              self.db = MySQLdb.connect(ip,'client','123456','landmarket')
              self.cur = self.db.cursor()
          except MySQLdb.Error,e:
              print self.tool.getCurTime(),u"连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])

      #插入数据
      def insertData(self, table, my_dict):
          try:
              self.db.set_character_set('utf8')
              cols = ', '.join(my_dict.keys())
              values = '"," '.join(my_dict.values())
              sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
              try:
                  result = self.cur.execute(sql)
                  insert_id = self.db.insert_id()
                  self.db.commit()
                  #判断是否执行成功
                  #if result:
                     #print "ID of inserted record is ", int(insert_id)
                  #   return int(insert_id)
                  #else:
                  #   return 0
              except MySQLdb.Error,e:
                 #发生错误时回滚
                  self.db.rollback()
                 #主键唯一，无法插入
                  if "key 'PRIMARY'" in e.args[1]:
                     print self.tool.getCurTime(),u"数据已存在，未插入数据"
                  else:
                     print self.tool.getCurTime(),u"插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
          except MySQLdb.Error,e:
              print self.tool.getCurTime(),u"数据库错误，原因%d: %s" % (e.args[0], e.args[1])

      def insertDatas(self, array_of_dict):
          if array_of_dict is None:
             return 
          for dict in array_of_dict:
              if dict is None:
                 return
              self.insertData("land",dict)

      def insert(self, dict):
          self.insertData("land", dict)
if __name__ == "__main__":
   dao = DAO()