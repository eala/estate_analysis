import os;
import pandas as pd;
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

plt.rcParams['font.family']=['AppleGothic'];

# dump font.family
# import matplotlib
# a=sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
#for i in a:
#    print(i)

# list directories
dirs = next(os.walk('.'))[1]

# three types of data
# xxx_lvr_land_a: house trade
# xxx_lvr_land_b: new house trade
# xxx_lvr_land_c: rental house trade
# xxx: city number, e.g. a: Taipei, b: Taichung, same as ID first eng

city = 'b'; # Taichung
analyze_type = 'a'  # all house trade
analyze_data = city + "_lvr_land_" + analyze_type + ".csv";

dfs = [];

focus_cols = ['Year', 'Q', 'district', 'target', 'unit_ping_price', 'address', 'area_in_ping', 'building_type', 'level', 'note'];

for d in dirs:
    # first row (0) contains categories in Chinese
    # second row (1) contains categories in Eng
    df = pd.read_csv(os.path.join(d, analyze_data), index_col=False, skiprows=[0]);
    # d: sample: estate107S1
    if len(d) == 11 :
        df["Year"] = str(1911 + int(d[-5: -2]));
    elif len(d) == 10 :
        df["Year"] = str(1911 + int(d[-4: -2]));
    else :
        df["Year"] = d[-6: -2];
    df['Q'] = d[-1];

    # rename columns
    df.rename(columns={'The villages and towns urban district' : 'district', 
                        'transaction sign' : 'target',
                        'the unit price (NTD / square meter)' : 'unit_ping_price',
                        'land sector position building sector house number plate' : 'address', 
                        'land shifting total area square meter' : 'area_in_ping', 
                        'building state' : 'building_type', 
                        'shifting level' : 'level', 
                        'the note' : 'note'}, 
                        errors="raise", inplace=True);

    # change unit meter square to ping
    meter_squre_per_ping = 3.305785;
    # unit in W
    df['unit_ping_price'] = df['unit_ping_price'] * meter_squre_per_ping / 10000;
    df['area_in_ping'] = df['area_in_ping'] / meter_squre_per_ping;

    # reduce cols
    focus_dt = pd.DataFrame(df, columns = focus_cols); 
    dfs.append(focus_dt.iloc[1: ]);

df = pd.concat(dfs, sort = True);

prices = {};

orig_districts = {'北區', '南區', '中區', '東區', '西區', '北屯區', '西屯區', '南屯區'}; 
for district in orig_districts:
    cond = (
        (df['district'] == district) &
        (df['target'] == '房地(土地+建物)') &
        (df['building_type'] == '公寓(5樓含以下無電梯)') &
        (df['level'] == '五層') &
        (df['note'].isna())
        );

    groups = df[cond]['Year'];
    prices[district] = df[cond]['unit_ping_price'].astype(float).groupby(groups).mean();
    #prices = df[cond]['unit_ping_price'].astype(float).groupby(groups).mean();
print(prices);

price_history = pd.DataFrame(prices);
price_history.plot();

plt.title("台中市各區無車位五樓老公寓單價 (元/坪)");
plt.xlabel("西元(年)");
plt.xlabel("單價(萬元/坪)");
plt.grid(True);
plt.show();

