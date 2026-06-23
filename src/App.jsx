import React, { useState, useMemo, useCallback } from 'react';
import {
  BarChart, Bar, LineChart, Line, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  ComposedChart, Area
} from 'recharts';
import { pressFreedomeData, regions, getCountriesByRegion, getRegionalTrends } from './data';
import './App.css';

// Simple map SVG (you can replace with actual library like react-map-gl later)
const EuropeMap = ({ selectedRegion, onCountryClick, data }) => {
  const getColor = (score) => {
    if (score <= 15) return '#2e7d32'; // Green - best
    if (score <= 30) return '#558b2f';
    if (score <= 45) return '#f57f17';
    return '#d32f2f'; // Red - worst
  };

  return (
    <div className="map-container">
      <svg viewBox="0 0 1000 600" className="europe-map">
        {/* Simple Europe outline - simplified representation */}
        <text x="500" y="300" textAnchor="middle" className="map-placeholder">
          🗺️ Interactive Map
        </text>
        <text x="500" y="330" textAnchor="middle" className="map-note">
          Showing {selectedRegion === 'All' ? 'Global' : selectedRegion} Press Freedom Distribution
        </text>
        
        {/* Simple visual representation of countries as dots */}
        <g className="country-dots">
          {data.slice(0, 30).map((item, idx) => {
            const score = item[2024];
            const angle = (idx / 30) * Math.PI * 2;
            const radius = 150;
            const x = 500 + Math.cos(angle) * radius;
            const y = 300 + Math.sin(angle) * radius;
            
            return (
              <circle
                key={idx}
                cx={x}
                cy={y}
                r="8"
                fill={getColor(score)}
                opacity="0.7"
                className="country-dot"
                title={`${item.country}: ${score}`}
              />
            );
          })}
        </g>
      </svg>
      <div className="map-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#2e7d32' }}></span>
          <span>Free (0-15)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#558b2f' }}></span>
          <span>Mostly Free (15-30)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#f57f17' }}></span>
          <span>Partly Free (30-45)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#d32f2f' }}></span>
          <span>Restricted (45+)</span>
        </div>
      </div>
    </div>
  );
};

