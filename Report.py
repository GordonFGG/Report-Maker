from pathlib import Path

desktop_dir = Path(__file__).resolve().parent
file_path = desktop_dir / 'report.txt'

good_day = 'В нерабочее время звонков не поступало.'

reports_by_day = {}


string1 = '1. Описание обращения: '
string2 = '2. Решено: '
string3 = '3. Время обращения: '
string4 = '4. Привлекались ли сотрудники других отделов: '

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

    with open(file_path, 'w', encoding='utf-8') as f:

        for date, day_reports in reports_by_day.items():
            f.write(f'Дата: {date}\n')
        
            if day_reports == None:
                f.write('\n')
                f.write(f'  ' + good_day + f'\n' + f'\n')

            else:
                for i, report in enumerate(day_reports, start=1):
                    f.write('\n')
                    f.write(f'  ' + string1 + f'{report['reason']}\n')
                    f.write(f'  ' + string2 + f'{report['complete']}\n')
                    f.write(f'  ' + string3 + f'{report['time']}\n')
                    f.write(f'  ' + string4 + f'{report['coop']}\n')
                    f.write(f'\n')
    
    