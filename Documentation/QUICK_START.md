# Quick Start Guide - Get Running in 10 Minutes

## 🚀 Fast Track Installation

### Step 1: Database (3 minutes)

```bash
# Create database
createdb -U postgres -p 5433 disaster_risk_db

# Enable PostGIS
psql -U postgres -p 5433 -d disaster_risk_db -c "CREATE EXTENSION postgis;"

# Restore data
psql -U postgres -p 5433 -d disaster_risk_db -f database/complete_backup.sql

# Verify (should show 28)
psql -U postgres -p 5433 -d disaster_risk_db -c "SELECT COUNT(*) FROM administrative_boundaries;"
```

### Step 2: Install Plugin (2 minutes)

**Windows:**
```powershell
# Copy plugin to QGIS
Copy-Item -Path "malawi-disaster-management-db-main" -Destination "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\" -Recurse
```

**Linux/Mac:**
```bash
# Copy plugin to QGIS
cp -r malawi-disaster-management-db-main ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

### Step 3: Enable in QGIS (1 minute)

1. Open QGIS
2. Plugins → Manage and Install Plugins
3. Find "Disaster Risk Assessment"
4. Check the box ✓
5. Close

### Step 4: Connect & Test (4 minutes)

1. **Click plugin icon** in toolbar
2. **Database Connection tab:**
   - Host: `localhost`
   - Port: `5433`
   - Database: `disaster_risk_db`
   - Username: `postgres`
   - Password: [your password]
   - Click **Connect**

3. **Districts & Data tab:**
   - Click **Load All Districts** → See 28 districts on map ✓

4. **Flood Risk Analysis tab:**
   - Select "All Districts"
   - Click **Run Flood Risk Analysis** → See results ✓

5. **Evacuation Planning tab:**
   - Select "Nsanje"
   - Click **Calculate Capacity Gap** → See analysis ✓
   - Click **Generate Full Evacuation Plan** → See complete plan ✓

---

## ✅ You're Done!

**Total Time**: ~10 minutes

---

## 🎯 What You Can Do Now

### Analyze Flood Risk
```
1. Go to "Flood Risk Analysis" tab
2. Select district or "All Districts"
3. Click "Run Flood Risk Analysis"
4. View results in "Results & Maps" tab
5. Export to CSV
```

### Plan Evacuations
```
1. Go to "Evacuation Planning" tab
2. Select a district
3. Click "View Evacuation Centers"
4. Click "Calculate Capacity Gap"
5. Click "Plan Evacuation Routes"
6. Click "Generate Full Evacuation Plan"
7. Click "Export Plan to File"
```

### Visualize Data
```
1. Go to "Districts & Data" tab
2. Click "Load Water Bodies" → See rivers/lakes
3. Click "Load Historical Disasters" → See past events
4. Click "Load Risk Zones" → See risk areas
5. Click "Load Infrastructure" → See facilities
```

---

## 🆘 Quick Troubleshooting

**Can't connect to database?**
```bash
# Check PostgreSQL is running
pg_ctl status

# Start if needed
pg_ctl start
```

**Plugin not showing?**
- Check plugin folder exists
- Restart QGIS
- Check Plugins → Manage and Install Plugins

**No data showing?**
- Verify database restore completed
- Check connection is active (green status)
- Try loading districts again

---

## 📚 Full Documentation

- **USER_GUIDE.md** - Complete user manual
- **INSTALLATION.md** - Detailed installation
- **TECHNICAL_DOCUMENTATION.md** - For developers
- **PRESENTATION_GUIDE.md** - For presentation

---

## 🎥 Watch the Demo

[Link to presentation video]

---

**Need help?** Check the full documentation or open an issue on GitHub.

