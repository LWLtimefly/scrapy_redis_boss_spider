# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JobSpiderPipeline(object):
    def __init__(self):
        self.db=pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='root',
                                db='final_boss_job',
                                charset='utf8')
        self.cursor=self.db.cursor()

    def process_item(self, item, spider):
        table_name='job_msg'
        if not self.existe_table(table_name):
            #   item['job_type'],item['job_time'],item['job_name'],item['job_money'],item['job_meanMoney'],
            #   item['job_address'],item['job_jy'],item['job_xl'],item['job_hrName'],item['job_hrleader'],
            #   item['job_zwtext'],item['job_tdtext'],item['job_gstext'],item['job_comName'],
            #   item['company_userName'],item['company_money'],item['company_time'],item['company_type'],item['company_status']
            create_sql='create table {}(id int(20) primary key auto_increment,job_type varchar(100),job_time varchar(100),job_name varchar(100),job_money varchar(100),job_meanMoney varchar(100),job_address varchar(100),job_jy varchar(100),job_xl varchar(100),job_hrName varchar(100),job_hrleader varchar(100),job_zwtext text,job_tdtext text,job_gstext text,job_comName varchar(100),company_userName varchar(100),company_money varchar(100),company_time varchar(100),company_type varchar(100),company_status varchar(100))'.format(table_name)
            self.cursor.execute(create_sql)
            print('创建表成功')

        insert_sql='insert into job_msg(job_type,job_time,job_name,job_money,job_meanMoney,job_address,job_jy,job_xl,job_hrName,job_hrleader,job_zwtext,job_tdtext,job_gstext,job_comName,company_userName,company_money,company_time,company_type,company_status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        self.cursor.execute(insert_sql,args=(item['job_type'],item['job_time'],item['job_name'],item['job_money'],item['job_meanMoney'],item['job_address'],item['job_jy'],item['job_xl'],item['job_hrName'],item['job_hrleader'],item['job_zwtext'],item['job_tdtext'],item['job_gstext'],item['job_comName'],item['company_userName'],item['company_money'],item['company_time'],item['company_type'],item['company_status']))
        self.db.commit()



    def existe_table(self,tableName):
        try:
            self.cursor.execute("select * from {}".format(tableName))
            return True
        except:
            return False
