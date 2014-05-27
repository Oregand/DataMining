# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import MySQLdb




class CarzonePipeline3(object):
    def __init__(self):
        self.myCSV = csv.writer(open('merc_e.csv', 'wb'))
        self.myCSV.writerow(['title', 'link', 'price', 'carYear', 'location', 'mileage', 'engineSize', 'engineType', 'Transmission', 'Colour', 'Owners', 'NCT',  'BodyType'])

    def process_item(self, item, spider):
        self.myCSV.writerow([item['title'][0:100].encode('utf-8'),
                             item['link'][0:100].encode('utf-8'),
                             item['price'][1:7].encode('utf-8'),
                             item['carYear'][0:5].encode('utf-8'),
                             item['location'][0:9].encode('utf-8'),
                             item['mileage'][0:20].encode('utf-8'),
                             item['engine'][0:3].encode('utf-8'),
                             item['engine'][13:20].encode('utf-8'),
                             item['Transmission'][0:20].encode('utf-8'),
                             item['Colour'][0:50].encode('utf-8'),
                             item['Owners'][0:5].encode('utf-8'),
                             item['NCT'][0:20].encode('utf-8'),
                             item['BodyType'][0:20].encode('utf-8')])

        return item


class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='root', db='carzone',port=8889, host='127.0.0.1',
                                    charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT IGNORE INTO merc_e (title, link, price, carYear, location, mileage, engineSize, engineType, Transmission, Colour, Owners, NCT, BodyType)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                (item['title'][0:100].encode('utf-8'),
                                 item['link'][0:100].encode('utf-8'),
                                 item['price'][1:7].encode('utf-8'),
                                 item['carYear'][0:5].encode('utf-8'),
                                 item['location'][0:9].encode('utf-8'),
                                 item['mileage'][0:20].encode('utf-8'),
                                 item['engine'][0:3].encode('utf-8'),
                                 item['engine'][13:20].encode('utf-8'),
                                 item['Transmission'][0:20].encode('utf-8'),
                                 item['Colour'][0:50].encode('utf-8'),
                                 item['Owners'][0:5].encode('utf-8'),
                                 item['NCT'][0:20].encode('utf-8'),
                                 item['BodyType'][0:20].encode('utf-8')))

            self.conn.commit()

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item

