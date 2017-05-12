from admin.lagou.https import Http
from admin.lagou.parse import Parse
from admin.lagou.setting import headers as hd
from admin.lagou.setting import cookies as ck
import time
import csv
import logging
import sys

# from flask import current_app
from modles import db,job_info
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')


def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=hd, cookies=ck)
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()
    info = []
    for i in range(1, 4000):
        print('第%s页' % i)
        para['pn'] = str(i)
        htmlCode = generalHttp.post(url, para=para, headers=hd, cookies=ck)
        generalParse = Parse(htmlCode)
        info = info + getInfoDetail(generalParse)
        # time.sleep(2)
    return info


def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info


def processInfo(info, para):
    """
    信息存储
    """
    logging.error('Process start')
    try:
        csvFile = open("./jobInfo.csv", 'wt', encoding = 'utf-8')
        writer = csv.writer(csvFile)
        writer.writerow(( 'companyName','industryField','positionName','jobNature','createTime','financeStage',\
                          'companyLabelList','companySize','city','district','positionType','education',\
                          'positionAdvantage','Salary','salaryMax','salaryMin','salaryAvg','workYear'))

        # file = open('test.txt', 'a')
        # file.write(title)
        for p in info:
            Salary = p['positionSalary']
            Salary = Salary.split('-')
            if len(Salary) == 1:
                salaryMax = int(Salary[0][:Salary[0].find('k')])
            else:
                 salaryMax = int(Salary[1][:Salary[1].find('k')])

            salaryMin = int(Salary[0][:Salary[0].find('k')])
            salaryAvg = (salaryMax + salaryMin) / 2
            writer.writerow(( str(p['companyName']) ,str(p['industryField']) ,str(p['positionName']),str(p['jobNature']),\
                              str(p['createTime']),str(p['companyStage']) , str(p['companyLabelList']),str(p['companySize']) ,\
                              str(p['city']) , str(p['district']) , str(p['positionType']),str(p['positionEducation']), \
                              str(p['positionAdvantage']) ,str(p['positionSalary']) ,salaryMax,salaryMin,salaryAvg,\
                              str(p['positionWorkYear'])))
        #     infos = job_info(companyName= str(p['companyName']) ,industryField=str(p['industryField']) ,positionName=str(p['positionName']),\
        #                              jobNature=str(p['jobNature']),createTime= str(p['createTime']),financeStage=str(p['companyStage']) , \
        #                              companyLabelList=str(p['companyLabelList']),companySize=str(p['companySize']) , city=str(p['city']) , \
        #                              district=str(p['district']) , positionType=str(p['positionType']),education=str(p['positionEducation']),\
        #                              positionAdvantage=str(p['positionAdvantage']) ,Salary=str(p['positionSalary']) ,salaryMax=salaryMax,\
        #                              salaryMin=salaryMin,salaryAvg=salaryAvg, workYear=str(p['positionWorkYear']))
        #     db.session.add(infos)
        # db.session.commit()

        csvFile.close()

        # file.close()
        return True
    except:
        logging.error('Process except')
        return None


# def lagou_main(url, para):
#     """
#     主函数逻辑
#     """
#     logging.error('Main start')
#     if url:
#         info = getInfo(url, para)             # 获取信息
#         flag = processInfo(info, para)             # 信息储存
#         return flag
#     else:
#         return None


if __name__ == '__main__':

    url = 'https://www.lagou.com/jobs/positionAjax.json?'
    para = {'first': 'true','pn': '1'}
    logging.error('Main start')
    info = getInfo(url, para)
    flag = processInfo(info, para)
    if flag: print('爬取成功' )
    else: print('爬取失败' )
