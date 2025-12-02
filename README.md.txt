# Malawi Disaster Management Database

## 📋 Overview
PostgreSQL/PostGIS database system for flood risk assessment and natural disaster management in Malawi. This database powers a QGIS plugin for disaster preparedness and response planning.

## 🗺️ Features
- **28 Malawi Districts** with real geographical boundaries
- **Historical Disaster Records** (2015-2024): 20+ documented events
- **Flood-Prone Rivers & Lakes** with district linkages
- **Critical Infrastructure Mapping** (hospitals, schools, bridges)
- **Risk Assessment Zones** by severity level
- **Evacuation Centers** with capacity data
- **Population Demographics** by district

## 📊 Database Statistics
- **Districts**: 28 (Northern, Central, Southern regions)
- **Water Bodies**: 8 major rivers and lakes
- **Historical Disasters**: 20 events (floods, cyclones, droughts)
- **Infrastructure Points**: 10 critical facilities
- **Risk Zones**: 7 classified areas
- **Evacuation Centers**: 8 facilities

## 🚀 Quick Start

### Prerequisites
- PostgreSQL 12+ with PostGIS extension
- Port: 5433 (or default 5432)
- pgAdmin 4 (recommended)

### Installation

1. **Create database:**
```bash
createdb -U postgres -p 5433 disaster_risk_db
```

2. **Enable PostGIS:**
```sql
CREATE EXTENSION postgis;
```

3. **Restore from backup:**
```bash
psql -U postgres -p 5433 -d disaster_risk_db -f database/complete_backup.sql
```

**OR using pgAdmin:**
1. Right-click on disaster_risk_db → Restore
2. Select `database/complete_backup.sql`
3. Click Restore

## 📖 Database Structure

### Main Tables

**administrative_boundaries** (28 records)
- All Malawi districts with population and area data
- Geometry: MultiPolygon (SRID: 4326)

**water_bodies** (8 records)
- Major rivers: Shire, Ruo, Likangala, Bua, Songwe, Dwangwa
- Lakes: Lake Malawi, Lake Chilwa
- Includes flood_prone status and district linkage

**disaster_events** (20 records)
- Historical floods, cyclones, droughts (2015-2024)
- Notable: Cyclone Idai (2019), Cyclone Freddy (2023)
- Casualties, displaced people, economic losses

**infrastructure** (10 records)
- Hospitals, schools, bridges, roads
- Vulnerability scores and operational status

**risk_zones** (7 records)
- Extreme, High, Medium, Low risk classifications
- Affected population estimates

**rainfall_data** (15 records)
- Weather station measurements
- Date-stamped precipitation data

**evacuation_centers** (8 records)
- Capacity, facilities, accessibility scores
- Strategic placement across districts

**elevation_data** (15 records)
- DEM sample points with slope and aspect
- Elevation ranges: 380m - 521m

**population_data** (10 records)
- Census data (2020, 2024)
- Vulnerable population tracking

**soil_data** (5 records)
- Soil types and drainage capacity
- Permeability measurements

### Views

**v_flood_prone_districts_ranked**
- Districts ranked by flood risk level
- Includes historical events and river proximity

**v_district_summary**
- Complete district profiles
- Aggregates all disaster and infrastructure data

**get_district_by_water_body()**
- Function to find which district contains a river/lake
- Example: `SELECT * FROM get_district_by_water_body('Likangala');`

## 🔍 Sample Queries

### Find flood-prone districts:
```sql
SELECT * FROM v_flood_prone_districts_ranked;
```

### Find which district Likangala River is in:
```sql
SELECT * FROM get_district_by_water_body('Likangala');
-- Result: Zomba District
```

### Historical disasters in Zomba:
```sql
SELECT event_type, event_date, severity, casualties, displaced_people
FROM disaster_events
WHERE affected_area = 'Zomba'
ORDER BY event_date DESC;
```

### Districts by disaster count:
```sql
SELECT affected_area, COUNT(*) as disasters, SUM(casualties) as casualties
FROM disaster_events
GROUP BY affected_area
ORDER BY disasters DESC;
```

### Evacuation capacity by district:
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

## 🛠️ Technology Stack
- **Database**: PostgreSQL 18
- **Spatial Extension**: PostGIS 3.4+
- **Coordinate System**: SRID 4326 (WGS84)
- **Encoding**: UTF-8
- **Port**: 5433

## 📁 Project Structure
```
malawi-disaster-management-db/
├── database/
│   └── complete_backup.sql       # Full database backup
├── documentation/
│   ├── Data_Dictionary.md
│   ├── ER_Diagram.md
│   └── Setup_Guide.md
├── scripts/
│   └── sample_queries.sql
└── README.md
```

## 👥 Project Information
**Database Architect**: Davie Nyirongo
**Institution**: [Your University]
**Course**: Flood Risk & Natural Disaster Management System
**Date**: December 2024
**Version**: 1.0

## 📧 Contact
- **GitHub**: [@DavieNyirongo](https://github.com/DavieNyirongo)
- **Email**: [Your Email]

## 📝 License
Educational/Academic Use

## ⚠️ Data Notice
This database contains both real geographical data (28 Malawi districts) and sample disaster records for demonstration purposes. For production disaster management use, verify and update with current official data.

## 🤝 Contributing
This is an academic project. For suggestions or improvements:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🔗 Related Projects
- QGIS Plugin: Disaster Risk Assessment System
- Uses this database as backend for spatial analysis

## 📚 References
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- PostGIS Manual: https://postgis.net/docs/
- Malawi NSO: https://www.nsomalawi.mw/

---
**Last Updated**: December 2024
```

Save and close the file.

---

## **STEP 4: Create .gitignore File**

1. In the main folder, create a new text file
2. Name it `.gitignore` (note the dot at the start)
3. Open with Notepad and paste:
```
# Backup files
*.backup
*.bak
*.tmp

# Logs
*.log

# Database passwords
*.pgpass
pg_service.conf

# OS files
.DS_Store
Thumbs.db