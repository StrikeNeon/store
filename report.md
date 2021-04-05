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

| Page                          | page loading | sql queries time | sql queries made | similar sql queries | dupe sql queries |templates  |
|-------------------------------|--------------|------------------|------------------|---------------------|------------------|-----------|
| index (initial)               | 2 s          | ~600ms           | 9                | 4                   |4                 | 1 s       |
| index (after optimisation)    | 1471.22 ms    | 354.87 ms       | 5                | 0                   |0                 | 602.56 ms |
| product detail                | 1044.51 ms    | 333.59 ms       | 5                | 0                   |0                 | 298.67 ms |
| brands                        | 985.34 ms     | 279.31 ms       | 4                | 0                   |0                 | 343.0 ms  |
| about                         | 935.51 ms     | 276.41 ms       | 4                | 0                   |0                 | 216.3 ms  |
| register                      | 765.86 ms     | 140.90 ms       | 4                | 0                   |0                 | 736.4 ms  |
| login                         | 797.32 ms     | 144.64 ms       | 4                | 0                   |0                 | 746.5 ms  |
| index after login             | 1471.22 ms    | 354.87 ms       | 7                | 0                   |0                 | 977.4 ms  |
| profile editing               | 1252.46 ms    | 419.41 ms       | 5                | 0                   |0                 | 362.4 ms  |
| cart (empty)                  | 959.96 ms     | 282.78 ms       | 4                | 0                   |0                 | 921.1 ms  |
| cart (with items)             | 1135.34 ms    | 352.71 ms       | 4                | 0                   |0                 | 1057.6 ms |
| order                         | 1059.40 ms    | 337.64 ms       | 4                | 0                   |0                 | 1012.5 ms |

### raw data:SIEGE

| Page                | Date & Time         | Trans | Elap Time | Data Trans | Resp Time | Trans Rate | Throughput | Concurrent | OKAY | Failed |
|---------------------|---------------------|-------|-----------|-----------|------------|------------|-----------|------------|-------|-------|
| index               | 2021-04-04 15:07:02 | 342   | 59.31     | 4         | 1.17       | 5.77       | 0.07      | 6.72       | 342   | 0     |
| product pages - 0   | 2021-04-04 15:07:02 | 342   | 59.31     | 4         | 1.17       | 5.77       | 0.07      | 6.72       | 342   | 0     |
| product pages - 1   | 2021-04-04 15:26:00 | 526   | 59.44     | 3         | 0.61       | 8.85       | 0.05      | 5.39       | 533   | 0     |
| product pages - 2   | 2021-04-04 15:27:26 | 522   | 59.33     | 2         | 0.62       | 8.80       | 0.03      | 5.41       | 528   | 0     |
| product pages - 3   | 2021-04-04 15:36:47 | 522   | 59.83     | 2         | 0.62       | 8.73       | 0.03      | 5.38       | 530   | 0     |
| brands              | 2021-04-04 16:00:41 | 38    | 59.02     | 3         | 0.58       | 9.12       | 0.05      | 5.30       | 545   | 0     |
| about               | 2021-04-04 16:02:55 | 518   | 59.63     | 2         | 0.57       | 8.69       | 0.03      | 4.99       | 525   | 0     |
| register            | 2021-04-04 16:04:18 | 604   | 59.50     | 3         | 0.46       | 10.15      | 0.05      | 4.71       | 610   | 0     |
| login               | 2021-04-04 16:05:59 | 610   | 59.87     | 3         | 0.47       | 10.19      | 0.05      | 4.77       | 619   | 0     |
