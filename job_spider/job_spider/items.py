# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class JobSpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #   item['job_type'],item['job_time'],item['job_name'],item['job_money'],item['job_meanMoney'],
    #   item['job_address'],item['job_jy'],item['job_xl'],item['job_hrName'],item['job_hrleader'],
    #   item['job_zwtext'],item['job_tdtext'],item['job_gstext'],item['job_comName'],
    #   item['company_userName'],item['company_money'],item['company_time'],item['company_type'],item['company_status']
    #工作类型
    job_type=Field()
    #工作发布时间
    job_time=Field()
    #岗位名称
    job_name=Field()
    #工作薪资
    job_money=Field()
    #工作平均薪资
    job_meanMoney=Field()
    #工作地点
    job_address=Field()
    #工作经验
    job_jy=Field()
    #学历
    job_xl=Field()
    #hr名字
    job_hrName=Field()
    #hr岗位
    job_hrleader=Field()
    #职位介绍
    job_zwtext=Field()
    #团队介绍
    job_tdtext=Field()
    #公司介绍
    job_gstext=Field()
    #公司名字
    job_comName=Field()
    #公司法人代表
    company_userName=Field()
    #公司注册资金
    company_money=Field()
    #公司成立时间
    company_time=Field()
    #公司类型
    company_type=Field()
    #公司状态
    company_status=Field()

#   'id','job_time','job_name','job_money','job_meanMoney','job_address','job_jy','job_xl','job_hrName','job_hrleader','job_zwtext','job_tdtext',
#   'job_gstext','job_comName','company_userName','company_money','company_time','company_type','company_status'