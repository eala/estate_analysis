import requests
import datetime
from pathlib import Path
import zipfile
import time

def estate_crawler(year, quarter):
    # pre-process
    assert isinstance(quarter, int) and quarter >= 1 and quarter <= 4, "quarter only can be 1, 2, 3, 4"
    cur_year = datetime.datetime.now().year - 1911;
    cur_quarter = (int)(datetime.datetime.now().month / 4 + 1);
    assert isinstance(year, int) and (year < cur_year or (year == cur_year and quarter < cur_quarter)), "queried: " + str(year) + "Q" + str(quarter) + " is over current " + str(cur_year) + "Q" + str(cur_quarter)

    # based on Taiwan"s year
    if year > 1911:
        year -= 1911;

    # download
    series = "" + str(year) + "S" + str(quarter);
    src_path = "https://plvr.land.moi.gov.tw//DownloadSeason?season=" + series + "&type=zip&fileName=lvr_landcsv.zip";
    res = requests.get(src_path);

    downloadZip = "estate" + str(year) + str(quarter) + '.zip'
    open(downloadZip, 'wb').write(res.content)

    directory = "estate" + series;
    Path(directory).mkdir(parents=True, exist_ok=True)

    # decompress
    with zipfile.ZipFile(downloadZip, 'r') as zip_ref:
        zip_ref.extractall(directory)

    time.sleep(10)

estate_crawler(108, 4)
estate_crawler(109, 1)

start_year = 105;
end_year = 109;

for year in range(start_year, end_year):
    for quarter in range(1, 4):
        estate_crawler(year, quarter)
