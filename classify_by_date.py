#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime
from functools import reduce
import logging
from os import get_terminal_size, linesep, listdir, mkdir, path
from shutil import move
from subprocess import check_output
from typing import List, Optional, Tuple

SNAPSHOT_VERSION = "202306262348"
SCRIPT_DIR = path.dirname(path.realpath(__file__))
EXIFTOOL_COMMAND:str = "exiftool"
# EXIFTOOL_COMMAND = path.join(SCRIPT_DIR, "exiftool")

def date_folder_name_fmt(dt:datetime) -> str:
	# return f'{dt.year}-{dt.month}-{dt.day}'
	return dt.strftime("%Y-%m-%d")

def get_exiftool_date_info_iphone(img:str) -> Optional[str]:
	command = [EXIFTOOL_COMMAND, '-T', img]
	info = check_output(command + ['-CreationDate']).decode(encoding = "utf-8")
	info = info.split(linesep)[0]
	info = info.split('+')[0]
	if info == '-':
		info = check_output(command + ['-DateTimeCreated']).decode(encoding = "utf-8")
		info = info.split(linesep)[0]
	if info == '-':
		info = check_output(command + ['-DateTimeOriginal']).decode(encoding = "utf-8")
		info = info.split(linesep)[0]
		info = info.split('+')[0]
	if info == '-':
		return None
	return info

def fit_one_line(s:str, keep_last_n_chars:int = 0, n_dots_ellipsis:int = 3) -> str:
	w = get_terminal_size().columns
	if w > 1:
		w -= 1
	sl = len(s)
	if sl <= w:
		return s + (' ' * (w - sl))
	if w <= n_dots_ellipsis:
		return s[:w + 1]
	if w <= keep_last_n_chars + n_dots_ellipsis:
		return s[:w - n_dots_ellipsis] + '.' * n_dots_ellipsis
	return s[:w - keep_last_n_chars - n_dots_ellipsis] + ('.' * n_dots_ellipsis) + ("" if keep_last_n_chars == 0 else s[-keep_last_n_chars:])

def clean_printing_line() -> None:
	print(' ' * (get_terminal_size().columns - 1), end = "\r")

def parse_exiftool_datetime(exiftooldate:str) -> Tuple[int, int, int, int, int, int]:
	return tuple(map(lambda a: int(a), reduce(lambda a, b: a + b, map(lambda a: a.split(':'), exiftooldate.split(" ")))))

def get_exif_date_time(img:str, progress:int, goal:int) -> datetime:
	exif_date_str = get_exiftool_date_info_iphone(img)
	if logging.root.isEnabledFor(logging.INFO):
		print(fit_one_line(f"[{progress}/{goal}] Processing \"{img}\""))
	if not exif_date_str or exif_date_str == '-':
		last_mod_date = datetime.fromtimestamp(path.getmtime(img))
		clean_printing_line()
		logging.info(f"Exiftool did not give a date for \"{img}\", using last modified date instead.")
		logging.info("Last modified date: " + last_mod_date.strftime("%Y:%m:%d %H:%M:%S"))
		return last_mod_date
	y, m, d, h, mins, secs = parse_exiftool_datetime(exif_date_str)
	return datetime(y, m, d, h, mins, secs)

def classify_by_date(parent:str, files:List[str], dates:List[datetime]) -> None:
	assert len(files) == len(dates)
	for file, date in zip(files, dates):
		ori_file = path.join(parent, file)
		date_folder = path.join(parent, date_folder_name_fmt(date))
		if not path.isdir(date_folder):
			mkdir(date_folder)
		new_file = path.join(date_folder, file)
		if path.exists(new_file):
			logging.warning(f"The path '{new_file}' is already taken, the file '{ori_file}' will not be moved.")
			continue
		move(ori_file, new_file)
		

def main() -> None:
	parser = ArgumentParser(description = "Classifies photos in a given folder by date based on their EXIF information.", epilog = f"This is still experimental. Snapshot {SNAPSHOT_VERSION}")
	parser.add_argument('folder', nargs = "*", default = '.', help = "The folder paths where you want the files inside to be classified by date.")
	parser.add_argument('-f', '--format', '--folder-date-format', action = "store", required = False, default = None, help = "The date format that the classification folders should be in. Use strftime format codes like \"https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes\"")
	args = parser.parse_args()

	logging.basicConfig(level = logging.WARNING, format = '[%(levelname)s] %(message)s')

	folders:list = args.folder

	if args.format:
		date_fmt:str = args.format
		global date_folder_name_fmt
		date_folder_name_fmt = lambda dt: dt.strftime(date_fmt)

	for folder in folders:
		if not path.isdir(folder):
			logging.warning(f"Path '{folder}' given is not a directory.")
			continue
		files = [i for i in listdir(folder) if path.isfile(path.join(folder, i))]
		goal = len(files)
		dates = [get_exif_date_time(path.join(folder, f), i, goal) for i, f in enumerate(files)]
		classify_by_date(folder, files, dates)

if __name__ == '__main__':
	main()
