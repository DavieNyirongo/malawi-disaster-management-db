# Technical Documentation - Malawi Disaster Risk Assessment System

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         QGIS Plugin                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         disaster_risk_assessment.py                   │  │
│  │         (Main Plugin Controller)                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐        │
│  │  database_  │  │ evacuation_ │  │  spatial_   │        │
│  │  manager.py │  │ planner.py  │  │ analyzer.py │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL + PostGIS Database                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tables: administrative_boundaries, water_bodies,     │  │
│  │  disaster_events, evacuation_centers, risk_zones,    │  │
│  │  infrastructure, population_data, etc.               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Documentation

### 1. disaster_risk_assessment.py

**Purpose**: Main plugin controller that manages the UI and coordinates between modules

**Key Classes**:
- `DisasterRiskAssessment`: Main plugin class

**Key Methods**:
- `initGui()`: Initialize plugin UI elements
- `connect_to_database()`: Establish database connection
- `run_flood_analysis()`: Execute flood risk analysis
- `generate_full_evacuation_plan()`: Create comprehensive evacuation plan

**Dependencies**:
- `database_manager.DatabaseManager`
- `evacuation_planner.EvacuationPlanner`
- `disaster_risk_dialog.DisasterRiskDialog`

---

### 2. database_manager.py

**Purpose**: Handle all database operations and queries

**Key Classes**:
- `DatabaseManager`: PostgreSQL/PostGIS connection and query manager

**Key Methods**:

```python
connect(host, port, database, user, password)
# Establishes database connection
# Returns: (success: bool, message: str)

execute_query(query, params=None, fetch=True)
# Executes SQL query with optional parameters
# Returns: List of dictionaries (if fetch=True) or True (if fetch=False)

load_layer_from_db(table_name, geometry_column='geom', layer_name=None, where_clause=None)
# Loads PostGIS layer into QGIS
# Returns: (layer: QgsVectorLayer, message: str)

get_flood_prone_districts()
# Retrieves districts ranked by flood risk
# Returns: List of district records with risk metrics

get_evacuation_centers(district_id=None)
# Gets evacuation centers, optionally filtered by district
# Returns: List of evacuation center records
```

**Database Schema**:

```sql
-- Key tables used by the plugin

administrative_boundaries (
    boundary_id SERIAL PRIMARY KEY,
    boundary_name VARCHAR(100),
    boundary_type VARCHAR(50),
    boundary_code VARCHAR(20),
    population INTEGER,
    area_sqkm NUMERIC(10,2),
    geom GEOMETRY(MultiPolygon, 4326)
)

water_bodies (
    water_id SERIAL PRIMARY KEY,
    water_name VARCHAR(100),
    water_type VARCHAR(50),
    flood_prone BOOLEAN,
    length_km NUMERIC(10,2),
    boundary_id INTEGER REFERENCES administrative_boundaries,
    geom GEOMETRY(LineString, 4326)
)

disaster_events (
    event_id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    event_date DATE,
    severity VARCHAR(50),
    affected_area VARCHAR(100),
    casualties INTEGER,
    displaced_people INTEGER,
    economic_loss_usd NUMERIC(15,2),
    description TEXT,
    geom GEOMETRY(Point, 4326)
)

evacuation_centers (
    center_id SERIAL PRIMARY KEY,
    center_name VARCHAR(100),
    capacity INTEGER,
    current_occupancy INTEGER,
    facilities TEXT,
    accessibility_score NUMERIC(3,2),
    boundary_id INTEGER REFERENCES administrative_boundaries,
    geom GEOMETRY(Point, 4326)
)

risk_zones (
    zone_id SERIAL PRIMARY KEY,
    zone_name VARCHAR(100),
    risk_level VARCHAR(50),
    risk_type VARCHAR(50),
    affected_population INTEGER,
    risk_score NUMERIC(5,2),
    boundary_id INTEGER REFERENCES administrative_boundaries,
    geom GEOMETRY(Polygon, 4326)
)
```

---

### 3. evacuation_planner.py

**Purpose**: Evacuation planning algorithms and capacity analysis

**Key Classes**:
- `EvacuationPlanner`: Evacuation route calculation and capacity analysis

**Key Methods**:

```python
identify_safe_zones(district_id)
# Identifies low-risk areas suitable for evacuation
# Returns: List of safe zone records

calculate_evacuation_capacity_gap(district_id)
# Calculates gap between evacuation capacity and population
# Returns: Dictionary with capacity metrics

calculate_evacuation_routes(district_id)
# Calculates optimal routes from high-risk zones to evacuation centers
# Algorithm: Nearest neighbor with capacity constraints
# Returns: List of route records with distance and time estimates

generate_evacuation_plan(district_id)
# Generates comprehensive evacuation plan
# Returns: Dictionary containing:
#   - capacity_analysis
#   - evacuation_routes
#   - safe_zones
#   - recommendations
#   - plan_status

export_evacuation_plan_report(plan, output_path)
# Exports evacuation plan to formatted text file
# Returns: (success: bool, message: str)
```

