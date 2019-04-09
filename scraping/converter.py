def index_days(lst):
    number_days = []
    days = ['m', 't', 'w', 'th', 'f']
    for i in lst:
        if i in days:
            number_days.append(days.index(i))
    return number_days
