# iPhone Photo Date Classifying Script
An automated script that will automatically put your photos and videos into folders with specific dates. It extracts the EXchangeable Image File (EXIF) information to determine when the media was taken, and use the information to create a folder with the date and classify to the correct folder. For files without EXIF data, the script will use it's OS-reported last modified time.

This is not tested on photos taken on Android. If the EXIF format used by Android is the same, this script should work too.
## Prerequisites
This script requires Exiftool to be available. It can downloaded from their official page (https://exiftool.org/). Follow the installation instructions on the page to get a working executable first. [Detailed instructions here](https://exiftool.org/install.html)
### Linux
For Linux users, exiftool is available as a Perl image library and can be installed using your package manager. For example, for Ubuntu:
```
sudo apt install libimage-exiftool-perl
```
Although there seems to be a standalone version on `apt`.
```
sudo apt install exiftool
```
For Fedora:
```
sudo dnf install perl-Image-ExifTool
```
For other distros, do search using your package repositories.

## Usage
It's a terminal app. Simply running while the current directory will automatically sort all files into dates. This script does not sort folders.

There are more options when you enter `classify_by_date.py --help`
```
usage: classify_by_date.py [-h] [-f FORMAT] [-v] [-c {auto,always,never}] [folder ...]

Classifies photos in a given folder by date based on their EXIF information.

positional arguments:
  folder                The folder paths where you want the files inside to be classified by date.

options:
  -h, --help            show this help message and exit
  -f, --format, --folder-date-format FORMAT
                        The date format that the classification folders should be in. Use strftime format codes like
                        "https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes"
  -v, --verbose         Prints more detailed information. By default it remains silent unless something went wrong.
  -c, --color {auto,always,never}
                        When to output ANSI colour formatting.
```

Most of these shall be self-explanatory. I'm too lazy to write out documentations for all the options :P.

### `-f` or `--format` option
For this format, the argument is directly passed into the python's [`datetime.strftime()`](https://docs.python.org/3/library/datetime.html#datetime.date.strftime) method. Thus the format is identical to [the format specified to the aforementioned function](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

The table below is directly ripped from [python 3.13.1's documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). The codes are most of the formats but not everything. There are some notes or caveats inside the [original documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) that is not included here.

| Directive | Meaning                                                                                                                                                                          | Example                                                                         |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `%a`      | Weekday as locale’s abbreviated name.                                                                                                                                            | Sun, Mon, …, Sat (en_US);<br>So, Mo, …, Sa (de_DE)                              |
| `%A`      | Weekday as locale’s full name.                                                                                                                                                   | Sunday, Monday, …, Saturday (en_US);<br>Sonntag, Montag, …, Samstag (de_DE)     |
| `%w`      | Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.                                                                                                                | 0, 1, …, 6                                                                      |
| `%d`      | Day of the month as a zero-padded decimal number.                                                                                                                                | 01, 02, …, 31                                                                   |
| `%b`      | Month as locale’s abbreviated name.                                                                                                                                              | Jan, Feb, …, Dec (en_US);<br>Jan, Feb, …, Dez (de_DE)                           |
| `%B`      | Month as locale’s full name.                                                                                                                                                     | January, February, …, December (en_US);<br>Januar, Februar, …, Dezember (de_DE) |
| `%m`      | Month as a zero-padded decimal number.                                                                                                                                           | 01, 02, …, 12                                                                   |
| `%y`      | Year without century as a zero-padded decimal number.                                                                                                                            | 00, 01, …, 99                                                                   |
| `%Y`      | Year with century as a decimal number.                                                                                                                                           | 0001, 0002, …, 2013, 2014, …, 9998, 9999                                        |
| `%H`      | Hour (24-hour clock) as a zero-padded decimal number.                                                                                                                            | 00, 01, …, 23                                                                   |
| `%I`      | Hour (12-hour clock) as a zero-padded decimal number.                                                                                                                            | 01, 02, …, 12                                                                   |
| `%p`      | Locale’s equivalent of either AM or PM.                                                                                                                                          | AM, PM (en_US);<br>am, pm (de_DE)                                               |
| `%M`      | Minute as a zero-padded decimal number.                                                                                                                                          | 00, 01, …, 59                                                                   |
| `%S`      | Second as a zero-padded decimal number.                                                                                                                                          | 00, 01, …, 59                                                                   |
| `%f`      | Microsecond as a decimal number, zero-padded to 6 digits.                                                                                                                        | 000000, 000001, …, 999999                                                       |
| `%z`      | UTC offset in the form `±HHMM[SS[.ffffff]]` (empty string if the object is naive).                                                                                               | (empty), +0000, -0400, +1030, +063415, -030712.345216                           |
| `%Z`      | Time zone name (empty string if the object is naive).                                                                                                                            | (empty), UTC, GMT                                                               |
| `%j`      | Day of the year as a zero-padded decimal number.                                                                                                                                 | 001, 002, …, 366                                                                |
| `%U`      | Week number of the year (Sunday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0. | 00, 01, …, 53                                                                   |
| `%W`      | Week number of the year (Monday as the first day of the week) as a zero-padded decimal number. All days in a new year preceding the first Monday are considered to be in week 0. | 00, 01, …, 53                                                                   |
| `%c`      | Locale’s appropriate date and time representation.                                                                                                                               | Tue Aug 16 21:30:00 1988 (en_US);<br>Di 16 Aug 21:30:00 1988 (de_DE)            |
| `%x`      | Locale’s appropriate date representation.                                                                                                                                        | 08/16/88 (None);<br>08/16/1988 (en_US);<br>16.08.1988 (de_DE)                   |
| `%X`      | Locale’s appropriate time representation.                                                                                                                                        | 21:30:00 (en_US);<br><br>21:30:00 (de_DE)                                       |
| `%%`      | A literal `'%'` character.                                                                                                                                                       | %                                                                               |
