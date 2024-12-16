

def determine_due_year(month_due, month_now, year_now):

    due_year = year_now

    if month_now > 6 and month_due < 6:
        due_year += 1

    return due_year