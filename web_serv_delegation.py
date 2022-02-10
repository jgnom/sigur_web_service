from flask import Flask, request, jsonify #импортируем модуль flask, requests и jsonify
import pyodbc        # импортируем библиотеку подключение к БД MSQ SQL через ODBC Driver
import configparser  # импортируем библиотеку для хранения отдельной конфигурации
import json          # импортируем библиотеку для работы с json данными

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini", encoding="utf8")  # читаем конфиг

#данные для подключения к MS SQL ДБ для чтения
driver = config["sql_read"]["driver"] #читаем из конфига поле driver в секции sql_read.
server = config["sql_read"]["server"] #читаем из конфига поле server в секции sql_read.
db = config["sql_read"]["database"]   #читаем из конфига поле database в секции sql_read.
user = config["sql_read"]["uid"]      #читаем из конфига поле uid в секции sql_read.
pw = config["sql_read"]["pwd"]        #читаем из конфига поле pwd в секции sql_read.
conn_str = ';'.join(['DRIVER='+driver, 'SERVER='+server, 'DATABASE='+db, 'UID='+user, 'PWD='+pw]) #формируем строку подключения для pyodbc.connect

#настройки хоста для запуска приложения.
ip = config["host_delegation"]["ip"]                       #читаем из конфига поле ip в секции host.
http_port = config["host_delegation"]["port"]              #читаем из конфига поле port в секции host.
http_debug = config["host_delegation"]["debug"]            #читаем из конфига поле debug в секции host.
http_app_route = config["route"]["app_route"]    #читаем из конфига поле app_route в секции host.

app = Flask(__name__)

@app.route(http_app_route, methods=['GET', 'POST']) #web-адрес для доступа по http // по этому пути будет работать приложение.
def get_data():
    if request.method == 'POST':                       #условие, если http запрос POST, то
        content = request.json                         #помещаем полученные из запроса json-данные в переменную content
        id_card = content['keyHex']                    #берем значение с ключем 'keyHex' из json портянки и помещаем в переменную id_card

        #Подключаемся к MS SQL
        cnxn = pyodbc.connect(conn_str)                #подключаемся к базе данных используя строку подключения conn_str и получаем коннект в виде переменной cnxn.
        cursor = cnxn.cursor()                         #создаем объект cursor который будет формировать запрос в БД.
        cursor.execute(f"SELECT V30 FROM dbo.T30_SKUD WHERE V30 = '{id_card}' AND D = 0") #выполнение запроса в БД
        row = cursor.fetchone()                                                           #помещение полученной одной записи в переменную row.
        if row: #условие, если какая либо запись есть, то.
            a = '{"allow":true, "message":"ID пропуска - '+id_card+' доступ разрешен БД библиотеки"}'                      #помещаем в переменную не сериализованный json.
            allow = json.loads(a)                                              #сериализуем json помещаем в переменную allow, т.е. чтоб программы понимали его как json-данные
            print(id_card + ' Доступ разрешен')                                #печатаем содержимое переменной id_card + инф. сообщение в консоль.
        elif not row: #условие, если записи в row нет, то.
            a = '{"allow":false, "message":"ID пропуска - '+id_card+' доступ запрещен БД библиотеки"}'                    #помещаем в переменную не сериализованный json.
            allow = json.loads(a)                                              #сериализуем json помещаем в переменную allow, т.е. чтоб программы понимали его как json-данные
            print(id_card + ' Доступ запрещен')                                #печатаем содержимое переменной id_card + инф. сообщение в консоль.
        else:
            print('Неизвестная ошибка')                                        #печатаем инф. сообщение в консоль
            
        cursor.close()                                                         #закрываем cursor
        cnxn.close()                                                           #закрываем соединение с БД.

        return jsonify(allow)                                                  #возвращает json из переменной allow http respons-ом для клиента приложения.

if __name__ == "__main__":
    app.run(host=ip, port=http_port, debug=http_debug)                         #хост, порт на котором запускается приложение и вкл/выкл отладку.