

def get_week_type(week_type):
    return 'чётная неделя' if week_type == 0 else 'нечётная неделя'


def convert_weekday(weekday):
    days_map = {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье'
    }
    return days_map.get(weekday.lower(), weekday)


def weekdays(title=False):
    if title:
        return ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    return ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
