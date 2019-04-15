def index_days(lst: list, day: int):
    days = ['m', 't', 'w', 'th', 'f']
    if days[day] in lst:
        return True
