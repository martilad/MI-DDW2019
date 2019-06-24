# HW5 - WebAnalytics & WebUsageMining

Solution of homework 5.

## Task (assignment)

- Execute data preprocessing

  - Design a suitable data representation for the analysis - association rule mining + any other analysis of your choice
    - e.g. file where each row represents one user visit/session and columns including all interesting descriptions or summaries of the visit
      - user-transactions matrix, pageview-feature matrix, transaction-feature matrix
  - Remove too short visits
  - Implement any other data cleaning mechanism
  - Identify conversions in data
    - main conversions
      - APPLICATION (reservation of the trip) or CATALOG (request the printed catalog) in the PageName (or category) attribute of clicks
    - micro conversions
      - DISCOUNT, HOWTOJOIN, INSURANCE, or WHOWEARE in the PageName attribute of clicks

  - Implement pattern extraction
    - Identify interesting association rules in the data (e.g. conversions in the consequent)
    - Realize any other analysis of the data of your choice (e.g. users, visits clustering etc.)

## Solution

This task I processed in Jupyter notebook (src/WebAnalytics_WebUsageMining.ipynb) and python 3.7. Here I will list the most important points and results from the implementation.

### General statistic

```
Total number of visitors: 15559
Total number of referrers 140
Total number of clicks 38451
Total number of pages 826
```

#### Some statistic about times on the page and the page score.

|       |   TimeOnPage |    PageScore |
| ----: | -----------: | -----------: |
| count | 38451.000000 | 38451.000000 |
|  mean |    72.412421 |   143.092975 |
|   std |   114.640528 |   260.595877 |
|   min |    30.000000 |    30.000000 |
|   25% |    30.000000 |    30.000000 |
|   50% |    30.000000 |    62.000000 |
|   75% |    60.000000 |   125.000000 |
|   max |  2640.000000 |  5753.000000 |



#### Some statistic about lenght of visit and number of visit pages for visitor.



|       | Length_seconds | Length_pagecount |
| ----: | -------------: | ---------------: |
| count |   15559.000000 |     15559.000000 |
|  mean |     128.908028 |         2.471239 |
|   std |     328.777507 |         2.998959 |
|   min |       0.000000 |         1.000000 |
|   25% |       0.000000 |         1.000000 |
|   50% |       0.000000 |         1.000000 |
|   75% |     120.000000 |         3.000000 |
|   max |    5280.000000 |        50.000000 |

### Preprocessing

I used the recommendation to remove too short visits for data preprocessing and data clearing. Next, I removed those where only one website was visited. The last cleansing was on the value of the website where I found in the names ww, wwww, www which corresponds more to badly captured data. Below is a sample pre-processing implementation code:

```python
# remove too short visits
data = data[data.Length_seconds > 7]

# remove when low pages visit
data = data[data['Length_pagecount'] > 1]
print("Kepp only users visit two or more pages. Size after remove:", len(data))

indexNames = data[ data['PageName'] == 'ww' ].index
# Delete these row indexes from dataFrame
data.drop(indexNames , inplace=True)
indexNames = data[ data['PageName'] == 'wwww' ].index
# Delete these row indexes from dataFrame
data.drop(indexNames , inplace=True)
indexNames = data[ data['PageName'] == 'www' ].index
# Delete these row indexes from dataFrame
data.drop(indexNames , inplace=True)
```

### Association rule task

#### Data selection

The data from the pandas data frame is required to get to the lists of lists for the apriori algorithm. Then I released the algorithm with the required 0.005 support. Once found, I create the rules and calculate confidence. The rules are sort by the support and then by the confession. I also added the option to list only the keyword rules on the left side of the rule. I generated the rules, so I always have one value on the left.

#### Output

There are not many generated rules, and most of the rules only apply to binary data because the text data did not support enough. Maybe more associative rules would be if I were generating left sides with more than one token. However, the rules show, for example, that a person has spent more time on a page if the site has a high rating and vice versa. If a high rating is likely to spend a lot of time on the page. Below is a sample of rules:

