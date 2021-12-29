# 日志记录统计
# server  log   使用dict进行数据统计
# 1. 统计不同ip访问次数
#    - 如果某个ip是第一次出现, k是ip地址，v是1
#    - 如果某个ip不是第一次出现, k对应的v+=1
#    匹配ip地址的正则：(\d+\.){3}\d+
# 2. 统计不同浏览器的访问次数
#    - 如果某个浏览器是第一次出现, k是浏览器，v是1
#    - 如果某个浏览器不是第一次出现, k对应的v+=1
#    匹配浏览器地址的正则：Firefox|Mozilla|MSIE
import re
def count_patt(fname, patt):
    # fname: 读取日志文件的路径
    # patt: 正则表达式
    patt_dict = {}  # 用于存储结果 k: ip  v: 次数
    cpatt = re.compile(patt)  # 编译正则
    with open(fname, mode="r") as fr:
        for line in fr.readlines():
            m = cpatt.search(line)  # Matchobject
            if m:  # if m != None:
                # 获取匹配到的字符串:ip
                key = m.group()
                # ip不存在，new_value为1
                # ip存在, value += 1
                # {"1.1.1.1": 2, "2.2.2.2": 1}
                # key: "1.1.1.1", 存在，让value+= 1，重新赋值
                # key: "2.2.2.2", 不存在，添加新kv对，值为1
                patt_dict[key] = patt_dict.get(key, 0)+1
                # if key not in patt_dict:
                #     patt_dict[key] = 1
                # else:
                #     patt_dict[key] += 1
    return patt_dict
if __name__ == '__main__':
    fname = "/tmp/my_web.log"
    patt = "(\d+\.){3}\d+"
    patt_browser = "Firefox|Mozilla|MSIE"
    res_dict = count_patt(fname, patt)
    res_br = count_patt(fname, patt_browser)
    print(res_dict)
    print(res_br)

# {"192.168.1.100": 1}
# vim /tmp/my_web.log
# 192.168.1.100  Get /index.html  Firefox
# 192.168.1.100  Get /index.html  Mozilla
# 192.168.1.101  Get /index.html  MSIE
# 192.168.1.102  Get /index.html  Firefox
# 192.168.1.102  Get /index.html  Mozilla


