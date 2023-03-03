from domains import *


async def async_worker(instance):
    ''' Ассинхронные подключения к АПИ '''
    request1 = await instance.run_worker_domain(url="https://api.viewdns.info/whois/", domain="domain", apikey=APIKEY, output="json", name="whois")
    request2 = await instance.run_worker_domain(url="https://api.viewdns.info/reverseip/", host="domain", apikey=APIKEY, output="json", name="reverseip")
    request3 = await instance.run_worker_domain(url="https://api.viewdns.info/iphistory/", domain="domain", apikey=APIKEY, output="json", name="iphistory")


    # Формируем запросы для определения ФИО и Email владельца домена
    registrant_email = regex_rawdata(validate(request1,["main","rawdata","Registrant Fax Ext"]))
    registrant_email = validate(registrant_email, ["Registrant Email"])
    registrant = validate(request1, ["main","owner"])


    if registrant and registrant != "REDACTED FOR PRIVACY":
        request4 = await instance.run_worker_domain(url="https://api.viewdns.info/reversewhois/", q=registrant, apikey=APIKEY, output="json", name="rw_owner")
    if registrant_email:
        request5 = await instance.run_worker_domain(url="https://api.viewdns.info/reversewhois/", q=registrant_email, apikey=APIKEY, output="json", name="rw_email")

    return instance.save_result_domain


if __name__ == "__main__":
    # Очищаем дирректории предыдущих результатов
    if os.path.exists(PATH_RESULTS_DIR):
        shutil.rmtree(PATH_RESULTS_DIR)
    os.mkdir(PATH_RESULTS_DIR)

    collector = CollectorRequests(path_file_with_domains=PATH_FILE_WITH_DOMAINS, setting_save_to_file=SETTING_SAVE_TO_FILE)
    collector.run_async_worker( async_worker )










