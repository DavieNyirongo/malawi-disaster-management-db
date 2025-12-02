# -*- coding: utf-8 -*-
"""
Dialog class for Disaster Risk Assessment Plugin
"""

from qgis.PyQt import QtWidgets, QtCore
from qgis.gui import QgsMapLayerComboBox
from qgis.core import QgsMapLayerProxyModel

class DisasterRiskDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DisasterRiskDialog, self).__init__(parent)
        self.setupUi()
    
    def setupUi(self):
        """Setup the user interface"""
        self.setWindowTitle("Malawi Disaster Risk Assessment System")
        self.resize(900, 700)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.tabWidget = QtWidgets.QTabWidget()
        
        self.tab_connection = self.create_connection_tab()
        self.tab_districts = self.create_districts_tab()
        self.tab_analysis = self.create_analysis_tab()
        self.tab_results = self.create_results_tab()
        self.tab_evacuation = self.create_evacuation_tab()
        
        self.tabWidget.addTab(self.tab_connection, "Database Connection")
        self.tabWidget.addTab(self.tab_districts, "Districts & Data")
        self.tabWidget.addTab(self.tab_analysis, "Flood Risk Analysis")
        self.tabWidget.addTab(self.tab_results, "Results & Maps")
        self.tabWidget.addTab(self.tab_evacuation, "Evacuation Planning")
        
        layout.addWidget(self.tabWidget)
        
        button_layout = QtWidgets.QHBoxLayout()
        self.closeButton = QtWidgets.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(self.closeButton)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def create_connection_tab(self):
        """Create database connection tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        
        self.hostLineEdit = QtWidgets.QLineEdit("localhost")
        self.portLineEdit = QtWidgets.QLineEdit("5433")
        self.databaseLineEdit = QtWidgets.QLineEdit("disaster_risk_db")
        self.userLineEdit = QtWidgets.QLineEdit("postgres")
        self.passwordLineEdit = QtWidgets.QLineEdit()
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        layout.addRow("Host:", self.hostLineEdit)
        layout.addRow("Port:", self.portLineEdit)
        layout.addRow("Database:", self.databaseLineEdit)
        layout.addRow("Username:", self.userLineEdit)
        layout.addRow("Password:", self.passwordLineEdit)
        
        self.connectButton = QtWidgets.QPushButton("Connect to Database")
        self.connectButton.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        layout.addRow(self.connectButton)
        
        self.statusLabel = QtWidgets.QLabel("Status: Not Connected")
        self.statusLabel.setStyleSheet("color: gray; font-weight: bold;")
        layout.addRow(self.statusLabel)
        
        self.logTextBrowser = QtWidgets.QTextBrowser()
        self.logTextBrowser.setMaximumHeight(200)
        layout.addRow("Log:", self.logTextBrowser)
        
        tab.setLayout(layout)
        return tab
    
    def create_districts_tab(self):
        """Create districts exploration tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        layout.addWidget(QtWidgets.QLabel("<b>Explore Malawi Districts:</b>"))
        
        form_layout = QtWidgets.QFormLayout()
        
        self.districtComboBox = QtWidgets.QComboBox()
        form_layout.addRow("Select District:", self.districtComboBox)
        
        self.loadDistrictsButton = QtWidgets.QPushButton("Load All Districts")
        self.viewDistrictInfoButton = QtWidgets.QPushButton("View District Details")
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.loadDistrictsButton)
        button_layout.addWidget(self.viewDistrictInfoButton)
        form_layout.addRow("Actions:", button_layout)
        
        layout.addLayout(form_layout)
        
        layout.addWidget(QtWidgets.QLabel("<b>District Information:</b>"))
        self.districtInfoText = QtWidgets.QTextBrowser()
        layout.addWidget(self.districtInfoText)
        
        layout.addWidget(QtWidgets.QLabel("<b>Quick Actions:</b>"))
        quick_layout = QtWidgets.QGridLayout()
        
        self.loadWaterBodiesButton = QtWidgets.QPushButton("Load Water Bodies")
        self.loadDisastersButton = QtWidgets.QPushButton("Load Historical Disasters")
        self.loadInfrastructureButton = QtWidgets.QPushButton("Load Infrastructure")
        self.loadRiskZonesButton = QtWidgets.QPushButton("Load Risk Zones")
        
        quick_layout.addWidget(self.loadWaterBodiesButton, 0, 0)
        quick_layout.addWidget(self.loadDisastersButton, 0, 1)
        quick_layout.addWidget(self.loadInfrastructureButton, 1, 0)
        quick_layout.addWidget(self.loadRiskZonesButton, 1, 1)
        
        layout.addLayout(quick_layout)
        
        tab.setLayout(layout)
        return tab
    
    def create_analysis_tab(self):
        """Create flood risk analysis tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        layout.addWidget(QtWidgets.QLabel("<b>Flood Risk Analysis:</b>"))
        
        form_layout = QtWidgets.QFormLayout()
        
        self.analysisDistrictCombo = QtWidgets.QComboBox()
        self.analysisDistrictCombo.addItem("All Districts")
        form_layout.addRow("Analyze:", self.analysisDistrictCombo)
        
        self.includeHistoricalCheck = QtWidgets.QCheckBox("Include Historical Disasters")
        self.includeHistoricalCheck.setChecked(True)
        
        self.includeWaterProximityCheck = QtWidgets.QCheckBox("Include Water Proximity")
        self.includeWaterProximityCheck.setChecked(True)
        
        self.includePopulationCheck = QtWidgets.QCheckBox("Include Population Risk")
        self.includePopulationCheck.setChecked(True)
        
        form_layout.addRow(self.includeHistoricalCheck)
        form_layout.addRow(self.includeWaterProximityCheck)
        form_layout.addRow(self.includePopulationCheck)
        
        layout.addLayout(form_layout)
        
        self.runFloodAnalysisButton = QtWidgets.QPushButton("Run Flood Risk Analysis")
        self.runFloodAnalysisButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 15px; font-size: 14px;")
        layout.addWidget(self.runFloodAnalysisButton)
        
        self.progressBar = QtWidgets.QProgressBar()
        layout.addWidget(self.progressBar)
        
        layout.addWidget(QtWidgets.QLabel("<b>Analysis Log:</b>"))
        self.analysisLogText = QtWidgets.QTextBrowser()
        layout.addWidget(self.analysisLogText)
        
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def create_results_tab(self):
        """Create results display tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        layout.addWidget(QtWidgets.QLabel("<b>Flood Risk Analysis Results:</b>"))
        
        self.resultsTableWidget = QtWidgets.QTableWidget()
        self.resultsTableWidget.setColumnCount(5)
        self.resultsTableWidget.setHorizontalHeaderLabels([
            "District", "Risk Level", "Flood Events", "Population Displaced", "Rivers"
        ])
        self.resultsTableWidget.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.resultsTableWidget)
        
        button_layout = QtWidgets.QHBoxLayout()
        self.generateFloodMapButton = QtWidgets.QPushButton("Generate Flood Risk Map")
        self.exportResultsButton = QtWidgets.QPushButton("Export to CSV")
        self.viewDetailsButton = QtWidgets.QPushButton("View Selected District")
        
        button_layout.addWidget(self.generateFloodMapButton)
        button_layout.addWidget(self.exportResultsButton)
        button_layout.addWidget(self.viewDetailsButton)
        layout.addLayout(button_layout)
        
        layout.addWidget(QtWidgets.QLabel("<b>Summary Statistics:</b>"))
        self.summaryText = QtWidgets.QTextBrowser()
        self.summaryText.setMaximumHeight(150)
        layout.addWidget(self.summaryText)
        
        tab.setLayout(layout)
        return tab
    
    def create_evacuation_tab(self):
        """Create evacuation planning tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        
        layout.addWidget(QtWidgets.QLabel("<b>Evacuation Planning:</b>"))
        
        form_layout = QtWidgets.QFormLayout()
        self.evacuationDistrictCombo = QtWidgets.QComboBox()
        form_layout.addRow("District:", self.evacuationDistrictCombo)
        layout.addLayout(form_layout)
        
        button_layout = QtWidgets.QGridLayout()
        self.viewEvacuationCentersButton = QtWidgets.QPushButton("View Evacuation Centers")
        self.identifySafeZonesButton = QtWidgets.QPushButton("Identify Safe Zones")
        self.calculateCapacityButton = QtWidgets.QPushButton("Calculate Capacity Gap")
        self.planRoutesButton = QtWidgets.QPushButton("Plan Evacuation Routes")
        
        button_layout.addWidget(self.viewEvacuationCentersButton, 0, 0)
        button_layout.addWidget(self.identifySafeZonesButton, 0, 1)
        button_layout.addWidget(self.calculateCapacityButton, 1, 0)
        button_layout.addWidget(self.planRoutesButton, 1, 1)
        
        layout.addLayout(button_layout)
        
        layout.addWidget(QtWidgets.QLabel("<b>Evacuation Centers:</b>"))
        self.evacuationCentersTable = QtWidgets.QTableWidget()
        self.evacuationCentersTable.setColumnCount(4)
        self.evacuationCentersTable.setHorizontalHeaderLabels([
            "Center Name", "Capacity", "Occupancy", "Facilities"
        ])
        layout.addWidget(self.evacuationCentersTable)
        
        layout.addWidget(QtWidgets.QLabel("<b>Capacity Analysis:</b>"))
        self.capacityText = QtWidgets.QTextBrowser()
        self.capacityText.setMaximumHeight(100)
        layout.addWidget(self.capacityText)
        
        tab.setLayout(layout)
        return tab