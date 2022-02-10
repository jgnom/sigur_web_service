from flask import Flask, request, jsonify
import pyodbc
import configparser
import json


config = configparser.ConfigParser()
config.read("settings.ini", encoding="utf8")
driver = config["sql_write"]["driver"]
server = config["sql_write"]["server"]
db = config["sql_write"]["database"]
user = config["sql_write"]["uid"]
pw = config["sql_write"]["pwd"]
conn_str = ';'.join(['DRIVER='+driver, 'SERVER='+server, 'DATABASE='+db, 'UID='+user, 'PWD='+pw])
ip = config["host_event"]["ip"]
http_port = config["host_event"]["port"]
http_debug = config["host_event"]["debug"]
http_app_route = config["route"]["event_route"]
app = Flask(__name__)
@app.route(http_app_route, methods=['GET', 'POST'])


def event_data():
    if request.method == 'POST':
        content = request.json
        content_list = content['logs']
        temp_list = []
        for i in content_list:
            id_card = i['keyHex']
            access_point = i['accessPoint']
            logid = i['logId']
            direction = i['direction']
            class DatabaseConnection(object):
                def __init__(self, connection_string):
                    self.conn = pyodbc.connect(connection_string)
                    self.conn.autocommit = True
                    self.cursor = self.conn.cursor()
                def __enter__(self):
                    return self.cursor
                def __exit__(self, *args):
                    self.cursor.close()
                    self.conn.close()
            sql = (f"set nocount on;EXEC [dbo].[pSKUD_EVENT] @ID10 = '{id_card}', @AccessPoint = '{access_point}', @LogID = '{logid}', @Direction = '{direction}';")
            with DatabaseConnection(conn_str) as cursor:
                row = cursor.execute(sql)
                if row:
                    res = cursor.fetchone()
                    if res[2] == logid:
                        response = {"confirmedLogId":logid}
                        temp_list.append(response)
                    else:
                        print('Запись', logid, 'не создана')        
        return jsonify(temp_list)
        
        
if __name__ == "__main__":
    app.run(host=ip, port=http_port, debug=http_debug)