import tools
import psycopg2


def pretty_day(rows, day):
    for i_row in range(len(rows)):
        if rows[i_row][0] == 'нет пары':
            day += f'{i_row + 1}. нет пары\n'
            day += f"{'-' * 50}\n"
        else:
            day += f"{i_row + 1}. {rows[i_row][0]} {rows[i_row][3].strftime('%H:%M')}\n{rows[i_row][1]} в {rows[i_row][2]} {rows[i_row][4]} \n{'-' * 50}\n"

    return day


def format_schedule(schedule):
    days = {}
    for lesson in schedule:
        day = lesson[0]
        if day not in days:
            days[day] = []
        days[day].append(lesson)

    output = ''
    for day, lessons in days.items():
        i = 1
        output += f'{day}\n{"-" * 50}\n'
        for lesson in lessons:
            if lesson[1] == 'нет пары':
                output += f'{i}. {lesson[1]}\n{"-" * 50}\n'
                i += 1
                continue
            subject = lesson[1]
            room = lesson[3]
            lesson_type = lesson[2]
            teacher = lesson[5]
            time = lesson[4].strftime('%H:%M')
            output += f'{i}. {subject} {room}\n{lesson_type} {teacher} {time}\n{"-" * 50}\n'
        output += '\n'
        i += 1
    return output


def day_handler(day, type_week):
    conn = psycopg2.connect(
        dbname="simple_bot",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    query = """SELECT timetable.fk_subject_name, type_lesson.type_lesson_name, timetable.room_num, 
                      timetable.start_time, teacher.full_name
               FROM timetable, teacher, teacher_type_lesson, type_lesson
               WHERE timetable.day = %s AND
                     timetable.type_week = %s AND
                     timetable.fk_type_lesson_id = teacher_type_lesson.type_lesson_id AND
                     teacher.fk_subject_name = timetable.fk_subject_name AND
                     teacher.teacher_id = teacher_type_lesson.teacher_id AND
                     teacher_type_lesson.type_lesson_id = type_lesson.type_lesson_id
                     ORDER BY timetable.timetable_id"""

    cursor.execute(query, (day, type_week))

    timetable_day = f"{day}\n{'-' * 50}\n"

    rows = cursor.fetchall()

    timetable_day = pretty_day(rows, timetable_day)

    cursor.close()
    conn.close()

    return timetable_day


def week_handler(week_info):
    conn = psycopg2.connect(
        dbname="simple_bot",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    query = """SELECT timetable.day, timetable.fk_subject_name, type_lesson.type_lesson_name, timetable.room_num, 
                    timetable.start_time, teacher.full_name
               FROM timetable, teacher, teacher_type_lesson, type_lesson
               WHERE timetable.type_week = %s AND
                     timetable.fk_type_lesson_id = teacher_type_lesson.type_lesson_id AND
                     teacher.fk_subject_name = timetable.fk_subject_name AND
                     teacher.teacher_id = teacher_type_lesson.teacher_id AND
                     teacher_type_lesson.type_lesson_id = type_lesson.type_lesson_id
			   ORDER BY timetable.timetable_id"""

    week = f'{tools.get_week_type(week_info[0])} ({week_info[1]})\n{"-" * 50}\n'
    cursor.execute(query, (week_info[0],))
    week += format_schedule(cursor.fetchall())
    cursor.close()
    conn.close()

    return week
