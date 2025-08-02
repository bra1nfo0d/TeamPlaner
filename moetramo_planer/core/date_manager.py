import datetime as dt

def get_date_str(day=0, form="ddmmyyyy"):
	tday = dt.date.today()
	date = str(tday + dt.timedelta(day))
	if form == "ddmmyyyy":
		return f"{date[8:]}.{date[5:7]}.{date[:4]}"
	elif form == "mmddyyyy":
		return "not yet implemented"
	elif form == "ddmmyy":
		return "not yet implemented"
	elif form == "mmddyy":
		return "not yet implemented"

def get_date_str_list(week=0, form="ddmmyyyy"):
	date_list = []
	tday = dt.date.today()
	weekday = dt.date.today().weekday()
	date_weekday0 = tday - dt.timedelta(weekday) + dt.timedelta(week * 7)
	if form == "ddmmyyyy":
		for i in range(8):
			date = str(date_weekday0 + dt.timedelta(i))
			date_list.append(f"{date[8:]}.{date[5:7]}.{date[:4]}")
		return date_list
	elif form == "ddmmyyyy":
		return "not yet implemented"
	elif form == "mmddyyyy":
		return "not yet implemented"
	elif form == "ddmmyy":
		return "not yet implemented"
	elif form == "mmddyy":
		return "not yet implemented"