#coding=utf-8
import os
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
class RedirectStd:  
    def __init__(self):
        #self.content = ''
        self.savedStdout = sys.stdout
        self.fileObj= None
        
        self.savedStderr = sys.stderr
        self.errFileObj = None

        self.outDir = "out\\"
        try:
            os.mkdir(self.outDir)
        except OSError:
            pass

    #外部的print语句将执行本write()方法，并由当前sys.stdout输出
    #def write(self, outStr):
        #self.content.append(outStr)
    #    self.content += outStr

    def outToCons(self):  #标准输出重定向至控制台
        sys.stdout = self.savedStdout #sys.__stdout__

    def outToFile(self, file='out.txt'):  #标准输出重定向至文件
        file = self.outDir+file
        self.fileObj = codecs.open(file, 'a+', 'utf-8') #改为行缓冲
        sys.stdout = self.fileObj
       

    def errToCons(self):  #标准错误重定向至控制台
        sys.stderr = self.savedStderr #sys.__stderr__

    def errToFile(self, file='err.txt'):  #标准错误重定向至文件
        file = self.outDir+file
        self.errFileObj = codecs.open(file, 'a+', 'utf-8') #改为行缓冲
        sys.stderr = self.errFileObj
        

    def restore(self):
        #self.content = ''
        if self.fileObj is not None and self.fileObj.closed != True:
            self.fileObj.close()
        if self.errFileObj is not None and self.errFileObj.closed != True:
            self.errFileObj.close()
        sys.stdout = self.savedStdout #sys.__stdout__
        sys.stderr = self.savedStderr
if __name__ == '__main__':
    redirect = RedirectStd()
    redirect.outToFile()
    print u'我的天\r\n'
    redirect.errToFile()
    raise Exception(u"我的天哪")
    redirect.restore()
    
