function Exiftool-DateInfo {
	param($Img)
	$info = $(exiftool -T $img -CreationDate).Split('+')[0]
	if ($info -eq "-") {
		$info = exiftool -T $img -DateTimeCreated
	}
	if ($info -eq "-") {
		$info = $(exiftool -T $img -DateTimeOriginal).Split('+')[0]
	}
	if ($info -eq "-") {
		return $info
	}
	return $info.Split(' ')
}

function Exiftool-Date {
	param($Img, [switch]$UseExifTool)
	if ($PSBoundParameters.ContainsKey('UseExifTool')) {
		$exifinfo = Exiftool-DateInfo -Img $img
		if ($exifinfo -eq '-') {
			return $(ls $img)[0].LastWriteTime
		}
		$exifinfo = $exifinfo.Split(' ')
		$ori_date = $exifinfo[0].Split(':')
		$ori_time = $exifinfo[1].Split(':')
		return [PSCustomObject]@{
			Year = $ori_date[0]
			Month = $ori_date[1]
			Day = $ori_date[2]
			Hour = $ori_time[0]
			Minute = $ori_time[1]
			Second = $ori_time[2]
		}
	} else {
		return $(ls $img)[0].LastWriteTime
	}
}

Get-ChildItem -Attributes !d | ForEach-Object {
	$date = Exiftool-Date -Img $_ -UseExifTool
	$folder = "$($date.Year)-$(([string]$date.Month).PadLeft(2, '0'))-$(([string]$date.Day).PadLeft(2, '0'))"
	if ( -not (Test-Path -Path $folder)) {
		mkdir $folder
	}
	Move-Item -Path "$($_.Name)" -Destination ".\$folder\$($_.Name)"
}