**Algorithms**:

1. **Route Calculation**:
   - Uses nearest neighbor algorithm
   - Considers evacuation center capacity
   - Calculates Euclidean distance (can be upgraded to network analysis)
   - Estimates time based on 5 km/h walking speed

2. **Capacity Analysis**:
   - Compares total population vs. evacuation capacity
   - Calculates coverage percentage
   - Identifies capacity gaps

3. **Recommendation Engine**:
   - Prioritizes recommendations (CRITICAL, HIGH, MEDIUM, LOW)
   - Categories: Capacity, Coverage, Routes, Safe Zones, Risk, Preparedness
   - Generates actionable suggestions

---

### 4. spatial_analyzer.py

**Purpose**: Spatial risk analysis algorithms

**Key Classes**:
- `DisasterRiskAnalyzer`: Multi-factor risk analysis

**Key Methods**:

```python
analyze_elevation_risk(area_geometry, elevation_layer, threshold=50)
# Analyzes flood risk based on elevation
# Lower elevation = Higher risk
# Returns: (score: int, details: dict)

analyze_water_proximity(area_geometry, water_layer, buffer_distance=500)
# Analyzes risk based on proximity to water bodies
# Creates buffer zones: 100m (very high), 300m (high), 500m (moderate)
# Returns: (score: int, details: dict)

analyze_historical_events(area_geometry, area_id)
# Analyzes risk based on historical disaster occurrences
# Factors: recency, severity, frequency
# Returns: (score: int, details: dict)

run_complete_analysis(area_feature, layers, parameters)
# Runs comprehensive multi-factor risk analysis
# Combines: elevation, water proximity, slope, rainfall, historical, drainage
# Returns: Dictionary with total_score, risk_category, detailed_scores
```

**Risk Scoring System**:

Each factor contributes 0-20 points:
- **Elevation**: Lower areas score higher
- **Water Proximity**: Closer to water scores higher
- **Historical Events**: More recent/severe events score higher
- **Slope**: Flatter areas score higher
- **Rainfall**: Higher rainfall scores higher
- **Drainage**: Poor drainage scores higher

**Total Score → Risk Category**:
- 80-100: Very High Risk
- 60-79: High Risk
- 40-59: Moderate Risk
- 20-39: Low Risk
- 0-19: Safe

---

### 5. disaster_risk_dialog.py

**Purpose**: User interface definition

**Key Classes**:
- `DisasterRiskDialog`: Main dialog window with tabs

**Tabs**:
1. **Database Connection**: Connection parameters and status
2. **Districts & Data**: District exploration and data loading
3. **Flood Risk Analysis**: Analysis configuration and execution
4. **Results & Maps**: Results display and export
5. **Evacuation Planning**: Evacuation planning tools

**UI Components**:
- QComboBox: District selection
- QPushButton: Action buttons
- QTableWidget: Results display
- QTextBrowser: Logs and information display
- QProgressBar: Analysis progress

---

## API Reference

### Database Manager API

```python
# Initialize
db = DatabaseManager()

# Connect
success, msg = db.connect('localhost', '5433', 'disaster_risk_db', 'postgres', 'password')

# Query districts
districts = db.get_all_districts()
# Returns: [{'boundary_id': 1, 'boundary_name': 'Zomba', 'population': 851000, ...}, ...]

# Query flood-prone districts
flood_districts = db.get_flood_prone_districts()
# Returns: [{'district': 'Nsanje', 'flood_risk_level': 'EXTREME RISK', ...}, ...]

# Load layer
layer, msg = db.load_layer_from_db('administrative_boundaries', layer_name='Districts')
QgsProject.instance().addMapLayer(layer)
```

### Evacuation Planner API

```python
# Initialize
planner = EvacuationPlanner(db_manager)

# Identify safe zones
safe_zones = planner.identify_safe_zones(district_id=5)
# Returns: [{'zone_name': 'Safe Zone A', 'risk_level': 'low', ...}, ...]

# Calculate capacity gap
capacity = planner.calculate_evacuation_capacity_gap(district_id=5)
# Returns: {'population': 500000, 'total_capacity': 450000, 'capacity_gap': 50000, ...}

# Calculate routes
routes = planner.calculate_evacuation_routes(district_id=5)
# Returns: [{'from_zone': 'High Risk Zone 1', 'to_center': 'Center A', 'distance_km': 5.2, ...}, ...]

# Generate full plan
plan = planner.generate_evacuation_plan(district_id=5)
# Returns: {'district': 'Nsanje', 'capacity_analysis': {...}, 'evacuation_routes': [...], ...}

# Export plan
success, msg = planner.export_evacuation_plan_report(plan, 'evacuation_plan.txt')
```

