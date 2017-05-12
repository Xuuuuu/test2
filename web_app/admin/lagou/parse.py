import re
import demjson

class Parse:
    '''
    解析网页信息
    '''
    def __init__(self, htmlCode):
        self.htmlCode = htmlCode
        try:
            self.json_info = demjson.decode(htmlCode)
            pass
        except:
            print('error')


    def parseTool(self,content):
        '''
        清除html标签
        '''
        if type(content) != str: return content
        sublist = ['<p.*?>','</p.*?>','<b.*?>','</b.*?>','<div.*?>','</div.*?>',
                   '</br>','<br />','<ul>','</ul>','<li>','</li>','<strong>',
                   '</strong>','<table.*?>','<tr.*?>','</tr>','<td.*?>','</td>',
                   '\r','\n','&.*?;','&','#.*?;','<em>','</em>']
        try:
            for substring in [re.compile(string, re.S) for string in sublist]:
                content = re.sub(substring, "", content).strip()
        except:
            raise Exception('Error '+str(substring.pattern))
        return content


    def parsePage(self):
        '''
        解析并计算页面数量
        :return: 页面数量
        '''
        totalCount = self.json_info['content']['positionResult']['totalCount']      #职位总数量
        resultSize = self.json_info['content']['positionResult']['resultSize']      #每一页显示的数量
        pageCount = int(totalCount) // int(resultSize) + 1          #页面数量
        print(pageCount)
        return pageCount


    def parseInfo(self):
        '''
        解析信息
        '''
        info = []
        try:
            for position in self.json_info['content']['positionResult']['result']:
                i = {}
                i['companyName'] = position['companyShortName']
                i['positionName'] = position['positionName']
                i['jobNature'] = position['jobNature']
                i['createTime'] = position['createTime']
                i['city'] = position['city']
                i['district'] = position['district']
                i['companyLabelList'] = position['companyLabelList']
                i['companySize'] = position['companySize']
                i['companyStage'] = position['financeStage']
                i['industryField'] = position['industryField']
                i['positionType'] = position['firstType']
                i['positionEducation'] = position['education']
                i['positionAdvantage'] = position['positionAdvantage']
                i['positionSalary'] = position['salary']
                i['positionWorkYear'] = position['workYear']
                info.append(i)
        except:
            print('error')
        return info