['PageScore=(24.277, 316.15]'] -> ['TimeOnPage=(27.39, 160.5]'] - SUPPORT: 0.849 - CONFIDENCE: 0.974
['TimeOnPage=(27.39, 160.5]'] -> ['PageScore=(24.277, 316.15]'] - SUPPORT: 0.849 - CONFIDENCE: 0.969
['SequenceNumber=(0.951, 3.45]'] -> ['PageScore=(24.277, 316.15]'] - SUPPORT: 0.519 - CONFIDENCE: 0.914
['PageScore=(24.277, 316.15]'] -> ['SequenceNumber=(0.951, 3.45]'] - SUPPORT: 0.519 - CONFIDENCE: 0.595
['SequenceNumber=(0.951, 3.45]', 'TimeOnPage=(27.39, 160.5]'] -> ['PageScore=(24.277, 316.15]'] - SUPPORT: 0.496 - CONFIDENCE: 1.0
['PageScore=(24.277, 316.15]', 'SequenceNumber=(0.951, 3.45]'] -> ['TimeOnPage=(27.39, 160.5]'] - SUPPORT: 0.496 - CONFIDENCE: 0.956
['SequenceNumber=(0.951, 3.45]'] -> ['TimeOnPage=(27.39, 160.5]'] - SUPPORT: 0.496 - CONFIDENCE: 0.874
['PageScore=(24.277, 316.15]', 'TimeOnPage=(27.39, 160.5]'] -> ['SequenceNumber=(0.951, 3.45]'] - SUPPORT: 0.496 - CONFIDENCE: 0.584
['TimeOnPage=(27.39, 160.5]'] -> ['SequenceNumber=(0.951, 3.45]'] - SUPPORT: 0.496 - CONFIDENCE: 0.566
['Length_seconds=(54.78, 321.0]'] -> ['PageScore=(24.277, 316.15]'] - SUPPORT: 0.459 - CONFIDENCE: 0.982

### The longest and shortest chain of page for one visit

#### Data selection

For a series of clicks during the visit, I used the original pandas of the data frame and created a dictionary with the ordered field in which they are on the visit. Then print the longest sequence and the shortest.

#### Output

##### The longest chain of pages:

TravelAgency -> light hiking -> sightseeing tours -> England France Ireland capital Dublin Paris London sightseeing tour -> Swiss Alps Valais -> Ireland &#39;green island&#39; -> England and London residence of English kings -> Baltics small circle pobaltíím a tour -> Lofoten Norway Sweden United Arctic Circle -> Norway Norwegian fjords -> francie bretaň daughter Ocean -> Russia Saint Petersburg jewel of Russia and the Republic pobaltíské -> Lofoten Norway Sweden United Arctic Circle -> kiev Kiev treasures and Ruthenia -> Swiss beauty of Switzerland and the Alpine giants -> Ireland &#39;green island&#39; -> Norway Norwegian fjords -> Poland Great Circle Poland -> Scotland United circuit Scotland -> large briánie Ireland Nature sights History -> Germany Denmark Hanseatic cities of the Baltic and Danish Kingdom -> Russia Moscow Novgorod St. Petersburg -> Ireland &#39;green island&#39; -> Turkey&#39;s west coast -> Serbia Montenegro Bosnia and Herzegovina treasures and secrets Yugoslav Balkans holiday 05 -> United Kingdom England classic circuit -> UK English Riviera and Cornwall magical corner of King Arthur -> Turkey Eastern Turkey airlines -> Sicily Southern Italy very detailed circuit -> corsica sardinia -> Mediterranean islands of Malta Gozo and Sicily -> Morocco Morocco big circle plane -> France wine and spirits -> stays with trips -> Aeolian Islands -> Central volcanoes of southern Italy (Sicily Lipari) -> volcanoes of central and southern Italy (Sicily Lipari) a tour -> Aeolian Islands -> Sicily Aeolian Islands with a visit to Sicily vacation residence with 05 trips -> Corsica -> Corsica (stay with excursions) holidays 05 -> Corsica Corsica with light tourism holiday 05 -> Corsica emerald island of Corsica holiday 05 -> Elba Corsica Sardinia -> stays with trips -> Sicily sea and sights with a trip to the Aeolian Islands -> Croatian national parks and natural beauty of Croatia -> CATALOG -> hotelbuses -> hotelbuses

tours with tents -> Turkey in the sign of the crescent (western Turkey) -> stays with trips -> ancient monuments of Greece staying in Tolu -> the northern Adriatic Sea and its islands -> Greece and Bulgaria stay with tours -> Provencal wander -> France with the scent of the Atlantic -> Spain French Riviera -> Corsica -> Corsica Corsica with light tourism holiday 05 -> corsica sardinia -> Elba Corsica Sardinia -> Corsica emerald island of Corsica tourism and holidays 05 -> Corsica (stay with excursions) holidays 05 -> Montenegro Alet Becici much stay with excursions in the price -> stays -> Lefkada air package tours -> hotelbuses -> Morocco Morocco cold country with a hot sun, a tour -> Tunisian dates land sea and sand -> sightseeing tours -> Italy Florence Renaissance gem -> Greco big circle and Ionian Islands -> Lombardy culture history, gastronomy -> Norway Norwegian fjords -> volcanoes of central and southern Italy (Sicily Lipari) a tour -> Lithuania Latvia Estonia Helsinki St. Petersburg circuit pobaltískými republics with a visit to St. Petersburg and Finland -> Hungarian wines and thermal baths -> Baltics small circle pobaltíím a tour -> Russia Saint Petersburg jewel of Russia and the Republic pobaltíské -> kiev Kiev treasures and Ruthenia -> Swiss beauty of Switzerland and the Alpine giants -> Poland Great Circle Poland -> Scotland United circuit Scotland -> Germany Denmark Hanseatic cities of the Baltic and Danish Kingdom -> Baltics small circle pobaltíím a tour -> canyons and islands south of france -> Germany Denmark Hanseatic cities of the Baltic and Danish Kingdom -> Hungary Budapest monuments and thermal spas and Bratislava -> Ukraine podkapatská rus relaxing vacation wander Carpathian Ruthenia 05 -> Ukraine podkapatská rus relaxing vacation wander Carpathian Ruthenia 05

TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency -> TravelAgency

TravelAgency -> tours with tents -> Morocco Morocco Maghreb tour of Pearl -> Romanian Danube delta on ships and dry feet -> light hiking -> France provence natural parks -> tours with tents -> Greek national parks and sea greece -> Greek Antiquity sea and mountains -> Greek island of Crete Gods stop to Corfu -> Baltics Baltic countries, Russia -> Greek national parks and sea greece -> National Parks and the southern coast of England and Wales -> Romania as Dracula and other pearls tourism Romania 05 -> Bulgarian national parks and sea Bulgaria -> Black Mountain NC Sea and the Black Mountains hiking tour of 05 tourism -> Iceland southern Norway Faroe Islands -> France Spain Pyrenees natural parks -> Portugal country seafarers -> Corsica emerald island of Corsica tourism and holidays 05 -> Turkey in the sign of the crescent (western Turkey) -> tours with tents -> Polish walks in the Polish Carpathians -> Ukraine wander Transcarpathian Ukraine holiday 05 -> Norway Sweden Norwegian fjords and glaciers -> Greek national parks and sea greece -> National parks and Sea of Italy Ligurian Riviera -> Bulgarian national parks and sea Bulgaria -> Greek national parks and sea greece -> Sicily Islands inner fire (Sicily Lipari) -> Indian summer in Crimea -> National parks and Sea of Italy Ligurian Riviera -> National Parks and the southern coast of England and Wales -> volcanoes and canyons monasteries France -> pearls Yugoslav Balkans -> National parks and sea greece -> Norway Sweden Norwegian fjords and glaciers -> Bulgarian national parks and sea Bulgaria -> Bulgarian national parks and sea Bulgaria

TravelAgency -> tours with tents -> Montenegro -> Montenegro Alet Becici much stay with excursions in the price -> Montenegro -> light hiking -> France provence natural parks -> Corsica Corsica with light tourism holiday 05 -> Italy relaxing week in the Alps iii. Queen of the Dolomites Marmolada -> Sicily Aeolian Islands with a visit to Sicily vacation residence with 05 trips -> Montenegro Alet Becici much stay with excursions in the price -> Spain Spanish spring festivities Andorra and southern France -> Bulgaria stay with trips vacation visit to Turkey 05 -> Montenegro Alet Becici much stay with excursions in the price -> island country of fire and ice -> Morocco Morocco cold country with a hot sun, a tour -> Croatia national parks and Korcula -> tours with tents -> Turkey in the sign of the crescent (western Turkey) -> Sicily Islands inner fire (Sicily Lipari) -> tours with tents -> Albania country eagles sea and mountains -> Romanian Danube delta on ships and dry feet -> Ukraine wander Transcarpathian Ukraine holiday 05 -> Elba Corsica Sardinia -> Natural parks and sea Perigord France -> Turkey in the sign of the crescent (western Turkey) -> hotelbuses -> island country of fire and ice -> Morocco Morocco cold country with a hot sun, a tour -> Tunisian dates land sea and sand -> Aeolian Islands -> Austria after plane through the Alps Tauern bike path cyclo tour -> Austro around lakes, mountains and lakes of the Salzkammergut cycling tour -> Balaton: wine volcano swimming -> dolomites on the flat trail Dravskem Austria Italy -> Vineyards and thermal Hungary Austria -> Vineyards and thermal Hungary Austria

##### The shortest chain of pages (all are same):

TravelAgency -> TravelAgency

### Implementation

The complete step-by-step implementation is shown in the Jupyter notebook as mentioned. In the implementation, I used the Pandas library for preprocessing and data preparation. Using data frames in pandas makes it very easy to work with data. I have implemented the association rules using the algorithm from the exercises, and I modified it. Finally, I drew the data for each visit from the data, listing the 5 longest and shortest page sequences. The short ones, however, are not as interesting and dull.

### Issues during design/implementation

The biggest problem I encountered in the implementation was the data itself; the data lacked description and also the meaning of the individual attributes. The description would be very useful in the analysis. It very complicates the choice of other methods for analyzing and choosing what to do.