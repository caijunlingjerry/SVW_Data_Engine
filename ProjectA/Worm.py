# 采集大众品牌汽车在网上的报价
# 数据源：易车网大众品牌汽车http://car.bitauto.com/xuanchegongju/?l=8&mid=8
# 可以采用八爪鱼或Python爬虫，最终导出为CSV格式文件
# 字段包括：名称，最低价格，最高价格，产品图片链接
# coding: utf-8
import requests
import pandas as pd
import numpy
from bs4 import BeautifulSoup#导入解析器

def parse_page ( ):
    # 请求URL
    url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
    # 伪装浏览器
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    #request方法获得页面
    html = requests.get ( url, headers=headers, timeout=10 )
    # 通过content创建BeautifulSoup对象
    content = html.text
    soup = BeautifulSoup ( content, 'html.parser' )
    result_list = soup.find_all ( 'div', class_='search-result-list-item' )
    #创建dataframe，定义列明
    df = pd.DataFrame ( columns=[ '名称', '最低价格', '最高价格', '产品图片链接'] )
    # print(result_list)
    for item in result_list:
        item_list = item.find_all ( 'p' )
        car = item_list[0].string
        price_range = item_list[1].string
        #分割文本获得最高价格，最低价格
        if len ( price_range.split ( '-' )[0] ) == 2:
            down_Price = price_range.split ( '-' )[0]
        #添加最低价格的单位缺失部分
        else:
            down_Price= price_range.split ( '-' )[0] + '万'
        #文本分割，获得最高价格
        up_Price = price_range.split ( '-' )[-1]
        #通过img标签查找所有相关图片url
        pic_url = 'http:' + item.find_all ( 'img' )[0].get ( 'src' )
        # print ( pic_url)
        #创建列表
        temp = {}
        temp['名称'], temp['最低价格'], temp['最高价格'], temp['产品图片链接'] = car, down_Price, up_Price, pic_url
        df = df.append (temp,ignore_index=True)
        # print(df)
    print ( df)
    #导出结果
    df.to_csv('result_car.csv',index=False)

if __name__ == '__main__':
    parse_page ( )
