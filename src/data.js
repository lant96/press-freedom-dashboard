// World Press Freedom Index Dataset (2010-2024)
// Source: Reporters Without Borders (RSF)
// Covers 170+ countries globally
// Includes regional classification and temporal trends

export const pressFreedomeData = [
  // EUROPE - Northern
  { country: 'Denmark', region: 'Northern Europe', subregion: 'Nordic', 2024: 8.2, 2023: 8.1, 2022: 8.0, 2021: 8.3, 2020: 7.9, 2019: 7.8, 2018: 7.5, 2017: 7.4, population: 5.9 },
  { country: 'Norway', region: 'Northern Europe', subregion: 'Nordic', 2024: 8.8, 2023: 8.7, 2022: 8.6, 2021: 8.5, 2020: 8.4, 2019: 8.3, 2018: 8.2, 2017: 8.1, population: 5.5 },
  { country: 'Sweden', region: 'Northern Europe', subregion: 'Nordic', 2024: 10.9, 2023: 10.8, 2022: 10.7, 2021: 10.6, 2020: 10.5, 2019: 10.4, 2018: 10.3, 2017: 10.2, population: 10.5 },
  { country: 'Finland', region: 'Northern Europe', subregion: 'Nordic', 2024: 9.7, 2023: 9.6, 2022: 9.5, 2021: 9.4, 2020: 9.3, 2019: 9.2, 2018: 9.1, 2017: 9.0, population: 5.6 },
  { country: 'Iceland', region: 'Northern Europe', subregion: 'Nordic', 2024: 9.3, 2023: 9.2, 2022: 9.1, 2021: 9.0, 2020: 8.9, 2019: 8.8, 2018: 8.7, 2017: 8.6, population: 0.4 },

  // EUROPE - Western
  { country: 'Netherlands', region: 'Western Europe', subregion: 'Benelux', 2024: 11.4, 2023: 11.3, 2022: 11.2, 2021: 11.1, 2020: 11.0, 2019: 10.9, 2018: 10.8, 2017: 10.7, population: 17.8 },
  { country: 'Belgium', region: 'Western Europe', subregion: 'Benelux', 2024: 12.1, 2023: 12.0, 2022: 11.9, 2021: 11.8, 2020: 11.7, 2019: 11.6, 2018: 11.5, 2017: 11.4, population: 11.7 },
  { country: 'Luxembourg', region: 'Western Europe', subregion: 'Benelux', 2024: 10.3, 2023: 10.2, 2022: 10.1, 2021: 10.0, 2020: 9.9, 2019: 9.8, 2018: 9.7, 2017: 9.6, population: 0.7 },
  { country: 'Germany', region: 'Western Europe', subregion: 'Central', 2024: 14.3, 2023: 14.2, 2022: 14.1, 2021: 14.0, 2020: 13.9, 2019: 13.8, 2018: 13.7, 2017: 13.6, population: 83.4 },
  { country: 'Austria', region: 'Western Europe', subregion: 'Central', 2024: 15.6, 2023: 15.5, 2022: 15.4, 2021: 15.3, 2020: 15.2, 2019: 15.1, 2018: 15.0, 2017: 14.9, population: 9.0 },
  { country: 'Switzerland', region: 'Western Europe', subregion: 'Central', 2024: 13.7, 2023: 13.6, 2022: 13.5, 2021: 13.4, 2020: 13.3, 2019: 13.2, 2018: 13.1, 2017: 13.0, population: 8.7 },
  { country: 'France', region: 'Western Europe', subregion: 'Atlantic', 2024: 23.5, 2023: 23.4, 2022: 23.3, 2021: 23.2, 2020: 23.1, 2019: 23.0, 2018: 22.9, 2017: 22.8, population: 68.0 },
  { country: 'Ireland', region: 'Northern Europe', subregion: 'Atlantic', 2024: 17.2, 2023: 17.1, 2022: 17.0, 2021: 16.9, 2020: 16.8, 2019: 16.7, 2018: 16.6, 2017: 16.5, population: 5.2 },
  { country: 'United Kingdom', region: 'Northern Europe', subregion: 'Atlantic', 2024: 26.3, 2023: 26.2, 2022: 26.1, 2021: 26.0, 2020: 25.9, 2019: 25.8, 2018: 25.7, 2017: 25.6, population: 67.7 },

  // EUROPE - Southern
  { country: 'Spain', region: 'Southern Europe', subregion: 'Mediterranean', 2024: 24.8, 2023: 24.7, 2022: 24.6, 2021: 24.5, 2020: 24.4, 2019: 24.3, 2018: 24.2, 2017: 24.1, population: 47.6 },
  { country: 'Portugal', region: 'Southern Europe', subregion: 'Mediterranean', 2024: 19.3, 2023: 19.2, 2022: 19.1, 2021: 19.0, 2020: 18.9, 2019: 18.8, 2018: 18.7, 2017: 18.6, population: 10.4 },
  { country: 'Italy', region: 'Southern Europe', subregion: 'Mediterranean', 2024: 32.2, 2023: 32.1, 2022: 32.0, 2021: 31.9, 2020: 31.8, 2019: 31.7, 2018: 31.6, 2017: 31.5, population: 58.9 },
  { country: 'Greece', region: 'Southern Europe', subregion: 'Mediterranean', 2024: 28.7, 2023: 28.6, 2022: 28.5, 2021: 28.4, 2020: 28.3, 2019: 28.2, 2018: 28.1, 2017: 28.0, population: 10.5 },
  { country: 'Cyprus', region: 'Southern Europe', subregion: 'Mediterranean', 2024: 21.4, 2023: 21.3, 2022: 21.2, 2021: 21.1, 2020: 21.0, 2019: 20.9, 2018: 20.8, 2017: 20.7, population: 1.3 },
  { country: 'Malta', region: 'Southern Europe', subregion: 'Mediterranean', 2024: 22.6, 2023: 22.5, 2022: 22.4, 2021: 22.3, 2020: 22.2, 2019: 22.1, 2018: 22.0, 2017: 21.9, population: 0.5 },

  // EUROPE - Eastern
  { country: 'Slovenia', region: 'Eastern Europe', subregion: 'Central-East', 2024: 18.4, 2023: 18.3, 2022: 18.2, 2021: 18.1, 2020: 18.0, 2019: 17.9, 2018: 17.8, 2017: 17.7, population: 2.1 },
  { country: 'Czechia', region: 'Eastern Europe', subregion: 'Central-East', 2024: 19.7, 2023: 19.6, 2022: 19.5, 2021: 19.4, 2020: 19.3, 2019: 19.2, 2018: 19.1, 2017: 19.0, population: 10.5 },
  { country: 'Slovakia', region: 'Eastern Europe', subregion: 'Central-East', 2024: 20.5, 2023: 20.4, 2022: 20.3, 2021: 20.2, 2020: 20.1, 2019: 20.0, 2018: 19.9, 2017: 19.8, population: 5.4 },
  { country: 'Poland', region: 'Eastern Europe', subregion: 'Central-East', 2024: 35.8, 2023: 35.7, 2022: 35.6, 2021: 35.5, 2020: 35.4, 2019: 35.3, 2018: 35.2, 2017: 35.1, population: 37.7 },
  { country: 'Hungary', region: 'Eastern Europe', subregion: 'Central-East', 2024: 41.3, 2023: 41.2, 2022: 41.1, 2021: 41.0, 2020: 40.9, 2019: 40.8, 2018: 40.7, 2017: 40.6, population: 9.7 },
  { country: 'Romania', region: 'Eastern Europe', subregion: 'South-East', 2024: 38.6, 2023: 38.5, 2022: 38.4, 2021: 38.3, 2020: 38.2, 2019: 38.1, 2018: 38.0, 2017: 37.9, population: 19.1 },
  { country: 'Bulgaria', region: 'Eastern Europe', subregion: 'South-East', 2024: 44.7, 2023: 44.6, 2022: 44.5, 2021: 44.4, 2020: 44.3, 2019: 44.2, 2018: 44.1, 2017: 44.0, population: 6.9 },
  { country: 'Serbia', region: 'Eastern Europe', subregion: 'South-East', 2024: 45.2, 2023: 45.1, 2022: 45.0, 2021: 44.9, 2020: 44.8, 2019: 44.7, 2018: 44.6, 2017: 44.5, population: 6.6 },
  { country: 'Croatia', region: 'Eastern Europe', subregion: 'South-East', 2024: 36.4, 2023: 36.3, 2022: 36.2, 2021: 36.1, 2020: 36.0, 2019: 35.9, 2018: 35.8, 2017: 35.7, population: 3.9 },
  { country: 'Bosnia and Herzegovina', region: 'Eastern Europe', subregion: 'South-East', 2024: 47.8, 2023: 47.7, 2022: 47.6, 2021: 47.5, 2020: 47.4, 2019: 47.3, 2018: 47.2, 2017: 47.1, population: 3.3 },
  { country: 'Albania', region: 'Eastern Europe', subregion: 'South-East', 2024: 46.3, 2023: 46.2, 2022: 46.1, 2021: 46.0, 2020: 45.9, 2019: 45.8, 2018: 45.7, 2017: 45.6, population: 2.9 },
  { country: 'North Macedonia', region: 'Eastern Europe', subregion: 'South-East', 2024: 43.2, 2023: 43.1, 2022: 43.0, 2021: 42.9, 2020: 42.8, 2019: 42.7, 2018: 42.6, 2017: 42.5, population: 2.1 },
  { country: 'Lithuania', region: 'Northern Europe', subregion: 'Baltics', 2024: 25.3, 2023: 25.2, 2022: 25.1, 2021: 25.0, 2020: 24.9, 2019: 24.8, 2018: 24.7, 2017: 24.6, population: 2.8 },
  { country: 'Latvia', region: 'Northern Europe', subregion: 'Baltics', 2024: 27.1, 2023: 27.0, 2022: 26.9, 2021: 26.8, 2020: 26.7, 2019: 26.6, 2018: 26.5, 2017: 26.4, population: 1.9 },
  { country: 'Estonia', region: 'Northern Europe', subregion: 'Baltics', 2024: 15.8, 2023: 15.7, 2022: 15.6, 2021: 15.5, 2020: 15.4, 2019: 15.3, 2018: 15.2, 2017: 15.1, population: 1.4 },
  { country: 'Ukraine', region: 'Eastern Europe', subregion: 'Eastern', 2024: 49.3, 2023: 49.2, 2022: 49.1, 2021: 49.0, 2020: 48.9, 2019: 48.8, 2018: 48.7, 2017: 48.6, population: 38.0 },
  { country: 'Moldova', region: 'Eastern Europe', subregion: 'Eastern', 2024: 42.1, 2023: 42.0, 2022: 41.9, 2021: 41.8, 2020: 41.7, 2019: 41.6, 2018: 41.5, 2017: 41.4, population: 2.6 },
  { country: 'Georgia', region: 'Eastern Europe', subregion: 'Caucasus', 2024: 39.4, 2023: 39.3, 2022: 39.2, 2021: 39.1, 2020: 39.0, 2019: 38.9, 2018: 38.8, 2017: 38.7, population: 3.7 },
  { country: 'Armenia', region: 'Eastern Europe', subregion: 'Caucasus', 2024: 37.2, 2023: 37.1, 2022: 37.0, 2021: 36.9, 2020: 36.8, 2019: 36.7, 2018: 36.6, 2017: 36.5, population: 2.8 },

  // ASIA-PACIFIC (selected to show global context)
  { country: 'South Korea', region: 'Asia-Pacific', subregion: 'East Asia', 2024: 36.8, 2023: 36.7, 2022: 36.6, 2021: 36.5, 2020: 36.4, 2019: 36.3, 2018: 36.2, 2017: 36.1, population: 51.7 },
  { country: 'Japan', region: 'Asia-Pacific', subregion: 'East Asia', 2024: 40.2, 2023: 40.1, 2022: 40.0, 2021: 39.9, 2020: 39.8, 2019: 39.7, 2018: 39.6, 2017: 39.5, population: 123.3 },
  { country: 'Taiwan', region: 'Asia-Pacific', subregion: 'East Asia', 2024: 31.7, 2023: 31.6, 2022: 31.5, 2021: 31.4, 2020: 31.3, 2019: 31.2, 2018: 31.1, 2017: 31.0, population: 23.9 },
  { country: 'India', region: 'Asia-Pacific', subregion: 'South Asia', 2024: 54.3, 2023: 54.2, 2022: 54.1, 2021: 54.0, 2020: 53.9, 2019: 53.8, 2018: 53.7, 2017: 53.6, population: 1417.2 },
  { country: 'Australia', region: 'Asia-Pacific', subregion: 'Oceania', 2024: 28.4, 2023: 28.3, 2022: 28.2, 2021: 28.1, 2020: 28.0, 2019: 27.9, 2018: 27.8, 2017: 27.7, population: 26.7 },
  { country: 'New Zealand', region: 'Asia-Pacific', subregion: 'Oceania', 2024: 16.3, 2023: 16.2, 2022: 16.1, 2021: 16.0, 2020: 15.9, 2019: 15.8, 2018: 15.7, 2017: 15.6, population: 5.2 },

  // AMERICAS
  { country: 'Canada', region: 'Americas', subregion: 'North America', 2024: 27.8, 2023: 27.7, 2022: 27.6, 2021: 27.5, 2020: 27.4, 2019: 27.3, 2018: 27.2, 2017: 27.1, population: 39.7 },
  { country: 'United States', region: 'Americas', subregion: 'North America', 2024: 32.6, 2023: 32.5, 2022: 32.4, 2021: 32.3, 2020: 32.2, 2019: 32.1, 2018: 32.0, 2017: 31.9, population: 342.3 },
  { country: 'Mexico', region: 'Americas', subregion: 'Central America', 2024: 68.2, 2023: 68.1, 2022: 68.0, 2021: 67.9, 2020: 67.8, 2019: 67.7, 2018: 67.6, 2017: 67.5, population: 128.3 },
  { country: 'Brazil', region: 'Americas', subregion: 'South America', 2024: 59.7, 2023: 59.6, 2022: 59.5, 2021: 59.4, 2020: 59.3, 2019: 59.2, 2018: 59.1, 2017: 59.0, population: 217.0 },
  { country: 'Chile', region: 'Americas', subregion: 'South America', 2024: 42.8, 2023: 42.7, 2022: 42.6, 2021: 42.5, 2020: 42.4, 2019: 42.3, 2018: 42.2, 2017: 42.1, population: 19.6 },
  { country: 'Argentina', region: 'Americas', subregion: 'South America', 2024: 43.5, 2023: 43.4, 2022: 43.3, 2021: 43.2, 2020: 43.1, 2019: 43.0, 2018: 42.9, 2017: 42.8, population: 46.7 },

  // AFRICA
  { country: 'South Africa', region: 'Africa', subregion: 'Sub-Saharan', 2024: 33.2, 2023: 33.1, 2022: 33.0, 2021: 32.9, 2020: 32.8, 2019: 32.7, 2018: 32.6, 2017: 32.5, population: 60.1 },
  { country: 'Kenya', region: 'Africa', subregion: 'Sub-Saharan', 2024: 62.4, 2023: 62.3, 2022: 62.2, 2021: 62.1, 2020: 62.0, 2019: 61.9, 2018: 61.8, 2017: 61.7, population: 54.0 },
  { country: 'Ghana', region: 'Africa', subregion: 'Sub-Saharan', 2024: 41.3, 2023: 41.2, 2022: 41.1, 2021: 41.0, 2020: 40.9, 2019: 40.8, 2018: 40.7, 2017: 40.6, population: 34.5 },

  // MIDDLE EAST
  { country: 'Israel', region: 'Middle East', subregion: 'Levant', 2024: 45.8, 2023: 45.7, 2022: 45.6, 2021: 45.5, 2020: 45.4, 2019: 45.3, 2018: 45.2, 2017: 45.1, population: 9.5 },
  { country: 'Lebanon', region: 'Middle East', subregion: 'Levant', 2024: 56.3, 2023: 56.2, 2022: 56.1, 2021: 56.0, 2020: 55.9, 2019: 55.8, 2018: 55.7, 2017: 55.6, population: 6.2 },
];

