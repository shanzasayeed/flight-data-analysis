# Flight Data Analysis

An exploratory analysis of every flight that left New York City's three airports in 2013, with a
Streamlit app that shows the same results as interactive charts.

## The question

Which airports, airlines and months had the most delayed and canceled flights out of New York in 2013?

## Dataset

`flight_data.csv` has 336,776 rows, one per scheduled flight in 2013 from Newark (EWR), JFK or
LaGuardia (LGA). There are 16 carriers and 16 columns: date, departure and arrival time, departure and
arrival delay in minutes, carrier, tail number, flight number, origin, destination, air time and distance.

This is the public [nycflights13](https://github.com/tidyverse/nycflights13) dataset: all flights
departing New York City airports in 2013, originally from the US Bureau of Transportation Statistics.
The file's columns and row count match it exactly.

Missing values in the raw file:

| Column | Missing rows |
|---|---|
| `dep_time`, `dep_delay` | 8,255 |
| `arr_time` | 8,713 |
| `arr_delay`, `air_time` | 9,430 |
| `tailnum` | 2,512 |

## Cleaning

The same steps run in `flight.ipynb` and in the app's `load_data()`:

1. **Times.** `dep_time` and `arr_time` are stored as numbers like `517`. They are padded to four digits
   and converted to time values (05:17).
2. **Arrival delay check.** Any arrival delay below -100 minutes is treated as a day rollover and has
   1,440 minutes added. No flight in this file is below that threshold (the minimum is -86), so the rule
   changes nothing here.
3. **Air time.** Where a flight has departure and arrival times but no air time, air time is filled with
   the gap between the two. This fills 717 rows (327,346 to 328,063 non-missing).
4. **Status labels.** Two new columns, `dep_status` and `arr_status`: `Late` if the delay is above 0,
   `OnTime` if it is 0 or less, and `Canceled` if the delay is missing.
5. **Columns.** `year`, `hour`, `minute` and `tailnum` are dropped, and month, day, carrier, origin,
   destination and the two status columns are stored as categories.

## Findings

All counts below are from the saved outputs of `flight.ipynb`. Percentages not printed in the notebook are
calculated from those counts.

**1. About 4 in 10 flights left late, but the typical flight left slightly early.**
Of 336,776 flights, 200,089 (59.4%) departed on time or early, 128,432 (38.1%) departed late and 8,255
(2.5%) have no departure recorded and are counted as canceled. The mean departure delay is 12.6 minutes
but the median is -2 minutes: a small number of very long delays, up to 1,301 minutes, pull the mean up.

**2. Newark was the busiest airport and the worst for departure delays.**

| Airport | Flights | Departed late | Canceled |
|---|---|---|---|
| EWR | 120,835 | 52,711 (43.6%) | 3,239 (2.68%) |
| JFK | 111,279 | 42,031 (37.8%) | 1,863 (1.67%) |
| LGA | 104,662 | 33,690 (32.2%) | 3,153 (3.01%) |

LaGuardia had the fewest late departures but the highest cancellation rate. JFK had the lowest.

**3. Delay rates varied a lot between airlines.**
Carriers appear in the data as two-letter codes. WN had the highest share of late departures at 53.4% of
12,275 flights, followed by FL at 50.7% and F9 at 49.8%. UA, the largest carrier with 58,665 flights, was
at 46.5%. The lowest were HA at 20.2% and US at 23.3%. Some of these carriers are small here: HA has 342
flights and F9 has 685. EV had the most cancellations (2,817), ahead of MQ (1,234) and 9E (1,044). HA
had none.

**4. Delays peaked in summer and December, and cancellations in February.**
Late departures were highest in July (13,909), December (13,550) and June (12,655), and lowest in
September (7,815). As a share of that month's flights, that is 47.3%, 48.2% and 44.8%, against 28.3% in
September. Cancellations were highest in February (1,261), which was also the month with the fewest
flights (24,951), and lowest in November (233) and October (236).

## Run the app

`project.py` is a multi-page Streamlit app. Tested on Python 3.12.

```bash
pip install -r requirements.txt
streamlit run project.py
```

Run it from the repo root, because the code reads `flight_data.csv` by relative path. It opens at
`http://localhost:8501`.

| Page | What it shows |
|---|---|
| `project` | The main analysis: flights by airport, destination and month, on-time / late / canceled shares, and delays and cancellations by airport, carrier, month and route |
| `about` | A quick overview: first rows, number of flights, average departure delay, a delay histogram, flights per carrier and the 10 busiest routes |
| `eda` | An automatic profiling report of the cleaned data. It is generated on each visit and takes a while. |

## Files

| File | What it is |
|---|---|
| `flight.ipynb` | The analysis notebook: loading, cleaning, profiling and the charts behind the findings above. It also needs `jupyter` and `PyQt6`, which it imports but doesn't use. |
| `project.py`, `pages/` | The Streamlit app |
| `flight_data.csv` | The dataset (27 MB) |
| `profile.html` | The profiling report the notebook generated. Open it in a browser. |
| `requirements.txt` | Pinned versions the app was tested with |

## Limitations

- **"Canceled" means "no delay recorded".** The data has no cancellation flag. 9,430 flights have no
  arrival delay, against 8,255 with no departure delay, so 1,175 flights that did depart are counted as
  canceled on arrival.
- **Delays are counted, not measured.** A flight 1 minute late and one 5 hours late both count as `Late`.
- **Airport comparisons are by origin only.** The "arrival delay" tables group by the New York airport
  the flight left from, not the airport it arrived at.
- **The app's captions are written by hand.** They are correct for this file but would not update if the
  data changed.
