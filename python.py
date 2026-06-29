from pathlib import Path
import sys
import win32com.client  # для работы с Outlook

if getattr(sys, 'frozen', False):
    base_dir = Path(sys.executable).resolve().parent
else:
    base_dir = Path(__file__).resolve().parent

file_path = base_dir / 'report.txt'

good_day = 'В нерабочее время звонков не поступало.'

reports_by_day = {}

string1 = '1. Описание обращения: '
string2 = '2. Решено: '
string3 = '3. Время обращения: '
string4 = '4. Привлекались ли сотрудники других отделов: '

# Основной цикл ввода отчётов
while True:
    date = input('Введите дату отчета: ').strip()

    if date.lower() == 'стоп':
        break

    day_reports = []

    while True:
        reason = (input(string1)).strip()

        if reason.lower() == 'стоп':
            break

        if reason == '':
            day_reports = None
            break

        complete = (input(string2)).strip()
        time = (input(string3)).strip()
        coop = (input(string4)).strip()

        day_reports.append({
            'reason': reason,
            'complete': complete,
            'time': time,
            'coop': coop
        })

    reports_by_day[date] = day_reports

# ---- Запись всех данных в файл ----
with open(file_path, 'w', encoding='utf-8') as f:
    for date, day_reports in reports_by_day.items():
        f.write(f'Дата: {date}\n')

        if day_reports is None:
            f.write('\n')
            f.write(f'  {good_day}\n\n')
        else:
            for i, report in enumerate(day_reports, start=1):
                f.write('\n')
                f.write(f'  {string1}{report["reason"]}\n')
                f.write(f'  {string2}{report["complete"]}\n')
                f.write(f'  {string3}{report["time"]}\n')
                f.write(f'  {string4}{report["coop"]}\n')
                f.write('\n')

# ---- Автоматическая отправка письма через Outlook ----
def send_report_via_outlook():
    try:
        # Читаем содержимое сохранённого отчёта
        with open(file_path, 'r', encoding='utf-8') as f:
            body_text = f.read()

        # Создаём экземпляр Outlook
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 = olMailItem

        # Заполняем поля шаблонного письма
        mail.Subject = f"Ежедневный отчёт за {max(reports_by_day.keys())}"  # или укажите свою тему
        mail.Body = body_text
        mail.To = "gap@sibrp.su; vny@sibrp.su; YaickijDA@sibrp.su; KaruninAI@sibrp.su"  # укажите нужный адрес
        # mail.CC = "cc@domain.com"
        # При необходимости можно прикрепить файл:
        # mail.Attachments.Add(str(file_path))

        # Отправка (снимаем комментарий, когда всё будет проверено)
        mail.Send()   # <-- раскомментируйте для реальной отправки
        # Для теста лучше сначала использовать mail.Display(True) — покажет письмо без отправки
        #mail.Display(True)
        print("Письмо подготовлено и отображено в Outlook.")

    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")

# Вызываем функцию отправки
if reports_by_day:
    send_report_via_outlook()
else:
    print("Нет данных для отправки.")