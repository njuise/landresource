# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import timeranger
import urlmanager
import mysqlhelper
import redirectstd
import excelhelper
import time
import tool
import re
import gc
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class LandCrawler:

    def __init__(self, url_manager, dao, time_ranger):
        # driver initialization
        # cap = webdriver.DesiredCapabilities.PHANTOMJS
        # cap["phantomjs.page.settings.loadImages"] = False
        # self.driver = webdriver.PhantomJS(executable_path=r'D:\tools\phantomjs-2.1.1-windows\bin\phantomjs.exe',desired_capabilities = cap)
        # option = webdriver.ChromeOptions()
        # option.add_argument('--user-data-dir=C:\Users\lenovo\AppData\Local\Google\Chrome\User Data')
        # chrome_options=option
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        self.wait_time = 5
        self.driver.implicitly_wait(self.wait_time)
        self.wait = WebDriverWait(self.driver, self.wait_time)
        # site initialization
        self.site_url = "http://www.landchina.com/"
        self.main_url = "http://www.landchina.com/default.aspx?tabid=263&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&p="

        self.cur_page_num = 1
        self.total_page_num = 0
        self.total_item = 0
        self.cur_start_date = ""
        self.cur_end_date = ""
        self.item_per_page = 30
        self.max_page = 200

        # self.get_main_page()
        # reference initialization
        self.time_ranger = time_ranger
        self.url_manager = url_manager
        self.dao = dao

        self.tool = tool.Tool()

    def get_main_page(self):
        driver = self.driver
        driver.get(self.main_url)

    def get_next_page(self):
        if self.cur_page_num + 1 > self.total_page_num:
            print self.tool.getCurTime(), u"达到该搜索条件下最大页数\r\n"
            return False
        nextPageElem = None
        try:
            # nextPageElem = driver.find_element_by_link_text(u"下页")
            nextPageElem = self.wait.until \
                (EC.element_to_be_clickable((By.LINK_TEXT, u'下页')))
        except TimeoutException:
            print >> sys.stderr, self.output_cur_page(), u"寻找下一页超时\r\n"
        except NoSuchElementException:
            print >> sys.stderr, self.output_cur_page(), u"无下一页按钮\r\n"

        if nextPageElem is None:  # 若没有“下页”或“下页”不可点击，进行下一时间段的搜索
            print self.tool.getCurTime(), u"当前搜索条件下已经达到尾页\r\n"
            return False
        if nextPageElem.get_attribute("disabled") is not None:
            print self.tool.getCurTime(), u"当前搜索条件下已经达到尾页\r\n"
            return False

        nextPageElem.click()
        # nextPageElem = driver.find_element_by_link_text(u"下页")
        self.cur_page_num += 1
        self.output_cur_page()
        return True

    def get_appropriate_page(self, start_date, start_page):
        driver = self.driver
        end_date = self.time_ranger.get_end_date(start_date)
        page_elem = ""
        while True:
            # 以新的条件加载主页
            self.get_page(start_date, end_date)
            page_info = ""
            total_page = 0
            try:
                page_elem = driver.find_element_by_xpath \
                    (u"//table[@id='Table1']//td[@class='pager'][starts-with(text(),'共')]")
                page_info = page_elem.text
            except NoSuchElementException:
                total_page = 1

            total_pattern = re.compile(r'\d+')
            match = re.search(total_pattern, page_info)

            if match:
                total_page = int(match.group())
            print self.tool.getCurTime(), end_date, u"为终止日期，共有", total_page, u"页数据\r\n"

            self.total_page_num = total_page

            if total_page <= self.max_page:
                if int(start_page) > int(total_page):
                    start_page = total_page
                break

            if self.time_ranger.compare_time(start_date, end_date) == 0:
                print self.tool.getCurTime(), u"搜索条件已经无法缩小\r\n"
                break
            print self.tool.getCurTime(), u"超过了限定页数，正在缩小搜索条件\r\n"
            end_date = self.time_ranger \
                .reduce_time_range(start_date, end_date)
        if page_elem is not None and page_elem != "":
            try:
                page_input = page_elem.find_element_by_xpath("..//input[last()-1]")
                go_input = page_elem.find_element_by_xpath("..//input[last()]")

                page_input.clear()

                page_input.send_keys(start_page)

                go_input.click()
                self.cur_page_num = int(start_page)
            except NoSuchElementException:
                print >> sys.stderr, self.tool.getCurTime(), u"无法跳转至第", start_page, u"页\r\n"

    # 获得下一个搜索条件的主页
    def get_new_main_page(self, cur_ed):
        self.get_main_page()
        self.cur_start_date = self.time_ranger \
            .get_next_start_date(cur_ed)
        self.get_appropriate_page(self.cur_start_date, 1)

    def get_page(self, start_date, end_date):
        driver = self.driver
        check_box = driver.find_element_by_id(u"TAB_QueryConditionItem270")
        start_date_input = driver.find_element_by_id(u"TAB_queryDateItem_270_1")
        end_date_input = driver.find_element_by_id(u"TAB_queryDateItem_270_2")
        search_button = driver.find_element_by_id(u"TAB_QueryButtonControl")

        if not check_box.is_selected():
            check_box.click()
        start_date_input.clear()
        end_date_input.clear()
        start_date_input.send_keys(start_date)
        end_date_input.send_keys(end_date)
        search_button.click()

        self.cur_page_num = 1
        self.cur_start_date = start_date
        self.cur_end_date = end_date
        self.output_cur_page()

    # 分析查询列表得到的表格，得到url,并进行管理
    def parse_main_table(self):
        driver = self.driver
        elems_with_url = list()
        try:
            table = driver.find_element_by_id(u"TAB_contentTable")
            elems_with_url = table.find_elements_by_xpath \
                (".//a[starts-with(@href,'default.aspx')]")
        except NoSuchElementException:
            return False

        if isinstance(elems_with_url, list) and len(elems_with_url) == 0:
            return False
        # print u"本页共",len(elems_with_url),u"个条目"
        for elem in elems_with_url:
            url = ""
            url = elem.get_attribute("href")
            if url is None or url == "":
                continue
            district = elem.find_element_by_xpath("../../td[2]").text
            # 检查地区名称是否完整，如果不完整则从span中提取title属性中的完整名称
            if district.find('...') >= 0:
                try:
                    district = elem.find_element_by_xpath("../../td[2]/span").get_attribute('title')
                except NoSuchElementException as e:
                    district = elem.find_element_by_xpath("../../td[2]").text
            self.url_manager.add_url((district, url))

        return True

    # 分析当前掌握url的土地的具体信息
    def save_detail_pages(self, length):
        driver = self.driver
        print self.tool.getCurTime(), u"即将处理共", length, u"条土地信息\r\n"
        failed_tuples = []
        for index in range(length):
            cur_tuple = self.url_manager.get_url()
            cur_url = cur_tuple[1]
            try:
                # 注意此时会在当前标签页加载
                driver.get(cur_url)
                detail = self.parse_detail_page()
                if detail is not None:
                    detail['district'] = cur_tuple[0]
                    self.dao.insert(detail)

            # except NoSuchElementException:
            #  failed_tuples.append(cur_tuple)
            # except TimeoutException:
            #  failed_tuples.append(cur_tuple)
            # except Error, er:
            #  print >>sys.stderr, self.tool.getCurTime(),er
            #  failed_tuples.append(cur_tuple)
            except Exception, e:
                print >> sys.stderr, self.tool.getCurTime(), e, "\r\n"
                failed_tuples.append(cur_tuple)
            # self.driver.delete_all_cookies()
            # print self.driver.get_cookies()
            print self.tool.getCurTime(), u"处理进度：", index + 1, u"/", length, "\r\n"
        for url in failed_tuples:
            self.url_manager.add_url(url)

    # 分析当前页的信息
    def parse_detail_page(self):
        driver = self.driver
        # district = driver.find_element_by_id\
        # ("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl").text
        area = driver.find_element_by_id \
            ("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl").text
        date = driver.find_element_by_id \
            ("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl").text
        price = driver.find_element_by_id \
            ("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl").text

        purpose = driver.find_element_by_id \
            ("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl").text
        supply = driver.find_element_by_id \
            ("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl").text
        location = driver.find_element_by_id \
            ("mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl").text
        # 'district' : district,
        detail = {

            'area': "0.0" if area is None or area == "" else area
            , 'date': date
            , 'price': "0.0" if price is None or price == "" else price
            , 'purpose': purpose
            , 'supply': supply
            , 'location': location
        }
        return detail

    def get_end_date(self):
        return self.cur_end_date

    def output_cur_page(self):
        print self.tool.getCurTime(), u"当前位于", self.cur_start_date, u"到", self.cur_end_date, \
            u"的第", self.cur_page_num, u"页\r\n"

    def back_ward(self):
        self.driver.back()

    def close_cur_tab(self):
        self.driver.close()

    def exit(self):
        self.driver.quit()


