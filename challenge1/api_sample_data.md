# Sample data for testing

You can use this sample data point from the dataset.

```
pH:  7.258203145845717
Iron:  6.107129837217062e-09
Nitrate:  9.26167580122401
Chloride:  182.2423407530417
Lead:  4.3998520479124295e-224
Zinc:  0.4164775464847408
Color:  Colorless
Turbidity:  0.0478031791644083
Fluoride:  1.0161962374839366
Copper:  0.2980934209430296
Odor:  3.1441986515867457
Sulfate:  114.55142662349748
Conductivity:  160.06255735415195
Chlorine:  2.3250939237169903
Manganese:  6.020679600903066e-16
Total_Dissolved_Solids:  214.5531038247008
Source:  River
Water_Temperature:  15.891904856714174
Air_Temperature:  61.13914033047329
Month:  April
Day:  11.0
Time_of_Day:  4.0

Target:  0
```

## Prediction API JSON schema

For each prediction you'll need a unique object key as an ID and each object value's must be an array of each features. The response will contain the same schema, but the array is now the probability of the classification with exactly two elements (`[probability of the good class, probability of the bad class]`).

Note:

1. All categorical features must be encoded as number. Refer to the `paramters.py` for more details
2. Feature column order is the same as in the above example

Example:

```json
{
   "single":[
      7.258203145845717,
      6.107129837217062e-09,
      9.26167580122401,
      182.2423407530417,
      4.3998520479124295e-224,
      0.4164775464847408,
      2, // parameters.py#COLOR_MAP
      0.0478031791644083,
      1.0161962374839366,
      0.2980934209430296,
      3.1441986515867457,
      114.55142662349748,
      160.06255735415195,
      2.3250939237169903,
      6.020679600903066e-16,
      214.5531038247008,
      1,// parameters.py#SOURCE_MAP
      15.891904856714174,
      61.13914033047329,
      1,// parameters.py#MONTH_MAP
      11.0,
      4.0
   ]
}
```

Using cURL:

```
(base) $ curl --location --request POST 'http://localhost:5000/predict' \
--header 'Content-Type: application/json' \
--data-raw '{
    "single": [7.258203145845717,6.107129837217062e-09,9.26167580122401,182.2423407530417,4.3998520479124295e-224,0.4164775464847408,2,0.0478031791644083,1.0161962374839366,0.2980934209430296,3.1441986515867457,114.55142662349748,160.06255735415195,2.3250939237169903,6.020679600903066e-16,214.5531038247008,1,15.891904856714174,61.13914033047329,1,11.0,4.0]
}'

{"single":[0.5000045723839148,0.4999954276160851]}
```

From the response above we can conclude the prediction is class 0 (good) because the first class probability is higher than the second class (>0.5).
