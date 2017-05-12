# -*- coding:utf-8 -*-

# matplotlib.use('Agg')

import  matplotlib
matplotlib.use('Agg')
from matplotlib.pylab import *
import pandas as pd
import seaborn as sns
# matplotlib.use('Agg')
from io import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

datas = pd.read_csv('./admin/jobInfo.csv')

# datas = datas.drop('',axis = 1)#删除无关项
# datas = datas.replace(['1-3','3-5'],['1-3年','3-5年'])##处理时间数据
# datas = datas[datas['jobNature']=='实习']#排除兼职和实习影响
#
# ###实习招聘 第一部分
# #全国实习招聘情况按城市排名
def practical_city():
    fig = plt.figure(figsize=(6, 7))
    datas_p = datas[datas['jobNature']=='实习']
    city_data = datas_p[datas['city'].isin(['北京','上海','广州','深圳','杭州'])]
    city = city_data.groupby('city').size()
    city.sort(ascending = False)
    #city.ix[:10].plot(kind = 'bar')
    city.plot(kind='bar')
    plt.title('全国实习招聘情况按城市排名')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/practical_city.png')
    plt.close(fig)



#全国实习招聘情况按职位领域排名
def practical_poistion():
    fig = plt.figure(figsize=(6, 7))
    datas_p = datas[datas['jobNature']=='实习']
    kk = datas_p.groupby('positionType').size()
    kk.sort(ascending = False)
    #print(kk)
    k1 = kk/len(datas)
    # for i in range(5):
    #     print(k1.ix[:5*i].sum())
    kk.plot(kind = 'bar')
    plt.title('全国实习招聘情况按职位领域排名')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/practical_poistion.png')
    plt.close(fig)


#
###全国招聘情况 第二部分
#全国招聘情况按工作经验排名
def global_experience():
    fig = plt.figure(figsize=(6, 7))
    work_year = datas.groupby('workYear').size()##7项
    work_year.sort(ascending = False)
    work_year.plot(kind='bar')
    plt.title('全国招聘情况按工作经验排名')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/global_experience.png')
    plt.close(fig)


#全国招聘情况按学历要求排名
def global_education():
    fig = plt.figure(figsize=(6, 7))
    education = datas.groupby('education').size()
    education.sort(ascending = False)
    education.plot(kind='bar')##如果是横的柱状图，则排序为True
    plt.title('全国招聘情况按学历要求排名')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/global_education.png')
    plt.close(fig)


#招聘公司类型统计
def company_size():
    fig = plt.figure(figsize=(6, 7))
    kk = datas.groupby('companySize').size()
    kk.sort()
    kk.plot(kind = 'barh')
    plt.title('公司人数大小')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/company_size.png')
    plt.close(fig)



def company_financeStage():
    fig = plt.figure(figsize=(6, 7))
    kk = datas.groupby('financeStage').size()
    kk.sort()
    kk.plot(kind = 'barh')
    plt.title('招聘公司上市类型')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/company_financeStage.png')
    plt.close(fig)


def company_positiontype():
    fig = plt.figure(figsize=(6, 7))
    kk = datas.groupby('positionType').size()
    kk.sort()
    kk.plot(kind = 'barh')
    plt.title('招聘职位统计')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/company_positiontype.png')
    plt.close(fig)

def postion_salary():
    fig = plt.figure(figsize=(6, 7))
    position = datas[datas['positionType']]
    postion_1 = position.piovt_table(['salaryAvg'],index='salaryAvg')
    postion_1 = postion_1.sort_values(by='salaryAvg',ascending=False)
    postion_1.plot(kind='bar',figsize=(6, 7))
    plt.title('每个职位的平均薪资')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/postion_salary.png')
    plt.close(fig)
