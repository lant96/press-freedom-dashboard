#!/usr/bin/env python3
"""
Convert RSF World Press Freedom Index Excel data to JSON for React dashboard

Usage:
    python convert_data.py --input "data/rsf_2024.xlsx" --output "src/data.js"

This script:
1. Reads multi-year World Press Freedom Index data from Excel
2. Extracts country names, codes, regions, and annual scores
3. Validates data quality and handles missing values
4. Generates optimized JSON for frontend consumption
5. Exports helper functions for data aggregation
"""

import pandas as pd
import json
import argparse
from pathlib import Path
import sys

def validate_data(df):
    """Validate data quality and completeness."""
    print("\n" + "="*70)
    print("DATA VALIDATION")
    print("="*70)
    
    # Check required columns
    required_cols = ['Country', 'Country Code ISO3']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"⚠️  Missing required columns: {missing_cols}")
        return False
    
    # Check for duplicates
    duplicates = df[df.duplicated(subset=['Country Code ISO3'], keep=False)]
    if len(duplicates) > 0:
        print(f"⚠️  Found {len(duplicates)} duplicate countries (check data)")
    
    # Data coverage
    print(f"✅ Total rows: {len(df)}")
    print(f"✅ Total columns: {len(df.columns)}")
    print(f"✅ Countries: {df['Country'].nunique()}")
    
    return True

def extract_countries(df, years=[2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]):
    """Extract country data with annual scores."""
    
    data_for_export = []
    
    for idx, row in df.iterrows():
        # Skip regional aggregates (check for valid ISO code)
        if pd.isna(row.get('Country Code ISO3')):
            continue
        
        country_data = {
            'country': row['Country'],
            'code': row['Country Code ISO3'],
            'region': row.get('Region', 'Unclassified'),
            'subregion': row.get('Subregion', 'Unclassified'),
        }
        
        # Extract annual scores
        score_found = False
        for year in years:
            col_name = f'{year}'  # Adjust column name if needed
            # Try alternative column names
            if col_name in df.columns and pd.notna(row[col_name]):
                country_data[year] = float(row[col_name])
                score_found = True
            elif f'Score {year}' in df.columns and pd.notna(row[f'Score {year}']):
                country_data[year] = float(row[f'Score {year}'])
                score_found = True
            elif f'Index {year}' in df.columns and pd.notna(row[f'Index {year}']):
                country_data[year] = float(row[f'Index {year}'])
                score_found = True
        
        # Only include if we found at least one year of data
        if score_found:
            # Add population if available
            if 'Population' in df.columns and pd.notna(row['Population']):
                country_data['population'] = float(row['Population'])
            elif 'Population 2024' in df.columns and pd.notna(row['Population 2024']):
                country_data['population'] = float(row['Population 2024'])
            
            data_for_export.append(country_data)
    
    return data_for_export

def generate_helper_functions():
    """Generate JavaScript helper functions for data aggregation."""
    
    helpers = """
// Helper: Get countries by region
export const getCountriesByRegion = (region) => {
  return pressFreedomeData.filter(c => c.region === region);
};

// Helper: Get time series for a country
export const getCountryTimeSeries = (country) => {
  const data = pressFreedomeData.find(c => c.country === country);
  if (!data) return [];
  const years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
  return years.map(year => ({ 
    year, 
    score: data[year] || null 
  })).filter(d => d.score !== null);
};

// Helper: Get regional averages by year
export const getRegionalTrends = () => {
  const years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
  const regions = [...new Set(pressFreedomeData.map(c => c.region))];
  const trends = {};
  
  regions.forEach(region => {
    trends[region] = {};
    const countries = getCountriesByRegion(region);
    years.forEach(year => {
      const scores = countries
        .map(c => c[year])
        .filter(s => s !== undefined);
      if (scores.length > 0) {
        const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
        trends[region][year] = parseFloat(avg.toFixed(2));
      }
    });
  });
  
  return trends;
};

// Helper: Get countries by score range
export const getCountriesByScoreRange = (minScore, maxScore, year = 2024) => {
  return pressFreedomeData
    .filter(c => {
      const score = c[year];
      return score !== undefined && score >= minScore && score <= maxScore;
    })
    .sort((a, b) => a[year] - b[year]);
};

// Helper: Detect trends (improving/declining)
export const detectTrends = (minYears = 3) => {
  const trends = {};
  
  pressFreedomeData.forEach(country => {
    const years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
      .filter(y => country[y] !== undefined);
    
    if (years.length >= minYears) {
      const firstYear = country[years[0]];
      const lastYear = country[years[years.length - 1]];
      const change = lastYear - firstYear;
      
      trends[country.country] = {
        change: parseFloat(change.toFixed(2)),
        direction: change < -1 ? 'improving' : change > 1 ? 'declining' : 'stable',
        percentChange: parseFloat(((change / firstYear) * 100).toFixed(1))
      };
    }
  });
  
  return trends;
};
"""
    
    return helpers

