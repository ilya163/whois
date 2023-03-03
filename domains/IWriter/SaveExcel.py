from domains.my_additional import *
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Font, Border, Side

class SaveExcel:

    @classmethod
    def save(cls, name_domain,  response):
            try:
                if not os.path.exists(PATH_EXCEL_FILE):
                    wb = Workbook()
                else:
                    wb = load_workbook(PATH_EXCEL_FILE)
                ws = wb.active

                results = cls.formed_data(response)

                column = ws.max_column+1
                for row, value in enumerate(results, 1):
                    ws.cell(row=row, column=column, value=value)

                wb.save(PATH_EXCEL_FILE)
            except Exception as err:
                logger.error(f"Ошибка при обработке данных для Excel: {str(err)}")

    @staticmethod
    def formed_header():
        return (
            "Анализируемый домен", "IP-адрес", "Владелец", "Регистратор", "Создан", "На последнем ip-адресе",
            "Оплачен до", "Контакты", "Статус","Список DNS-серверов",'IP-адреса на которых размещался домен',
            'Прочие домены на сервере','Прочие домены принадлежащие владельцу'
        )


    @staticmethod
    def formed_data(response):
        try:
            if "main" in response:
                main = response["main"]
                results = [
                    main.get("domain"),
                    main.get("ip"),
                    main.get("owner"),
                    main.get("registrar"),
                    main.get("create_time"),
                    main.get("on_last_ip_address"),
                    main.get("expires"),
                    main.get("contact"),
                    main.get("status"),
                    field_ns_server(main.get("ns"))
                           ]

                if "ip_history" in main:
                    if len(main["ip_history"]) > 0:
                        result = xls_worker_dynamic_type(main["ip_history"])
                        results.append(result)

                if "other_domain" in main:
                    if len(main["other_domain"]) > 0:
                        result = xls_worker_dynamic_type(main["other_domain"], typeList=True)
                        results.append(result)

                if "rw_domain" in main:
                    if len(main["rw_domain"]) > 0:
                        result = xls_worker_dynamic_type(main["rw_domain"])
                        results.append(result)

                return results

        except Exception as err:
            logger.error(f"Ошибка при запуске обработчика Excel: {str(err)}")


    @classmethod
    def finally_xls(cls):
        wb = load_workbook(PATH_EXCEL_FILE)
        ws = wb.active

        header = cls.formed_header()

        for row, value in enumerate(header, 1):
            ws.cell(row=row, column=1, value=value)
        ws.freeze_panes = "A1"

        ft = Font(bold=True)
        al = Alignment(wrap_text=True, vertical='top')

        from openpyxl.utils.cell import get_column_letter
        for i in range(1, ws.max_column + 1):
            letter = get_column_letter(i)
            ws.column_dimensions[letter].width = 50

        for cols in ws.rows:
            for num, cell in enumerate(cols, 1):
                if num == 1:
                    cell.font = ft
                cell.alignment = al

        wb.save(PATH_EXCEL_FILE)