if __name__ == "__main__":

    # landCrawler.close_cur_tab()
    # landCrawler.get_main_page()
    start_date = raw_input(u"请输入开始日期yyyy-mm-dd,以回车结束：".encode("utf-8"))
    terminal_date = raw_input(u"请输入结束日期yyyy-mm-dd,以回车结束：".encode("utf-8"))
    indent_days = 5
    # try:
    #  indent_days = int(raw_input(u"请输入初始时间跨度（天）,以回车结束;直接敲回车将使用默认时间间隔：".encode("utf-8")))
    # except ValueError:
    #  pass

    # ip = raw_input(u"请输入数据库ip,以回车结束;直接敲回车将使用本地数据库：".encode("utf-8"))
    # if (not isinstance(ip, str)) or ip == "":
    #  ip = "localhost"

    um = urlmanager.UrlManager()
    # mysqlhelper.DAO(ip)
    d = excelhelper.DAO()
    tr = timeranger.TimeRanger(indent_days, terminal_date)
    # 将标准输出、错误重定向至文件
    redirect = redirectstd.RedirectStd()
    starttime = str(time.time())

    redirect.outToFile("out" + starttime + ".txt")
    redirect.errToFile("err" + starttime + ".txt")

    landCrawler = LandCrawler(um, d, tr)
    tl = tool.Tool()

    try:
        landCrawler.get_main_page()

        # start_p = raw_input(u"请输入开始页码（若不确定则输入1）,以回车结束：".encode("utf-8"))
        landCrawler.get_appropriate_page(start_date, "1")
        landCrawler.parse_main_table()

        items_saved_per_loop = 300

        while True:
            while landCrawler.get_next_page():
                landCrawler.parse_main_table()
                gc.collect()

            ed = landCrawler.get_end_date()
            while um.has_url():
                length_to_save = items_saved_per_loop if \
                    um.get_length() > items_saved_per_loop else um.get_length()
                landCrawler.save_detail_pages(length_to_save)

                # 释放内存
                landCrawler.exit()
                del landCrawler
                gc.collect()
                print tl.getCurTime(), u"重开浏览器以释放内存\r\n"
                landCrawler = LandCrawler(um, d, tr)
            print tl.getCurTime(), u"保存完毕\r\n"

            if tr.compare_time(ed, terminal_date) >= 0:
                print tl.getCurTime(), u"查询已超过预定结束的日期,来到：", ed, "\r\n"
                landCrawler.exit()
                break
            landCrawler.get_new_main_page(ed)
            landCrawler.parse_main_table()
    except Exception, ex:
        print >> sys.stderr, tl.getCurTime(), ex, "\r\n"
    finally:
        d.saveTable()
        redirect.restore()
        print u"数据获取完毕,结果以excel格式输出，过程日志可参考err", starttime, u".txt和out", starttime, u".txt文件"
        raw_input(u"输入回车以结束".encode("utf-8"))