def export_to_javascript(data, output_path):
    """Export data as JavaScript module."""
    
    # Calculate metadata
    regions_list = sorted(list(set(d['region'] for d in data if 'region' in d)))
    years_covered = sorted(list(set(
        year for d in data 
        for year in [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024] 
        if year in d
    )))
    
    # Sort by region, then by country
    data_sorted = sorted(data, key=lambda x: (x.get('region', ''), x.get('country', '')))
    
    # Build the output
    output = """// World Press Freedom Index Dataset
// Generated from RSF data using convert_data.py
// Source: Reporters Without Borders (https://rsf.org/)
// Last updated: 2024

export const pressFreedomeData = """
    
    output += json.dumps(data_sorted, indent=2)
    
    output += f""";

// Region definitions
export const regions = [
{json.dumps([{'name': r, 'color': '#666'} for r in regions_list], indent=2)[1:-1]}
];

// Metadata
export const metadata = {{
  sourceUrl: 'https://rsf.org/',
  source: 'Reporters Without Borders World Press Freedom Index',
  yearsCovered: {years_covered},
  countryCount: {len(data)},
  lastUpdated: '2024'
}};

"""
    
    output += generate_helper_functions()
    
    # Write to file
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    return len(data)

def main():
    parser = argparse.ArgumentParser(
        description='Convert RSF World Press Freedom Index to JSON for React dashboard'
    )
    parser.add_argument(
        '--input', '-i',
        default='data/rsf_world_press_freedom_index.xlsx',
        help='Path to input Excel file'
    )
    parser.add_argument(
        '--output', '-o',
        default='src/data.js',
        help='Path to output JavaScript file'
    )
    parser.add_argument(
        '--sheet',
        default='Sheet1',
        help='Excel sheet name'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input).exists():
        print(f"❌ Error: Input file not found: {args.input}")
        print("\nExpected file structure:")
        print("  data/rsf_world_press_freedom_index.xlsx")
        print("\nColumns should include:")
        print("  - Country (country name)")
        print("  - Country Code ISO3 (3-letter code)")
        print("  - Region (geographic region)")
        print("  - 2024, 2023, 2022, ... (annual scores)")
        sys.exit(1)
    
    try:
        # Load data
        print(f"\n📖 Loading data from: {args.input}")
        df = pd.read_excel(args.input, sheet_name=args.sheet)
        
        # Validate
        if not validate_data(df):
            sys.exit(1)
        
        # Extract
        print("\n🔄 Extracting country data...")
        countries = extract_countries(df)
        print(f"✅ Extracted {len(countries)} countries")
        
        # Export
        print(f"\n💾 Exporting to JavaScript: {args.output}")
        count = export_to_javascript(countries, args.output)
        
        # Summary
        print("\n" + "="*70)
        print("EXPORT COMPLETE ✅")
        print("="*70)
        print(f"✅ {count} countries exported")
        print(f"✅ Output: {args.output}")
        print(f"✅ Ready for React dashboard\n")
        
        # Sample
        print("Sample data:")
        sample = json.dumps(countries[0], indent=2)
        print(sample)
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
