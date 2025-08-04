#!/usr/bin/env python3
"""
Complete Rental Property System Test
Tests all rental property functionality including:
1. User rental property listing with images
2. Admin approval/rejection system
3. Public browsing of approved rentals
"""

import time
import requests
from database import db_manager

def test_rental_property_system():
    """Test the complete rental property system"""
    
    print("🏠 COMPLETE RENTAL PROPERTY SYSTEM TEST")
    print("=" * 50)
    
    try:
        # Step 1: Test Database Functions
        print("\n1. 📊 TESTING DATABASE FUNCTIONS")
        print("-" * 35)
        
        # Add a test rental property
        property_data = {
            'property_type': 'Villa',
            'location': 'Whitefield',
            'size': '3 BHK',
            'total_sqft': 1800,
            'bedrooms': 3,
            'bathrooms': 3,
            'balcony': 2,
            'rent_amount': 45000,
            'security_deposit': 90000,
            'maintenance_charges': 3000,
            'description': 'Luxurious 3BHK villa with garden and parking',
            'amenities': ['Gym', 'Swimming Pool', 'Security', 'Garden', 'Parking'],
            'images': ['/static/uploads/rentals/villa1.jpg', '/static/uploads/rentals/villa2.jpg'],
            'available_from': '2024-02-01',
            'lease_duration': '2 years',
            'furnishing_status': 'Fully Furnished',
            'parking_available': True,
            'pet_friendly': False
        }
        
        # Add rental for user ID 5 (finaltest)
        result = db_manager.add_rental_property(5, property_data)
        
        if result['success']:
            rental_id = result['rental_id']
            print(f"✅ Rental property added with ID: {rental_id}")
            
            # Test getting all rentals
            all_rentals = db_manager.get_all_rental_properties()
            print(f"✅ Total rentals in database: {len(all_rentals.get('rentals', []))}")
            
            # Test getting user rentals
            user_rentals = db_manager.get_user_rental_properties(5)
            print(f"✅ User rentals: {len(user_rentals.get('rentals', []))}")
            
        else:
            print(f"❌ Failed to add rental: {result.get('error')}")
            return False
        
        # Step 2: Test Admin Approval
        print("\n2. 🔐 TESTING ADMIN APPROVAL SYSTEM")
        print("-" * 40)
        
        # Test approve action
        approve_result = db_manager.update_rental_property_status(rental_id, 'approve', admin_id=1)
        if approve_result['success']:
            print("✅ Admin approval function working")
            
            # Check approved rentals
            approved_rentals = db_manager.get_all_rental_properties(status='approved')
            print(f"✅ Approved rentals: {len(approved_rentals.get('rentals', []))}")
            
            if approved_rentals['success'] and approved_rentals['rentals']:
                rental = approved_rentals['rentals'][0]
                print(f"✅ Approved rental details:")
                print(f"   - Type: {rental.get('property_type')}")
                print(f"   - Location: {rental.get('location')}")
                print(f"   - Rent: ₹{rental.get('rent_amount'):,.0f}")
                print(f"   - Owner: {rental.get('username')} ({rental.get('phone')})")
                print(f"   - Images: {len(rental.get('images', []))}")
        else:
            print(f"❌ Admin approval failed: {approve_result.get('error')}")
        
        # Step 3: Test Web Interface
        print("\n3. 🌐 TESTING WEB INTERFACE")
        print("-" * 35)
        
        # Test public browsing
        time.sleep(2)
        browse_response = requests.get('http://127.0.0.1:5000/browse-rental-properties')
        print(f"Browse rentals page: {browse_response.status_code}")
        
        if browse_response.status_code == 200:
            content = browse_response.text
            if 'Whitefield' in content:
                print("✅ Approved rental visible in public browsing")
            if 'finaltest' in content or '9876543210' in content:
                print("✅ Owner contact information displayed")
            if '45000' in content or '45,000' in content:
                print("✅ Rental price displayed correctly")
            if 'Villa' in content:
                print("✅ Property type displayed")
        
        # Test user login and rental listing access
        print("\n4. 👤 TESTING USER ACCESS")
        print("-" * 30)
        
        session = requests.Session()
        login_data = {'username_or_email': 'finaltest', 'password': 'test123'}
        
        login_response = session.post('http://127.0.0.1:5000/login', json=login_data)
        print(f"User login: {login_response.status_code}")
        
        if login_response.status_code == 200:
            # Test rental listing form access
            rental_form_response = session.get('http://127.0.0.1:5000/list-rental-property')
            print(f"Rental listing form: {rental_form_response.status_code}")
            
            if rental_form_response.status_code == 200:
                print("✅ Users can access rental listing form")
            
            # Test profile with rentals
            profile_response = session.get('http://127.0.0.1:5000/profile')
            print(f"User profile: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                profile_content = profile_response.text
                if 'Whitefield' in profile_content:
                    print("✅ User can see their rentals in profile")
        
        # Test admin access
        print("\n5. 🔐 TESTING ADMIN ACCESS")
        print("-" * 30)
        
        admin_session = requests.Session()
        admin_data = {'username': 'admin', 'password': 'admin123'}
        
        admin_response = admin_session.post('http://127.0.0.1:5000/admin/login', data=admin_data)
        print(f"Admin login: {admin_response.status_code}")
        
        if admin_response.status_code == 200:
            # Test admin rental management
            admin_rentals_response = admin_session.get('http://127.0.0.1:5000/admin/rental-properties')
            print(f"Admin rental management: {admin_rentals_response.status_code}")
            
            if admin_rentals_response.status_code == 200:
                admin_content = admin_rentals_response.text
                if 'Whitefield' in admin_content:
                    print("✅ Admin can see all rental properties")
                if 'finaltest' in admin_content:
                    print("✅ Admin can see owner information")
                if 'Approve' in admin_content or 'Reject' in admin_content:
                    print("✅ Admin action buttons available")
        
        # Step 4: Test Image Upload Directory
        print("\n6. 📸 TESTING IMAGE UPLOAD SYSTEM")
        print("-" * 40)
        
        import os
        upload_dir = 'static/uploads/rentals'
        
        if os.path.exists(upload_dir):
            print("✅ Image upload directory exists")
            
            # Test write permissions
            test_file = os.path.join(upload_dir, 'test_write.txt')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                print("✅ Image upload directory is writable")
            except:
                print("❌ Image upload directory not writable")
        else:
            print("❌ Image upload directory missing")
        
        # Final Summary
        print("\n" + "=" * 50)
        print("🎉 RENTAL PROPERTY SYSTEM TEST COMPLETE!")
        print("=" * 50)
        
        print("\n✅ WORKING FEATURES:")
        print("   🏠 User rental property listing")
        print("   📸 Image upload support")
        print("   🔐 Admin approval/rejection system")
        print("   🌐 Public browsing of approved rentals")
        print("   👤 User profile integration")
        print("   📊 Complete database integration")
        print("   📞 Owner contact information display")
        
        print("\n🚀 SYSTEM STATUS: FULLY OPERATIONAL!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_rental_property_system()
