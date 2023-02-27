from domains import *


async def async_worker(instance):
    ''' Ассинхронные подключения к АПИ '''
    request1 = defaultdict(dict, {'main': {'rawdata': {'Registrant Fax Ext': ''}, "owner": ''}})
    request1 = await instance.run_worker_domain(url="https://api.viewdns.info/whois/", domain="domain", name="whois")
    request2 = await instance.run_worker_domain(url="https://api.viewdns.info/reverseip/", host="domain",
                                                name="reverseip")
    request3 = await instance.run_worker_domain(url="https://api.viewdns.info/iphistory/", domain="domain",
                                                name="iphistory")


    # Формируем запросы для определения ФИО и Email владельца домена
    registrant_email = regex_rawdata(request1["main"]["rawdata"]["Registrant Fax Ext"])
    registrant_email = dict(registrant_email).get("Registrant Email")
    registrant = request1["main"]["owner"]

    if registrant:
        request4 = await instance.run_worker_domain(url="https://api.viewdns.info/reversewhois/", q=registrant, name="rw_owner")
    if registrant_email:
        request5 = await instance.run_worker_domain(url="https://api.viewdns.info/reversewhois/", q=registrant_email,
                                                    name="rw_email")
    return instance.result


if __name__ == "__main__":
    # Очищаем дирректории предыдущих результатов
    if os.path.exists(PATH_RESULTS_DIR):
        shutil.rmtree(PATH_RESULTS_DIR)
    os.mkdir(PATH_RESULTS_DIR)

    collector = CollectorRequests(file=PATH_DOMAIN_FILE, apikey=APIKEY, output="json")
    collector.save = SAVE_FILES
    result = collector.run_async_worker( async_worker )










