import os
from datetime import datetime, timedelta, timezone
from app import app
from models import db, User, Pet, Product, AdoptionRequest, Order, OrderItem

def utc_now():
    return datetime.now(timezone.utc)

def seed_database():
    with app.app_context():
        # Drop and recreate tables for clean seed
        print("Recreating database schema...")
        db.drop_all()
        db.create_all()

        print("Seeding Users with authentic Indian profiles...")
        # 1. Admin User (Aarav Sharma)
        admin = User(
            name="Aarav Sharma",
            email="admin@adoptnshop.com",
            role="admin",
            phone="+91 98200 12345",
            address="Adopt n Shop Shelter HQ, Bandra Kurla Complex (BKC), Mumbai, Maharashtra - 400051"
        )
        admin.set_password("admin123")
        db.session.add(admin)

        # 2. Demo Customers
        rohan = User(
            name="Rohan Verma",
            email="rohan@example.com",
            role="customer",
            phone="+91 98765 43210",
            address="Flat 402, Shanti Heights, Bandra West, Mumbai, Maharashtra - 400050"
        )
        rohan.set_password("user123")
        db.session.add(rohan)

        priya = User(
            name="Priya Patel",
            email="priya@example.com",
            role="customer",
            phone="+91 98234 56789",
            address="12, Gokuldham Society, Satellite Road, Ahmedabad, Gujarat - 380015"
        )
        priya.set_password("user123")
        db.session.add(priya)

        ananya = User(
            name="Ananya Iyer",
            email="ananya@example.com",
            role="customer",
            phone="+91 97123 45678",
            address="88, 12th Main, Indiranagar, Bengaluru, Karnataka - 560038"
        )
        ananya.set_password("user123")
        db.session.add(ananya)

        db.session.commit()

        print("Seeding Pets across Indian cities...")
        pets = [
            Pet(
                name="Bruno",
                species="Dog",
                breed="Indian Pariah (Desi)",
                age_years=1,
                age_months=6,
                gender="Male",
                size="Medium",
                city="Mumbai",
                health_status="Fully Vaccinated, Dewormed & Microchipped",
                vaccinated=True,
                description="Bruno is a resilient and affectionate Indian Indie dog rescued from Marine Drive promenade. Highly alert, friendly, extremely low-maintenance, and great with society apartments.",
                image_url="https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                name="Simba",
                species="Cat",
                breed="Persian Longhair",
                age_years=1,
                age_months=2,
                gender="Female",
                size="Small",
                city="Bengaluru",
                health_status="Vaccinated & Spayed",
                vaccinated=True,
                description="Simba is a gentle cream-white Persian beauty with amber eyes. She enjoys quiet balconies, afternoon naps in the Bangalore breeze, and soft chin scratches.",
                image_url="https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                name="Sheru",
                species="Dog",
                breed="Golden Retriever",
                age_years=2,
                age_months=4,
                gender="Male",
                size="Large",
                city="Delhi NCR",
                health_status="Up-to-date on 7-in-1 Vaccine & Anti-Rabies",
                vaccinated=True,
                description="Sheru is a magnificent, playful Golden Retriever who loves morning park runs in Lodhi Gardens. Very gentle with kids and loves ball games.",
                image_url="https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                owner_id=rohan.id,  # Listed by Rohan Verma
                name="Bella",
                species="Dog",
                breed="Beagle",
                age_years=0,
                age_months=9,
                gender="Female",
                size="Medium",
                city="Mumbai",
                health_status="Vaccinated & Health Checked",
                vaccinated=True,
                description="Bella is a curious, energetic Beagle pup listed for rehoming as our family is relocating abroad. She is house-trained, friendly, and loves treat puzzles.",
                image_url="https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?auto=format&fit=crop&w=600&q=80",
                status="pending"
            ),
            Pet(
                owner_id=priya.id,  # Listed by Priya Patel
                name="Milo",
                species="Cat",
                breed="Indian Indie Cat",
                age_years=1,
                age_months=0,
                gender="Male",
                size="Small",
                city="Ahmedabad",
                health_status="Vaccinated & Neutered",
                vaccinated=True,
                description="Rescued as a stray kitten, Milo has blossomed into a clean, playful indoor cat. He is litter-trained, loves chasing feather toys, and purrs non-stop.",
                image_url="https://images.unsplash.com/photo-1573865526739-10659fec78a5?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                name="Mithu",
                species="Bird",
                breed="Indian Ringneck Parakeet",
                age_years=2,
                age_months=0,
                gender="Male",
                size="Small",
                city="Pune",
                health_status="Avian Vet Inspected & Healthy",
                vaccinated=True,
                description="Mithu is a lively green parrot who loves fresh guava slices and almonds. He whistles tunes and greets family members with cheerful chirps.",
                image_url="https://images.unsplash.com/photo-1552728089-57bdde30beb3?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                name="Clover",
                species="Rabbit",
                breed="Holland Lop",
                age_years=0,
                age_months=8,
                gender="Female",
                size="Small",
                city="Hyderabad",
                health_status="Vaccinated & Vet Checked",
                vaccinated=True,
                description="Clover is a sweet bunny with floppy ears and a calm temperament. She loves fresh coriander, spinach, and gentle ear rubs.",
                image_url="https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                name="Rocky",
                species="Dog",
                breed="Labrador Retriever",
                age_years=2,
                age_months=0,
                gender="Male",
                size="Large",
                city="Bengaluru",
                health_status="Vaccinated & Dewormed",
                vaccinated=True,
                description="Rocky is an energetic chocolate Labrador who loves playing fetch in Cubbon Park. Perfect companion for an active family.",
                image_url="https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                name="Cleo",
                species="Cat",
                breed="Siamese Mix",
                age_years=1,
                age_months=8,
                gender="Female",
                size="Small",
                city="Pune",
                health_status="Vaccinated & Spayed",
                vaccinated=True,
                description="Cleo is a blue-eyed Siamese mix who loves curling up on the sofa during monsoons. She gets along well with calm dogs and other cats.",
                image_url="https://images.unsplash.com/photo-1513360309081-38f076278f1e?auto=format&fit=crop&w=600&q=80",
                status="available"
            ),
            Pet(
                name="Moti",
                species="Dog",
                breed="Desi Indie Hound",
                age_years=3,
                age_months=0,
                gender="Male",
                size="Medium",
                city="Jaipur",
                health_status="Vaccinated & Neutered",
                vaccinated=True,
                description="Moti is a proud, intelligent desi dog who was adopted by Ananya through Adopt n Shop. He is now living his happiest life!",
                image_url="https://images.unsplash.com/photo-1591769225440-811ad7d6eab2?auto=format&fit=crop&w=600&q=80",
                status="adopted"
            )
        ]
        db.session.add_all(pets)
        db.session.commit()

        print("Seeding Products with Indian Rupee (INR) Pricing...")
        products = [
            # Food
            Product(
                name="Royal Canin Maxi Adult Dry Dog Food (15kg)",
                category="Food",
                description="Complete nutritional feed tailored for large adult dogs. Enriched with EPA & DHA omega fatty acids for bone health and radiant shiny coat.",
                price=5499.00,
                stock=25,
                image_url="https://images.unsplash.com/photo-1589924691995-400dc9ecc119?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Whiskas Ocean Fish & Tuna Wet Cat Food (12-Pouch Multipack)",
                category="Food",
                description="Delicious tender fish chunks in savory gravy formulated for adult cats. Packed with essential Taurine, Vitamin E, and Zinc for eye and coat health.",
                price=899.00,
                stock=40,
                image_url="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Drools Absolute Calcium Bone Supplement for Dogs (50 Pcs)",
                category="Food",
                description="Essential calcium-phosphorus ratio supplement strengthening teeth and joint development in active puppies and adult dogs.",
                price=450.00,
                stock=50,
                image_url="https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Kaytee Forti-Diet Healthy Grain & Seed Blend for Birds (2kg)",
                category="Food",
                description="Wholesome seed, millets, and nut blend enriched with DHA and prebiotics to support immunity and vibrant plumage in parakeets and lovebirds.",
                price=799.00,
                stock=30,
                image_url="https://images.unsplash.com/photo-1555685812-4b943f1cb0eb?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Oxbow Western Timothy High-Fiber Grass Hay (1kg)",
                category="Food",
                description="Hand-sorted fragrant grass hay essential for the digestion and dental health of rabbits and guinea pigs. 100% natural and pesticide free.",
                price=850.00,
                stock=35,
                image_url="https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            # Toys
            Product(
                name="KONG Classic Durable Natural Rubber Dog Chew Toy (Large)",
                category="Toys",
                description="Ultra-durable natural red rubber toy with erratic bounce for fetch. Excellent for stuffing with peanut butter or kibble to keep dogs mentally stimulated.",
                price=999.00,
                stock=45,
                image_url="https://images.unsplash.com/photo-1601758228041-f3b2795255f1?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Interactive Feather Wand & LED Laser Pointer Cat Toy Combo",
                category="Toys",
                description="Stimulate your indoor cat's natural hunting instinct. Includes a flexible telescopic wand with organic feathers and a USB rechargeable laser light.",
                price=499.00,
                stock=40,
                image_url="https://images.unsplash.com/photo-1545249390-6bdfa286032f?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Heavy-Duty Braided Pure Cotton Tug Rope with Squeaker",
                category="Toys",
                description="100% natural washable cotton rope designed for intense tug-of-war. Helps remove tartar and plaque during play.",
                price=349.00,
                stock=30,
                image_url="https://images.unsplash.com/photo-1576201836106-db1758fd1c97?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Handcrafted Wooden Hanging Swing & Bell Toy for Birds",
                category="Toys",
                description="Natural non-toxic wooden perches with colorful wooden beads and copper bells providing hours of exercise inside bird cages.",
                price=399.00,
                stock=25,
                image_url="https://images.unsplash.com/photo-1552728089-57bdde30beb3?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            # Accessories
            Product(
                name="Adjustable Ergonomic Reflective No-Pull Dog Harness",
                category="Accessories",
                description="Breathable air-mesh padding with dual leash attachment rings. Front D-ring discourages pulling, with 3M reflective trims for night walk safety.",
                price=899.00,
                stock=35,
                image_url="https://images.unsplash.com/photo-1608096299210-db7e38487075?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Orthopedic Memory Foam Ultra-Soft Velvet Pet Lounge Bed",
                category="Accessories",
                description="High-density therapeutic orthopedic foam relieving joint and hip pressure. Removable water-resistant, machine-washable soft velvet cover.",
                price=2499.00,
                stock=18,
                image_url="https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Non-Skid Stainless Steel Double Feeding & Water Bowls",
                category="Accessories",
                description="Rust-proof food grade stainless steel bowls fitted inside an anti-spill non-skid silicone base keeping feeding areas clean.",
                price=699.00,
                stock=40,
                image_url="https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="One-Click Self-Cleaning Deshedding Pet Grooming Brush",
                category="Accessories",
                description="Gently removes shedding undercoat, mats, and knots with fine bent wire bristles. One-click button retracts bristles for effortless hair disposal.",
                price=549.00,
                stock=40,
                image_url="https://images.unsplash.com/photo-1516734212186-a967f81ad0d7?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            # Healthcare
            Product(
                name="Frontline Plus Flea & Tick Spot-On Treatment (3 Pipettes)",
                category="Healthcare",
                description="Fast-acting veterinary formula that kills adult fleas, ticks, and flea eggs on contact for a full 30 days per pipette application.",
                price=1499.00,
                stock=22,
                image_url="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?auto=format&fit=crop&w=600&q=80",
                is_active=True
            ),
            Product(
                name="Himalaya Herbal Erina-EP Anti-Tick Pet Shampoo (400ml)",
                category="Healthcare",
                description="Enriched with natural Neem and Eucalyptus oil. Prevents ectoparasites, relieves skin itching, and leaves a pleasant herbal aroma.",
                price=380.00,
                stock=30,
                image_url="https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=600&q=80",
                is_active=True
            )
        ]
        db.session.add_all(products)
        db.session.commit()

        print("Seeding Adoption Requests...")
        # Ananya's approved request for Moti
        req1 = AdoptionRequest(
            user_id=ananya.id,
            pet_id=10,  # Moti
            full_name="Ananya Iyer",
            phone="+91 97123 45678",
            address="88, 12th Main, Indiranagar, Bengaluru, Karnataka - 560038",
            living_situation="Own House with Fenced Yard",
            has_other_pets=False,
            previous_experience="Grew up with indie dogs in Bengaluru. Knowledgeable about regular vet checkups and daily exercise.",
            reason="Looking for a loyal and affectionate companion for our home.",
            status="approved",
            admin_notes="Home verification complete. Ananya is a wonderful pet parent. Moti is happily adopted!",
            created_at=utc_now() - timedelta(days=12),
            updated_at=utc_now() - timedelta(days=10)
        )
        db.session.add(req1)

        # Priya's pending request for Bruno
        req2 = AdoptionRequest(
            user_id=priya.id,
            pet_id=1,  # Bruno
            full_name="Priya Patel",
            phone="+91 98234 56789",
            address="12, Gokuldham Society, Satellite Road, Ahmedabad, Gujarat - 380015",
            living_situation="Own House with Fenced Yard",
            has_other_pets=True,
            previous_experience="Have experience caring for rescued indie dogs and cats.",
            reason="We love Bruno's calm nature and have plenty of time for daily evening walks.",
            status="pending",
            admin_notes="Application under initial review. Scheduling phone verification with applicant.",
            created_at=utc_now() - timedelta(days=2),
            updated_at=utc_now() - timedelta(days=2)
        )
        db.session.add(req2)
        db.session.commit()

        print("Seeding Sample Orders with Indian Rupee (INR)...")
        # Order 1: Rohan's delivered order
        order1 = Order(
            user_id=rohan.id,
            order_number="ANS-IN-20261110-A98F21",
            subtotal_amount=6498.00,
            shipping_fee=0.0,
            tax_amount=324.90,
            total_amount=6822.90,
            status="Delivered",
            payment_method="UPI / QR (Google Pay)",
            payment_status="Paid",
            shipping_name="Rohan Verma",
            shipping_phone="+91 98765 43210",
            shipping_address="Flat 402, Shanti Heights, Bandra West",
            shipping_city="Mumbai",
            shipping_pincode="400050",
            created_at=utc_now() - timedelta(days=8)
        )
        db.session.add(order1)
        db.session.flush()

        item1_1 = OrderItem(
            order_id=order1.id,
            product_id=1,
            product_name="Royal Canin Maxi Adult Dry Dog Food (15kg)",
            price=5499.00,
            quantity=1,
            subtotal=5499.00
        )
        item1_2 = OrderItem(
            order_id=order1.id,
            product_id=6,
            product_name="KONG Classic Durable Natural Rubber Dog Chew Toy (Large)",
            price=999.00,
            quantity=1,
            subtotal=999.00
        )
        db.session.add_all([item1_1, item1_2])

        # Order 2: Priya's processing order
        order2 = Order(
            user_id=priya.id,
            order_number="ANS-IN-20261118-B47C56",
            subtotal_amount=3398.00,
            shipping_fee=0.0,
            tax_amount=169.90,
            total_amount=3567.90,
            status="Processing",
            payment_method="UPI / QR (PhonePe)",
            payment_status="Paid",
            shipping_name="Priya Patel",
            shipping_phone="+91 98234 56789",
            shipping_address="12, Gokuldham Society, Satellite Road",
            shipping_city="Ahmedabad",
            shipping_pincode="380015",
            created_at=utc_now() - timedelta(days=1)
        )
        db.session.add(order2)
        db.session.flush()

        item2_1 = OrderItem(
            order_id=order2.id,
            product_id=2,
            product_name="Whiskas Ocean Fish & Tuna Wet Cat Food (12-Pouch Multipack)",
            price=899.00,
            quantity=1,
            subtotal=899.00
        )
        item2_2 = OrderItem(
            order_id=order2.id,
            product_id=11,
            product_name="Orthopedic Memory Foam Ultra-Soft Velvet Pet Lounge Bed",
            price=2499.00,
            quantity=1,
            subtotal=2499.00
        )
        db.session.add_all([item2_1, item2_2])

        db.session.commit()
        print("Database seeded with Indian demo accounts, pets across Indian cities, INR pricing, and UPI payments!")

if __name__ == '__main__':
    seed_database()
