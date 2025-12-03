# Installation Guide - Malawi Disaster Risk Assessment System

## Complete Step-by-Step Installation

---

## Part 1: Database Setup

### Step 1: Install PostgreSQL with PostGIS

**Windows:**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer
3. During installation, select "PostGIS" in the Stack Builder
4. Note your password and port (default: 5432)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib postgis
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql postgis
brew services start postgresql
```

### Step 2: Create Database

**Option A: Command Line**

```bash
# Create database
createdb -U postgres -p 5433 disaster_risk_db

# Connect to database
psql -U postgres -p 5433 -d disaster_risk_db

# Enable PostGIS
CREATE EXTENSION postgis;

# Verify PostGIS installation
SELECT PostGIS_version();

# Exit
\q
```

**Option B: pgAdmin (GUI)**

1. Open pgAdmin 4
2. Right-click on "Databases" → Create → Database
3. Name: `disaster_risk_db`
4. Click Save
5. Right-click on `disaster_risk_db` → Query Tool
6. Run: `CREATE EXTENSION postgis;`
7. Verify: `SELECT PostGIS_version();`

### Step 3: Restore Database from Backup

**Option A: Command Line**

```bash
# Navigate to project directory
cd malawi-disaster-management-db-main

# Restore database
psql -U postgres -p 5433 -d disaster_risk_db -f database/complete_backup.sql

# Verify tables were created
psql -U postgres -p 5433 -d disaster_risk_db -c "\dt"
```

**Option B: pgAdmin (GUI)**

1. Right-click on `disaster_risk_db` → Restore
2. Format: Plain
3. Filename: Browse to `database/complete_backup.sql`
4. Click Restore
5. Wait for completion message
6. Refresh database to see tables

### Step 4: Verify Database

```sql
-- Connect to database
psql -U postgres -p 5433 -d disaster_risk_db

-- Check tables
\dt

-- Count records in key tables
SELECT 'administrative_boundaries' as table_name, COUNT(*) as records FROM administrative_boundaries
UNION ALL
SELECT 'water_bodies', COUNT(*) FROM water_bodies
UNION ALL
SELECT 'disaster_events', COUNT(*) FROM disaster_events
UNION ALL
SELECT 'evacuation_centers', COUNT(*) FROM evacuation_centers
UNION ALL
SELECT 'risk_zones', COUNT(*) FROM risk_zones;

-- Expected output:
-- administrative_boundaries: 28
-- water_bodies: 8
-- disaster_events: 20
-- evacuation_centers: 8
-- risk_zones: 7

-- Test spatial query
SELECT boundary_name, ST_AsText(ST_Centroid(geom)) as centroid 
FROM administrative_boundaries 
LIMIT 3;

-- Exit
\q
```

---

## Part 2: QGIS Installation

### Step 1: Install QGIS

**Windows:**
1. Download QGIS from https://qgis.org/en/site/forusers/download.html
2. Choose "QGIS Standalone Installer" (latest version)
3. Run installer with default options
4. Launch QGIS Desktop

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install qgis qgis-plugin-grass
```

**macOS:**
```bash
brew install qgis
```

Or download from https://qgis.org/en/site/forusers/download.html

### Step 2: Verify QGIS Installation

1. Open QGIS
2. Go to Help → About
3. Verify version is 3.0 or higher
4. Check Python version (should be 3.7+)

---

## Part 3: Plugin Installation

### Method 1: Manual Installation (Recommended)

**Step 1: Clone or Download Repository**

```bash
# Option A: Using Git
git clone https://github.com/yourusername/malawi-disaster-management.git

# Option B: Download ZIP
# Download from GitHub and extract
```

**Step 2: Locate QGIS Plugins Directory**

**Windows:**
```
C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
```

**Linux:**
```
~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

**macOS:**
```
~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
```

**Step 3: Copy Plugin Files**

```bash
# Windows (PowerShell)
Copy-Item -Path "malawi-disaster-management-db-main" -Destination "C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\" -Recurse

# Linux/macOS
cp -r malawi-disaster-management-db-main ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

**Step 4: Enable Plugin in QGIS**

1. Open QGIS
2. Go to **Plugins → Manage and Install Plugins**
3. Click **Installed** tab
4. Find "Disaster Risk Assessment"
5. Check the box to enable
6. Click Close

**Step 5: Verify Plugin Installation**

1. Look for the plugin icon in the toolbar
2. Or go to **Plugins** menu and find "Disaster Risk Assessment"
3. Click to open the plugin dialog

### Method 2: ZIP Installation

**Step 1: Create Plugin ZIP**

```bash
# Navigate to parent directory
cd ..

# Create ZIP file
zip -r disaster_risk_assessment.zip malawi-disaster-management-db-main/

# Or on Windows (PowerShell)
Compress-Archive -Path malawi-disaster-management-db-main -DestinationPath disaster_risk_assessment.zip
```

**Step 2: Install in QGIS**

1. Open QGIS
2. Go to **Plugins → Manage and Install Plugins**
3. Click **Install from ZIP** tab
4. Browse to `disaster_risk_assessment.zip`
5. Click **Install Plugin**
6. Wait for installation to complete
7. Click Close

---

## Part 4: First Run Configuration

### Step 1: Launch Plugin

