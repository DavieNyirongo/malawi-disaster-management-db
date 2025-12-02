# -*- coding: utf-8 -*-
"""
Main Plugin Class - Disaster Risk Assessment System
"""

from qgis.PyQt.QtCore import QSettings, QCoreApplication
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QTableWidgetItem
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsSymbol,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory
)

from .database_manager import DatabaseManager
from .disaster_risk_dialog import DisasterRiskDialog

import os.path

class DisasterRiskAssessment:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        
        self.db_manager = DatabaseManager()
        
        self.action = None
        self.dlg = None

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI"""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        
        self.action = QAction(
            QIcon(icon_path) if os.path.exists(icon_path) else QIcon(),
            "Disaster Risk Assessment",
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)
        
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Disaster Risk Assessment", self.action)

    def unload(self):
        """Remove the plugin menu item and icon"""
        self.iface.removePluginMenu("&Disaster Risk Assessment", self.action)
        self.iface.removeToolBarIcon(self.action)
        
        if self.db_manager:
            self.db_manager.close()

    def connect_signals(self):
        """Connect UI button clicks to functions"""
        # Connection tab
        self.dlg.connectButton.clicked.connect(self.connect_to_database)
        
        # Districts tab
        self.dlg.loadDistrictsButton.clicked.connect(self.load_all_districts)
        self.dlg.viewDistrictInfoButton.clicked.connect(self.view_district_info)
        self.dlg.loadWaterBodiesButton.clicked.connect(self.load_water_bodies)
        self.dlg.loadDisastersButton.clicked.connect(self.load_disasters)
        self.dlg.loadInfrastructureButton.clicked.connect(self.load_infrastructure)
        self.dlg.loadRiskZonesButton.clicked.connect(self.load_risk_zones)
        
        # Analysis tab
        self.dlg.runFloodAnalysisButton.clicked.connect(self.run_flood_analysis)
        
        # Results tab
        self.dlg.generateFloodMapButton.clicked.connect(self.generate_flood_map)
        self.dlg.exportResultsButton.clicked.connect(self.export_results)
        self.dlg.viewDetailsButton.clicked.connect(self.view_district_details)
        
        # Evacuation tab
        self.dlg.viewEvacuationCentersButton.clicked.connect(self.view_evacuation_centers)
        self.dlg.calculateCapacityButton.clicked.connect(self.calculate_evacuation_capacity)

    def connect_to_database(self):
        """Connect to PostgreSQL database"""
        host = self.dlg.hostLineEdit.text()
        port = self.dlg.portLineEdit.text()
        database = self.dlg.databaseLineEdit.text()
        user = self.dlg.userLineEdit.text()
        password = self.dlg.passwordLineEdit.text()
        
        success, message = self.db_manager.connect(host, port, database, user, password)
        
        if success:
            self.dlg.statusLabel.setText("Status: Connected ✓")
            self.dlg.statusLabel.setStyleSheet("color: green; font-weight: bold;")
            
            self.dlg.logTextBrowser.append("✓ Connected to database successfully!")
            self.dlg.logTextBrowser.append(f"Database: {database}")
            self.dlg.logTextBrowser.append(f"Host: {host}:{port}")
            
            # Populate district dropdowns
            self.populate_district_lists()
            
            QMessageBox.information(self.dlg, "Success", "Connected to Malawi Disaster Database!")
        else:
            self.dlg.statusLabel.setText("Status: Connection Failed ✗")
            self.dlg.statusLabel.setStyleSheet("color: red; font-weight: bold;")
            self.dlg.logTextBrowser.append(f"✗ Connection failed: {message}")
            QMessageBox.critical(self.dlg, "Error", message)

    def populate_district_lists(self):
        """Populate all district combo boxes"""
        try:
            districts = self.db_manager.get_all_districts()
            
            self.dlg.districtComboBox.clear()
            self.dlg.analysisDistrictCombo.clear()
            self.dlg.evacuationDistrictCombo.clear()
            
            self.dlg.analysisDistrictCombo.addItem("All Districts")
            
            for district in districts:
                district_name = district['boundary_name']
                self.dlg.districtComboBox.addItem(district_name)
                self.dlg.analysisDistrictCombo.addItem(district_name)
                self.dlg.evacuationDistrictCombo.addItem(district_name)
            
            self.dlg.logTextBrowser.append(f"✓ Loaded {len(districts)} districts into dropdowns")
        except Exception as e:
            self.dlg.logTextBrowser.append(f"✗ Error loading districts: {str(e)}")

    def load_all_districts(self):
        """Load administrative boundaries layer"""
        try:
            layer, message = self.db_manager.load_layer_from_db(
                'administrative_boundaries',
                layer_name='Malawi Districts'
            )
            
            if layer:
                QgsProject.instance().addMapLayer(layer)
                self.iface.mapCanvas().setExtent(layer.extent())
                self.iface.mapCanvas().refresh()
                self.dlg.logTextBrowser.append("✓ Loaded: Malawi Districts (28 districts)")
                QMessageBox.information(self.dlg, "Success", "Loaded 28 Malawi districts!")
            else:
                self.dlg.logTextBrowser.append(f"✗ Failed to load districts: {message}")
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Failed to load districts: {str(e)}")

    def view_district_info(self):
        """Display detailed information about selected district"""
        try:
            district_name = self.dlg.districtComboBox.currentText()
            if not district_name:
                QMessageBox.warning(self.dlg, "Warning", "Please select a district")
                return
            
            summary = self.db_manager.get_district_summary(district_name)
            
            if summary:
                info_html = f"""
                <h2>{summary['district']}</h2>
                <table border='1' cellpadding='5'>
                <tr><td><b>District Code:</b></td><td>{summary['boundary_code']}</td></tr>
                <tr><td><b>Population:</b></td><td>{summary['population']:,}</td></tr>
                <tr><td><b>Area:</b></td><td>{summary['area_sqkm']:.2f} sq km</td></tr>
                <tr><td><b>Water Bodies:</b></td><td>{summary['num_water_bodies']}</td></tr>
                <tr><td><b>Historical Disasters:</b></td><td>{summary['num_disasters'] or 0}</td></tr>
                <tr><td><b>Total Casualties:</b></td><td>{summary['total_casualties'] or 0}</td></tr>
                <tr><td><b>People Displaced:</b></td><td>{summary['total_displaced'] or 0:,}</td></tr>
                <tr><td><b>Economic Loss:</b></td><td>${summary['total_economic_loss'] or 0:,.2f}</td></tr>
                </table>
                <br>
                <b>Rivers/Lakes:</b> {summary['water_bodies_list'] or 'None'}
                """
                
                self.dlg.districtInfoText.setHtml(info_html)
            else:
                self.dlg.districtInfoText.setText("No data found for this district")
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Error loading district info: {str(e)}")

    def load_water_bodies(self):
        """Load water bodies layer"""
        try:
            layer, message = self.db_manager.load_layer_from_db(
                'water_bodies',
                layer_name='Rivers and Lakes'
            )
            
            if layer:
                QgsProject.instance().addMapLayer(layer)
                self.dlg.logTextBrowser.append("✓ Loaded: Water Bodies")
                
                # Style flood-prone rivers differently
                self.style_water_bodies(layer)
            else:
                self.dlg.logTextBrowser.append(f"✗ Failed: water_bodies - {message}")
        except Exception as e:
            self.dlg.logTextBrowser.append(f"✗ Error: {str(e)}")

    def style_water_bodies(self, layer):
        """Style water bodies based on flood prone status"""
        from qgis.core import QgsCategorizedSymbolRenderer, QgsRendererCategory
        
        categories = []
        
        # Flood prone (red)
        flood_symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        flood_symbol.setColor(QColor('#FF0000'))
        flood_symbol.setWidth(1.5)
        flood_category = QgsRendererCategory(True, flood_symbol, 'Flood Prone')
        categories.append(flood_category)
        
        # Not flood prone (blue)
        safe_symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        safe_symbol.setColor(QColor('#0000FF'))
        safe_symbol.setWidth(0.8)
        safe_category = QgsRendererCategory(False, safe_symbol, 'Safe')
        categories.append(safe_category)
        
        renderer = QgsCategorizedSymbolRenderer('flood_prone', categories)
        layer.setRenderer(renderer)
        layer.triggerRepaint()

    def load_disasters(self):
        """Load historical disaster events"""
        try:
            layer, message = self.db_manager.load_layer_from_db(
                'disaster_events',
                layer_name='Historical Disasters'
            )
            
            if layer:
                QgsProject.instance().addMapLayer(layer)
                self.dlg.logTextBrowser.append("✓ Loaded: Historical Disaster Events")
                
                # Style by severity
                self.style_disasters(layer)
            else:
                self.dlg.logTextBrowser.append(f"✗ Failed: disaster_events - {message}")
        except Exception as e:
            self.dlg.logTextBrowser.append(f"✗ Error: {str(e)}")

    def style_disasters(self, layer):
        """Style disasters by severity"""
        categories = []
        
        severities = {
            'extreme': ('#8B0000', 'Extreme'),
            'high': ('#FF0000', 'High'),
            'medium': ('#FFA500', 'Medium'),
            'low': ('#FFFF00', 'Low')
        }
        
        for severity, (color, label) in severities.items():
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(color))
            symbol.setSize(4)
            category = QgsRendererCategory(severity, symbol, label)
            categories.append(category)
        
        renderer = QgsCategorizedSymbolRenderer('severity', categories)
        layer.setRenderer(renderer)
        layer.triggerRepaint()

    def load_infrastructure(self):
        """Load infrastructure layer"""
        try:
            layer, message = self.db_manager.load_layer_from_db(
                'infrastructure',
                layer_name='Critical Infrastructure'
            )
            
            if layer:
                QgsProject.instance().addMapLayer(layer)
                self.dlg.logTextBrowser.append("✓ Loaded: Infrastructure")
            else:
                self.dlg.logTextBrowser.append(f"✗ Failed: infrastructure - {message}")
        except Exception as e:
            self.dlg.logTextBrowser.append(f"✗ Error: {str(e)}")

    def load_risk_zones(self):
        """Load risk zones layer"""
        try:
            layer, message = self.db_manager.load_layer_from_db(
                'risk_zones',
                layer_name='Flood Risk Zones'
            )
            
            if layer:
                QgsProject.instance().addMapLayer(layer)
                self.dlg.logTextBrowser.append("✓ Loaded: Risk Zones")
                
                # Style by risk level
                self.style_risk_zones(layer)
            else:
                self.dlg.logTextBrowser.append(f"✗ Failed: risk_zones - {message}")
        except Exception as e:
            self.dlg.logTextBrowser.append(f"✗ Error: {str(e)}")

    def style_risk_zones(self, layer):
        """Style risk zones by risk level"""
        categories = []
        
        risk_styles = {
            'extreme': ('#8B0000', 'Extreme Risk'),
            'high': ('#FF0000', 'High Risk'),
            'medium': ('#FFA500', 'Medium Risk'),
            'low': ('#FFFF00', 'Low Risk')
        }
        
        for risk_level, (color, label) in risk_styles.items():
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(color))
            symbol.setOpacity(0.5)
            category = QgsRendererCategory(risk_level, symbol, label)
            categories.append(category)
        
        renderer = QgsCategorizedSymbolRenderer('risk_level', categories)
        layer.setRenderer(renderer)
        layer.triggerRepaint()

    def run_flood_analysis(self):
        """Run flood risk analysis using database data"""
        try:
            self.dlg.analysisLogText.clear()
            self.dlg.analysisLogText.append("=== Starting Flood Risk Analysis ===\n")
            
            # Get flood-prone districts from database
            results = self.db_manager.get_flood_prone_districts()
            
            if not results:
                QMessageBox.information(self.dlg, "Info", "No flood risk data found")
                return
            
            self.dlg.progressBar.setMaximum(len(results))
            
            # Display results in table
            self.dlg.resultsTableWidget.setRowCount(0)
            
            total_displaced = 0
            risk_counts = {}
            
            for i, result in enumerate(results):
                self.dlg.progressBar.setValue(i + 1)
                
                row = self.dlg.resultsTableWidget.rowCount()
                self.dlg.resultsTableWidget.insertRow(row)
                
                self.dlg.resultsTableWidget.setItem(row, 0, QTableWidgetItem(result['district']))
                self.dlg.resultsTableWidget.setItem(row, 1, QTableWidgetItem(result['flood_risk_level']))
                self.dlg.resultsTableWidget.setItem(row, 2, QTableWidgetItem(str(result['total_flood_events'] or 0)))
                self.dlg.resultsTableWidget.setItem(row, 3, QTableWidgetItem(f"{result['total_people_displaced'] or 0:,}"))
                self.dlg.resultsTableWidget.setItem(row, 4, QTableWidgetItem(result['flood_prone_rivers'] or 'None'))
                
                # Color code by risk
                risk_level = result['flood_risk_level']
                if 'EXTREME' in risk_level:
                    color = QColor('#8B0000')
                elif 'HIGH' in risk_level:
                    color = QColor('#FF0000')
                elif 'MEDIUM' in risk_level:
                    color = QColor('#FFA500')
                else:
                    color = QColor('#FFFF00')
                
                for col in range(5):
                    self.dlg.resultsTableWidget.item(row, col).setBackground(color)
                
                total_displaced += (result['total_people_displaced'] or 0)
                risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
                
                self.dlg.analysisLogText.append(f"✓ Analyzed: {result['district']} - {risk_level}")
                QCoreApplication.processEvents()
            
            # Display summary
            summary = f"""
            <h3>Analysis Summary:</h3>
            <b>Districts Analyzed:</b> {len(results)}<br>
            <b>Total People Displaced (Historical):</b> {total_displaced:,}<br>
            <br>
            <b>Risk Distribution:</b><br>
            """
            
            for risk, count in sorted(risk_counts.items()):
                summary += f"&nbsp;&nbsp;• {risk}: {count} districts<br>"
            
            self.dlg.summaryText.setHtml(summary)
            
            self.dlg.analysisLogText.append("\n✓ Analysis Complete!")
            QMessageBox.information(self.dlg, "Success", f"Analyzed {len(results)} districts!")
            
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Analysis failed: {str(e)}")
            self.dlg.analysisLogText.append(f"\n✗ Error: {str(e)}")

    def generate_flood_map(self):
        """Generate flood risk map"""
        try:
            # Load districts layer
            layer, message = self.db_manager.load_layer_from_db(
                'administrative_boundaries',
                layer_name='Flood Risk Map'
            )
            
            if not layer:
                QMessageBox.warning(self.dlg, "Warning", "Could not load districts layer")
                return
            
            QgsProject.instance().addMapLayer(layer)
            self.iface.mapCanvas().setExtent(layer.extent())
            self.iface.mapCanvas().refresh()
            
            QMessageBox.information(self.dlg, "Success", "Flood risk map generated!")
            self.dlg.analysisLogText.append("✓ Flood risk map displayed")
            
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Map generation failed: {str(e)}")

    def export_results(self):
        """Export results to CSV"""
        try:
            from qgis.PyQt.QtWidgets import QFileDialog
            import csv
            
            filename, _ = QFileDialog.getSaveFileName(
                self.dlg,
                "Save Results",
                "",
                "CSV Files (*.csv)"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['District', 'Risk Level', 'Flood Events', 'People Displaced', 'Rivers'])
                    
                    for row in range(self.dlg.resultsTableWidget.rowCount()):
                        row_data = []
                        for col in range(5):
                            item = self.dlg.resultsTableWidget.item(row, col)
                            row_data.append(item.text() if item else '')
                        writer.writerow(row_data)
                
                QMessageBox.information(self.dlg, "Success", f"Results exported to:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Export failed: {str(e)}")

    def view_district_details(self):
        """View details of selected district from results table"""
        try:
            current_row = self.dlg.resultsTableWidget.currentRow()
            if current_row < 0:
                QMessageBox.warning(self.dlg, "Warning", "Please select a district from the table")
                return
            
            district_name = self.dlg.resultsTableWidget.item(current_row, 0).text()
            
            # Get historical events
            events = self.db_manager.get_historical_events_in_district(district_name)
            
            details = f"<h2>{district_name} - Historical Disasters</h2><br>"
            
            if events:
                details += "<table border='1' cellpadding='5'>"
                details += "<tr><th>Date</th><th>Type</th><th>Severity</th><th>Casualties</th><th>Displaced</th></tr>"
                
                for event in events:
                    details += f"<tr>"
                    details += f"<td>{event['event_date']}</td>"
                    details += f"<td>{event['event_type'].title()}</td>"
                    details += f"<td>{event['severity'].title()}</td>"
                    details += f"<td>{event['casualties']}</td>"
                    details += f"<td>{event['displaced_people']:,}</td>"
                    details += f"</tr>"
                
                details += "</table>"
            else:
                details += "No historical disasters recorded"
            
            msg = QMessageBox(self.dlg)
            msg.setWindowTitle(f"{district_name} Details")
            msg.setTextFormat(1)  # Rich text
            msg.setText(details)
            msg.exec_()
            
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Error: {str(e)}")

    def view_evacuation_centers(self):
        """View evacuation centers for selected district"""
        try:
            district_name = self.dlg.evacuationDistrictCombo.currentText()
            
            # Get district ID
            districts = self.db_manager.get_all_districts()
            district_id = None
            for d in districts:
                if d['boundary_name'] == district_name:
                    district_id = d['boundary_id']
                    break
            
            if not district_id:
                QMessageBox.warning(self.dlg, "Warning", "District not found")
                return
            
            centers = self.db_manager.get_evacuation_centers(district_id)
            
            self.dlg.evacuationCentersTable.setRowCount(0)
            
            for center in centers:
                row = self.dlg.evacuationCentersTable.rowCount()
                self.dlg.evacuationCentersTable.insertRow(row)
                
                self.dlg.evacuationCentersTable.setItem(row, 0, QTableWidgetItem(center['center_name']))
                self.dlg.evacuationCentersTable.setItem(row, 1, QTableWidgetItem(str(center['capacity'])))
                self.dlg.evacuationCentersTable.setItem(row, 2, QTableWidgetItem(str(center['current_occupancy'])))
                self.dlg.evacuationCentersTable.setItem(row, 3, QTableWidgetItem(center['facilities'] or 'N/A'))
            
            QMessageBox.information(self.dlg, "Success", f"Found {len(centers)} evacuation centers")
            
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Error: {str(e)}")

    def calculate_evacuation_capacity(self):
        """Calculate evacuation capacity vs population"""
        try:
            district_name = self.dlg.evacuationDistrictCombo.currentText()
            
            summary = self.db_manager.get_district_summary(district_name)
            
            # Get district ID
            districts = self.db_manager.get_all_districts()
            district_id = None
            for d in districts:
                if d['boundary_name'] == district_name:
                    district_id = d['boundary_id']
                    break
            
            centers = self.db_manager.get_evacuation_centers(district_id)
            
            total_capacity = sum(c['capacity'] for c in centers)
            population = summary['population']
            gap = population - total_capacity
            coverage = (total_capacity / population * 100) if population > 0 else 0
            
            capacity_html = f"""
            <h3>{district_name} Evacuation Capacity:</h3>
            <b>Population:</b> {population:,}<br>
            <b>Evacuation Centers:</b> {len(centers)}<br>
            <b>Total Capacity:</b> {total_capacity:,}<br>
            <b>Capacity Gap:</b> {gap:,}<br>
            <b>Coverage:</b> {coverage:.1f}%<br>
            """
            
            if gap > 0:
                capacity_html += f"<br><span style='color:red;'><b>⚠ Warning: Insufficient capacity for {gap:,} people!</b></span>"
            else:
                capacity_html += f"<br><span style='color:green;'><b>✓ Adequate capacity</b></span>"
            
            self.dlg.capacityText.setHtml(capacity_html)
            
        except Exception as e:
            QMessageBox.critical(self.dlg, "Error", f"Error: {str(e)}")

    def run(self):
        """Show the plugin dialog"""
        if not self.dlg:
            self.dlg = DisasterRiskDialog()
            self.connect_signals()
        
        self.dlg.show()
        result = self.dlg.exec_()