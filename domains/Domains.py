from .Requests import *
from .saveJson import *
from .saveExcel import *


class Domains:
    '''Класс для работы с доменом '''
    def __init__(self, domain, **params):
        self.domain = domain
        self.params = params
        self.result = {}

    @staticmethod
    def get_file_domains(path):
        ''' Инициируем файл с доменами'''
        results = []
        try:
            with open(path, "r", encoding="utf-8") as f_domains:
                for i in f_domains:
                    if len(i) > 3:
                        results.append(i.strip())
        except Exception as err:
            logger.error("Ошибка при считывании файла: " + str(err))
        return results

    def run_worker_domain(self, **other_params):
        ''' Запускаем воркер для одного домена '''
        if "name" not in other_params:
            raise "Задайте 'name' для АПИ запроса"
        if "url" not in other_params:
            raise "Задайте 'url' для АПИ запроса"
        for i in other_params.values():
            if not i:
                return False
        return asyncio.create_task(self.build_request_domains(other_params))

    async def build_request_domains(self, other_params):
        ''' Детализация воркера для одного домена'''
        name = other_params.pop("name")
        logger.info(f"Запрос: {self.domain} - {name}")

        request_data = self.preparing_request(other_params)  # Подготовка данных для формирования URL
        url = Requests.generate_url(request_data)  # Формирование URL
        # answer = await Requests.run(url, name)  # Запуск API запроса
        # await Requests.write_api_test(self.domain, name, answer)  # Загрузка данных в файлы для теста
        answer = await Requests.read_api_test(self.domain, name)  # Чтение данных из файлов для теста
        result = self.controller_api(name, answer)  # Обработка API ответа
        if result:
            self.result[name] = result


    def preparing_request(self, other_params):
        ''' Подготовка данных для передачи в модуль Request '''

        for k, i in other_params.items():
            if i == "domain":
                other_params[k] = self.domain
        return {**self.params, **other_params}

    # =========== Обработка ответов АПИ ===========

    def controller_api(self, name, answer):
        if not answer:
            return None
        result = {}
        result["main"] = main = {}
        main["domain"] = self.domain

        if name == "whois":
            whois = validate(answer, ["response"])
            main["owner"] = fieldPrivatePerson(validate(whois, ["registrant"]))
            main["registrar"] = validate(whois, ["registration","registrar"])
            main["create_time"] = f_format_time(
                validate(whois, ["registration","created"]), out_format="{0}  ( существует {1} {3} и {2} {4} )")
            main["expires"] = f_format_time(
                validate(whois,["registration","expires"]), out_format="{0}  ( на {1} {3} и {2} {4} вперед )")
            main["contact"] = validate(whois,["abuseEmail"])
            main["status"] = get_status(validate(whois,["registration","statuses"]))
            main["ns"] = validate(whois,["name_servers"], [])
            main["rawdata"] = regex_rawdata(validate(whois,["rawdata"],{}))

        elif name == "reverseip":
            main["other_domain"], result["other_domain_all"] = process_data_array(
                validate(answer,["response","domains"]), lambda i: i["name"])

        elif name == "iphistory":
            iphistory = validate(answer,["response"])
            main["ip"] = validate(iphistory,["records",0,"ip"])
            list_ip = 1 if len(validate(iphistory,["records"])) > 1 else 0
            main["on_last_ip_address"] = f_format_time(
                validate(iphistory,["records",list_ip,"lastseen"]),
                in_format="%Y-%m-%d", out_format="{0}  ( {1} {3} и {2} {4} )")
            main["ip_history"], result["ip_history_all"] = process_data_array(
                validate(iphistory,["records"]))

        if name == "rw_owner":
            main["rw_domain"], result["rw_domain_all"] = process_data_array(validate(answer,["response","matches"]), limit=20)

        if name == "rw_email":
            main["rw_domain"], result["rw_domain_all"] = process_data_array(validate(answer["response","matches"]), limit=20)

        return result

    def save(self, settings, result):
        if settings is None:
            return 1
        for save in settings:
            if "json" in save:
                obj = saveJson(self.domain)
                obj.run(result)
            if "excel" in save:
                obj = saveExcel(self.domain)
                obj.run(result)