# XMU_Electricity_Fee

### 爬取厦大的电费信息

- Spider_XMU.py 用于爬取厦大电费信息, 修改xiaoqu,yuanqu,sushe这三个参数就能使用。
- Spider_JOJO.py 练习爬虫


[厦大电费网址](https://elec.xmu.edu.cn/PdmlWebSetup/Pages/SMSMain.aspx)

这个网站描述的信息花里胡哨，使用前最好先查看一下所要填的信息在网站里面的真实描述名称。

代码内提供了获取校区、园区的相关代码，如果是个人使用，可以自由发挥，禁止商用用途。

#### 使用案例 Spider_XMU.py：
> 规则: list_ele = [['xiaoqu', 'yuanqu','sushe']]

> 修改: list_ele = ['本部南光区', '南光7','0301']


运行输出：

>本部南光区 南光7 0301:    账户余额：28.81元    剩余电量：54.36度

----------------------------------------------------------
## 2019.07.31

今天厦大电费只能查询厦门大学本部校区的电费，其他校区无法查询。
----------------------------------------------------------
## 2021.05.05

今天查询发现无法获取楼道信息，测试了各种情况，结果只是网址协议从http变成了https，代码已修改。
