# Functionality and Performance Report
* this report should be updated upon site functionality changes

## data presented below was gathered with django debug toolbar and siege performance testing tool


### testing result bulletpoints

* page loading is very slow, probably due to heroku db or aws as a file storage, regardless,
* testing revealed only one major sql error which resulted in duplicate queries.

  [banner template tag had a severe logical error and was making ~3-4 queries for choosing a banner, where it should have made at most 2.](https://github.com/StrikeNeon/store/blob/aws_migration/mainapp/templatetags/banner.py#L17)
  still, some queries seem unnesessary or, potentially, computation - heavy at higher load and should be optimised further.

* A much larger error was accidentally discovered - debug mode could not be turned off as it resulted in a server error relating to a missing css file, currently it's unclear what actually causes the error, but it is likely related to an error in migrating file system to aws or a conflict between aws and heroku file system.

* siege testing revealed a hard limit on user connections at ~100, which limited testing potential, but no major errors were discovered

* overall the site seems pretty slow, with simple template rendering taking up to a full second,
though it very well might be hosting related and not the issue of the site.

  Query logic is optimal, but far from ideal, mainly the fact that the server retrieves all product and banner records
  this __will__ be the cause of horrible performance at high load and should be corrected ASAP, before this problem is encountered

* geekshop_templates test found 0 errors

### raw data: debug toolbar

#### index
page loading (initial) = 2s (partially due to aws file storage/heroku limits?)
sql queries (9 made/4 similar /4 dupes) = ~600ms, templates = 1s

page loading  after select_related optimisation = 1471.22ms
sql queries(5/0/0) = 354.87 ms, templates = 602.56ms

#### product detail

page loading = 1044.51ms
sql queries (5/0/0) = 333.59ms, templates = 298.67ms

#### brands

page loading = 985.34ms
sql queries (4/0/0) = 279.31 ms, templates = 343.0ms

#### about

page loading = 935.51ms
sql queries (4/0/0) = 276.41 ms, templates = 216.3ms

#### register

page loading = 765.86ms
sql queries (4/0/0) = 140.90 ms, templates = 736.4ms

#### login

page loading = 797.32ms
sql queries (4/0/0) = 144.64 ms, templates = 746.5ms

#### index after login

page loading = 794.80 ms
sql queries (7/0/0) = 144.64 ms, templates = 977.4ms

#### profile editing

page loading = 1252.46ms
sql queries (5/0/0) = 419.41 ms, templates = 362.4ms

#### cart (empty)

page loading = 959.96ms
sql queries (4/0/0) = 282.78 ms, templates = 921.1ms

#### cart (with items)

page loading = 1135.34ms
sql queries (5/0/0) = 352.71 ms, templates = 1057.6ms

#### order

page loading = 1059.40ms
sql queries (5/0/0) = 337.64 ms, templates = 1012.5ms



### raw data:SIEGE

      Date & Time,  Trans,  Elap Time,  Data Trans,  Resp Time,  Trans Rate,  Throughput,  Concurrent,    OKAY,   Failed

#### index

2021-04-04 15:07:02,    342,      59.31,           4,       1.17,        5.77,        0.07,        6.72,     342,       0

#### product pages

2021-04-04 15:26:00,    526,      59.44,           3,       0.61,        8.85,        0.05,        5.39,     533,       0
2021-04-04 15:27:26,    522,      59.33,           2,       0.62,        8.80,        0.03,        5.41,     528,       0
2021-04-04 15:36:47,    522,      59.83,           2,       0.62,        8.73,        0.03,        5.38,     530,       0

#### brands

2021-04-04 16:00:41,    538,      59.02,           3,       0.58,        9.12,        0.05,        5.30,     545,       0

#### about

2021-04-04 16:02:55,    518,      59.63,           2,       0.57,        8.69,        0.03,        4.99,     525,       0

#### register

2021-04-04 16:04:18,    604,      59.50,           3,       0.46,       10.15,        0.05,        4.71,     610,       0

#### login

2021-04-04 16:05:59,    610,      59.87,           3,       0.47,       10.19,        0.05,        4.77,     619,       0
