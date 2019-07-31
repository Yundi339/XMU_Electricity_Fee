# _*_ coding:utf-8 _*_
import requests
from lxml import etree

url = "http://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Referer": url
}


# 修改post的data参数
# @param data {'name':'value', ...}
# @param html 网页源代码
def changeData(data, html):
    data['__EVENTTARGET'] = ''
    data['__EVENTARGUMENT'] = ''
    data['__LASTFOCUS'] = ''
    names = html.xpath('//input[@type="hidden" and @value]/@name')
    values = html.xpath('//input[@type="hidden" and @value]/@value')
    for name, value in zip(names, values):
        data[name] = value


# 获取电费
# @param drxiaoqu 校区代号
# @param drlou 园区代号
# @param txtRoomid 宿舍
def query(drxiaoqu, drlou, txtRoomid):
    # initial
    req = requests.session()
    data = {}

    response = req.get(url=url, headers=headers)  # 第一次请求
    html = etree.HTML(response.content.decode())
    # 获取园区信息
    drxiaoqu_value_list = html.xpath('//select[@name="drxiaoqu"]/option/@value')
    drxiaoqu_name_list = html.xpath('//select[@name="drxiaoqu"]/option/text()')
    # 寻找校区是否匹配
    try:
        drxiaoqu_index = drxiaoqu_name_list.index(drxiaoqu)
    except:
        return 'ERROR drxiaoqu'
    changeData(data, html)
    data['drxiaoqu'] = drxiaoqu_value_list[drxiaoqu_index]
    response = req.post(url=url, headers=headers, data=data)  # 第二次请求
    html = etree.HTML(response.content.decode())
    # 获取楼道信息
    drlou_value_list = html.xpath('//select[@name="drlou"]/option/@value')
    drlou_name_list = html.xpath('//select[@name="drlou"]/option/text()')
    # 寻找园区是否匹配
    try:
        drlou_index = drlou_name_list.index(drlou)
    except:
        return 'ERROR drlou'
    changeData(data, html)
    data['drlou'] = drlou_value_list[drlou_index]
    data['txtRoomid'] = txtRoomid
    response = req.post(url=url, headers=headers, data=data)  # 第三次请求
    html = etree.HTML(response.content.decode())
    # 获取剩余电费
    result = html.xpath('//label[@class="dxeBase_Aqua" and @id="lableft"]/text()')
    return result[0] if len(result) == 1 else "ERROR txtRoomid or SERVICE BOOM!"


xiaoqu = '本部南光区'
yuanqu = '南光7'
sushe = '0301'
print(xiaoqu + ' ' + yuanqu + ' ' + sushe + ':', end='    ')
print(query(xiaoqu, yuanqu, sushe))
