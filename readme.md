### 运行说明
进入项目根目录下，执行命令：
scrapy crawl land -a startDate=<起始时间> -a endDate=<结束时间>

startDate,endDate为命令参数，指定爬取的时间段。如：scrapy crawl land -a startDate=2019-1-1 -a endDate=2019-1-2

### 运行结果
采集的数据结果保存在项目根目录下，以时间戳命名

### 关于反爬取
为防止ip被封，可以修改setting.py中的 DOWNLOAD_DELAY， 调整爬取的速度