# -*- coding: utf-8 -*-


import unittest
import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from database_manager import DatabaseManager
from evacuation_planner import EvacuationPlanner

class TestDatabaseManager(unittest.TestCase):
    """Test database connection and query functionality"""
    
    def setUp(self):
        """Set up test database connection"""
        self.db = DatabaseManager()
        # Update these credentials for your environment
        self.host = 'localhost'
        self.port = '5433'
        self.database = 'disaster_risk_db'
        self.user = 'postgres'
        self.password = 'your_password'  # Update this
    
    def test_database_connection(self):
        """Test database connection"""
        success, message = self.db.connect(
            self.host, self.port, self.database, self.user, self.password
        )
        self.assertTrue(success, f"Database connection failed: {message}")
        print(f"✓ Database connection successful: {message}")
    
    def test_get_all_districts(self):
        """Test retrieving all districts"""
        self.db.connect(self.host, self.port, self.database, self.user, self.password)
        districts = self.db.get_all_districts()
        
        self.assertIsInstance(districts, list)
        self.assertGreater(len(districts), 0, "No districts found")
        self.assertEqual(len(districts), 28, "Should have 28 districts")
        
        # Check district structure
        first_district = districts[0]
        self.assertIn('boundary_id', first_district)
        self.assertIn('boundary_name', first_district)
        self.assertIn('population', first_district)
        
        print(f"✓ Retrieved {len(districts)} districts")
    
    def test_get_flood_prone_districts(self):
        """Test flood-prone districts query"""
        self.db.connect(self.host, self.port, self.database, self.user, self.password)
        flood_districts = self.db.get_flood_prone_districts()
        
        self.assertIsInstance(flood_districts, list)
        
        if len(flood_districts) > 0:
            first = flood_districts[0]
            self.assertIn('district', first)
            self.assertIn('flood_risk_level', first)
            self.assertIn('total_flood_events', first)
            print(f"✓ Retrieved {len(flood_districts)} flood-prone districts")
        else:
            print("⚠ No flood-prone districts found (check data)")
    
    def test_get_evacuation_centers(self):
        """Test evacuation centers query"""
        self.db.connect(self.host, self.port, self.database, self.user, self.password)
        centers = self.db.get_evacuation_centers()
        
        self.assertIsInstance(centers, list)
        
        if len(centers) > 0:
            first = centers[0]
            self.assertIn('center_name', first)
            self.assertIn('capacity', first)
            self.assertIn('district', first)
            print(f"✓ Retrieved {len(centers)} evacuation centers")
        else:
            print("⚠ No evacuation centers found (check data)")
    
    def test_get_district_summary(self):
        """Test district summary query"""
        self.db.connect(self.host, self.port, self.database, self.user, self.password)
        
        # Test with a known district
        summary = self.db.get_district_summary('Zomba')
        
        if summary:
            self.assertIn('district', summary)
            self.assertIn('population', summary)
            self.assertIn('area_sqkm', summary)
            print(f"✓ Retrieved summary for Zomba district")
        else:
            print("⚠ No summary found for Zomba (check data)")


