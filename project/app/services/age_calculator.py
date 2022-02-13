from datetime import date


def calculate_age(iin: str) -> int:
    year_of_birth = iin[0:2]
    month_of_birth = iin[2:4]
    day_of_birth = iin[4:6]
    person_sex = int(iin[6])
    century = 18
    if person_sex in [3, 4]:
        century += 1
    elif person_sex in [5, 6]:
        century += 2
    year_of_birth = str(century) + year_of_birth
    current_date = date.today().strftime("%d.%m.%Y").split('.')
    current_day, current_month, current_year = int(current_date[0]), int(current_date[1]), int(current_date[2])
    age = current_year - int(year_of_birth)
    if (current_month < int(month_of_birth)) or (
            (current_month == int(month_of_birth)) and (current_day <= int(day_of_birth))
    ):
        age -= 1
    return age
