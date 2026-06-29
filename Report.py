from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
    base_dir = Path(sys.executable).resolve().parent
else: 
    base_dir = Path(__file__).resolve().parent

file_path = base_dir / 'report.txt'

good_day = 'В нерабочее время звонков не поступало.'

reports_by_day = {}


reason_label = '1. Описание обращения: '
complete_label = '2. Решено: '
time_label = '3. Время обращения: '
deps_label = '4. Привлекались ли сотрудники других отделов: '

while True:
    date = input('Введите дату отчета: ').strip()
    
    if date.lower() == 'стоп':
        break

    day_reports = []

    while True:
        reason = (input(reason_label)).strip()

        if reason.lower() == 'стоп':
            break

        if reason == '':
            if not day_reports:
                day_reports = None
            break

        complete = (input(complete_label)).strip()
        time = (input(time_label)).strip()
        deps = (input(deps_label)).strip()

        day_reports.append({
            'reason': reason,
            'complete': complete,
            'time': time,
            'deps': deps
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
                    f.write(f'  ' + reason_label + f'{report['reason']}\n')
                    f.write(f'  ' + complete_label + f'{report['complete']}\n')
                    f.write(f'  ' + time_label + f'{report['time']}\n')
                    f.write(f'  ' + deps_label + f'{report['deps']}\n')
                    f.write(f'\n')
    
    