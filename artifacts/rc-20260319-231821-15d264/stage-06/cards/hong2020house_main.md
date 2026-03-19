# Random Forest vs OLS Hedonic Models for Mass Appraisal of Apartments in Gangnam, South Korea

## Cite_Key
hong2020house

## Problem
Mass appraisal for real estate taxation relies traditionally on hedonic OLS regression models whose stability and predictive accuracy have been questioned, especially in complex and nonlinear housing markets such as Gangnam, Seoul.

## Method
Compare a Random Forest (RF) house price predictor against a conventional OLS-based hedonic pricing model. Use the same feature set and transaction dataset; train RF and OLS on 40% of all apartment transactions in the study area (2006–2017), then evaluate predictive performance out-of-sample via percentage deviation between predicted and actual sale prices and probability of predictions falling within predefined error bands.

## Data
Apartment transaction records from Gangnam district, Seoul, South Korea, covering years 2006–2017; sample uses 40% of all transactions in the area (exact N not stated in abstract). Features are typical hedonic attributes of apartments (structural, locational, and temporal variables).

## Metrics
1) Mean (average) percentage deviation between predicted and actual transaction prices. 2) Probability that prediction error lies within ±5% of actual market price (share of cases).

## Findings
1) The RF predictor achieved an average percentage deviation of ~5.5% between predicted and actual prices, compared with ~20% for the OLS hedonic model. 2) The probability that the predicted price was within ±5% of actual market price was 72% for RF versus ~17.5% for OLS. 3) Results suggest that RF better captures complex and nonlinear patterns in the housing market than linear OLS, making RF a strong complementary tool for mass appraisal.

## Limitations
1) Single-case study in one high-demand, developed district (Gangnam) may limit generalizability to other housing markets or property types. 2) Only one machine learning method (Random Forest) is benchmarked against a single baseline (OLS hedonic regression), excluding other advanced models. 3) Potential sensitivity to feature engineering, temporal market shifts, and data quality is not detailed in the abstract. 4) Use of 40% of transactions (sampling strategy) could introduce selection effects if not strictly random.

## Citation
Hong, J., Choi, H., & Kim, W. (2020). A HOUSE PRICE VALUATION BASED ON THE RANDOM FOREST APPROACH: THE MASS APPRAISAL OF RESIDENTIAL PROPERTY IN SOUTH KOREA. International Journal of Strategic Property Management. https://doi.org/10.3846/ijspm.2020.11544