1. Click the **Disaster Risk Assessment** icon in toolbar
2. Plugin dialog should open with 5 tabs

### Step 2: Configure Database Connection

1. Go to **Database Connection** tab
2. Enter your database credentials:
   - **Host**: `localhost`
   - **Port**: `5433` (or `5432` if you used default)
   - **Database**: `disaster_risk_db`
   - **Username**: `postgres`
   - **Password**: [your PostgreSQL password]
3. Click **Connect to Database**
4. Wait for "Connected successfully" message
5. Verify districts are loaded in dropdowns

### Step 3: Test Basic Functionality

**Test 1: Load Districts**
1. Go to **Districts & Data** tab
2. Click **Load All Districts**
3. Verify 28 districts appear on map

**Test 2: View District Info**
1. Select "Zomba" from dropdown
2. Click **View District Details**
3. Verify information appears

**Test 3: Run Analysis**
1. Go to **Flood Risk Analysis** tab
2. Select "All Districts"
3. Click **Run Flood Risk Analysis**
4. Verify results appear in Results tab

**Test 4: Evacuation Planning**
1. Go to **Evacuation Planning** tab
2. Select "Nsanje"
3. Click **Calculate Capacity Gap**
4. Verify capacity analysis appears

---

## Part 5: Troubleshooting

### Issue 1: "Connection failed" Error

**Possible Causes:**
- PostgreSQL not running
- Wrong port number
- Wrong password
- Database doesn't exist

**Solutions:**

```bash
# Check if PostgreSQL is running
# Windows
pg_ctl status

# Linux
sudo systemctl status postgresql

# Start PostgreSQL if not running
# Windows
pg_ctl start

# Linux
sudo systemctl start postgresql

# Verify database exists
psql -U postgres -l

# Test connection
psql -U postgres -p 5433 -d disaster_risk_db
```

### Issue 2: Plugin Not Appearing

**Solutions:**

1. **Check plugin directory:**
```bash
# Windows
dir "C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\"

# Linux/macOS
ls ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

2. **Check plugin files:**
   - Verify `__init__.py` exists
   - Verify `metadata.txt` exists

3. **Check QGIS Python console for errors:**
   - Go to **Plugins → Python Console**
   - Look for error messages

4. **Reinstall plugin:**
   - Delete plugin folder
   - Copy again
   - Restart QGIS

### Issue 3: "Invalid layer" Error

**Solutions:**

1. **Verify PostGIS extension:**
```sql
SELECT PostGIS_version();
```

2. **Check table geometries:**
```sql
SELECT f_table_name, f_geometry_column, srid, type 
FROM geometry_columns;
```

3. **Verify SRID is 4326:**
```sql
SELECT DISTINCT ST_SRID(geom) FROM administrative_boundaries;
```

### Issue 4: Python Import Errors

**Solutions:**

1. **Check Python version in QGIS:**
   - Go to **Help → About**
   - Verify Python 3.7+

2. **Install missing packages:**
```bash
# In QGIS Python console
import pip
pip.main(['install', 'psycopg2'])
```

### Issue 5: Slow Performance

**Solutions:**

1. **Create spatial indexes:**
```sql
CREATE INDEX IF NOT EXISTS idx_admin_boundaries_geom 
ON administrative_boundaries USING GIST(geom);

CREATE INDEX IF NOT EXISTS idx_water_bodies_geom 
ON water_bodies USING GIST(geom);

CREATE INDEX IF NOT EXISTS idx_risk_zones_geom 
ON risk_zones USING GIST(geom);

CREATE INDEX IF NOT EXISTS idx_evacuation_centers_geom 
ON evacuation_centers USING GIST(geom);
```

2. **Vacuum database:**
```sql
VACUUM ANALYZE;
```

---

## Part 6: Verification Checklist

- [ ] PostgreSQL installed and running
- [ ] PostGIS extension enabled
- [ ] Database `disaster_risk_db` created
- [ ] Database restored from backup
- [ ] 28 districts in `administrative_boundaries` table
- [ ] QGIS 3.0+ installed
- [ ] Plugin files copied to plugins directory
- [ ] Plugin enabled in QGIS
- [ ] Plugin icon visible in toolbar
- [ ] Database connection successful
- [ ] Districts load on map
- [ ] Analysis runs without errors
- [ ] Evacuation planning works

---

## Part 7: Uninstallation (if needed)

### Remove Plugin

1. Open QGIS
2. Go to **Plugins → Manage and Install Plugins**
3. Find "Disaster Risk Assessment"
4. Click **Uninstall Plugin**

Or manually delete:
```bash
# Windows
Remove-Item -Path "C:\Users\[YourUsername]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\malawi-disaster-management-db-main" -Recurse

# Linux/macOS
rm -rf ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/malawi-disaster-management-db-main
```

### Remove Database

```bash
# Drop database
dropdb -U postgres -p 5433 disaster_risk_db
```

---

## Support

If you encounter issues not covered here:

1. Check **TECHNICAL_DOCUMENTATION.md** for detailed information
2. Review **USER_GUIDE.md** for usage instructions
3. Open an issue on GitHub
4. Contact: disaster.management@example.com

---

**Installation complete! You're ready to use the Malawi Disaster Risk Assessment System.**

