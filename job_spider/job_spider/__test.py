# coding:utf-8
import requests as rq
from lxml import etree
import random


headers = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:60.0) Gecko/20100101 Firefox/60.0',
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
]



proxy = {
    'http://': 'http://122.114.31.177:808',
    'https://': ['https://112.87.246.66:53281', 'https://101.236.21.22:8866', 'https://27.184.125.67:8118'],
}

opener = rq.get('https://www.zhipin.com/c101010100-p100102/', proxies=proxy,
                headers={'User-Agent': random.choice(headers)})

# print('响应内容',opener.text)
print('响应头', opener.headers)
print(opener.text)

# with open('job_test.html','w+') as f:
#     f.write(opener.text)

inner = etree.HTML(opener.text)
# dl=inner.xpath('//dl[@class="condition-city show-condition-district"]/dd/a/@href')
# print(dl)
jl = inner.xpath('//div[@class="job-list"]//ul/li//div[@class="info-primary"]//a/@href')
#
print('job_url:', jl)

# url=inner.xpath('//div[@class="page"]/a[last()]/@href')
# print(url)
job = rq.get('https://www.zhipin.com' + jl[0], proxies=proxy, headers={'User-Agent': random.choice(headers)})

# with open('job_xq.html','w') as f:
#     f.write(job.text)
job_inner = etree.HTML(job.text)
job_time = job_inner.xpath('//div[@class="job-author"]/span/text()') if len(job_inner.xpath('//div[@class="job-author"]/span/text()')) else None
print('时间', job_time)

job_name = job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/h1/text()') if len(job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/h1/text()')) else None
print('工作名字：', job_name)

job_money = job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/span/text()')[0] if len(job_inner.xpath('//div[@class="info-primary"]/div[@class="name"]/span/text()')) else None
print('薪资:', job_money)

#计算薪资的平均数
if job_money != None:
    split_job=job_money.split('-')
    job_meanMoney=(int(split_job[0][:-1])+int(split_job[1][:-1]))//2*1000
else:
    job_meanMoney=None
print('平均薪资：',job_meanMoney)

job_ajx = job_inner.xpath('//div[@class="info-primary"]/p/text()') if len(job_inner.xpath('//div[@class="info-primary"]/p/text()')) else None
print('地址经验：', job_ajx)
#截取地址、经验、学历信息
job_address=job_ajx[0].split(':')[-1] if len(job_ajx) >=1 else None
print('工作地点：',job_address)

job_jy = job_ajx[1].split(':')[-1] if len(job_ajx)>=2 else None
print('经验要求：',job_jy)

job_xl = job_ajx[2].split(':')[-1] if len(job_ajx) >=3 else None
print('学历要求:',job_xl)


job_hrName = job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/h2/text()')[0] if len(job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/h2/text()')) else None
print('hr姓名：', job_hrName)
job_hrleader = job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/p/text()')[0] if len(job_inner.xpath('//div[@class="job-detail"]/div[@class="detail-op"]/p/text()')) else None
print('hr的职位：', job_hrleader)

job_text = job_inner.xpath('//div[@class="detail-content"]//div[starts-with(@class,"job-sec")]')
print('公司信息：', job_text)
for job in job_text:
    h3_text = job.xpath('./h3/text()')
    if not len(h3_text):
        continue
    if h3_text[0] == '职位描述':
        job_zwtext = job.xpath('./div[@class="text"]/text()') if len(job.xpath('./div[@class="text"]/text()')) else None
        print('职位描述', job_zwtext)

    elif h3_text[0] == '团队介绍':
        job_tdtext = job.xpath('./div[@class="text"]/text()') if len(job.xpath('./div[@class="text"]/text()')) else None
        print('团队介绍', job_tdtext)

    elif h3_text[0] == '公司介绍':
        job_gstext = job.xpath('./div[@class="text"]/text()') if len(job.xpath('./div[@class="text"]/text()')) else None
        print('公司介绍', job_gstext)

    elif h3_text[0] == '工商信息':
        job_comName = job.xpath('./div[@class="name"]/text()')
        print('公司名称', job_comName)
        company_msg = job.xpath('./div[@class="level-list"]/li') if len(
            job.xpath('./div[@class="level-list"]/li')) else None
        # 当工商信息不存在时，将以下字段名都设为None
        if company_msg == None:
            company_userName = company_money = company_time = company_type = company_status = None
        else:
            company_userName=company_msg[0].xpath('./text()')[0] if len(company_msg[0].xpath('./text()')) else None
            print('公司法人:',company_userName)
            company_money=company_msg[1].xpath('./text()')[0] if len(company_msg[1].xpath('./text()')) else None
            print('注册资金:',company_money)
            company_time=company_msg[2].xpath('./text()')[0] if len(company_msg[2].xpath('./text()')) else None
            print('成立时间：',company_time)
            company_type=company_msg[3].xpath('./text()')[0] if len(company_msg[3].xpath('./text()')) else None
            print('企业类型：',company_type)
            company_status = company_msg[4].xpath('./text()')[0] if len(company_msg[4].xpath('./text()')) else None
            print('经营状态：', company_status)

