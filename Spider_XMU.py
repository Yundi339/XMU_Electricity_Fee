# _*_ coding:utf-8 _*_
import requests
from lxml import etree

url = "https://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx"
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
    req = requests.session()
    data = {}
    response = req.get(url=url, headers=headers)  # 第一次请求
    html = etree.HTML(response.content.decode())
    # 获取园区信息
    drxiaoqu_value_list = html.xpath('//select[@name="drxiaoqu"]/option/@value')
    drxiaoqu_name_list = html.xpath('//select[@name="drxiaoqu"]/option/text()')
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
    try:
        drlou_index = drlou_name_list.index(drlou)
    except:
        return 'ERROR drlou'
    changeData(data, html)
    data['drlou'] = drlou_value_list[drlou_index]
    data['txtRoomid'] = txtRoomid

    # data['__CALLBACKID'] = 'dxgvElec'
    # data['__CALLBACKPARAM'] = 'c0:GB|20;12|PAGERONCLICK3|PN4;'

    response = req.post(url=url, headers=headers, data=data)  # 第三次请求
    html = etree.HTML(response.content.decode())
    result = html.xpath('//label[@class="dxeBase_Aqua" and @id="lableft"]/text()')
    return result[0] if len(result) == 1 else "ERROR txtRoomid or SERVICE BOOM!"


if __name__ == '__main__':
    list_ele = [
        ['本部南光区', '南光7', '0201'],
        ['本部南光区', '南光7', '0202'],
        ['本部南光区', '南光7', '0203'],
    ]
    for xiaoqu, yuanqu, sushe in list_ele:
        print(xiaoqu + ' ' + yuanqu + ' ' + sushe + ':', end=' ')
        print(query(xiaoqu, yuanqu, sushe))
    input('press enter to exit.')