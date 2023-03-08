from .Requests import *
from .Serializer import *
from domains.IWriter import *


class Domains:
    '''Класс для работы с доменом '''
    def __init__(self, name_domain, save_to_file):
        self.name_domain = name_domain     # Name Domain
        self.save_to_file = save_to_file   # Setting save to file
        self.save_result_domain = {}     # Massive save result domain


    def run_worker_domain(self, **params_url):
        ''' Запускаем воркер для одного домена '''
        if "name" not in params_url:
            raise "Задайте 'name' для АПИ запроса"
        if "url" not in params_url:
            raise "Задайте 'url' для АПИ запроса"
        for i in params_url.values():
            if not i:
                return False
        return asyncio.create_task(self.task_request_domains(params_url))

    async def task_request_domains(self, params_url):
        ''' Запуск одного таска (API)'''

        name_url = params_url.pop("name")
        try:
            logger.info(f"Запрос: {self.name_domain} - {name_url}")

            request_data = self.preparing_request(params_url)  # Подготовка данных для формирования URL
            url = Requests.generate_url(request_data)  # Формирование URL
            answer = await Requests.read_api_test(self.name_domain, name_url)  # Чтение данных из файлов для теста

            if not answer:
                answer = await Requests.run(url, name_url)  # Запуск API запроса
                await Requests.write_api_test(self.name_domain, name_url, answer)  # Загрузка данных в файлы для теста

            result = self.controller_api(name_url, answer)  # Обработка API ответа
            if result:
                self.save_result_domain[name_url] = result
                return result

        except:
            logger.error(f"Запрос {name_url} отработал некорректно")


    def preparing_request(self, params):
        ''' Замена домена в запросе '''
        for k, i in params.items():
            if i == "domain":
                params[k] = self.name_domain
        return params

    # =========== Обработка ответов АПИ ===========
    def controller_api(self, name, answer):
        # save_to_file(answer, "test.json")
        result = answer = Serializer(answer)
        try:
            result["main"] = main = {}
            main["domain"] = self.name_domain

            if name == "whois":
                main["status"] = get_status(answer.get("response > registration > statuses", "Не подтвержден"))
                main["owner"] = field_private_person(answer.get("response > registrant"))
                main["registrar"] = answer.get("response > registration > registrar")
                main["create_time"] = f_format_time(answer.get("response > registration > created"),
                                                    out_format="{0}  ( существует {1} {3} и {2} {4} назад)")
                main["expires"] = f_format_time(
                    answer.get("response > registration > expires"), out_format="{0}  ( на {1} {3} и {2} {4} вперед )")
                main["ns"] = answer.get("response > name_servers")
                main["rawdata"] = regex_rawdata(answer.get("response > rawdata"))
                main["contact"] = find_contacts(main["rawdata"])

            elif name == "reverseip":
                main["other_domain"], result["other_domain_all"] = process_data_array(
                    answer.get("response > domains"), lambda i: i["name"])

            elif name == "iphistory":
                main["ip"] = answer.get("response > records > 0 > ip")
                list_ip = 1 if len(answer.get("response > records")) > 1 else 0
                main["on_last_ip_address"] = f_format_time(
                    answer.get("response > records > " + str(list_ip) + " > lastseen"),
                    in_format="%Y-%m-%d", out_format="{0}  ( {1} {3} и {2} {4} )")
                main["ip_history"], result["ip_history_all"] = process_data_array(answer.get("response > records"))

            if name == "rw_owner":
                main["rw_domain"], result["rw_domain_all"] = process_data_array(answer.get("response > matches"), lambda i: i["domain"], limit=20)

            if name == "rw_email":
                main["rw_domain"], result["rw_domain_all"] = process_data_array(answer.get("response > matches"), lambda i: i["domain"], limit=20)

            return result.results
        except Exception as err:
            logger.error(f"Функция преобразования результатов отработала некорректно {str(err)}")

    def save(self, response):
        writer = Writer(self.name_domain, response)
        if "json" in self.save_to_file:
            writer.run_writer(SaveJson)
        if "excel" in self.save_to_file:
            writer.run_writer(SaveExcel)
        if "word" in self.save_to_file:
            writer.run_writer(SaveWord)