### Spatial Analyzer API

```python
# Initialize
analyzer = DisasterRiskAnalyzer(db_manager)

# Run complete analysis
result = analyzer.run_complete_analysis(
    area_feature=feature,
    layers={'elevation': elev_layer, 'water_bodies': water_layer},
    parameters={'elevation_threshold': 50, 'water_buffer': 500}
)
# Returns: {
#     'total_score': 75,
#     'risk_category': 'High',
#     'color': '#FF0000',
#     'scores': {'elevation': 15, 'water_proximity': 20, ...},
#     'population_at_risk': 50000
# }
```

---

## Testing

### Unit Tests

Create `test_evacuation_planner.py`:

```python
import unittest
from evacuation_planner import EvacuationPlanner
from database_manager import DatabaseManager

class TestEvacuationPlanner(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager()
        self.db.connect('localhost', '5433', 'disaster_risk_db', 'postgres', 'password')
        self.planner = EvacuationPlanner(self.db)
    
    def test_identify_safe_zones(self):
        zones = self.planner.identify_safe_zones(district_id=1)
        self.assertIsInstance(zones, list)
    
    def test_calculate_capacity_gap(self):
        capacity = self.planner.calculate_evacuation_capacity_gap(district_id=1)
        self.assertIsNotNone(capacity)
        self.assertIn('capacity_gap', capacity)
    
    def test_calculate_routes(self):
        routes = self.planner.calculate_evacuation_routes(district_id=1)
        self.assertIsInstance(routes, list)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

Test complete workflow:

```python
def test_complete_evacuation_workflow():
    # Connect to database
    db = DatabaseManager()
    success, _ = db.connect('localhost', '5433', 'disaster_risk_db', 'postgres', 'password')
    assert success
    
    # Initialize planner
    planner = EvacuationPlanner(db)
    
    # Generate plan for district
    plan = planner.generate_evacuation_plan(district_id=1)
    assert plan is not None
    assert 'evacuation_routes' in plan
    assert 'recommendations' in plan
    
    # Export plan
    success, _ = planner.export_evacuation_plan_report(plan, 'test_plan.txt')
    assert success
```

---

## Performance Considerations

### Database Optimization

1. **Indexes**: Ensure spatial indexes exist
```sql
CREATE INDEX idx_admin_boundaries_geom ON administrative_boundaries USING GIST(geom);
CREATE INDEX idx_water_bodies_geom ON water_bodies USING GIST(geom);
CREATE INDEX idx_risk_zones_geom ON risk_zones USING GIST(geom);
```

2. **Query Optimization**: Use spatial queries efficiently
```sql
-- Good: Use ST_DWithin for distance queries
SELECT * FROM evacuation_centers 
WHERE ST_DWithin(geom, ST_MakePoint(35.0, -15.0)::geography, 5000);

-- Avoid: Calculating distance for all rows
SELECT *, ST_Distance(geom, ST_MakePoint(35.0, -15.0)) as dist 
FROM evacuation_centers 
ORDER BY dist;
```

### Memory Management

- Load layers on demand, not all at once
- Use `QgsVectorLayer.setSubsetString()` to filter large datasets
- Clear unused layers from memory

---

## Deployment

### Plugin Packaging

1. Create `metadata.txt`:
```ini
[general]
name=Disaster Risk Assessment
qgisMinimumVersion=3.0
description=Flood risk assessment and evacuation planning for Malawi
version=1.0
author=Your Team
email=your@email.com
```

2. Package plugin:
```bash
zip -r disaster_risk_assessment.zip malawi-disaster-management-db-main/
```

3. Install in QGIS:
   - Plugins → Manage and Install Plugins → Install from ZIP

---

## Future Enhancements

1. **Network Analysis**: Use road networks for realistic evacuation routes
2. **Real-time Data**: Integrate weather APIs for current conditions
3. **Mobile App**: Companion mobile app for field data collection
4. **Machine Learning**: Predict future flood risk using ML models
5. **Multi-hazard**: Extend to earthquakes, droughts, cyclones

---

## References

- QGIS Python API: https://qgis.org/pyqgis/
- PostGIS Documentation: https://postgis.net/docs/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

---

**Last Updated**: December 2024
