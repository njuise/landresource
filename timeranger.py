#coding=utf-8
import time
from datetime import date
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class TimeRanger:
    def __init__(self, indent_days ,terminal_date):
       #print u"time ranger initialized"
        self.seconds_of_day = 24*60*60
        self.initial_Indent = indent_days*self.seconds_of_day #初始的时间跨度(s)
        self.terminal_date = terminal_date
    #
    def get_end_date(self, start_date):
        end_date = self.get_added_time(start_date,self.initial_Indent)
        if self.compare_time(end_date, self.terminal_date)>0:
           end_date = self.terminal_date
        return end_date

    def get_next_start_date(self, previous_end_date):
        start_date = self.get_added_time(previous_end_date,self.seconds_of_day)
        return start_date
    
    def get_added_time(self, previous, indent):
        #previous必须是格式为yyyy-mm-dd的字符串;
        #indent为需要增加的秒数
        previous_second = self.convert_string_to_second(previous)
        added_second = previous_second + indent
        added_date = time.localtime(added_second)
        return self.convert_time_to_string(added_date)

    def convert_string_to_second(self, time_str):
    	arr = time_str.split("-")
        d = date(int(arr[0]),int(arr[1]),int(arr[2]))
        time_tuple = d.timetuple()
        return time.mktime(time_tuple)

    def convert_time_to_string(self,time_stuct):
        return time.strftime( '%Y-%m-%d',time_stuct)

    def reduce_time_range(self, start_date , old_end_date):
        s = self.convert_string_to_second(start_date)
        o = self.convert_string_to_second(old_end_date)

        ne = (s+o)/2
        new_end_date = time.localtime(ne)
        new_end_date_str = self.convert_time_to_string(new_end_date)

        if new_end_date_str == self.convert_time_to_string(time.localtime(o)):
            #若搜索条件已经不可缩小，则将终止日期设置与开始日期相同
           return start_date
        else:
           return new_end_date_str

    def compare_time(self, this_date, that_date):
        t1 = self.convert_string_to_second(this_date)
        t2 = self.convert_string_to_second(that_date)
        return -1 if t1<t2 else (0 if t1==t2 else 1)

if __name__ == "__main__":
	t = TimeRanger(5,"2000-1-4")
	start_date = "2000-1-1"
	end = t.get_end_date(start_date)
	print end
	new_end = t.reduce_time_range(start_date, end)
	print new_end
	nsd = t.get_next_start_date(new_end)
	print nsd
	i = t.compare_time(start_date,start_date)
	print i
	print t.compare_time(start_date,new_end)
	print t.compare_time(new_end,start_date)