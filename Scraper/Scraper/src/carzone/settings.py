

''''
# SQL DATABASE SETTING
SQL_DB = 'mysql'
SQL_TABLE = 'david(First)'
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_PASSWD = 'Arnotts08_Cache'

# connect to the MySQL server
try:
    CONN = MySQLdb.connect(host=SQL_HOST,
                         user=SQL_USER,
                         passwd=SQL_PASSWD,
                         db=SQL_DB)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

'''


#Bot Info
BOT_NAME = 'Carzone Bot - David O Regan, 4th year project, DCU, david.oregan7@mail.dcu.ie'
BOT_VERSION = '0.1'

# Moduals
SPIDER_MODULES = ['carzone.spiders']
NEWSPIDER_MODULE = 'carzone.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#Misc faults
DOWNLOAD_DELAY = 2.0


#Pipelines
ITEM_PIPELINES = ['carzone.pipelines.CarzonePipeline3',
                  'carzone.pipelines.MySQLStorePipeline',
                 ]

#MYSQL
#MYSQL_HOST = '127.0.0.1:8889'
#MYSQL_DBNAME = 'Carzone'
#MYSQL_USER = 'root'
#MYSQL_PASSWD = 'root'







# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'src (+http://www.yourdomain.com)'
