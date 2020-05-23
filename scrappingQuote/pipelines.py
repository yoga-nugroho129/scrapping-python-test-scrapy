# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 8) Save to the sqlite3 database
# 8.1) Importting the sqlite3 DB
import sqlite3

# 7.3) the flow are :
    # a) whenever we scrap data using 'quoteSpider.py' using yield in for loop
    # b) it will go to the 'pipepline.py' & goes to the 'process_item' as 'item' params
class ScrappingquotePipeline:
    def __init__(self):
        # 8.4) call (8.2) & (8.3) inside init method
        self.createConnection()
        self.createTable()

    # 8.2) create connection
    def createConnection(self):
        self.conn = sqlite3.connect("myquotes.db") # create batabase with param of db name
        self.curr = self.conn.cursor() # create currsor using connection   
    
    # 8.3) create table inside database
    def createTable(self):
        # handler for condition if the table already exist so it will drop it
        self.curr.execute("""DROP TABLE IF EXISTS quotesTable""")
        self.curr.execute("""create table quotesTable(
            quote "text",
            author "text",
            tags "text"
        )""")

    def process_item(self, item, spider): # 'item' is containing the yield from our spider
        # # c) lets try the flow usign code down bellow
        # print('Pipelines :' + item['quote'][0]) # on every loop it will has 'Pipelines :'
        
        # 8.6) call function to store the data inside the table of database
        self.storeDb(item)
        return item

    # 8.5) create function to store the data inside the table of database
    def storeDb(self, item):
        self.curr.execute("""insert into quotesTable values (?, ?, ?)""", (
            item['quote'][0],
            item['author'][0],
            item['tags'][0]
        ))
        self.conn.commit()