#
#
# ###城市 第三部分
cities = datas[datas['city'].isin(['北京','上海','广州','深圳','杭州','成都','武汉','南京','郑州','长沙'])]
# print(cities)
### 不同城市薪酬
def city_salary():
    fig = plt.figure()
    city1 = cities.pivot_table(['salaryMin','salaryMax','salaryAvg'],index='city')
    print(city1)
    city1 = city1.sort_values(by='salaryMin',ascending=False)
    city1.plot(kind='bar',figsize=(6, 7))
    plt.title('工作需求最多的十大城市平均薪资')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/city_salary.png')
    plt.close(fig)

#
# ###城市对学历人数及薪酬
# #不同城市对不同学历要求招聘人数
xl = cities[cities['education'].isin(['本科','大专','学历不限','硕士'])]
def city_education_num():
    fig = plt.figure()
    xl1 = xl.pivot_table('salaryMax',index='education',columns='city',aggfunc=len)

    xl1.T.plot(kind='bar',stacked = True,figsize=(6, 7))
    plt.title('不同城市对不同学历要求招聘人数')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/city_education_num.png')
    plt.close(fig)



#不同城市招聘针对不同学历平均薪酬
def city_education_salary():
    fig = plt.figure()
    xl2 = xl.pivot_table('salaryAvg',index='education',columns='city')
    print(xl2)
    xl2.T. plot(kind='bar',figsize=(6, 7))
    plt.title('不同城市招聘针对不同学历平均薪酬')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/city_education_salary.png')
    plt.close(fig)


#不同城市针对不同工作经验招聘人数
def city_experience_num():
    fig = plt.figure()
    jy = cities[cities['workYear'].isin(['1-3年','3-5年','5-10年','不限','应届毕业生'])]
    jy1 = jy.pivot_table('salaryMin',index='workYear',columns='city',aggfunc=len)
    jy1.T.plot(kind='bar',stacked= True,figsize=(6, 7))
    plt.title('不同城市针对不同工作经验招聘人数')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/city_experience_num.png')
    plt.close(fig)

# #不同城市招聘针对不同工作经验平均薪酬
def city_experience_salary():
    fig = plt.figure()
    jy = cities[cities['workYear'].isin(['1-3年','3-5年','5-10年','不限','应届毕业生'])]
    jy2 = jy.pivot_table('salaryMin',index='workYear',columns='city')
    jy2.T.plot(kind='bar',figsize=(6, 7))
    plt.title('不同城市招聘针对不同工作经验平均薪酬')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/city_experience_salary.png')
    plt.close(fig)

##前十职位薪酬，这里主要是按照薪酬来计算，调用的是全国数据，而非前十城市数据
###或者可以再加一段不同城市不同职位的薪酬

rec = datas.groupby('positionType').size()#只考虑全职
rec.sort(ascending=False)
#rec.sort_values(inplace=True)
rec=list(rec.index[:10])

def hotjob_salary():
    fig = plt.figure()
    pt = datas[datas['positionType'].isin(rec)]
    pt1 = pt.pivot_table(['salaryMin','salaryMax'],index='positionType')
    pt1 = pt1.sort_values(by='salaryMin')
    pt1.plot(kind='bar',figsize=(6, 7))
    plt.title('热门职位领域薪资水平')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/hotjob_salary.png')
    plt.close(fig)


##
def hotjob_hotsalary_fivecity():
    pt = datas[datas['positionType'].isin(rec)]
    pt_city = pt[pt['city'].isin(['北京','深圳','广州','上海','杭州'])]
    fig=plt.figure()
    pc1 = pt_city.pivot_table('salaryMin',index='positionType', columns='city')
    pc1.plot(kind='bar',figsize=(6, 7))
    plt.title('热门领域在五大城市薪酬水平')
    plt.savefig('C:/Users/xsh/PycharmProjects/web_app/static/img_pandas/hotjob_hotsalary_fivecity.png')
    plt.close(fig)



#

# practical_city()
# practical_poistion()
# global_education()
# global_experience()
# company_financeStage()
# company_positiontype()
# company_size()
# city_experience_salary()
# city_education_num()
# city_salary()
# city_education_salary()
# city_experience_num()
# hotjob_hotsalary_fivecity()
# hotjob_salary()




