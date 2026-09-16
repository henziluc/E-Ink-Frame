import pandas as pd

holidays_data = [['Flims', '12.09.2026', '14.09.2026'],
                ['Austria', '21.12.2026', '02.01.2027'],
                ['Catania', '13.11.2026','16.11.2026'],
                ['TestTest', '10.10.2026', '20.10.2026'],
                ['South Africa', '22.01.2027', '11.02.2027']]

holidays = pd.DataFrame(holidays_data, columns=['location', 'start_date', 'end_date'])

holidays['start_date'] = pd.to_datetime(
    holidays['start_date'],
    format='%d.%m.%Y'
)

holidays['end_date'] = pd.to_datetime(
    holidays['end_date'],
    format='%d.%m.%Y'
)

holidays = holidays.sort_values('start_date').reset_index(drop=True)