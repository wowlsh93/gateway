# coding=utf-8

import time
import psycopg2
import psycopg2.extras

import warnings

from UtilLog import plog2, plog
from influxdb import InfluxDBClient
import UtilTime


class InfluxDB:
    def __init__(self, szServerIP, nPort, szID, szPwd, szDbName, gateway_id):
        self.m_szServerIP = szServerIP
        self.m_nPort = nPort
        self.m_szID = szID
        self.m_szPwd = szPwd

        if gateway_id is '':
            self.m_szDbName = szDbName
        else:
            self.m_szDbName = szDbName + "_" + gateway_id

    def open(self):

        bConti = True

        while bConti:

            try:

                self.m_dConn = InfluxDBClient(self.m_szServerIP, self.m_nPort, self.m_szID, self.m_szPwd,
                                              self.m_szDbName)

                bConti = False

            except Exception as e:

                time.sleep(SASGlobal.g_nConnectionRetryInterval)

                print ("--------------------------------- influxdb connect fail -------------------------------------")

    def createDatabase(self, name):
        self.m_dConn.create_database(name)

    def insertData(self, jsondata):

        # print("Write points: {0}".format(jsondata))

        return self.m_dConn.write_points(jsondata)

    def selectData(self, query):
        result = self.m_dConn.query(query)
        return result

        # def deleteData(self,query):
        #     self.m_dConn.


