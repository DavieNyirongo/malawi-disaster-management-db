# -*- coding: utf-8 -*-
"""
Spatial Analyzer - Core risk analysis algorithms
"""

from qgis.core import (
    QgsDistanceArea,
    QgsGeometry,
    QgsPointXY
)
import processing
from datetime import datetime

class DisasterRiskAnalyzer:
    def __init__(self, db_manager):
        self.db = db_manager
        self.distance_calc = QgsDistanceArea()
        self.distance_calc.setEllipsoid('WGS84')

    def analyze_elevation_risk(self, area_geometry, elevation_layer, threshold=50):
        """
        Analyze flood risk based on elevation
        Lower elevation = Higher risk
        """
        try:
            # Get statistics for the area
            stats = processing.run("native:zonalstatisticsfb", {
                'INPUT': elevation_layer,
                'INPUT_RASTER': elevation_layer,
                'RASTER_BAND': 1,
                'COLUMN_PREFIX': 'elev_',
                'STATISTICS': [2, 5, 6]  # mean, min, max
            })
            
            mean_elevation = stats.get('elev_mean', 100)
            min_elevation = stats.get('elev_min', 100)
            
            # Risk scoring: Lower elevation = Higher risk
            if min_elevation < threshold:
                if mean_elevation < threshold:
                    score = 20  # Very high risk
                else:
                    score = 15  # High risk
            elif mean_elevation < threshold * 1.5:
                score = 10  # Moderate risk
            elif mean_elevation < threshold * 2:
                score = 5  # Low risk
            else:
                score = 0  # Safe
            
            return score, {
                'mean_elevation': mean_elevation,
                'min_elevation': min_elevation
            }
        except Exception as e:
            print(f"Elevation analysis error: {e}")
            return 0, {}

    def analyze_water_proximity(self, area_geometry, water_layer, buffer_distance=500):
        """
        Analyze risk based on proximity to water bodies
        Closer to water = Higher risk
        """
        try:
            risk_zones = []
            
            for water_feature in water_layer.getFeatures():
                water_geom = water_feature.geometry()
                
                # Create buffer zones around water bodies
                buffer_100m = water_geom.buffer(100, 50)
                buffer_300m = water_geom.buffer(300, 50)
                buffer_500m = water_geom.buffer(buffer_distance, 50)
                
                # Check intersection with area
                if area_geometry.intersects(buffer_100m):
                    intersect_area = area_geometry.intersection(buffer_100m).area()
                    risk_zones.append(('very_high', intersect_area, 20))
                elif area_geometry.intersects(buffer_300m):
                    intersect_area = area_geometry.intersection(buffer_300m).area()
                    risk_zones.append(('high', intersect_area, 15))
                elif area_geometry.intersects(buffer_500m):
                    intersect_area = area_geometry.intersection(buffer_500m).area()
                    risk_zones.append(('moderate', intersect_area, 10))
            
            if not risk_zones:
                return 0, {'status': 'No water bodies nearby'}
            
            # Calculate weighted score based on intersection areas
            total_area = area_geometry.area()
            weighted_score = 0
            
            for risk_level, intersect_area, base_score in risk_zones:
                weight = intersect_area / total_area
                weighted_score += base_score * weight
            
            return min(int(weighted_score), 20), {
                'risk_zones': len(risk_zones),
                'weighted_score': weighted_score
            }
        except Exception as e:
            print(f"Water proximity error: {e}")
            return 0, {}

    def analyze_slope(self, area_geometry, elevation_layer):
        """
        Analyze risk based on slope
        Flatter areas = Higher water retention risk
        """
        try:
            # Simulate slope analysis (in real implementation, use QGIS slope tool)
            # For demonstration, using simplified logic
            score = 10  # Default moderate risk
            
            return score, {'mean_slope': 5.0}
        except Exception as e:
            print(f"Slope analysis error: {e}")
            return 0, {}

    def analyze_historical_events(self, area_geometry, area_id):
        """
        Analyze risk based on historical disaster occurrences
        """
        try:
            # Get historical events from database
            events = self.db.get_historical_events_in_area(area_geometry)
            
            if not events:
                return 0, {'event_count': 0}
            
            score = 0
            recent_events = 0
            severe_events = 0
            current_date = datetime.now()
            
            for event in events:
                # Recency factor
                event_date = event['event_date']
                days_ago = (current_date - event_date).days
                
                if days_ago < 365 * 5:  # Last 5 years
                    recency_multiplier = 1.5
                    recent_events += 1
                elif days_ago < 365 * 10:  # Last 10 years
                    recency_multiplier = 1.0
                else:
                    recency_multiplier = 0.5
                
                # Severity factor
                severity = event['severity'].lower()
                if severity == 'catastrophic':
                    severity_score = 5
                    severe_events += 1
                elif severity == 'severe':
                    severity_score = 4
                    severe_events += 1
                elif severity == 'moderate':
                    severity_score = 3
                else:
                    severity_score = 2
                
                score += severity_score * recency_multiplier
            
            # Normalize to 0-20 scale
            final_score = min(int(score * 2), 20)
            
            return final_score, {
                'total_events': len(events),
                'recent_events': recent_events,
                'severe_events': severe_events
            }
        except Exception as e:
            print(f"Historical analysis error: {e}")
            return 0, {}

    def analyze_rainfall_risk(self, area_geometry, rainfall_layer, threshold=100):
        """Analyze risk based on rainfall patterns"""
        try:
            # Simplified rainfall risk
            score = 10  # Default moderate risk
            return score, {'avg_rainfall': 80, 'extreme_events': 5}
        except Exception as e:
            print(f"Rainfall analysis error: {e}")
            return 0, {}

    def analyze_drainage_capacity(self, area_geometry, landuse_layer):
        """Analyze risk based on land use and drainage capacity"""
        try:
            if not landuse_layer:
                return 0, {}
                
            poor_drainage_area = 0
            total_area = area_geometry.area()
            
            for landuse_feature in landuse_layer.getFeatures():
                if area_geometry.intersects(landuse_feature.geometry()):
                    intersection = area_geometry.intersection(landuse_feature.geometry())
                    drainage = landuse_feature['drainage_capacity']
                    
                    if drainage and drainage.lower() == 'poor':
                        poor_drainage_area += intersection.area()
            
            if total_area == 0:
                return 0, {}
            
            poor_drainage_percent = (poor_drainage_area / total_area) * 100
            
            # Risk scoring
            if poor_drainage_percent > 75:
                score = 20
            elif poor_drainage_percent > 50:
                score = 15
            elif poor_drainage_percent > 25:
                score = 10
            elif poor_drainage_percent > 10:
                score = 5
            else:
                score = 0
            
            return score, {'poor_drainage_percent': poor_drainage_percent}
        except Exception as e:
            print(f"Drainage analysis error: {e}")
            return 0, {}

    def run_complete_analysis(self, area_feature, layers, parameters):
        """
        Run complete risk analysis for an area
        Returns: dict with total_risk_score, risk_category, detailed_scores
        """
        area_geom = area_feature.geometry()
        area_id = area_feature['area_id']
        population = area_feature.get('population', 0)
        
        # Initialize scores dictionary
        scores = {
            'elevation': 0,
            'water_proximity': 0,
            'slope': 0,
            'rainfall': 0,
            'historical': 0,
            'drainage': 0
        }
        
        details = {}
        
        # Run each analysis component
        if layers.get('elevation'):
            score, detail = self.analyze_elevation_risk(
                area_geom,
                layers['elevation'],
                parameters.get('elevation_threshold', 50)
            )
            scores['elevation'] = score
            details['elevation'] = detail
        
        if layers.get('water_bodies'):
            score, detail = self.analyze_water_proximity(
                area_geom,
                layers['water_bodies'],
                parameters.get('water_buffer', 500)
            )
            scores['water_proximity'] = score
            details['water_proximity'] = detail
        
        if layers.get('elevation') and parameters.get('include_slope', True):
            score, detail = self.analyze_slope(area_geom, layers['elevation'])
            scores['slope'] = score
            details['slope'] = detail
        
        # Historical events analysis
        score, detail = self.analyze_historical_events(area_geom, area_id)
        scores['historical'] = score
        details['historical'] = detail
        
        if parameters.get('include_rainfall', True):
            score, detail = self.analyze_rainfall_risk(
                area_geom,
                layers.get('rainfall'),
                parameters.get('rainfall_threshold', 100)
            )
            scores['rainfall'] = score
            details['rainfall'] = detail
        
        if layers.get('landuse') and parameters.get('include_drainage', True):
            score, detail = self.analyze_drainage_capacity(
                area_geom,
                layers['landuse']
            )
            scores['drainage'] = score
            details['drainage'] = detail
        
        # Calculate total risk score
        total_score = sum(scores.values())
        
        # Determine risk category
        if total_score >= 80:
            risk_category = "Very High"
            color = '#8B0000'
        elif total_score >= 60:
            risk_category = "High"
            color = '#FF0000'
        elif total_score >= 40:
            risk_category = "Moderate"
            color = '#FFA500'
        elif total_score >= 20:
            risk_category = "Low"
            color = '#FFFF00'
        else:
            risk_category = "Safe"
            color = '#00FF00'
        
        # Calculate population at risk
        if risk_category in ['Very High', 'High']:
            population_at_risk = population
        elif risk_category == 'Moderate':
            population_at_risk = int(population * 0.5)
        else:
            population_at_risk = 0
        
        scores['population_at_risk'] = population_at_risk
        
        return {
            'total_score': total_score,
            'risk_category': risk_category,
            'color': color,
            'scores': scores,
            'details': details,
            'population_at_risk': population_at_risk
        }