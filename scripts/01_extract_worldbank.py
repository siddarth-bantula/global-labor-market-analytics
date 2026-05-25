# 01_extract_worldbank.py
# Project : Global Labour Market Analytics (US vs India vs Germany)
# Purpose : Extract labour market data from World Bank API (ILO modelled estimates)
# Author  : Siddarth Bantula

import os
import wbgapi as wb
import pandas as pd

# Configuration

COUNTRIES  = ['USA', 'IND', 'DEU']
START_YEAR = 2000
END_YEAR   = 2023
YEARS      = range(START_YEAR, END_YEAR + 1)

# World Bank indicator codes
INDICATORS = {
    'unemployment_rate'      : 'SL.UEM.TOTL.ZS',
    'labour_participation'   : 'SL.TLF.ACTI.ZS',
    'female_participation'   : 'SL.TLF.ACTI.FE.ZS',
    'employment_ratio'       : 'SL.EMP.TOTL.SP.ZS',
    'youth_unemployment'     : 'SL.UEM.1524.ZS',
    'vulnerable_employment'  : 'SL.EMP.VULN.ZS',
    'gni_per_capita'         : 'NY.GNP.PCAP.PP.CD',
}

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'raw')

# Functions

def fetch_indicator(name, code):
    """
    Pulls one World Bank indicator for our three countries and year range.
    Returns a clean DataFrame with columns: country, year, value, indicator_name
    Returns None if the pull fails.
    """
    print(f'\nFetching: {name} ({code})')

    try:
        # Pull data using wbgapi — returns a DataFrame indexed by country
        df = wb.data.DataFrame(code, COUNTRIES, time=YEARS)

        # DataFrame comes with years as columns (YR2000, YR2001...)
        # and countries as rows — we need to reshape it to long format
        df = df.reset_index()
        df = df.melt(id_vars='economy', var_name='year', value_name='value')

        # Clean the year column — remove 'YR' prefix and convert to integer
        df['year'] = df['year'].str.replace('YR', '').astype(int)

        # Rename economy to country for clarity
        df = df.rename(columns={'economy': 'country'})

        # Add indicator name so we know what this data represents
        df['indicator'] = name

        # Drop rows where value is missing
        df = df.dropna(subset=['value'])

        print(f'  Rows pulled : {len(df):,}')
        print(f'  Countries   : {df["country"].unique().tolist()}')
        print(f'  Year range  : {df["year"].min()} – {df["year"].max()}')

        return df

    except Exception as e:
        print(f'  ERROR: Could not fetch {code} — {e}')
        return None


def save_raw(df, name):
    #Saves the DataFrame as a CSV file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f'{name}.csv')
    df.to_csv(filepath, index=False)
    print(f'  Saved to : {filepath}')


# Main

def main():
    print('=' * 60)
    print('World Bank Data Extraction Started')
    print(f'Countries  : {", ".join(COUNTRIES)}')
    print(f'Year Range : {START_YEAR} to {END_YEAR}')
    print(f'Indicators : {len(INDICATORS)}')
    print('=' * 60)

    success = []
    failed  = []

    for name, code in INDICATORS.items():
        df = fetch_indicator(name, code)

        if df is not None and not df.empty:
            save_raw(df, name)
            success.append(name)
        else:
            print(f'  Skipped: {name}')
            failed.append(name)

    print('\n' + '=' * 60)
    print('Extraction Complete')
    print(f'  Successful : {len(success)} of {len(INDICATORS)} indicators')
    if failed:
        print(f'  Failed     : {failed}')
    print('=' * 60)


if __name__ == '__main__':
    main()