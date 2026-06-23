#!/usr/bin/env python3
"""
Fetch Press Freedom Index data from Our World in Data API
and export to JSON for React dashboard.

Usage:
    python fetch_live_data.py                    # Default output: src/data.js
    python fetch_live_data.py --output dist/data.js  # Custom output
    python fetch_live_data.py --refresh         # Force refresh (ignore cache)
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
OWID_API_URL = "https://ourworldindata.org/grapher/press-freedom-index-rsf.csv"
OWID_PARAMS = {
    'v': '1',
    'csvType': 'full',
    'useColumnShortNames': 'false'
}

# Region mapping (European focus)
REGION_MAPPING = {
    # Northern Europe / Nordic
    'Norway': 'Northern Europe',
    'Sweden': 'Northern Europe',
    'Denmark': 'Northern Europe',
    'Finland': 'Northern Europe',
    'Iceland': 'Northern Europe',
    
    # Baltics
    'Lithuania': 'Northern Europe',
    'Latvia': 'Northern Europe',
    'Estonia': 'Northern Europe',
    
    # British Isles
    'United Kingdom': 'Northern Europe',
    'Ireland': 'Northern Europe',
    
    # Western Europe
    'Germany': 'Western Europe',
    'France': 'Western Europe',
    'Netherlands': 'Western Europe',
    'Belgium': 'Western Europe',
    'Luxembourg': 'Western Europe',
    'Austria': 'Western Europe',
    'Switzerland': 'Western Europe',
    
    # Southern Europe
    'Spain': 'Southern Europe',
    'Italy': 'Southern Europe',
    'Greece': 'Southern Europe',
    'Portugal': 'Southern Europe',
    'Cyprus': 'Southern Europe',
    'Malta': 'Southern Europe',
    
    # Eastern Europe / Central Europe
    'Poland': 'Eastern Europe',
    'Hungary': 'Eastern Europe',
    'Romania': 'Eastern Europe',
    'Bulgaria': 'Eastern Europe',
    'Czechia': 'Eastern Europe',
    'Czech Republic': 'Eastern Europe',
    'Slovakia': 'Eastern Europe',
    'Slovenia': 'Eastern Europe',
    'Croatia': 'Eastern Europe',
    'Serbia': 'Eastern Europe',
    'Bosnia and Herzegovina': 'Eastern Europe',
    'Albania': 'Eastern Europe',
    'North Macedonia': 'Eastern Europe',
    'Moldova': 'Eastern Europe',
    'Ukraine': 'Eastern Europe',
    'Georgia': 'Eastern Europe',
    'Armenia': 'Eastern Europe',
    
    # Rest of world (for context)
    'United States': 'Americas',
    'Canada': 'Americas',
    'Mexico': 'Americas',
    'Brazil': 'Americas',
    'Chile': 'Americas',
    'Argentina': 'Americas',
    'Japan': 'Asia-Pacific',
    'South Korea': 'Asia-Pacific',
    'Australia': 'Asia-Pacific',
    'New Zealand': 'Asia-Pacific',
    'Taiwan': 'Asia-Pacific',
    'India': 'Asia-Pacific',
    'South Africa': 'Africa',
    'Kenya': 'Africa',
    'Ghana': 'Africa',
    'Israel': 'Middle East',
    'Lebanon': 'Middle East',
}

def fetch_data_from_api():
    """Fetch Press Freedom Index data from Our World in Data API."""
    logger.info("📡 Fetching data from Our World in Data API...")
    logger.info(f"   URL: {OWID_API_URL}")
    
    try:
        response = requests.get(
            OWID_API_URL,
            params=OWID_PARAMS,
            headers={
                'User-Agent': 'Press Freedom Analytics Dashboard/1.0 (https://github.com/lant96/press-freedom-analytics)',
                'Accept': 'text/csv'
            },
            timeout=10
        )
        response.raise_for_status()
        
        # Parse CSV
        df = pd.read_csv(pd.io.common.StringIO(response.text))
        logger.info(f"✅ Downloaded {len(df):,} data points")
        logger.info(f"   Columns: {list(df.columns)}")
        logger.info(f"   Date range: {df['Year'].min():.0f} - {df['Year'].max():.0f}")
        logger.info(f"   Countries: {df['Entity'].nunique()}")
        
        return df
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Error parsing data: {e}")
        return None

def process_data(df):
    """Process raw data into structure for React dashboard."""
    logger.info("\n🔄 Processing data...")
    
    # Find the correct column name for the index
    index_cols = [col for col in df.columns if 'press freedom' in col.lower() or 'index' in col.lower()]
    if not index_cols:
        logger.error("❌ Could not find Press Freedom Index column")
        logger.info(f"   Available columns: {list(df.columns)}")
        return None
    
    index_col = index_cols[0]
    logger.info(f"   Using column: '{index_col}'")
    
    # Pivot: countries as rows, years as columns
    pivot_data = {}
    
    for _, row in df.iterrows():
        country = row['Entity']
        year = int(row['Year'])
        score = row[index_col]
        
        # Skip if no score or country not in mapping
        if pd.isna(score) or country not in REGION_MAPPING:
            continue
        
        if country not in pivot_data:
            pivot_data[country] = {
                'country': country,
                'region': REGION_MAPPING[country],
                'subregion': 'Europe' if REGION_MAPPING[country] != 'Other' else 'Other',
            }
        
        pivot_data[country][year] = round(float(score), 2)
    
    # Convert to sorted list
    data_list = list(pivot_data.values())
    data_list.sort(key=lambda x: (x['region'], x['country']))
    
    logger.info(f"✅ Processed {len(data_list)} countries")
    
    # Show sample data
    if data_list:
        sample = data_list[0]
        years = sorted([k for k in sample.keys() if isinstance(k, int)])
        logger.info(f"   Sample: {sample['country']} ({sample['region']})")
        if years:
            logger.info(f"   Years available: {years[0]}-{years[-1]}")
    
    return data_list

def export_to_javascript(data, output_path='src/data.js'):
    """Export processed data as JavaScript ES6 module."""
    logger.info(f"\n💾 Exporting to JavaScript...")
    logger.info(f"   Path: {output_path}")
    
    # Ensure directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate JavaScript module
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    
    output_content = f'''// Press Freedom Index Dataset
// Source: Reporters Without Borders (RSF) via Our World in Data
// Last updated: {timestamp}
// URL: https://ourworldindata.org/grapher/press-freedom-index-rsf
//
// License: CC BY 4.0
// Attribution: Our World in Data / Reporters Without Borders

export const pressFreedomeData = {json.dumps(data, indent=2)};

export const regions = [
  {{ name: 'Northern Europe', color: '#2e7d32' }},
  {{ name: 'Western Europe', color: '#558b2f' }},
  {{ name: 'Southern Europe', color: '#f57f17' }},
  {{ name: 'Eastern Europe', color: '#d32f2f' }},
  {{ name: 'Asia-Pacific', color: '#1565c0' }},
  {{ name: 'Americas', color: '#6a1b9a' }},
  {{ name: 'Africa', color: '#f57c00' }},
  {{ name: 'Middle East', color: '#00796b' }},
];

export const metadata = {{
  source: 'Reporters Without Borders (RSF)',
  dataProvider: 'Our World in Data',
  lastUpdated: '{timestamp}',
  sourceUrl: 'https://ourworldindata.org/grapher/press-freedom-index-rsf',
  countries: {len(data)},
}};

// Get countries by region
export const getCountriesByRegion = (region) => {{
  return pressFreedomeData.filter(c => c.region === region);
}};

// Get time series for a country
export const getCountryTimeSeries = (country) => {{
  const data = pressFreedomeData.find(c => c.country === country);
  if (!data) return [];
  const years = Object.keys(data)
    .filter(k => !isNaN(parseInt(k)))
    .map(k => parseInt(k))
    .sort((a, b) => a - b);
  return years.map(year => ({{
    year,
    score: data[year]
  }}));
}};

// Get regional trends over time
export const getRegionalTrends = () => {{
  const years = new Set();
  const regionTrends = {{}};
  
  // Collect all years
  pressFreedomeData.forEach(d => {{
    Object.keys(d).forEach(k => {{
      if (!isNaN(parseInt(k))) years.add(parseInt(k));
    }});
  }});
  
  const sortedYears = Array.from(years).sort();
  
  // Calculate regional averages per year
  regions.forEach(r => {{
    regionTrends[r.name] = {{}};
    const regionCountries = pressFreedomeData.filter(c => c.region === r.name);
    
    sortedYears.forEach(year => {{
      const scores = regionCountries
        .map(c => c[year])
        .filter(s => typeof s === 'number');
      if (scores.length > 0) {{
        const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
        regionTrends[r.name][year] = parseFloat(avg.toFixed(2));
      }}
    }});
  }});
  
  return regionTrends;
}};

// Detect improving/declining trends
export const detectTrends = () => {{
  const trends = {{}};
  
  pressFreedomeData.forEach(country => {{
    const years = Object.keys(country)
      .filter(k => !isNaN(parseInt(k)))
      .map(k => parseInt(k))
      .sort((a, b) => a - b);
    
    if (years.length >= 2) {{
      const firstScore = country[years[0]];
      const lastScore = country[years[years.length - 1]];
      const change = lastScore - firstScore;
      const percentChange = ((change / firstScore) * 100);
      
      trends[country.country] = {{
        change: parseFloat(change.toFixed(2)),
        percentChange: parseFloat(percentChange.toFixed(1)),
        direction: change < -1 ? 'improving' : change > 1 ? 'declining' : 'stable',
        years: `${{years[0]}}-${{years[years.length - 1]}}`
      }};
    }}
  }});
  
  return trends;
}};
'''
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        logger.info(f"✅ Exported {len(data)} countries to {output_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error writing file: {e}")
        return False

def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Fetch Press Freedom Index data and export for React dashboard'
    )
    parser.add_argument(
        '--output', '-o',
        default='src/data.js',
        help='Output JavaScript file path (default: src/data.js)'
    )
    parser.add_argument(
        '--refresh',
        action='store_true',
        help='Force refresh (ignore cache)'
    )
    
    args = parser.parse_args()
    
    logger.info("="*70)
    logger.info("Press Freedom Analytics - Data Fetch Script")
    logger.info("="*70)
    
    # Fetch data
    df = fetch_data_from_api()
    if df is None:
        logger.error("\n❌ Failed to fetch data. Cannot proceed.")
        return 1
    
    # Process data
    data = process_data(df)
    if data is None or len(data) == 0:
        logger.error("\n❌ No data to process. Cannot proceed.")
        return 1
    
    # Export
    success = export_to_javascript(data, args.output)
    if not success:
        logger.error("\n❌ Export failed.")
        return 1
    
    # Success summary
    logger.info("\n" + "="*70)
    logger.info("✅ SUCCESS - Data ready for dashboard")
    logger.info("="*70)
    logger.info(f"Next steps:")
    logger.info(f"  1. npm run dev        # Start development server")
    logger.info(f"  2. http://localhost:5173  # Open dashboard")
    logger.info(f"\nData attribution:")
    logger.info(f"  © Reporters Without Borders (RSF)")
    logger.info(f"  Data: https://ourworldindata.org/grapher/press-freedom-index-rsf")
    logger.info(f"  License: CC BY 4.0")
    logger.info("="*70)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
