# Malawi Disaster Risk Assessment System

[![QGIS](https://img.shields.io/badge/QGIS-3.0+-green.svg)](https://qgis.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.4+-orange.svg)](https://postgis.net/)
[![Python](https://img.shields.io/badge/Python-3.7+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

A comprehensive database-driven QGIS plugin for flood risk assessment and evacuation planning across Malawi's 28 districts.

---


## 🎯 Project Overview

### Problem Statement

Malawi faces recurring natural disasters, particularly floods during the rainy season. Districts like Nsanje, Chikwawa, and Zomba experience devastating floods that displace thousands of people annually. Traditional disaster management methods are time-consuming and lack spatial analysis capabilities.

### Our Solution

A QGIS plugin backed by a PostgreSQL/PostGIS spatial database that:
- Analyzes flood risk across all 28 Malawi districts
- Calculates optimal evacuation routes
- Identifies capacity gaps in evacuation infrastructure
- Generates comprehensive evacuation plans with actionable recommendations

---

## ✨ Key Features

### 🗺️ Spatial Data Visualization
- Display all 28 Malawi districts with boundaries
- Visualize flood-prone rivers and lakes
- Show historical disaster events (2015-2024)
- Map evacuation centers and critical infrastructure
- Display risk zones by severity level

### 📊 Flood Risk Analysis
- Multi-factor risk assessment
- Historical disaster pattern analysis
- Water proximity calculations
- Population risk evaluation
- Color-coded risk classification (Extreme, High, Medium, Low)

### 🚨 Evacuation Planning
- **Capacity Gap Analysis**: Calculate evacuation capacity vs. population
- **Safe Zone Identification**: Find low-risk areas for evacuation
- **Route Optimization**: Calculate shortest paths from high-risk zones to centers
- **Time Estimation**: Estimate evacuation times based on distance
- **Comprehensive Planning**: Generate complete evacuation strategies

### 📄 Reporting & Export
- Export analysis results to CSV
- Generate detailed evacuation plan reports
- View district-specific disaster histories
- Priority-based recommendations

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      QGIS Plugin (UI)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      disaster_risk_assessment.py (Controller)         │  │
│  └──────────────────────────────────────────────────────┘  │
│         │                    │                    │          │
│  ┌──────▼──────┐  ┌─────────▼────────┐  ┌────────▼──────┐ │
│  │  database_  │  │  evacuation_     │  │   spatial_    │ │
│  │  manager.py │  │  planner.py      │  │  analyzer.py  │ │
│  └─────────────┘  └──────────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│           PostgreSQL + PostGIS Database                      │
│  • administrative_boundaries (28 districts)                  │
│  • water_bodies (8 rivers/lakes)                            │
│  • disaster_events (20+ historical events)                  │
│  • evacuation_centers (8 facilities)                        │
│  • risk_zones (7 classified areas)                          │
│  • infrastructure (10 critical facilities)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites

1. **QGIS 3.0+** - [Download here](https://qgis.org/en/site/forusers/download.html)
2. **PostgreSQL 12+** - [Download here](https://www.postgresql.org/download/)
3. **PostGIS 3.4+** - Usually bundled with PostgreSQL
4. **Python 3.7+** - Included with QGIS

### Database Setup

1. **Create the database:**
```bash
createdb -U postgres -p 5433 disaster_risk_db
```

2. **Enable PostGIS extension:**
```sql
psql -U postgres -p 5433 -d disaster_risk_db
CREATE EXTENSION postgis;
\q
```

3. **Restore from backup:**
```bash
psql -U postgres -p 5433 -d disaster_risk_db -f database/complete_backup.sql
```

**Alternative (using pgAdmin):**
1. Open pgAdmin 4
2. Right-click on `disaster_risk_db` → Restore
3. Select `database/complete_backup.sql`
4. Click Restore

### Plugin Installation

**Method 1: Manual Installation**

1. Clone this repository:
```bash
git clone https://github.com/yourusername/malawi-disaster-management.git
```

2. Copy to QGIS plugins directory:
   - **Windows**: `C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **Mac**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

3. Restart QGIS

4. Enable the plugin:
   - Go to **Plugins → Manage and Install Plugins**
   - Search for "Disaster Risk Assessment"
   - Check the box to enable

**Method 2: ZIP Installation**

1. Download the ZIP file from releases
2. In QGIS: **Plugins → Manage and Install Plugins → Install from ZIP**
3. Select the downloaded ZIP file
4. Click Install

---

##  Quick Start Guide

### 1. Connect to Database

1. Click the **Disaster Risk Assessment** icon in the toolbar
2. Go to **Database Connection** tab
3. Enter credentials:
   - Host: `localhost`
   - Port: `5433` (or `5432`)
   - Database: `disaster_risk_db`
   - Username: `postgres`
   - Password: [your password]
4. Click **Connect to Database**

### 2. Load District Data

1. Go to **Districts & Data** tab
2. Click **Load All Districts** to see all 28 districts
3. Select a district from dropdown
4. Click **View District Details** for information

### 3. Run Flood Risk Analysis

1. Go to **Flood Risk Analysis** tab
2. Select "All Districts" or specific district
3. Click **Run Flood Risk Analysis**
4. View results in **Results & Maps** tab

### 4. Plan Evacuations

1. Go to **Evacuation Planning** tab
2. Select a district
3. Click **Calculate Capacity Gap** to see evacuation capacity
4. Click **Generate Full Evacuation Plan** for comprehensive plan
5. Click **Export Plan to File** to save report

---

## Database Schema

### Key Tables

| Table | Records | Description |
|-------|---------|-------------|
| `administrative_boundaries` | 28 | Malawi districts with population and geometry |
| `water_bodies` | 8 | Rivers and lakes with flood-prone status |
| `disaster_events` | 20+ | Historical floods, cyclones, droughts (2015-2024) |
| `evacuation_centers` | 8 | Evacuation facilities with capacity data |
| `risk_zones` | 7 | Areas classified by flood risk level |
| `infrastructure` | 10 | Hospitals, schools, bridges, roads |
| `population_data` | 10 | Census data with vulnerable populations |
| `rainfall_data` | 15 | Weather station measurements |
| `elevation_data` | 15 | DEM sample points |
| `soil_data` | 5 | Soil types and drainage capacity |

### Sample Queries

**Find flood-prone districts:**
```sql
SELECT * FROM v_flood_prone_districts_ranked;
```

**Get evacuation capacity gap:**
```sql
SELECT 
    ab.boundary_name,
    ab.population,
    SUM(ec.capacity) as total_capacity,
    ab.population - SUM(ec.capacity) as capacity_gap
FROM administrative_boundaries ab
LEFT JOIN evacuation_centers ec ON ab.boundary_id = ec.boundary_id
GROUP BY ab.boundary_name, ab.population
ORDER BY capacity_gap DESC;
```

---

## Testing

### Run Tests

1. Update database credentials in `test_plugin.py`
2. Run tests:
```bash
python test_plugin.py
```

### Test Coverage

- ✅ Database connection
- ✅ District queries
- ✅ Evacuation center queries
- ✅ Capacity gap calculation
- ✅ Route calculation
- ✅ Evacuation plan generation
- ✅ Report export
- ✅ Complete workflow integration

---

## Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user manual with tutorials
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Technical architecture and API reference
- **[PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)** - Presentation script and demo guide
- **[README.md.txt](README.md.txt)** - Database documentation

---

## Team Members

| Member | Role | Responsibilities |
|--------|------|------------------|
| Davie Nyirongo | Database Architect | Database design, schema, data population |
| Lucy Sabola | Risk Analysis Lead | Spatial analysis algorithms, risk scoring |
| Joel Ganizani | UI/UX Lead | User interface design, dialog implementation |
| Chipulumutso Phiri | Evacuation Planning & Documentation Lead | Evacuation planning features, testing, documentation, presentation |

---

##  Academic Context

**Institution**: University of Malawi  
**Course**: GIS Programming and Databases  
**Assignment**: Database-driven web application or plugin for spatial problem-solving  
**Date**: December 2025 
**Version**: 1.0

---

## Technology Stack

- **Frontend**: QGIS 3.x Python Plugin API
- **Backend**: PostgreSQL 18 + PostGIS 3.4
- **Language**: Python 3.7+
- **Libraries**: 
  - `psycopg2` - PostgreSQL adapter
  - `qgis.core` - QGIS core functionality
  - `qgis.PyQt` - Qt UI framework
- **Coordinate System**: SRID 4326 (WGS84)

---

## Performance

- **Analysis Speed**: All 28 districts analyzed in < 10 seconds
- **Database Size**: ~50 MB with sample data
- **Query Performance**: < 1 second for most queries
- **Scalability**: Can handle 100+ districts with proper indexing

---

##  Known Issues & Limitations

1. **Route Calculation**: Uses straight-line distance, not road networks
2. **Real-time Data**: No integration with live weather APIs
3. **Elevation Data**: Limited sample points (15 records)
4. **Historical Data**: Sample data for demonstration purposes

---

## Future Enhancements

- [ ] Network analysis using actual road networks
- [ ] Real-time weather data integration
- [ ] Mobile app for field data collection
- [ ] Machine learning for predictive risk modeling
- [ ] Multi-hazard analysis (earthquakes, droughts, cyclones)
- [ ] Web-based dashboard for remote access
- [ ] Automated alert system
- [ ] Integration with national disaster management systems

---

##  License

This project is for educational/academic use. 

---

##  Contributing

This is an academic project. For suggestions or improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

---

## Contact & Support

- **GitHub Issues**: [Repository Issues](https://github.com/yourusername/malawi-disaster-management/issues)
- **Email**: disaster.management@example.com
- **Documentation**: See docs folder

---

## Acknowledgments

- Malawi National Statistical Office for district data
- OpenStreetMap contributors for geographical data
- QGIS community for excellent documentation
- PostGIS team for spatial database capabilities

---

## 📊 Project Statistics

- **Lines of Code**: ~2,500
- **Database Tables**: 10
- **Districts Covered**: 28
- **Historical Events**: 20+
- **Evacuation Centers**: 8
- **Development Time**: 4 weeks
- **Team Size**: 4 members

---

## Related Resources

- [QGIS Documentation](https://qgis.org/en/docs/)
- [PostGIS Manual](https://postgis.net/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Malawi NSO](https://www.nsomalawi.mw/)

---

##  Data Notice

This database contains both real geographical data (28 Malawi districts) and sample disaster records for demonstration purposes. For production disaster management use, verify and update with current official data from:
- Malawi Department of Disaster Management Affairs (DoDMA)
- Malawi Meteorological Services
- National Statistical Office

---

**Last Updated**: December 2025
**Version**: 1.0  
**Status**: Active Development

---


**If you find this project useful, please star the repository!**

---

