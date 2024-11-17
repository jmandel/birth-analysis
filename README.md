# Birth Delivery Analysis

This code analyzes delivery methods and timing for births to mothers aged 39-42 with normal BMI and masters+ education.

## Data Preparation

1. Download the 2023 Natality Public Use File:
   - Visit the CDC Wonder website
   - Download `nat2023us.zip`

2. Prepare the data file:
   ```bash
   unzip nat2023us.zip
   mv "VS23NATL.DETL.PUB" Nat2023us.txt
   ```

## Sample Results

```
Weekly Delivery Statistics:

Week 34 (Births: 300, 1.5% of population)
  Vaginal Non-Operative-No Induction: 70 (0.3% of population)
  Vaginal Non-Operative-Induced: 37 (0.2% of population)
  Vaginal Operative-No Induction: 1 (0.0% of population)
  Vaginal Operative-Induced: 2 (0.0% of population)
  C-Section-No Induction: 170 (0.8% of population)
  C-Section-Induced: 20 (0.1% of population)

Week 35 (Births: 441, 2.2% of population)
  Vaginal Non-Operative-No Induction: 127 (0.6% of population)
  Vaginal Non-Operative-Induced: 77 (0.4% of population)
  Vaginal Operative-No Induction: 6 (0.0% of population)
  Vaginal Operative-Induced: 7 (0.0% of population)
  C-Section-No Induction: 212 (1.1% of population)
  C-Section-Induced: 12 (0.1% of population)

Week 36 (Births: 1005, 5.0% of population)
  Vaginal Non-Operative-No Induction: 260 (1.3% of population)
  Vaginal Non-Operative-Induced: 173 (0.9% of population)
  Vaginal Operative-No Induction: 13 (0.1% of population)
  Vaginal Operative-Induced: 9 (0.0% of population)
  C-Section-No Induction: 494 (2.5% of population)
  C-Section-Induced: 55 (0.3% of population)

Week 37 (Births: 2232, 11.2% of population)
  Vaginal Non-Operative-No Induction: 628 (3.1% of population)
  Vaginal Non-Operative-Induced: 452 (2.3% of population)
  Vaginal Operative-No Induction: 40 (0.2% of population)
  Vaginal Operative-Induced: 27 (0.1% of population)
  C-Section-No Induction: 964 (4.8% of population)
  C-Section-Induced: 120 (0.6% of population)

Week 38 (Births: 3910, 19.5% of population)
  Vaginal Non-Operative-No Induction: 1505 (7.5% of population)
  Vaginal Non-Operative-Induced: 792 (4.0% of population)
  Vaginal Operative-No Induction: 71 (0.4% of population)
  Vaginal Operative-Induced: 43 (0.2% of population)
  C-Section-No Induction: 1323 (6.6% of population)
  C-Section-Induced: 174 (0.9% of population)

Week 39 (Births: 7715, 38.6% of population)
  Vaginal Non-Operative-No Induction: 2214 (11.1% of population)
  Vaginal Non-Operative-Induced: 2249 (11.2% of population)
  Vaginal Operative-No Induction: 118 (0.6% of population)
  Vaginal Operative-Induced: 158 (0.8% of population)
  C-Section-No Induction: 2473 (12.4% of population)
  C-Section-Induced: 491 (2.5% of population)

Week 40 (Births: 3067, 15.3% of population)
  Vaginal Non-Operative-No Induction: 1212 (6.1% of population)
  Vaginal Non-Operative-Induced: 888 (4.4% of population)
  Vaginal Operative-No Induction: 68 (0.3% of population)
  Vaginal Operative-Induced: 78 (0.4% of population)
  C-Section-No Induction: 546 (2.7% of population)
  C-Section-Induced: 263 (1.3% of population)

Week 41 (Births: 993, 5.0% of population)
  Vaginal Non-Operative-No Induction: 407 (2.0% of population)
  Vaginal Non-Operative-Induced: 259 (1.3% of population)
  Vaginal Operative-No Induction: 13 (0.1% of population)
  Vaginal Operative-Induced: 22 (0.1% of population)
  C-Section-No Induction: 199 (1.0% of population)
  C-Section-Induced: 93 (0.5% of population)

Week 42 (Births: 342, 1.7% of population)
  Vaginal Non-Operative-No Induction: 125 (0.6% of population)
  Vaginal Non-Operative-Induced: 73 (0.4% of population)
  Vaginal Operative-No Induction: 6 (0.0% of population)
  Vaginal Operative-Induced: 5 (0.0% of population)
  C-Section-No Induction: 98 (0.5% of population)
  C-Section-Induced: 35 (0.2% of population)
```

## Data Source

Data from the 2023 Natality Public Use File, National Center for Health Statistics. The file contains birth certificate data for all US births in 2023.

Key fields used:
- Mother's age (MAGER)
- Mother's Education (MEDUC)
- BMI Category (BMI_R)
- Gestation (COMBGEST)
- Delivery Route (ME_ROUT)
- Induction Status (LD_INDL)