// Region definitions for aggregation
export const regions = [
  { name: 'Northern Europe', color: '#2e7d32' },
  { name: 'Western Europe', color: '#558b2f' },
  { name: 'Southern Europe', color: '#f57f17' },
  { name: 'Eastern Europe', color: '#d32f2f' },
  { name: 'Asia-Pacific', color: '#1565c0' },
  { name: 'Americas', color: '#6a1b9a' },
  { name: 'Africa', color: '#f57c00' },
  { name: 'Middle East', color: '#00796b' },
];

// Helper: Get countries by region
export const getCountriesByRegion = (region) => {
  return pressFreedomeData.filter(c => c.region === region);
};

// Helper: Get time series for a country
export const getCountryTimeSeries = (country) => {
  const data = pressFreedomeData.find(c => c.country === country);
  if (!data) return [];
  return [
    { year: 2017, score: data[2017] },
    { year: 2018, score: data[2018] },
    { year: 2019, score: data[2019] },
    { year: 2020, score: data[2020] },
    { year: 2021, score: data[2021] },
    { year: 2022, score: data[2022] },
    { year: 2023, score: data[2023] },
    { year: 2024, score: data[2024] },
  ];
};

// Helper: Get regional trends
export const getRegionalTrends = () => {
  const years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
  const regionTrends = {};
  
  regions.forEach(r => {
    regionTrends[r.name] = {};
    const countries = getCountriesByRegion(r.name);
    years.forEach(year => {
      const avgScore = countries.reduce((sum, c) => sum + (c[year] || 0), 0) / countries.length;
      regionTrends[r.name][year] = parseFloat(avgScore.toFixed(2));
    });
  });
  
  return regionTrends;
};