export default function App() {
  const [selectedRegion, setSelectedRegion] = useState('Northern Europe');
  const [selectedCountries, setSelectedCountries] = useState(['Norway', 'Denmark', 'Hungary']);
  const [viewMode, setViewMode] = useState('overview'); // 'overview' | 'detailed' | 'map'
  const [sortBy, setSortBy] = useState('score');

  // All global data
  const allCountries = pressFreedomeData;

  // Filter data by selected region
  const filteredData = useMemo(() => {
    return selectedRegion === 'All'
      ? allCountries
      : getCountriesByRegion(selectedRegion);
  }, [selectedRegion]);

  // Calculate metrics for filtered region
  const metrics = useMemo(() => {
    const scores = filteredData.map(d => d[2024]);
    const validScores = scores.filter(s => s !== undefined);
    
    return {
      avgScore: (validScores.reduce((a, b) => a + b, 0) / validScores.length).toFixed(2),
      medianScore: validScores.sort((a, b) => a - b)[Math.floor(validScores.length / 2)].toFixed(2),
      bestCountry: filteredData.reduce((prev, curr) => 
        (curr[2024] || 100) < (prev[2024] || 100) ? curr : prev
      ),
      worstCountry: filteredData.reduce((prev, curr) => 
        (curr[2024] || 0) > (prev[2024] || 0) ? curr : prev
      ),
      totalCountries: filteredData.length,
      stdDev: Math.sqrt(validScores.reduce((sq, n) => sq + Math.pow(n - validScores.reduce((a, b) => a + b, 0) / validScores.length, 2), 0) / validScores.length).toFixed(2),
    };
  }, [filteredData]);

  // Get top and bottom countries
  const topCountries = useMemo(() => {
    return [...filteredData]
      .sort((a, b) => (a[2024] || 100) - (b[2024] || 100))
      .slice(0, 8);
  }, [filteredData]);

  const bottomCountries = useMemo(() => {
    return [...filteredData]
      .sort((a, b) => (b[2024] || 0) - (a[2024] || 0))
      .slice(0, 8);
  }, [filteredData]);

  // Prepare regional data for chart
  const regionalComparison = useMemo(() => {
    return regions
      .filter(r => r.name !== 'All')
      .map(r => {
        const countries = getCountriesByRegion(r.name);
        const scores = countries.map(c => c[2024]).filter(s => s !== undefined);
        return {
          name: r.name,
          avgScore: parseFloat((scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(2)),
          count: countries.length,
          color: r.color,
          minScore: Math.min(...scores),
          maxScore: Math.max(...scores),
        };
      })
      .sort((a, b) => a.avgScore - b.avgScore);
  }, []);

  // Time series for selected countries
  const timeSeriesData = useMemo(() => {
    const years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
    return years.map(year => {
      const point = { year };
      selectedCountries.forEach(country => {
        const countryData = allCountries.find(c => c.country === country);
        if (countryData) {
          point[country] = countryData[year];
        }
      });
      return point;
    });
  }, [selectedCountries]);

  // Scatter plot data
  const scatterData = useMemo(() => {
    return filteredData
      .filter(c => c[2024] !== undefined && c.population !== undefined)
      .map(c => ({
        name: c.country,
        population: Math.log10(c.population),
        score: c[2024],
        region: c.region,
        actualPopulation: c.population,
      }));
  }, [filteredData]);

  const regionsList = ['All', ...new Set(allCountries.map(c => c.region))];
  const countryList = [...new Set(allCountries.map(c => c.country))].sort();

  const toggleCountry = (country) => {
    setSelectedCountries(prev => 
      prev.includes(country)
        ? prev.filter(c => c !== country)
        : [...prev, country].slice(-4)
    );
  };

  const getScoreColor = (score) => {
    if (score <= 15) return '#2e7d32';
    if (score <= 30) return '#558b2f';
    if (score <= 45) return '#f57f17';
    return '#d32f2f';
  };

  return (
    <div className="app-premium">
      {/* Header */}
      <header className="header-premium">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">📰</div>
            <div>
              <h1>Press Freedom Analytics</h1>
              <p className="tagline">Global media freedom trends 2017-2024</p>
            </div>
          </div>
          <div className="header-controls">
            <div className="view-modes">
              <button 
                className={`mode-btn ${viewMode === 'overview' ? 'active' : ''}`}
                onClick={() => setViewMode('overview')}
              >
                📊 Overview
              </button>
              <button 
                className={`mode-btn ${viewMode === 'detailed' ? 'active' : ''}`}
                onClick={() => setViewMode('detailed')}
              >
                📈 Detailed
              </button>
              <button 
                className={`mode-btn ${viewMode === 'map' ? 'active' : ''}`}
                onClick={() => setViewMode('map')}
              >
                🗺️ Map
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="main-premium">
        {/* Sidebar Filter */}
        <aside className="sidebar-premium">
          <div className="filter-panel">
            <h3>Regions</h3>
            <div className="region-filters">
              {regionsList.map(region => (
                <button
                  key={region}
                  className={`region-btn ${selectedRegion === region ? 'active' : ''}`}
                  onClick={() => setSelectedRegion(region)}
                >
                  {region}
                </button>
              ))}
            </div>

            {/* Key Metrics */}
            <div className="metrics-panel">
              <h4>Metrics</h4>
              <div className="metric-compact">
                <span className="label">Average</span>
                <span className="value">{metrics.avgScore}</span>
              </div>
              <div className="metric-compact">
                <span className="label">Median</span>
                <span className="value">{metrics.medianScore}</span>
              </div>
              <div className="metric-compact">
                <span className="label">Std Dev</span>
                <span className="value">{metrics.stdDev}</span>
              </div>
              <div className="metric-compact">
                <span className="label">Countries</span>
                <span className="value">{metrics.totalCountries}</span>
              </div>
            </div>

            {/* Country Rankings */}
            <div className="rankings-mini">
              <h4>🏆 Top 3</h4>
              {topCountries.slice(0, 3).map((c, i) => (
                <div key={i} className="ranking-mini-item">
                  <span className="rank">{i + 1}</span>
                  <span className="name">{c.country}</span>
                  <span className="score">{c[2024]?.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <div className="content-premium">
          {viewMode === 'overview' && (
            <div className="view-overview">
              {/* Key Stats Cards */}
              <div className="stats-grid">
                <div className="stat-card primary">
                  <div className="stat-icon">📍</div>
                  <div className="stat-content">
                    <h5>Best Performer</h5>
                    <p className="stat-value">{metrics.bestCountry.country}</p>
                    <p className="stat-subtitle">{metrics.bestCountry[2024]?.toFixed(1)} score</p>
                  </div>
                </div>

                <div className="stat-card warning">
                  <div className="stat-icon">⚠️</div>
                  <div className="stat-content">
                    <h5>Most Challenged</h5>
                    <p className="stat-value">{metrics.worstCountry.country}</p>
                    <p className="stat-subtitle">{metrics.worstCountry[2024]?.toFixed(1)} score</p>
                  </div>
                </div>

                <div className="stat-card secondary">
                  <div className="stat-icon">📊</div>
                  <div className="stat-content">
                    <h5>Global Average</h5>
                    <p className="stat-value">{metrics.avgScore}</p>
                    <p className="stat-subtitle">Lower is better (0-100)</p>
                  </div>
                </div>
              </div>

              {/* Main Charts Grid */}
              <div className="charts-grid">
                {/* Regional Comparison */}
                <div className="chart-card">
                  <h3>Regional Comparison (2024)</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={regionalComparison}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                      <XAxis dataKey="name" angle={-20} textAnchor="end" height={80} fontSize={10} />
                      <YAxis fontSize={10} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#fff', border: '1px solid #ddd', borderRadius: '4px' }}
                        formatter={(value) => value.toFixed(2)}
                      />
                      <Bar dataKey="avgScore" fill="#1a1a1a" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                {/* Score Distribution */}
                <div className="chart-card">
                  <h3>Score Distribution</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                      <XAxis dataKey="score" name="Press Freedom Score" type="number" fontSize={10} />
                      <YAxis dataKey="population" name="Population (log)" type="number" fontSize={10} />
                      <Tooltip 
                        cursor={{ fill: 'rgba(0,0,0,0.1)' }}
                        contentStyle={{ backgroundColor: '#fff', border: '1px solid #ddd', borderRadius: '4px' }}
                      />
                      <Scatter name="Countries" data={scatterData} fill="#666" />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>

                {/* Temporal Trends */}
                <div className="chart-card span-2">
                  <div className="chart-header">
                    <h3>Temporal Trends (2017-2024)</h3>
                    <div className="country-selector-inline">
                      {countryList.slice(0, 15).map(country => (
                        <button
                          key={country}
                          className={`chip ${selectedCountries.includes(country) ? 'active' : ''}`}
                          onClick={() => toggleCountry(country)}
                        >
                          {country}
                        </button>
                      ))}
                    </div>
                  </div>
                  <ResponsiveContainer width="100%" height={280}>
                    <LineChart data={timeSeriesData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                      <XAxis dataKey="year" fontSize={10} />
                      <YAxis fontSize={10} />
                      <Tooltip contentStyle={{ backgroundColor: '#fff', border: '1px solid #ddd', borderRadius: '4px' }} />
                      <Legend wrapperStyle={{ fontSize: '11px' }} />
                      {selectedCountries.map((country, idx) => (
                        <Line
                          key={country}
                          type="monotone"
                          dataKey={country}
                          stroke={getScoreColor(pressFreedomeData.find(c => c.country === country)?.[2024] || 50)}
                          strokeWidth={2.5}
                          dot={false}
                          connectNulls
                        />
                      ))}
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                {/* Top Performers */}
                <div className="chart-card">
                  <h3>🏆 Most Free</h3>
                  <div className="ranking-list-compact">
                    {topCountries.map((c, idx) => (
                      <div key={idx} className="ranking-item-compact good">
                        <span className="rank">{idx + 1}</span>
                        <span className="name">{c.country}</span>
                        <span className="score">{c[2024]?.toFixed(1)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Most Challenged */}
                <div className="chart-card">
                  <h3>⚠️ Most Restricted</h3>
                  <div className="ranking-list-compact">
                    {bottomCountries.map((c, idx) => (
                      <div key={idx} className="ranking-item-compact poor">
                        <span className="rank">{idx + 1}</span>
                        <span className="name">{c.country}</span>
                        <span className="score">{c[2024]?.toFixed(1)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {viewMode === 'map' && (
            <div className="view-map">
              <EuropeMap 
                selectedRegion={selectedRegion} 
                data={filteredData}
              />
            </div>
          )}

          {viewMode === 'detailed' && (
            <div className="view-detailed">
              <div className="detailed-grid">
                <div className="detail-section">
                  <h3>Regional Profiles</h3>
                  {regionalComparison.map((region, idx) => (
                    <div key={idx} className="region-profile">
                      <div className="profile-header">
                        <h4>{region.name}</h4>
                        <span className="country-count">{region.count} countries</span>
                      </div>
                      <div className="profile-stats">
                        <div className="stat">
                          <span>Average:</span>
                          <strong>{region.avgScore.toFixed(2)}</strong>
                        </div>
                        <div className="stat">
                          <span>Range:</span>
                          <strong>{(region.maxScore - region.minScore).toFixed(1)}</strong>
                        </div>
                        <div className="progress-bar">
                          <div 
                            className="progress-fill" 
                            style={{ 
                              width: `${(region.avgScore / 100) * 100}%`,
                              backgroundColor: region.color
                            }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="detail-section">
                  <h3>Key Insights</h3>
                  <div className="insights-list">
                    <div className="insight-item">
                      <span className="insight-icon">📍</span>
                      <div>
                        <h5>Geographic Clustering</h5>
                        <p>Clear geographic patterns with Northern Europe leading, Eastern Europe most challenged</p>
                      </div>
                    </div>
                    <div className="insight-item">
                      <span className="insight-icon">📉</span>
                      <div>
                        <h5>Global Trend</h5>
                        <p>Press freedom declining globally with regional disparities widening</p>
                      </div>
                    </div>
                    <div className="insight-item">
                      <span className="insight-icon">⚖️</span>
                      <div>
                        <h5>Stability Analysis</h5>
                        <p>Year-to-year correlations >0.99 indicate reliable, stable measurements</p>
                      </div>
                    </div>
                    <div className="insight-item">
                      <span className="insight-icon">🎯</span>
                      <div>
                        <h5>Policy Implications</h5>
                        <p>Regional interventions and knowledge transfer can improve outcomes</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="footer-premium">
        <div className="footer-content">
          <p><strong>Data Source:</strong> Reporters Without Borders (RSF) World Press Freedom Index</p>
          <p><strong>Coverage:</strong> 170+ countries | 2017-2024 | Higher scores = less freedom</p>
          <p><a href="https://github.com/lant96/press-freedom-analytics">View on GitHub</a> • <a href="https://rsf.org">RSF Index</a></p>
        </div>
      </footer>
    </div>
  );
}
