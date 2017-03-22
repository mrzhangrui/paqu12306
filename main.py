import requests, re
from prettytable import PrettyTable


class Train_jiexi():
    header = '车次 出发地/到达地 出发时间/到达时间 历时 商务座 特等座 一等 二等 高级软卧 软卧 硬卧 软座 硬座 无座 其他'.split()

    def __init__(self, desc):
        self.desc = desc

    def lishi_parse(self, d):
        lishi = d['lishi'].replace(':', '时') + '分'
        return lishi

    @property
    def trains(self):
        for l in self.desc:
            d=l['queryLeftNewDTO']
            #print(d)
            train = [
                d['station_train_code'],
                d['from_station_name']+'/'+d['to_station_name'],
                d['start_time']+'/'+d['arrive_time'],
                self.lishi_parse(d),
                d['swz_num'],
                d['tz_num'],
                d['zy_num'],
                d['ze_num'],
                d['gr_num'],
                d['rw_num'],
                d['yb_num'],
                d['rz_num'],
                d['yz_num'],
                d['wz_num'],
                d['qt_num']
            ]
            yield train

    def train_print(self):
        pt = PrettyTable(self.header)
        for train in self.trains:
            pt.add_row(train)
            #print(train)
        print(pt)

def get_stationname():
    stations_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9001'

    r = requests.get(stations_url, verify=False)

    data = r.text

    s = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', data)
    # print(s)
    stations = {}
    for l in s:
        stations[l[0]] = l[1]
    return stations


def get_stationdesc(fr, to, date):
    stations = get_stationname()
    from_station = stations[fr]
    to_station = stations[to]
    # print(from_station, to_station)
    request_station = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)
    print(request_station)
    respon = requests.get(request_station, verify=False)
    #print(respon.json())
    desc = respon.json()['data']
    Train_jiexi(desc).train_print()


if __name__ == '__main__':
    fr = input('出发地：')
    to = input('到达地：')
    date = input('出发时间(格式：例如：2017-03-19)：')
    get_stationdesc(fr, to, date)
