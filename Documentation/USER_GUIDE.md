# Malawi Disaster Risk Assessment System - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features Overview](#features-overview)
5. [Step-by-Step Tutorials](#step-by-step-tutorials)
6. [Troubleshooting](#troubleshooting)

---

## Introduction

The **Malawi Disaster Risk Assessment System** is a QGIS plugin designed to help disaster management professionals assess flood risks, plan evacuations, and manage disaster response in Malawi's 28 districts.

### Key Features
- **Flood Risk Analysis**: Analyze historical disaster data and identify high-risk areas
- **Evacuation Planning**: Calculate evacuation routes and capacity gaps
- **Spatial Visualization**: View districts, water bodies, risk zones, and infrastructure on maps
- **Database Integration**: PostgreSQL/PostGIS backend for robust spatial data management

---

## Installation

### Prerequisites
1. **QGIS 3.x** or higher
2. **PostgreSQL 12+** with PostGIS extension
3. **Python 3.7+** (included with QGIS)

### Database Setup

1. **Create the database:**
```bash
createdb -U postgres -p 5433 disaster_risk_db
```

2. **Enable PostGIS extension:**
```sql
CREATE EXTENSION postgis;
```

3. **Restore from backup:**
```bash
psql -U postgres -p 5433 -d disaster_risk_db -f database/complete_backup.sql
```

### Plugin Installation

1. Copy the plugin folder to your QGIS plugins directory:
   - **Windows**: `C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - **Mac**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`

2. Restart QGIS

3. Enable the plugin:
   - Go to **Plugins → Manage and Install Plugins**
   - Search for "Disaster Risk Assessment"
   - Check the box to enable it

---

## Getting Started

### Connecting to the Database

1. Click the **Disaster Risk Assessment** icon in the toolbar
2. Go to the **Database Connection** tab
3. Enter your database credentials:
   - **Host**: localhost
   - **Port**: 5433 (or 5432)
   - **Database**: disaster_risk_db
   - **Username**: postgres
   - **Password**: [your password]
4. Click **Connect to Database**
5. Wait for the "Connected successfully" message

---

## Features Overview

### 1. Districts & Data Tab
- **Load All Districts**: Display all 28 Malawi districts on the map
- **View District Details**: See population, area, and disaster history
- **Load Water Bodies**: Display rivers and lakes with flood-prone indicators
- **Load Historical Disasters**: Show past flood, cyclone, and drought events
- **Load Infrastructure**: Display hospitals, schools, and critical facilities
- **Load Risk Zones**: Show areas classified by risk level

### 2. Flood Risk Analysis Tab
- **Run Flood Risk Analysis**: Analyze flood risk for all districts or a specific district
- **Include Historical Disasters**: Factor in past events
- **Include Water Proximity**: Consider distance to flood-prone rivers
- **Include Population Risk**: Account for population density

### 3. Results & Maps Tab
- **View Analysis Results**: See districts ranked by flood risk
- **Generate Flood Risk Map**: Create visual risk maps
- **Export to CSV**: Save results for further analysis
- **View Selected District**: See detailed disaster history

### 4. Evacuation Planning Tab
- **View Evacuation Centers**: List all evacuation facilities
- **Identify Safe Zones**: Find low-risk areas suitable for evacuation
- **Calculate Capacity Gap**: Determine if evacuation capacity is sufficient
- **Plan Evacuation Routes**: Calculate optimal routes from high-risk areas to centers
- **Generate Full Evacuation Plan**: Create comprehensive evacuation strategy
- **Export Plan to File**: Save evacuation plan as a text report

---

## Step-by-Step Tutorials

### Tutorial 1: Analyzing Flood Risk in Zomba District

1. **Connect to Database** (see Getting Started)

2. **Load District Data:**
   - Go to **Districts & Data** tab
   - Click **Load All Districts**
   - Select "Zomba" from the dropdown
   - Click **View District Details**

3. **Load Related Data:**
   - Click **Load Water Bodies** (see Likangala River)
   - Click **Load Historical Disasters** (see past floods)
   - Click **Load Risk Zones**

4. **Run Analysis:**
   - Go to **Flood Risk Analysis** tab
   - Select "Zomba" from the dropdown
   - Ensure all checkboxes are checked
   - Click **Run Flood Risk Analysis**

5. **View Results:**
   - Go to **Results & Maps** tab
   - Review the risk level and statistics
   - Click **Generate Flood Risk Map**
   - Click **Export to CSV** to save results

### Tutorial 2: Creating an Evacuation Plan for Nsanje District

1. **Connect to Database**

2. **Go to Evacuation Planning Tab**

3. **Select District:**
   - Choose "Nsanje" from the dropdown

4. **View Current Evacuation Centers:**
   - Click **View Evacuation Centers**
   - Review capacity and facilities

5. **Calculate Capacity Gap:**
   - Click **Calculate Capacity Gap**
   - Review the capacity analysis in the text box below

6. **Identify Safe Zones:**
   - Click **Identify Safe Zones**
   - Review areas with low flood risk

7. **Plan Evacuation Routes:**
   - Click **Plan Evacuation Routes**
   - Review routes from high-risk zones to evacuation centers

8. **Generate Complete Plan:**
   - Click **Generate Full Evacuation Plan**
   - Review the comprehensive plan with recommendations

9. **Export Plan:**
   - Click **Export Plan to File**
   - Choose a location and filename
   - Save the report for distribution

### Tutorial 3: Comparing Multiple Districts

1. **Run Analysis for All Districts:**
   - Go to **Flood Risk Analysis** tab
   - Select "All Districts"
   - Click **Run Flood Risk Analysis**

2. **Review Results:**
   - Go to **Results & Maps** tab
   - Sort the table by clicking column headers
   - Identify districts with "EXTREME RISK" or "HIGH RISK"

3. **Export Results:**
   - Click **Export to CSV**
   - Open in Excel or other spreadsheet software

4. **View Individual District Details:**
   - Click on a district row in the table
   - Click **View Selected District**
   - Review historical disaster events

---

## Troubleshooting

### Connection Issues

**Problem**: "Connection failed" error

**Solutions**:
- Verify PostgreSQL is running: `pg_ctl status`
- Check port number (5432 or 5433)
- Verify database exists: `psql -U postgres -l`
- Check username and password
- Ensure PostGIS extension is installed: `SELECT PostGIS_version();`

### Layer Loading Issues

**Problem**: "Invalid layer" or layers not displaying

**Solutions**:
- Verify database connection is active
- Check that tables exist in the database
- Ensure geometry columns are properly configured
- Verify SRID is 4326 (WGS84)

### Analysis Errors

**Problem**: "No flood risk data found"

**Solutions**:
- Verify disaster_events table has data
- Check that water_bodies table has flood_prone = TRUE entries
- Ensure selected district has historical data

### Evacuation Planning Issues

**Problem**: "No evacuation routes calculated"

**Solutions**:
- Verify evacuation_centers table has data for the district
- Check that risk_zones table has high-risk areas
- Ensure district has both high-risk zones and evacuation centers

---

## Data Dictionary

### Key Tables

**administrative_boundaries**: 28 Malawi districts with population and geometry

**water_bodies**: Rivers and lakes with flood-prone status

**disaster_events**: Historical floods, cyclones, droughts (2015-2024)

**evacuation_centers**: Evacuation facilities with capacity data

**risk_zones**: Areas classified by flood risk level

**infrastructure**: Hospitals, schools, bridges, roads

---

## Support

For technical support or questions:
- **GitHub Issues**: [Repository URL]
- **Email**: [Your Email]
- **Documentation**: See README.md and TECHNICAL_DOCUMENTATION.md

---

## Credits

**Developed by**: Malawi Disaster Management Team
**Database Architect**: Davie Nyirongo
**Evacuation Planning Lead**: [Chipulumutso Phiri]
**Institution**: [University of Malawi]
**Date**: December 2025

---

## License

Educational/Academic Use

---

**Last Updated**: December 2025
