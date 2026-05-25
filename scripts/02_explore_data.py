
# 02_explore_data.py
# Project : Global Labour Market Analytics (US vs India vs Germany)
# Purpose : Explore raw data before transformation — understand structure,
#           check for missing values, verify ranges and distributions
# Author  : Siddarth Bantula

import os
import pandas as pd

# Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR  = os.path.join(BASE_DIR, 'data', 'raw')

INDICATORS = [
    'unemployment_rate',
    'labour_participation',
    'female_participation',
    'employment_ratio',
    'youth_unemployment',
    'vulnerable_employment',
    'gni_per_capita',
]

COUNTRIES = ['USA', 'IND', 'DEU']

# Functions

def explore_file(name):
    """
    Loads one raw CSV and prints a full diagnostic report:
    structure, missing values, value ranges, and per-country summary.
    """
    filepath = os.path.join(RAW_DIR, f'{name}.csv')
    df = pd.read_csv(filepath)

    print(f'\n{"=" * 60}')
    print(f'INDICATOR: {name}')
    print(f'{"=" * 60}')

    # Basic structure
    print(f'\n--- Structure ---')
    print(f'Rows        : {len(df)}')
    print(f'Columns     : {list(df.columns)}')
    print(f'Data types  :\n{df.dtypes}')

    # Missing values
    print(f'\n--- Missing Values ---')
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.any() else 'No missing values')

    # Value range for the value column
    print(f'\n--- Value Range ---')
    print(f'Min   : {df["value"].min():.2f}')
    print(f'Max   : {df["value"].max():.2f}')
    print(f'Mean  : {df["value"].mean():.2f}')

    # Per country summary
    print(f'\n--- Per Country Summary ---')
    for country in COUNTRIES:
        subset = df[df['country'] == country]
        if not subset.empty:
            print(f'\n  {country}:')
            print(f'    Years     : {subset["year"].min()} – {subset["year"].max()}')
            print(f'    Min value : {subset["value"].min():.2f}')
            print(f'    Max value : {subset["value"].max():.2f}')
            print(f'    Mean value: {subset["value"].mean():.2f}')

    # Sample rows
    print(f'\n--- Sample Rows ---')
    print(df.sample(5).to_string(index=False))


# Main

def main():
    print('=' * 60)
    print('Data Exploration Started')
    print(f'Reading from: {RAW_DIR}')
    print('=' * 60)

    for name in INDICATORS:
        explore_file(name)

    print(f'\n{"=" * 60}')
    print('Exploration Complete')
    print('=' * 60)


if __name__ == '__main__':
    main()