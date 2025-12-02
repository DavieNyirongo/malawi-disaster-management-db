# -*- coding: utf-8 -*-
"""
Disaster Risk Assessment System
A QGIS plugin for flood risk and natural disaster analysis
"""

def classFactory(iface):
    """Load DisasterRiskAssessment class from file disaster_risk_assessment.
    
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .disaster_risk_assessment import DisasterRiskAssessment
    return DisasterRiskAssessment(iface)