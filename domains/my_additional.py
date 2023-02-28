from .settings import *
import os
import logging
from datetime import datetime
import re
import json
import shutil
import asyncio
import aiohttp
from collections import defaultdict

ru_month = {"01":"января","02":"февраля","03":"марта","04":"апреля","05":"мая","06":"июня","07":"июля","08":"августа","09":"сентября","10":"октября","11":"ноября","12":"декабря"}

def init_logger():
    ''' Инициализируем логгер '''
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s, %(levelname)s, Line: %(lineno)d, %(message)s')
    logger.setLevel("DEBUG")
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    streamHandler.setLevel("INFO")
    logger.addHandler(streamHandler)
    fileHandler = logging.FileHandler(filename="log.txt", mode="w")
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel("INFO")
    # logger.addHandler(fileHandler)
    return logger

logger = init_logger()

# ========== Create Time function ===========
def f_format_time(f_time, in_format="%Y-%m-%dT%H:%M:%SZ", out_format="{0} ( с {1} {3} {2} {4} )"):
    ''' Функиця для формирования полей "Дата создания" и "Оплачен до"  '''
    try:
        out_format = "{0} ( {1} {3} и {2} {4} )"
        f_time = datetime.strptime(f_time,
                                   in_format)  # время в Unix
        day = datetime.strftime(f_time, "%d")
        month = ru_month[datetime.strftime(f_time, "%m")]
        year = datetime.strftime(f_time, "%Y")
        create_time_format = "{} {} {}".format(day, month, year)
        duration_days = abs(f_time - datetime.now())

        c_year =  int(duration_days.days / 365) # кол-во лет
        c_month = int((duration_days.days - c_year * 365) / 30) # кол-во месяцев

        if c_year == 0 and c_month == 0:
            p_del = r'\s\{1\}|\s\{2\}|\s\{3\}|\s[си]'
        elif c_year == 0:
            p_del = r'\s\{1\}|\s\{3\}|\sи'
        elif c_month == 0:
            p_del = r'\s\{2\}|\s\{4\}|\sи'
        else:
            p_del = ''
        out_format = re.sub(p_del, '', out_format)

        results = out_format.format(
            create_time_format, c_year, c_month, f_year(c_year), f_month(c_month))
        return results
    except:
        return ''

def f_year(year):
    if year == 1:
        return 'год'
    elif 2 <= year <= 4:
        return 'года'
    else:
        return 'лет'


def f_month(month):
    if month == 0:
        return 'менее 1 месяца'
    elif month == 1:
        return 'месяц'
    elif month >= 2 and month <= 4:
        return 'месяца'
    else:
        return 'месяцев'

def process_data_array(response, f_fields = lambda x: x, limit=10):
    ''' Создает два списка: один с лимитом 10, другой цельный '''
    domains = {}
    try:
        length = len(response)
        domains_all = [f_fields(i) for i in response]
        domains["name"] = domains_all[:limit]
        domains["remains"] = length - limit if length > limit else 0
        return domains, domains_all
    except Exception as err:
        logger.error(f"Ошибка в функции для обработки массивов: {str(err)}")
        return [], []


def xls_worker_dynamic_type(response, header='', typeList = False):
    result = []
    try:
        if typeList:
            if len(response["name"]) == 0:
                return [header, '']
            st = ''
            for i in response["name"]:
                st += i+"\n"
            if response["remains"] != 0:
                st += "и ещё " + str(response["remains"]) + " адреса"
            result = [header, st]
        else:
            if len(response["name"]) == 0:
                return [[header, '']]
            for i in response["name"]:
                st = ''
                for j in i.values():
                    st += j + '\n'
                result.append(['',st])
                result[0][0] = header
        return result
    except Exception as err:
        logger.error(f"Ошибка в функции для обработки массивов excel: {str(err)}")


def xls_worker_dynamic_type_all(response, header=''):
    excel = []
    if type(response[0]) == dict:
        excel.append(header)
        for i in response:
            excel.append(list(i.values()))
    elif type(response[0]) == str:
        excel = [[i] for i in response]
        excel.insert(0, header)
    return excel


def field_ns_server(response):
    result = ''
    try:
        for i in response:
            result += i + '\n'
        return result
    except Exception as err:
        logger.error(f"Ошибка при формировании поля ns server: {str(err)}")


def fieldPrivatePerson(value):
    try:
        return "Частное лицо" if value == "Private Registration" else value
    except:
        return ''

def get_status(response):
    try:
        if response[0].find("VERIFIED"):
            return "Подтвержден"
    except:
        return ""

def regex_rawdata(rawdata):
    try:
        if rawdata:
            value = re.findall("^(.[^:]+):(?:\s+)?(.+)\n?", rawdata, re.MULTILINE)
            if value:
                return {i[0]:i[1] for i in value}
            else:
                return rawdata
    except:
        return ''







def dirs(obj):
    return [i for i in obj.__dir__() if i[0] != "_"]

def save_to_file(result, path):
    with open(path,"w") as file:
        json.dump(result, file, indent=3, ensure_ascii=False)

def read_to_json(filename):
    path = r'domains/source/' + filename
    if os.path.exists(path):
        with open(path, "r") as file:
            return json.load(file)

def validate(massive, direction, default=''):
    ''' Валидация поступающих данных с АПИ'''
    try:
        if len(direction) == 1:
            return massive[direction[0]]
        else:
            if massive[direction[0]]:
                return validate(massive[direction[0]], direction[1:])
    except:
        return default




