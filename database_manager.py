# -*- coding: utf-8 -*-
"""
Database Manager - Handles PostgreSQL/PostGIS connections and operations
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from qgis.core import QgsVectorLayer, QgsDataSourceUri

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.connection_params = {}

    def connect(self, host, port, database, user, password):
        """Establish database connection"""
        try:
            self.connection_params = {
                'host': host,
                'port': port,
                'database': database,
                'user': user,
                'password': password
            }
            
            self.conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            return True, "Connected successfully"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"

    def execute_query(self, query, params=None, fetch=True):
        """Execute SQL query"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            
            if fetch:
                return cursor.fetchall()
            else:
                self.conn.commit()
                return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Query error: {str(e)}")

    def load_layer_from_db(self, table_name, geometry_column='geom', layer_name=None, where_clause=None):
        """Load PostGIS layer into QGIS"""
        try:
            uri = QgsDataSourceUri()
            uri.setConnection(
                self.connection_params['host'],
                self.connection_params['port'],
                self.connection_params['database'],
                self.connection_params['user'],
                self.connection_params['password']
            )
            
            uri.setDataSource("public", table_name, geometry_column, where_clause)
            
            if layer_name is None:
                layer_name = table_name.replace('_', ' ').title()
            
            layer = QgsVectorLayer(uri.uri(), layer_name, "postgres")
            
            if layer.isValid():
                return layer, "Layer loaded successfully"
            else:
                return None, "Invalid layer"
        except Exception as e:
            return None, f"Error loading layer: {str(e)}"

    def get_flood_prone_districts(self):
        """Get districts most prone to flooding"""
        query = """
        SELECT 
            ab.boundary_id,
            ab.boundary_name as district,
            ab.population,
            ab.area_sqkm,
            COUNT(DISTINCT de.event_id) as total_flood_events,
            SUM(de.casualties) as total_casualties,
            SUM(de.displaced_people) as total_people_displaced,
            ROUND(SUM(de.economic_loss_usd)/1000000, 2) as economic_loss_millions_usd,
            STRING_AGG(DISTINCT wb.water_name, ', ') as flood_prone_rivers,
            COUNT(DISTINCT wb.water_id) as num_flood_prone_waters,
            CASE 
                WHEN COUNT(DISTINCT de.event_id) >= 3 THEN 'EXTREME RISK'
                WHEN COUNT(DISTINCT de.event_id) = 2 THEN 'HIGH RISK'
                WHEN COUNT(DISTINCT de.event_id) = 1 THEN 'MEDIUM RISK'
                WHEN COUNT(DISTINCT wb.water_id) > 0 THEN 'LOW RISK'
                ELSE 'MINIMAL RISK'
            END as flood_risk_level
        FROM administrative_boundaries ab
        LEFT JOIN disaster_events de 
            ON ab.boundary_name = de.affected_area 
            AND de.event_type = 'flood'
        LEFT JOIN water_bodies wb 
            ON ab.boundary_id = wb.boundary_id 
            AND wb.flood_prone = TRUE
        GROUP BY ab.boundary_id, ab.boundary_name, ab.population, ab.area_sqkm
        HAVING COUNT(DISTINCT de.event_id) > 0 OR COUNT(DISTINCT wb.water_id) > 0
        ORDER BY 
            COUNT(DISTINCT de.event_id) DESC,
            SUM(de.displaced_people) DESC;
        """
        return self.execute_query(query)

    def get_district_by_river(self, river_name):
        """Find which district a river is in"""
        query = """
        SELECT 
            wb.water_name,
            ab.boundary_name as district_name,
            wb.water_type,
            wb.flood_prone,
            wb.length_km
        FROM water_bodies wb
        JOIN administrative_boundaries ab ON wb.boundary_id = ab.boundary_id
        WHERE wb.water_name ILIKE %s;
        """
        return self.execute_query(query, (f'%{river_name}%',))

    def get_historical_events_in_district(self, district_name):
        """Get historical disaster events in a district"""
        query = """
        SELECT 
            event_id,
            event_type, 
            event_date, 
            severity, 
            affected_area,
            casualties,
            displaced_people,
            economic_loss_usd,
            description
        FROM disaster_events
        WHERE affected_area = %s
        ORDER BY event_date DESC;
        """
        return self.execute_query(query, (district_name,))

    def get_all_districts(self):
        """Get all administrative boundaries (districts)"""
        query = """
        SELECT 
            boundary_id,
            boundary_name,
            boundary_type,
            boundary_code,
            population,
            area_sqkm
        FROM administrative_boundaries
        ORDER BY boundary_name;
        """
        return self.execute_query(query)

    def get_infrastructure_in_district(self, district_id):
        """Get all infrastructure in a district"""
        query = """
        SELECT 
            infra_id,
            infra_name,
            infra_type,
            capacity,
            operational_status,
            vulnerability_score
        FROM infrastructure
        WHERE boundary_id = %s
        ORDER BY infra_type, infra_name;
        """
        return self.execute_query(query, (district_id,))

    def get_evacuation_centers(self, district_id=None):
        """Get evacuation centers, optionally filtered by district"""
        if district_id:
            query = """
            SELECT 
                center_id,
                center_name,
                capacity,
                current_occupancy,
                facilities,
                accessibility_score,
                ab.boundary_name as district
            FROM evacuation_centers ec
            JOIN administrative_boundaries ab ON ec.boundary_id = ab.boundary_id
            WHERE ec.boundary_id = %s
            ORDER BY capacity DESC;
            """
            return self.execute_query(query, (district_id,))
        else:
            query = """
            SELECT 
                center_id,
                center_name,
                capacity,
                current_occupancy,
                facilities,
                accessibility_score,
                ab.boundary_name as district
            FROM evacuation_centers ec
            JOIN administrative_boundaries ab ON ec.boundary_id = ab.boundary_id
            ORDER BY ab.boundary_name, capacity DESC;
            """
            return self.execute_query(query)

    def get_risk_zones(self, risk_level=None):
        """Get risk zones, optionally filtered by risk level"""
        if risk_level:
            query = """
            SELECT 
                rz.zone_id,
                rz.zone_name,
                rz.risk_level,
                rz.risk_type,
                rz.affected_population,
                rz.risk_score,
                ab.boundary_name as district
            FROM risk_zones rz
            JOIN administrative_boundaries ab ON rz.boundary_id = ab.boundary_id
            WHERE rz.risk_level = %s
            ORDER BY rz.risk_score DESC;
            """
            return self.execute_query(query, (risk_level,))
        else:
            query = """
            SELECT 
                rz.zone_id,
                rz.zone_name,
                rz.risk_level,
                rz.risk_type,
                rz.affected_population,
                rz.risk_score,
                ab.boundary_name as district
            FROM risk_zones rz
            JOIN administrative_boundaries ab ON rz.boundary_id = ab.boundary_id
            ORDER BY rz.risk_score DESC;
            """
            return self.execute_query(query)

    def get_district_summary(self, district_name):
        """Get complete summary for a specific district"""
        query = """
        SELECT 
            ab.boundary_name as district,
            ab.boundary_code,
            ab.population,
            ab.area_sqkm,
            COUNT(DISTINCT wb.water_id) as num_water_bodies,
            COUNT(DISTINCT de.event_id) as num_disasters,
            SUM(de.casualties) as total_casualties,
            SUM(de.displaced_people) as total_displaced,
            ROUND(SUM(de.economic_loss_usd), 2) as total_economic_loss,
            STRING_AGG(DISTINCT wb.water_name, ', ') as water_bodies_list
        FROM administrative_boundaries ab
        LEFT JOIN water_bodies wb ON ab.boundary_id = wb.boundary_id
        LEFT JOIN disaster_events de ON ab.boundary_name = de.affected_area
        WHERE ab.boundary_name = %s
        GROUP BY ab.boundary_id, ab.boundary_name, ab.boundary_code, ab.population, ab.area_sqkm;
        """
        result = self.execute_query(query, (district_name,))
        return result[0] if result else None

    def get_population_data(self, district_id):
        """Get population data for a district"""
        query = """
        SELECT 
            census_year,
            total_population,
            male_population,
            female_population,
            households,
            vulnerable_population
        FROM population_data
        WHERE boundary_id = %s
        ORDER BY census_year DESC;
        """
        return self.execute_query(query, (district_id,))

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()