class InfluxDBManager:
    m_oDBConn = None

    def __init__(self, szServerIP, nPort, szID, szPwd, szDbName, gateway_id):

        self.m_oDBConn = InfluxDB(szServerIP, nPort, szID, szPwd, szDbName, gateway_id)

        self.m_oDBConn.open()
        self.gateway_id = gateway_id

    # influxdb python 에서는 삭제가 안되는듯?
    # def delete_by_date(self, measurement, start_day,end_day):
    #     dRecord = self.m_oDBConn.selectData('''
    #                   DELETE  FROM "{0}" WHERE time > {1} and time < {2}
    #                   '''.format(measurement, start_day, end_day))


    def getOneDataFromDB(self, dayIdx):
        return [0, 0, 0, 0, 0, 0, 0, 300, 290, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300]

    # 하루전 부터의 데이터 얻기
    # table : 데이터가 저장된 measurement (문자열)
    # group : 1s,1m,1h 등 그룹할 시간 (문자열)
    def getWatt(self, table, group):

        dRecord = self.m_oDBConn.selectData('''
              SELECT mean("watt") as watt, mean("pf") as pf FROM "{0}" WHERE time > now() - 1d GROUP BY time({1}) fill(null)
              '''.format(table, group))

        for recs in dRecord:
            for rec in recs:
                mean = rec['watt']
                mean_1 = rec['pf']
                time = rec['time']

                yield mean, mean_1, time

    # getwatt_by_range 사용하는것으로 변경
    def getWatt_day(self, table, group, start_time, end_time, method):
        warnings.warn("deprecated", DeprecationWarning)

    # 데이터베이스별 전력/PF 컬럼 명
    # home -> watt, pf
    # office -> watt, pfc1
    # jinyoung total -> wattDelta, pfDelta

    # 시간 범위로 데이터 얻기
    # table : 데이터가 저장된 measurement (문자열)
    # group : 1s,1m,1h 등 그룹할 시간 (문자열)
    # start_time : 시작 시간 ('2017-06-29 15:00:00' 방식)  (문자열)
    # end_time : 끝 시간  ('2017-06-30 15:00:00' 방식)  (문자열)
    # method : "mean", "medain", "distinct" 등 집합 방식 (문자열)
    def getWatt_by_range(self, table, id, group, start_time, end_time, method):

        dRecord = []

        if method is None:
            dRecord = self.m_oDBConn.selectData('''
                                    SELECT "watt" , "pf" FROM "{0}"
                                    WHERE id = '{3}' and time > '{1}' and time < '{2}'
                                    '''.format(table, start_time, end_time, id))

        else:
            dRecord = self.m_oDBConn.selectData('''
                         SELECT {4}("watt") as watt, {4}("pf") as pf FROM "{0}"
                         WHERE id = '{5}' and  time > '{2}' and time < '{3}'
                         GROUP BY time({1}) fill(null)
                         '''.format(table, group, start_time, end_time, method, id))

        for recs in dRecord:
            for rec in recs:
                mean = rec['watt']
                mean_pf = rec['pf']
                time = rec['time']

                yield mean, mean_pf, time

    def getWatt_count(self, sql):
        dRecord = self.m_oDBConn.selectData(sql)
        return dRecord

    def getWatt_by_range_by_sql(self, sql):

        dRecord = self.m_oDBConn.selectData(sql)

        for recs in dRecord:
            for rec in recs:
                mean = rec['watt']
                mean_pf = rec['pf']
                time = rec['time']

                yield mean, mean_pf, time

    def getWatt_by_range_only_watt(self, sql):

        dRecord = self.m_oDBConn.selectData(sql)

        for recs in dRecord:
            for rec in recs:
                mean = rec['watt']
                time = rec['time']

                yield mean, time

    # 실시간으로 진영 데이터의 2,3,4 번 노드의 합을 구해서 Insert ( 배치방식 )
    def getWatt_total(self):

        try:
            dRecord = self.m_oDBConn.selectData('''
                      SELECT mean("watt") as watt FROM jinyoung1_2
                      WHERE  time > now() - 479s and time < now() - 420s
                      GROUP BY time({0}) fill(null);
                      SELECT mean("watt") as watt FROM jinyoung1_3
                      WHERE  time > now() - 479s and time < now() - 420s
                      GROUP BY time({0}) fill(null);
                      SELECT mean("watt") as watt FROM jinyoung1_4
                      WHERE  time > now() - 479s and time < now() - 420s
                      GROUP BY time({0}) fill(null);
                  '''.format("1s"))

            sum_mean = [0 for j in range(60)]
            sum_time = ['' for j in range(60)]
            i = 0

            for recs in dRecord:
                i = 0
                for rec in recs:
                    for value in rec:
                        mean = value['watt']
                        time = value['time']

                        if mean is None:
                            print ("mean is None")
                            break

                        sum_mean[i] += mean
                        sum_time[i] = time
                        i += 1

            for mean, time in zip(sum_mean, sum_time):
                json_meter_body = [

                    {

                        "measurement": 'jinyoung1_total',

                        "tags": {

                            "id": 1

                        },
                        "time": time,
                        "fields": {

                            "id": 1,
                            "wattDelta": float(mean),
                            "pfDelta": 0
                        }

                    }

                ]

                self.m_oDBConn.insertData(json_meter_body)
                print ("----------------------------------------------")

        except Exception as  e:
            print ("--------------------------------- influxdb total fail -------------------------------------")

    # 시간 범위의 진영 데이터의 2,3,4 번 노드의 합을 구해서 Insert ( 배치방식 )
    def getWatt_total_batch(self):

        try:
            dRecord = self.m_oDBConn.selectData('''
                      SELECT mean("watt") as watt FROM jinyoung1_2
                      WHERE  time > '{1}' and time < '{2}'
                      GROUP BY time({0}) fill(null);
                      SELECT mean("watt") as watt FROM jinyoung1_3
                      WHERE  time > '{1}' and time < '{2}'
                      GROUP BY time({0}) fill(null);
                      SELECT mean("watt") as watt FROM jinyoung1_4
                      WHERE  time > '{1}' and time < '{2}'
                      GROUP BY time({0}) fill(null);
                  '''.format("1s", "2017-04-06", "2017-04-07"))

            sum_mean = [0 for j in range(86400)]
            sum_time = ['' for j in range(86400)]

            i = 0

            for recs in dRecord:
                i = 0
                for rec in recs:
                    for value in rec:
                        mean = value['watt']
                        time = value['time']

                        if mean is None:
                            mean = 0.0

                        sum_mean[i] += mean
                        sum_time[i] = time
                        i += 1

            for mean, time in zip(sum_mean, sum_time):
                json_meter_body = [

                    {

                        "measurement": 'jinyoung1_total',

                        "tags": {

                            "id": 1

                        },
                        "time": time,
                        "fields": {

                            "id": 1,
                            "wattDelta": float(mean),
                            "pfDelta": 0
                        }

                    }

                ]

                self.m_oDBConn.insertData(json_meter_body)

        except Exception as  e:
            print ("--------------------------------- influxdb total fail -------------------------------------")

    # Json 형식으로 하나의 데이터를 Insert
    def insertToDB(self, pattern, nodeid):

        json_meter_body = [

            {

                "measurement": self.gateway_id + str(nodeid),

                "tags": {

                    "id": pattern.id

                },

                "fields": {

                    "id": pattern.id,
                    "wattDelta": int(pattern.wattDelta),
                    "watt1": int(pattern.watt1),
                    "watt2": int(pattern.watt2),
                    "pfDelta": int(pattern.pfDelta),
                    "updcount": pattern.updcount

                }

            }

        ]

        self.m_oDBConn.insertData(json_meter_body)

        return 0

    # 외부에서 Json 으로 만들어진 여러개의 데이터를 Insert
    def insertToDB2(self, data):

        try:
            if self.m_oDBConn.insertData(data):
                print ("InfluxDB Insert OK!!")
            else:
                print ("InfluxDB Insert Fail!!")
        except Exception as ex:
            print ("InfluxDB Insert Execptin!!! ", ex)

        return 0

    def insertEvent(self, data):
        try:
            if self.m_oDBConn.insertData(data):
                print ("InfluxDB Insert OK!!")
            else:
                print ("InfluxDB Insert Fail!!")
        except Exception as ex:
            print ("InfluxDB Insert Execptin!!! ", ex)

        return 0
