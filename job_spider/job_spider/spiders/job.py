# -*- coding: utf-8 -*-
import scrapy
import scrapy_redis
from scrapy_redis.spiders import RedisCrawlSpider,RedisSpider
from selenium import webdriver

from lxml import etree

from job_spider.items import JobSpiderItem


class JobSpider(RedisSpider):
    name = 'job'
    allowed_domains = ['www.zhipin.com']
    #start_urls = ['http://www.zhipin.com/']

    redis_key = 'job:start_urls'

    def __init__(self):
        super(JobSpider, self).__init__()
        self.browser=webdriver.Chrome()


    def parse(self, response):
        '''
        解析boss主页内容，获取所有职位访问路径
        :param response:
        :return:
        '''
        print('代理：',response.meta)
        print('ttttttt',response.url[:-1])
        self.browser.get(response.url)

        # with open('boss.html','wb') as f:
        #     print(type(self.browser.page_source))
        #     f.write(self.browser.page_source.encode())
        main_html=etree.HTML(self.browser.page_source)
        #main_html=response.xpath('//div[@id="main"]//dl[@class=""]')
        dl = main_html.xpath('//div[@id="main"]//div[@class="job-menu"]/dl')
        print('dl信息：',dl)
        for li in dl:
            #获取所有的岗位路径
            a_url = li.xpath('./div[@class="menu-sub"]/ul//a')
            # print('li信息:',len(a_url))
            for a in a_url:
                #拼接岗位访问路径
                final_url=response.url[:-1]+a.xpath('./@href')[0]
                #print('岗位路径：', final_url)
                job_type=a.xpath('./text()')[0]
                print('岗位类型',job_type)
                yield scrapy.Request(final_url,callback=self.parse_cityMsg,
                                     meta={'job_type':job_type}, priority=1,
                                     dont_filter=True)

    def parse_cityMsg(self,response):
        '''
        解析职位相关城市信息，获取相关职位城市信息内容
        :param response:
        :return:
        '''
        #self.browser.get(response.url)
        # with open('job_msg.html','wb') as f:
        #     f.write(response.body)

        print('job_type_第二层:',response.meta)
        #获取某个岗位的城市路径
        citys_url = response.xpath('//dl[@class="condition-city show-condition-district"]/dd/a/@href').extract()
        print('ppppppp',citys_url)
        #去除前两个a标签的内容（不需要）
        i=0
        for city_url in citys_url[2:]:
            #拼接城市访问路径
            final_city_url ='https://'+response.url.split('/')[2]+city_url
            print('城市路径为：',final_city_url)
            i+=1
            print('城市数量:',i)
            yield scrapy.Request(final_city_url,callback=self.parse_jobmsg,meta={'job_type':response.meta['job_type']},
                                 dont_filter=True,priority=1)


    def parse_jobmsg(self,response):
        # with open('job_url.html','wb') as f:
        #     f.write(response.body)
        print('job_meta第三层:',response.meta)
        jobs_url = response.xpath('//div[@class="job-list"]//ul/li//div[@class="info-primary"]//a/@href').extract()
        print('jobs_url路径:',jobs_url)
        for job_url in jobs_url:
            final_job_url ='https://'+response.url.split('/')[2]+job_url
            print('工作详情页面：',final_job_url)
            yield scrapy.Request(final_job_url,callback=self.parse_jobxq,dont_filter=True,priority=1,
                                 meta={'job_type':response.meta.get('job_type',None)})
        try:
            next_url=response.xpath('//div[@class="page"]/a[last()]/@href').extract_first()
        except:
            pass
        else:
            print('next_url路径:',next_url)
            final_next_url='https://'+response.url.split('/')[2]+next_url
            yield scrapy.Request(final_next_url,callback=self.parse_jobmsg,
                                 dont_filter=True,priority=2)


    def parse_jobxq(self,response):
        #item=JobSpiderItem()
        #item={}
        item={'job_type':None,'job_time':None,'job_name':None,'job_money':None,'job_meanMoney':None,'job_address':None,'job_jy':None,'job_xl':None,'job_hrName':None,'job_hrleader':None,'job_zwtext':None,'job_tdtext':None,'job_gstext':None,'job_comName':None,'company_userName':None,'company_money':None,'company_time':None,'company_type':None,'company_status':None}

        print('默认item:',item)
        job_inner = etree.HTML(response.text)
        print('meta:-----',response.meta)

        item['job_type']=response.meta.get('job_type',None)
        print('岗位类型：',item['job_type'])

        item['job_time'] = job_inner.xpath('//div[@class="job-author"]/span/text()')[0] if len(
            job_inner.xpath('//div[@class="job-author"]/span/text()')) else None
        print('时间', item['job_time'])

        item['job_name'] = job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/h1/text()')[0] if len(
            job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/h1/text()')) else None
        print('工作名字：', item['job_name'])

        item['job_money'] = job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/span/text()')[0] if len(
            job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/span/text()')) else None
        print('薪资:', item['job_money'])

        # 计算薪资的平均数
        if item['job_money'] != None:
            split_job = item['job_money'].split('-')
            item['job_meanMoney'] = (int(split_job[0][:-1]) + int(split_job[1][:-1])) // 2 * 1000
        else:
            item['job_meanMoney'] = None
        print('平均薪资：', item['job_meanMoney'])

        job_ajx = job_inner.xpath('//div[@class="info-primary"]/p/text()') if len(
            job_inner.xpath('//div[@class="info-primary"]/p/text()')) else None
        print('地址经验：', job_ajx)
        # 截取地址、经验、学历信息
        item['job_address'] = job_ajx[0].split('：')[-1] if len(job_ajx) >= 1 else None
        print('工作地点：', item['job_address'])

        item['job_jy'] = job_ajx[1].split('：')[-1] if len(job_ajx) >= 2 else None
        print('经验要求：', item['job_jy'])

        item['job_xl'] = job_ajx[2].split('：')[-1] if len(job_ajx) >= 3 else None
        print('学历要求:', item['job_xl'])

        item['job_hrName'] = job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/h2/text()')[0] if len(
            job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/h2/text()')) else None
        print('hr姓名：', item['job_hrName'])
        item['job_hrleader'] = job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/p/text()')[0] if len(
            job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/p/text()')) else None
        print('hr的职位：', item['job_hrleader'])

        job_text = job_inner.xpath('//div[@class="detail-content"]//div[starts-with(@class,"job-sec")]')
        print('公司信息：', job_text)
        for job in job_text:
            h3_text = job.xpath('./h3/text()')
            if not len(h3_text):
                continue
            if h3_text[0] == '职位描述':
                job_zwtext_list = job.xpath('./div[@class="text"]/text()') if len(
                    job.xpath('./div[@class="text"]/text()')) else None
                job_zwtext=''
                if job_zwtext_list==None:
                    item['job_zwtext']=None
                else:
                    for i in job_zwtext_list:
                        job_zwtext+=i.strip()

                    item['job_zwtext']=job_zwtext
                    print('职位描述', item['job_zwtext'])

            elif h3_text[0] == '团队介绍':
                job_tdtext_list = job.xpath('./div[@class="text"]/text()') if len(
                    job.xpath('./div[@class="text"]/text()')) else None
                job_tdtext=''
                if job_tdtext_list==None:
                    item['job_tdtext']=None
                    print('团队介绍', item['job_tdtext'])
                else:
                    for i in job_tdtext_list:
                        job_tdtext+=i.strip()
                    item['job_tdtext']=job_tdtext
                    print('团队介绍', item['job_tdtext'])

            elif h3_text[0] == '公司介绍':
                job_gstext_list = job.xpath('./div[@class="text"]/text()') if len(
                    job.xpath('./div[@class="text"]/text()')) else None
                job_gstext=''
                if job_gstext_list==None:
                    item['job_gstext']=None
                    print('公司介绍', item['job_gstext'])
                else:
                    for i in job_gstext_list:
                        job_gstext+=i.strip()
                    item['job_gstext']=job_gstext
                    print('公司介绍', item['job_gstext'])

            elif h3_text[0] == '工商信息':
                item['job_comName'] = job.xpath('./div[@class="name"]/text()')[0]
                print('公司名称', item['job_comName'])
                company_msg = job.xpath('./div[@class="level-list"]/li') if len(
                    job.xpath('./div[@class="level-list"]/li')) else None
                # 当工商信息不存在时，将以下字段名都设为None
                if company_msg == None:
                    item['company_userName'] = item['company_money'] = item['company_time'] = item['company_type'] = item['company_status'] = None
                else:
                    item['company_userName'] = company_msg[0].xpath('./text()')[0] if len(
                        company_msg[0].xpath('./text()')) else None
                    print('公司法人:', item['company_userName'])
                    item['company_money'] = company_msg[1].xpath('./text()')[0] if len(
                        company_msg[1].xpath('./text()')) else None
                    print('注册资金:', item['company_money'])
                    item['company_time'] = company_msg[2].xpath('./text()')[0] if len(
                        company_msg[2].xpath('./text()')) else None
                    print('成立时间：', item['company_time'])
                    item['company_type'] = company_msg[3].xpath('./text()')[0] if len(
                        company_msg[3].xpath('./text()')) else None
                    print('企业类型：', item['company_type'])
                    item['company_status'] = company_msg[4].xpath('./text()')[0] if len(
                        company_msg[4].xpath('./text()')) else None
                    print('经营状态：', item['company_status'])
        print('需要保存的数据：',item)

        yield item




#   item['job_type'],item['job_time'],item['job_name'],item['job_money'],item['job_meanMoney'],
#   item['job_address'],item['job_jy'],item['job_xl'],item['job_hrName'],item['job_hrleader'],
#   item['job_zwtext'],item['job_tdtext'],item['job_gstext'],item['job_comName'],
#   item['company_userName'],item['company_money'],item['company_time'],item['company_type'],item['company_status']



