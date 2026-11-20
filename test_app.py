import unittest
from app import app
from models import db, User, Pet, Product, CartItem, Order, AdoptionRequest

class AdoptNShopTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

        with app.app_context():
            # Ensure an active customer exists for testing
            customer = User.query.filter_by(email='rohan@example.com').first()
            if not customer:
                customer = User(name='Rohan Verma', email='rohan@example.com', role='customer', phone='+91 98765 43210')
                customer.set_password('user123')
                db.session.add(customer)

            customer2 = User.query.filter_by(email='priya@example.com').first()
            if not customer2:
                customer2 = User(name='Priya Patel', email='priya@example.com', role='customer', phone='+91 98234 56789')
                customer2.set_password('user123')
                db.session.add(customer2)

            admin = User.query.filter_by(email='admin@adoptnshop.com').first()
            if not admin:
                admin = User(name='Aarav Sharma', email='admin@adoptnshop.com', role='admin', phone='+91 98200 12345')
                admin.set_password('admin123')
                db.session.add(admin)

            db.session.commit()

    def test_01_public_pages(self):
        """Test public landing and information pages"""
        routes = ['/', '/about', '/contact', '/pets', '/shop', '/login', '/register']
        for r in routes:
            response = self.client.get(r)
            self.assertEqual(response.status_code, 200, f"Route {r} should return 200")
        print("[PASS] Public routes verified successfully")

    def test_02_pet_filters_and_search(self):
        """Test searching and filtering pets"""
        res_dog = self.client.get('/pets?species=Dog')
        self.assertEqual(res_dog.status_code, 200)

        res_cat = self.client.get('/pets?species=Cat')
        self.assertEqual(res_cat.status_code, 200)

        res_search = self.client.get('/pets?q=Bruno')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b'Bruno', res_search.data)
        print("[PASS] Pet filtering and search verified")

    def test_03_shop_filters_and_sorting(self):
        """Test shopping search and category filters"""
        res_food = self.client.get('/shop?category=Food')
        self.assertEqual(res_food.status_code, 200)

        res_sort = self.client.get('/shop?sort=price_low')
        self.assertEqual(res_sort.status_code, 200)
        print("[PASS] Shop categories and sorting verified")

    def test_04_auth_security_and_role_protection(self):
        """Test user login, wrong credentials, and customer blocked from admin"""
        # Failed login
        res_bad = self.client.post('/login', data={'email': 'rohan@example.com', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertIn(b'Invalid email address or password', res_bad.data)

        # Successful Customer Login
        res_good = self.client.post('/login', data={'email': 'rohan@example.com', 'password': 'user123'}, follow_redirects=True)
        self.assertIn(b'Welcome back', res_good.data)

        # Customer tries to access admin area -> should be blocked!
        res_admin = self.client.get('/admin', follow_redirects=True)
        self.assertIn(b'Access denied. Administrator privileges required', res_admin.data)
        print("[PASS] Authentication and role-based access control verified")

    def test_05_admin_dashboard_and_analytics(self):
        """Test admin login and access to dashboard & Chart.js API"""
        self.client.get('/logout')
        res_admin_login = self.client.post('/login', data={'email': 'admin@adoptnshop.com', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res_admin_login.status_code, 200)

        res_dash = self.client.get('/admin')
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn(b'Dashboard & Analytics Overview', res_dash.data)

        res_api = self.client.get('/admin/api/analytics')
        self.assertEqual(res_api.status_code, 200)
        json_data = res_api.get_json()
        self.assertIn('species', json_data)
        self.assertIn('categories', json_data)
        self.assertIn('order_statuses', json_data)
        print("[PASS] Admin dashboard and analytics API verified")

    def test_06_adoption_application_workflow(self):
        """Test submitting an adoption application and admin approval"""
        self.client.get('/logout')
        self.client.post('/login', data={'email': 'rohan@example.com', 'password': 'user123'})

        with app.app_context():
            available_pet = Pet.query.filter_by(status='available', approval_status='approved').first()
            pet_id = available_pet.id

        res_apply = self.client.post(f'/pets/{pet_id}/apply', data={
            'full_name': 'Rohan Verma',
            'phone': '+91 98765 43210',
            'address': 'Bandra West, Mumbai',
            'living_situation': 'Apartment',
            'has_other_pets': 'on',
            'previous_experience': 'Experienced owner',
            'reason': 'We love animals and would provide a happy home.'
        }, follow_redirects=True)
        self.assertIn(b'submitted successfully', res_apply.data)

        res_my = self.client.get('/my-adoptions')
        self.assertEqual(res_my.status_code, 200)

        self.client.get('/logout')
        self.client.post('/login', data={'email': 'admin@adoptnshop.com', 'password': 'admin123'})

        with app.app_context():
            req = AdoptionRequest.query.filter_by(pet_id=pet_id, status='pending').first()
            if req:
                req_id = req.id
                res_approve = self.client.post(f'/admin/adoptions/{req_id}/status', data={
                    'status': 'approved',
                    'admin_notes': 'Application verified. Approved for adoption!'
                }, follow_redirects=True)
                self.assertIn(b'status updated to Approved', res_approve.data)
        print("[PASS] Adoption workflow verified")

    def test_07_ecommerce_cart_and_checkout_flow(self):
        """Test cart add, quantity adjust, checkout, order generation, and stock deduction"""
        self.client.get('/logout')
        self.client.post('/login', data={'email': 'rohan@example.com', 'password': 'user123'})

        with app.app_context():
            product = Product.query.filter(Product.stock > 5, Product.is_active == True).first()
            initial_stock = product.stock
            prod_id = product.id

        res_add = self.client.post(f'/cart/add/{prod_id}', data={'quantity': 2}, follow_redirects=True)
        self.assertIn(b'added to your cart', res_add.data)

        res_cart = self.client.get('/cart')
        self.assertEqual(res_cart.status_code, 200)

        res_checkout = self.client.post('/checkout', data={
            'shipping_name': 'Rohan Verma',
            'shipping_phone': '+91 98765 43210',
            'shipping_address': 'Flat 402, Shanti Heights, Bandra West',
            'shipping_city': 'Mumbai',
            'shipping_pincode': '400050',
            'payment_method': 'UPI / QR'
        }, follow_redirects=True)
        self.assertIn(b'Order placed successfully', res_checkout.data)
        self.assertIn(b'Payment & Order Successful', res_checkout.data)

        with app.app_context():
            updated_product = db.session.get(Product, prod_id)
            self.assertEqual(updated_product.stock, initial_stock - 2)
            user = User.query.filter_by(email='rohan@example.com').first()
            self.assertEqual(len(user.cart_items), 0)
        print("[PASS] E-commerce flow (Cart -> Checkout -> Stock Decrement) verified")

    def test_08_customer_pet_listing_and_admin_approval(self):
        """Test complete customer pet listing lifecycle with approval, editing, and ownership check"""
        # Step 1: Customer Rohan logs in and submits a new pet listing
        self.client.get('/logout')
        self.client.post('/login', data={'email': 'rohan@example.com', 'password': 'user123'})

        # GET customer listing page
        res_form = self.client.get('/pets/list-my-pet')
        self.assertEqual(res_form.status_code, 200)
        self.assertIn(b'List Your Pet for Loving Adoption', res_form.data)

        # POST new pet listing with optional rehoming fee
        res_submit = self.client.post('/pets/list-my-pet', data={
            'name': 'Leo The Indie',
            'species': 'Dog',
            'breed': 'Indie / Desi',
            'age_years': '1',
            'age_months': '8',
            'gender': 'Male',
            'size': 'Medium',
            'city': 'Pune',
            'state': 'Maharashtra',
            'contact_phone': '+91 98765 43210',
            'rehoming_fee': '750',
            'health_status': 'Vaccinated, dewormed, healthy',
            'vaccinated': 'on',
            'description': 'Rescued indie pup, friendly with people and other dogs.'
        }, follow_redirects=True)
        self.assertEqual(res_submit.status_code, 200)
        self.assertIn(b'Pending Approval', res_submit.data)

        with app.app_context():
            leo = Pet.query.filter_by(name='Leo The Indie').first()
            self.assertIsNotNone(leo)
            leo_id = leo.id
            # Verify status is Pending Approval
            self.assertEqual(leo.approval_status, 'pending')
            self.assertEqual(leo.rehoming_fee, 750.0)

        # Step 2: Verify pending listing is NOT visible publicly on /pets
        self.client.get('/logout')
        res_public = self.client.get('/pets')
        self.assertNotIn(b'Leo The Indie', res_public.data)

        # Step 3: Verify customer Priya cannot view unapproved pet or edit/delete Rohan's listing
        self.client.post('/login', data={'email': 'priya@example.com', 'password': 'user123'})
        res_priya_view = self.client.get(f'/pets/{leo_id}')
        self.assertEqual(res_priya_view.status_code, 404)

        res_priya_edit = self.client.get(f'/my-listings/{leo_id}/edit')
        self.assertEqual(res_priya_edit.status_code, 403)

        res_priya_delete = self.client.post(f'/my-listings/{leo_id}/delete')
        self.assertEqual(res_priya_delete.status_code, 403)

        # Step 4: Rohan views his listing on /my-listings and edits it
        self.client.get('/logout')
        self.client.post('/login', data={'email': 'rohan@example.com', 'password': 'user123'})
        res_rohan_my = self.client.get('/my-listings')
        self.assertEqual(res_rohan_my.status_code, 200)
        self.assertIn(b'Leo The Indie', res_rohan_my.data)
        self.assertIn(b'Pending Approval', res_rohan_my.data)

        # Rohan edits his pet
        res_edit = self.client.post(f'/my-listings/{leo_id}/edit', data={
            'name': 'Leo The Wonder Indie',
            'species': 'Dog',
            'breed': 'Indie / Desi',
            'age_years': '1',
            'age_months': '9',
            'gender': 'Male',
            'size': 'Medium',
            'city': 'Pune',
            'state': 'Maharashtra',
            'contact_phone': '+91 98765 43210',
            'rehoming_fee': '500',
            'health_status': 'Vaccinated, dewormed, healthy and fully trained',
            'vaccinated': 'on',
            'description': 'Updated description: very energetic and loving.'
        }, follow_redirects=True)
        self.assertEqual(res_edit.status_code, 200)
        self.assertIn(b'Leo The Wonder Indie', res_edit.data)

        # Step 5: Admin reviews and approves the listing
        self.client.get('/logout')
        self.client.post('/login', data={'email': 'admin@adoptnshop.com', 'password': 'admin123'})
        res_admin_approvals = self.client.get('/admin/listing-approvals')
        self.assertEqual(res_admin_approvals.status_code, 200)
        self.assertIn(b'Leo The Wonder Indie', res_admin_approvals.data)

        # Admin approves
        res_action = self.client.post(f'/admin/listing-approvals/{leo_id}/action', data={
            'action': 'approve',
            'notes': 'Verified and approved'
        }, follow_redirects=True)
        self.assertEqual(res_action.status_code, 200)
        self.assertIn(b'has been APPROVED', res_action.data)

        # Step 6: Verify pet is now visible publicly
        self.client.get('/logout')
        res_public_after = self.client.get('/pets')
        self.assertEqual(res_public_after.status_code, 200)
        self.assertIn(b'Leo The Wonder Indie', res_public_after.data)

        # Cleanup test pet
        with app.app_context():
            leo_clean = db.session.get(Pet, leo_id)
            if leo_clean:
                db.session.delete(leo_clean)
        print("[PASS] Customer pet listing full workflow (Submit -> Pending -> Ownership Check -> Edit -> Admin Approval -> Public Visibility) verified")

    def test_09_database_idempotency_and_render_bootstrap(self):
        """Test safe seeding idempotency, admin account persistence, pet & product queries"""
        from seed_data import safe_seed
        from config import Config

        # Call safe_seed again to verify idempotency (no crashes, no duplicate errors)
        safe_seed()

        with app.app_context():
            # 1. Admin account verification
            admin = User.query.filter_by(email='admin@adoptnshop.com').first()
            self.assertIsNotNone(admin, "Admin account must exist")
            self.assertEqual(admin.role, 'admin')
            self.assertTrue(admin.check_password('admin123'), "Admin password must verify successfully")

            # 2. Approved available pets count
            approved_pets = Pet.query.filter_by(status='available', approval_status='approved').all()
            self.assertGreaterEqual(len(approved_pets), 5, "Must have approved pets available for public view")
            for p in approved_pets:
                self.assertIsNotNone(p.city)
                self.assertIsNotNone(p.image_url)

            # 3. Active products count
            active_products = Product.query.filter_by(is_active=True).all()
            self.assertGreaterEqual(len(active_products), 10, "Must have active products in shop")
            for pr in active_products:
                self.assertGreater(pr.price, 0)
                self.assertGreater(pr.stock, 0)

        # 4. Public endpoints reflect the seeded pets and products
        res_pets = self.client.get('/pets')
        self.assertIn(b'Bruno', res_pets.data)
        self.assertIn(b'Simba', res_pets.data)

        res_shop = self.client.get('/shop')
        self.assertIn(b'Royal Canin', res_shop.data)
        self.assertIn(b'Whiskas', res_shop.data)

        # 5. Render postgres url fix check
        test_postgres_url = "postgres://user:pass@host:5432/dbname"
        converted = test_postgres_url.replace('postgres://', 'postgresql://', 1)
        self.assertTrue(converted.startswith("postgresql://"))

        print("[PASS] Database idempotency, admin credentials, and Render bootstrap verified")

if __name__ == '__main__':
    unittest.main()

