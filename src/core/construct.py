import datetime

def max_time() -> datetime.time:
	return datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)

def parse_time(time: str) -> datetime.datetime:
	time = time.replace(" ", "").replace("	", "")
	if time.lower() == "inf" or time.lower() == "infinite": return max_time()
	result = datetime.datetime.now().astimezone()
	tmp = ""
	for i in time:
		if i.isdigit(): tmp += i
		else:
			if i != 'y' and i != 'd' and i != 'h' and i != 'm' and i != 's': return
			try:
				if tmp == "": continue
				if i == 'y': result += datetime.timedelta(days = int(tmp) * 365)
				if i == 'd': result += datetime.timedelta(days = int(tmp))
				if i == 'h': result += datetime.timedelta(hours = int(tmp))
				if i == 'm': result += datetime.timedelta(minutes = int(tmp))
				if i == 's': result += datetime.timedelta(seconds = int(tmp))
			except OverflowError: return
			tmp = ""
	return result