class TestEvacuationPlanner(unittest.TestCase):
    """Test evacuation planning functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.db = DatabaseManager()
        # Update these credentials
        self.host = 'localhost'
        self.port = '5433'
        self.database = 'disaster_risk_db'
        self.user = 'postgres'
        self.password = 'your_password'  # Update this
        
        # Connect to database
        success, _ = self.db.connect(
            self.host, self.port, self.database, self.user, self.password
        )
        
        if success:
            self.planner = EvacuationPlanner(self.db)
        else:
            self.skipTest("Database connection failed")
    
    def test_identify_safe_zones(self):
        """Test safe zone identification"""
        # Get first district ID
        districts = self.db.get_all_districts()
        if not districts:
            self.skipTest("No districts available")
        
        district_id = districts[0]['boundary_id']
        safe_zones = self.planner.identify_safe_zones(district_id)
        
        self.assertIsInstance(safe_zones, list)
        print(f"✓ Identified {len(safe_zones)} safe zones for district {district_id}")
    
    def test_calculate_capacity_gap(self):
        """Test capacity gap calculation"""
        districts = self.db.get_all_districts()
        if not districts:
            self.skipTest("No districts available")
        
        district_id = districts[0]['boundary_id']
        capacity = self.planner.calculate_evacuation_capacity_gap(district_id)
        
        if capacity:
            self.assertIn('population', capacity)
            self.assertIn('total_capacity', capacity)
            self.assertIn('capacity_gap', capacity)
            self.assertIn('coverage_percent', capacity)
            
            print(f"✓ Capacity analysis for district {district_id}:")
            print(f"  Population: {capacity['population']:,}")
            print(f"  Capacity: {capacity['total_capacity']:,}")
            print(f"  Gap: {capacity['capacity_gap']:,}")
            print(f"  Coverage: {capacity['coverage_percent']}%")
        else:
            print(f"⚠ No capacity data for district {district_id}")
    
    def test_calculate_evacuation_routes(self):
        """Test evacuation route calculation"""
        districts = self.db.get_all_districts()
        if not districts:
            self.skipTest("No districts available")
        
        district_id = districts[0]['boundary_id']
        routes = self.planner.calculate_evacuation_routes(district_id)
        
        self.assertIsInstance(routes, list)
        
        if len(routes) > 0:
            first_route = routes[0]
            self.assertIn('from_zone', first_route)
            self.assertIn('to_center', first_route)
            self.assertIn('distance_km', first_route)
            self.assertIn('estimated_time_minutes', first_route)
            
            print(f"✓ Calculated {len(routes)} evacuation routes")
            print(f"  Example: {first_route['from_zone']} → {first_route['to_center']}")
            print(f"  Distance: {first_route['distance_km']} km")
            print(f"  Time: {first_route['estimated_time_minutes']} minutes")
        else:
            print(f"⚠ No routes calculated for district {district_id}")
    
    def test_generate_evacuation_plan(self):
        """Test full evacuation plan generation"""
        districts = self.db.get_all_districts()
        if not districts:
            self.skipTest("No districts available")
        
        district_id = districts[0]['boundary_id']
        plan = self.planner.generate_evacuation_plan(district_id)
        
        if plan:
            self.assertIn('district', plan)
            self.assertIn('capacity_analysis', plan)
            self.assertIn('evacuation_routes', plan)
            self.assertIn('safe_zones', plan)
            self.assertIn('recommendations', plan)
            self.assertIn('plan_status', plan)
            
            print(f"✓ Generated evacuation plan for {plan['district']}")
            print(f"  Status: {plan['plan_status']}")
            print(f"  Routes: {len(plan['evacuation_routes'])}")
            print(f"  Safe Zones: {len(plan['safe_zones'])}")
            print(f"  Recommendations: {len(plan['recommendations'])}")
        else:
            print(f"⚠ Could not generate plan for district {district_id}")
    
    def test_export_evacuation_plan(self):
        """Test evacuation plan export"""
        districts = self.db.get_all_districts()
        if not districts:
            self.skipTest("No districts available")
        
        district_id = districts[0]['boundary_id']
        plan = self.planner.generate_evacuation_plan(district_id)
        
        if plan:
            output_path = 'test_evacuation_plan.txt'
            success, message = self.planner.export_evacuation_plan_report(plan, output_path)
            
            self.assertTrue(success, f"Export failed: {message}")
            self.assertTrue(os.path.exists(output_path), "Output file not created")
            
            # Check file content
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('EVACUATION PLAN REPORT', content)
                self.assertIn(plan['district'], content)
            
            print(f"✓ Exported evacuation plan to {output_path}")
            
            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)
        else:
            self.skipTest("Could not generate plan for export test")


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up test environment"""
        self.db = DatabaseManager()
        self.host = 'localhost'
        self.port = '5433'
        self.database = 'disaster_risk_db'
        self.user = 'postgres'
        self.password = 'your_password'  # Update this
    
    def test_complete_evacuation_workflow(self):
        """Test complete evacuation planning workflow"""
        print("\n" + "="*60)
        print("INTEGRATION TEST: Complete Evacuation Workflow")
        print("="*60)
        
        # Step 1: Connect to database
        print("\n1. Connecting to database...")
        success, message = self.db.connect(
            self.host, self.port, self.database, self.user, self.password
        )
        self.assertTrue(success, f"Connection failed: {message}")
        print(f"   ✓ {message}")
        
        # Step 2: Get districts
        print("\n2. Retrieving districts...")
        districts = self.db.get_all_districts()
        self.assertGreater(len(districts), 0, "No districts found")
        print(f"   ✓ Found {len(districts)} districts")
        
        # Step 3: Initialize evacuation planner
        print("\n3. Initializing evacuation planner...")
        planner = EvacuationPlanner(self.db)
        print("   ✓ Planner initialized")
        
        # Step 4: Select a district for testing
        test_district = districts[0]
        district_id = test_district['boundary_id']
        district_name = test_district['boundary_name']
        print(f"\n4. Testing with district: {district_name} (ID: {district_id})")
        
        # Step 5: Calculate capacity gap
        print("\n5. Calculating capacity gap...")
        capacity = planner.calculate_evacuation_capacity_gap(district_id)
        if capacity:
            print(f"   ✓ Population: {capacity['population']:,}")
            print(f"   ✓ Capacity: {capacity['total_capacity']:,}")
            print(f"   ✓ Gap: {capacity['capacity_gap']:,}")
        else:
            print("   ⚠ No capacity data available")
        
        # Step 6: Identify safe zones
        print("\n6. Identifying safe zones...")
        safe_zones = planner.identify_safe_zones(district_id)
        print(f"   ✓ Found {len(safe_zones)} safe zones")
        
        # Step 7: Calculate evacuation routes
        print("\n7. Calculating evacuation routes...")
        routes = planner.calculate_evacuation_routes(district_id)
        print(f"   ✓ Calculated {len(routes)} routes")
        
        # Step 8: Generate full evacuation plan
        print("\n8. Generating complete evacuation plan...")
        plan = planner.generate_evacuation_plan(district_id)
        if plan:
            print(f"   ✓ Plan generated for {plan['district']}")
            print(f"   ✓ Status: {plan['plan_status']}")
            print(f"   ✓ Recommendations: {len(plan['recommendations'])}")
        else:
            print("   ⚠ Could not generate plan")
        
        # Step 9: Export plan
        print("\n9. Exporting evacuation plan...")
        if plan:
            output_path = f'test_plan_{district_name}.txt'
            success, message = planner.export_evacuation_plan_report(plan, output_path)
            self.assertTrue(success, f"Export failed: {message}")
            print(f"   ✓ Plan exported to {output_path}")
            
            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)
                print(f"   ✓ Cleaned up test file")
        
        print("\n" + "="*60)
        print("INTEGRATION TEST COMPLETE")
        print("="*60 + "\n")


def run_tests():
    """Run all tests with detailed output"""
    print("\n" + "="*70)
    print("MALAWI DISASTER RISK ASSESSMENT SYSTEM - TEST SUITE")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseManager))
    suite.addTests(loader.loadTestsFromTestCase(TestEvacuationPlanner))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result


if __name__ == '__main__':
    # Update database credentials before running
    print("\n⚠ IMPORTANT: Update database credentials in the test file before running!")
    print("   Edit test_plugin.py and update the password variable.\n")
    
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
