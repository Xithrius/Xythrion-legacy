def index_days(lst, day):
    days = ['m', 't', 'w', 'th', 'f']
    if days[day] in lst:
        return True
