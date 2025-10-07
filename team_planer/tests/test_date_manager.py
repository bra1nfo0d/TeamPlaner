import datetime as dt
import pytest
from team_planer.core.date_manager import DateManager

@pytest.mark.parametrize("fmt, expected", [
	("dd.mm.yyyy", lambda d: f"{d[8:]}.{d[5:7]}.{d[:4]}"),
	("dd/mm/yyyy", lambda d: f"{d[8:]}/{d[5:7]}/{d[:4]}"),
	("dd.mm.yy",   lambda d: f"{d[8:]}.{d[5:7]}.{d[2:4]}"),
	("dd/mm/yy",   lambda d: f"{d[8:]}/{d[5:7]}/{d[2:4]}"),
	("mm.dd.yyyy", lambda d: f"{d[5:7]}.{d[8:]}.{d[:4]}"),
	("mm/dd/yyyy", lambda d: f"{d[5:7]}/{d[8:]}/{d[:4]}"),
	("mm.dd.yy",   lambda d: f"{d[5:7]}.{d[8:]}.{d[2:4]}"),
	("mm/dd/yy",   lambda d: f"{d[5:7]}/{d[8:]}/{d[2:4]}"),
])
@pytest.mark.parametrize("offsets", [-7, -3, 0, 2, 6, 30])

def test_get_date_str_formats(fmt, expected, offsets):
	"""Check all support date formats and offsets."""
	date_manager = DateManager()
	output = date_manager.get_date_str(day=offsets, date_format=fmt)
	tdate = str(dt.date.today() + dt.timedelta(offsets))
	assert output == expected(tdate)

def test_get_date_str_error():
	"""Return 'ERROR' for unsupported formats."""
	date_manager = DateManager()
	output = date_manager.get_date_str(date_format="")
	assert output == "ERROR"