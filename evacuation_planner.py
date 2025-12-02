# -*- coding: utf-8 -*-
"""
Evacuation Planner - Safe zone identification and route calculation
"""

from qgis.core import QgsGeometry, QgsPointXY

class EvacuationPlanner:
    def __init__(self, db_manager):
        self.db = db_manager

    def identify_safe_zones(self, risk_layer, min_area_sqkm=1.0):
        """
        Identify areas suitable for evacuation centers
        Criteria: Low/Safe risk areas with sufficient space
        """
        safe_zones = []
        
        for feature in risk_layer.getFeatures():
            risk_category = feature['risk_category']
            area_sqkm = feature.geometry().area() / 1000000
            
            if risk_category in ['Low', 'Safe'] and area_sqkm >= min_area_sqkm:
                safe_zones.append({
                    'area_id': feature['area_id'],
                    'area_name': feature['area_name'],
                    'geometry': feature.geometry(),
                    'area_sqkm': area_sqkm
                })
        
        return safe_zones

    def calculate_evacuation_routes(self, high_risk_areas, evacuation_centers):
        """
        Calculate optimal evacuation routes from high-risk areas to safe centers
        """
        routes = []
        
        for risk_area in high_risk_areas:
            risk_centroid = risk_area.geometry().centroid()
            nearest_center = None
            min_distance = float('inf')
            
            for center in evacuation_centers:
                center_point = center.geometry().asPoint()
                distance = risk_centroid.distance(QgsGeometry.fromPointXY(center_point))
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_center = center
            
            if nearest_center:
                # Create straight-line route
                route_geom = QgsGeometry.fromPolylineXY([
                    risk_centroid.asPoint(),
                    nearest_center.geometry().asPoint()
                ])
                
                routes.append({
                    'from_area_id': risk_area['area_id'],
                    'to_center_id': nearest_center['center_id'],
                    'distance_km': min_distance / 1000,
                    'geometry': route_geom
                })
        
        return routes

    def save_evacuation_routes_to_db(self, routes):
        """Save calculated evacuation routes to database"""
        for route in routes:
            query = """
            INSERT INTO evacuation_routes
            (from_area_id, to_center_id, distance_km, estimated_time_minutes, geom)
            VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326))
            """
            
            # Estimate time: assume 5 km/h walking speed
            estimated_time = int((route['distance_km'] / 5) * 60)
            
            params = (
                route['from_area_id'],
                route['to_center_id'],
                route['distance_km'],
                estimated_time,
                route['geometry'].asWkt()
            )
            
            self.db.execute_query(query, params, fetch=False)