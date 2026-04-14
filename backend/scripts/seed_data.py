# scripts/seed_data.py
# This script populates the database with real Indian traffic law data
# Run this once to fill the database with initial data

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.models.models import State, Jurisdiction, Law, Fine, RTOOffice, VehicleType

def seed_states(db):
    """Seed 5 Indian states"""
    print("Seeding states...")
    
    states_data = [
        {"name": "Delhi", "code": "DL", "has_amendments": True, "capital": "New Delhi"},
        {"name": "Maharashtra", "code": "MH", "has_amendments": True, "capital": "Mumbai"},
        {"name": "Karnataka", "code": "KA", "has_amendments": True, "capital": "Bengaluru"},
        {"name": "Tamil Nadu", "code": "TN", "has_amendments": True, "capital": "Chennai"},
        {"name": "Uttar Pradesh", "code": "UP", "has_amendments": True, "capital": "Lucknow"},
    ]
    
    states = {}
    for data in states_data:
        # Check if already exists
        existing = db.query(State).filter(State.code == data["code"]).first()
        if not existing:
            state = State(**data)
            db.add(state)
            db.flush()  # flush to get the ID
            states[data["code"]] = state
            print(f"  ✅ Added state: {data['name']}")
        else:
            states[data["code"]] = existing
            print(f"  ⏭️  State exists: {data['name']}")
    
    db.commit()
    return states


def seed_laws(db):
    """Seed real MV Act laws"""
    print("\nSeeding laws...")
    
    laws_data = [
        {
            "section": "Section 112",
            "title": "Over Speeding",
            "description": "Whoever drives a motor vehicle in contravention of the speed limits referred to in section 112 shall be punishable.",
            "category": "Speed",
            "is_national": True,
            "plain_language": "Driving faster than the allowed speed limit on any road."
        },
        {
            "section": "Section 129",
            "title": "Helmet Not Worn",
            "description": "Every person driving or riding on a motorcycle shall wear a protective headgear conforming to the standards of Bureau of Indian Standards.",
            "category": "Safety",
            "is_national": True,
            "plain_language": "Riding a two-wheeler without wearing a proper ISI-marked helmet."
        },
        {
            "section": "Section 130",
            "title": "Seat Belt Not Worn",
            "description": "Every person driving or sitting in a motor vehicle shall wear a safety belt as required by the Central Government.",
            "category": "Safety",
            "is_national": True,
            "plain_language": "Driving or sitting in a car without wearing a seat belt."
        },
        {
            "section": "Section 177",
            "title": "General Traffic Rule Violation",
            "description": "Whoever contravenes any provision of this Act or of any rule, regulation or notification made thereunder shall be punishable.",
            "category": "General",
            "is_national": True,
            "plain_language": "Breaking any general traffic rule like jumping a red light or wrong parking."
        },
        {
            "section": "Section 179",
            "title": "Disobedience of Orders of Authorities",
            "description": "Whoever wilfully disobeys any direction lawfully given by any person or authority empowered under this Act shall be punishable.",
            "category": "General",
            "is_national": True,
            "plain_language": "Refusing to follow instructions given by a traffic police officer."
        },
        {
            "section": "Section 180",
            "title": "Allowing Unauthorised Person to Drive",
            "description": "Whoever drives a motor vehicle in any public place without a valid driving licence or allows any person not holding a valid driving licence to drive shall be punishable.",
            "category": "Documents",
            "is_national": True,
            "plain_language": "Letting someone drive your vehicle who does not have a valid driving licence."
        },
        {
            "section": "Section 181",
            "title": "Driving Without Licence",
            "description": "Whoever drives a motor vehicle in any public place without a valid licence is punishable under this section.",
            "category": "Documents",
            "is_national": True,
            "plain_language": "Driving any vehicle on a public road without a valid driving licence."
        },
        {
            "section": "Section 182",
            "title": "Driving Despite Disqualification",
            "description": "Whoever drives a motor vehicle in any public place when he has been disqualified from holding or obtaining a licence is punishable.",
            "category": "Documents",
            "is_national": True,
            "plain_language": "Driving even after your licence has been cancelled or suspended by authorities."
        },
        {
            "section": "Section 183",
            "title": "Driving at Excessive Speed",
            "description": "Whoever drives a motor vehicle at a speed exceeding the limit prescribed shall be punishable under this section.",
            "category": "Speed",
            "is_national": True,
            "plain_language": "Driving at a speed that is dangerously above the posted speed limit."
        },
        {
            "section": "Section 184",
            "title": "Dangerous Driving",
            "description": "Whoever drives a motor vehicle in any public place in a manner which is dangerous to the public shall be punishable.",
            "category": "Dangerous Driving",
            "is_national": True,
            "plain_language": "Driving recklessly or in a way that puts other people in danger."
        },
        {
            "section": "Section 185",
            "title": "Drunk Driving / DUI",
            "description": "Whoever drives or attempts to drive a motor vehicle while under the influence of alcohol or drugs exceeding prescribed limits shall be punishable.",
            "category": "Drunk Driving",
            "is_national": True,
            "plain_language": "Driving while drunk or under the influence of drugs. Blood alcohol limit is 30mg per 100ml."
        },
        {
            "section": "Section 186",
            "title": "Driving When Mentally or Physically Unfit",
            "description": "Whoever drives a motor vehicle in any public place when he is in such a physical or mental condition as to be incapable of exercising proper control shall be punishable.",
            "category": "Safety",
            "is_national": True,
            "plain_language": "Driving when you are too sick, tired, or mentally unfit to drive safely."
        },
        {
            "section": "Section 189",
            "title": "Racing and Trials of Speed",
            "description": "Whoever promotes, abets, takes part in or is otherwise concerned with any race or trial of speed between motor vehicles in any public place shall be punishable.",
            "category": "Dangerous Driving",
            "is_national": True,
            "plain_language": "Street racing or speed competitions on public roads."
        },
        {
            "section": "Section 192A",
            "title": "Vehicle Without Permit",
            "description": "Whoever drives a motor vehicle or causes or allows a motor vehicle to be used without a permit required shall be punishable.",
            "category": "Documents",
            "is_national": True,
            "plain_language": "Operating a commercial vehicle without the required permit."
        },
        {
            "section": "Section 194",
            "title": "Driving Overloaded Vehicle",
            "description": "Whoever drives or causes or allows to be driven in any public place any motor vehicle which exceeds the limits of weight shall be punishable.",
            "category": "Overloading",
            "is_national": True,
            "plain_language": "Carrying more passengers or load than the vehicle is legally allowed to carry."
        },
        {
            "section": "Section 194A",
            "title": "Overloading of Passengers",
            "description": "Whoever drives or causes or allows to be driven any motor vehicle with passengers in excess of the seating capacity shall be punishable.",
            "category": "Overloading",
            "is_national": True,
            "plain_language": "Carrying more passengers than the number of seats in the vehicle."
        },
        {
            "section": "Section 194B",
            "title": "Not Wearing Seat Belt",
            "description": "Whoever drives a motor vehicle without wearing a seat belt or allows passengers to sit without seat belts where required shall be punishable.",
            "category": "Safety",
            "is_national": True,
            "plain_language": "Driver or passenger not wearing seat belt in a car."
        },
        {
            "section": "Section 194C",
            "title": "Driving Without Helmet",
            "description": "Whoever drives or rides on a motor cycle without wearing a protective headgear shall be punishable.",
            "category": "Safety",
            "is_national": True,
            "plain_language": "Riding a two-wheeler without a helmet — applies to both rider and pillion."
        },
        {
            "section": "Section 194D",
            "title": "Not Giving Way to Emergency Vehicles",
            "description": "Whoever does not give way to emergency vehicles such as ambulance, fire brigade or police vehicles shall be punishable.",
            "category": "General",
            "is_national": True,
            "plain_language": "Not moving aside to let ambulance, fire engine or police vehicle pass."
        },
        {
            "section": "Section 196",
            "title": "Driving Without Insurance",
            "description": "Whoever drives a motor vehicle or causes or allows a motor vehicle to be driven without a valid insurance policy shall be punishable.",
            "category": "Documents",
            "is_national": True,
            "plain_language": "Driving any vehicle without a valid third-party insurance policy."
        },
    ]
    
    laws = {}
    for data in laws_data:
        existing = db.query(Law).filter(Law.section == data["section"]).first()
        if not existing:
            law = Law(**data)
            db.add(law)
            db.flush()
            laws[data["section"]] = law
            print(f"  ✅ Added law: {data['section']} - {data['title']}")
        else:
            laws[data["section"]] = existing
            print(f"  ⏭️  Law exists: {data['section']}")
    
    db.commit()
    return laws


def seed_fines(db, states, laws):
    """Seed fine amounts per state per violation"""
    print("\nSeeding fines...")
    
    # Fine data structure:
    # (section, state_code, vehicle_type, first_offence, repeat_offence, mv_act_ref)
    fines_data = [
        # OVER SPEEDING - Section 183
        ("Section 183", None, VehicleType.two_wheeler, 1000, 2000, "S.183 MV Act"),
        ("Section 183", None, VehicleType.four_wheeler, 1000, 2000, "S.183 MV Act"),
        ("Section 183", None, VehicleType.commercial, 2000, 4000, "S.183 MV Act"),
        ("Section 183", "DL", VehicleType.two_wheeler, 2000, 4000, "S.183 MV Act + Delhi Amendment"),
        ("Section 183", "MH", VehicleType.two_wheeler, 1500, 3000, "S.183 MV Act + MH Amendment"),

        # HELMET - Section 194C
        ("Section 194C", None, VehicleType.two_wheeler, 1000, 2000, "S.194C MV Act"),
        ("Section 194C", "DL", VehicleType.two_wheeler, 1000, 2000, "S.194C MV Act + Delhi Amendment"),
        ("Section 194C", "MH", VehicleType.two_wheeler, 500, 1500, "S.194C MV Act + MH Amendment"),
        ("Section 194C", "KA", VehicleType.two_wheeler, 500, 1000, "S.194C MV Act + KA Amendment"),
        ("Section 194C", "TN", VehicleType.two_wheeler, 1000, 2000, "S.194C MV Act + TN Amendment"),
        ("Section 194C", "UP", VehicleType.two_wheeler, 1000, 2000, "S.194C MV Act + UP Amendment"),

        # SEAT BELT - Section 194B
        ("Section 194B", None, VehicleType.four_wheeler, 1000, 1000, "S.194B MV Act"),
        ("Section 194B", "DL", VehicleType.four_wheeler, 1000, 1000, "S.194B MV Act + Delhi Amendment"),
        ("Section 194B", "MH", VehicleType.four_wheeler, 500, 1000, "S.194B MV Act + MH Amendment"),

        # DRUNK DRIVING - Section 185
        ("Section 185", None, VehicleType.all_vehicles, 10000, 15000, "S.185 MV Act"),
        ("Section 185", "DL", VehicleType.all_vehicles, 10000, 15000, "S.185 MV Act + Delhi Amendment"),
        ("Section 185", "MH", VehicleType.all_vehicles, 10000, 15000, "S.185 MV Act + MH Amendment"),

        # DRIVING WITHOUT LICENCE - Section 181
        ("Section 181", None, VehicleType.all_vehicles, 5000, 10000, "S.181 MV Act"),
        ("Section 181", "DL", VehicleType.all_vehicles, 5000, 10000, "S.181 MV Act + Delhi Amendment"),

        # DRIVING WITHOUT INSURANCE - Section 196
        ("Section 196", None, VehicleType.all_vehicles, 2000, 4000, "S.196 MV Act"),
        ("Section 196", "DL", VehicleType.all_vehicles, 2000, 4000, "S.196 MV Act + Delhi Amendment"),
        ("Section 196", "MH", VehicleType.all_vehicles, 2000, 4000, "S.196 MV Act + MH Amendment"),

        # DANGEROUS DRIVING - Section 184
        ("Section 184", None, VehicleType.all_vehicles, 5000, 10000, "S.184 MV Act"),

        # GENERAL VIOLATION - Section 177
        ("Section 177", None, VehicleType.all_vehicles, 500, 1500, "S.177 MV Act"),
        ("Section 177", "DL", VehicleType.all_vehicles, 500, 1500, "S.177 MV Act + Delhi Amendment"),

        # OVERLOADING - Section 194
        ("Section 194", None, VehicleType.commercial, 20000, 20000, "S.194 MV Act"),
        ("Section 194", None, VehicleType.heavy_vehicle, 20000, 20000, "S.194 MV Act"),

        # RACING - Section 189
        ("Section 189", None, VehicleType.all_vehicles, 5000, 10000, "S.189 MV Act"),

        # NOT GIVING WAY TO EMERGENCY - Section 194D
        ("Section 194D", None, VehicleType.all_vehicles, 10000, 10000, "S.194D MV Act"),

        # USING MOBILE WHILE DRIVING - Section 177
        ("Section 177", "DL", VehicleType.all_vehicles, 1000, 2000, "S.177 MV Act - Mobile Use"),
    ]

    count = 0
    for section, state_code, vehicle_type, first_amt, repeat_amt, mv_ref in fines_data:
        law = laws.get(section)
        if not law:
            continue

        state = states.get(state_code) if state_code else None
        state_id = state.id if state else None

        # Check if fine already exists
        existing = db.query(Fine).filter(
            Fine.law_id == law.id,
            Fine.state_id == state_id,
            Fine.vehicle_type == vehicle_type
        ).first()

        if not existing:
            fine = Fine(
                law_id=law.id,
                state_id=state_id,
                vehicle_type=vehicle_type,
                first_offence_amount=first_amt,
                repeat_offence_amount=repeat_amt,
                mv_act_reference=mv_ref
            )
            db.add(fine)
            count += 1

    db.commit()
    print(f"  ✅ Added {count} fine records")


def seed_rto_offices(db, states):
    """Seed RTO offices for major cities"""
    print("\nSeeding RTO offices...")

    rto_data = [
        # DELHI
        {"name": "RTO Delhi Central", "code": "DL-01", "city": "New Delhi",
         "state_code": "DL", "address": "Shakti Nagar, Delhi 110007",
         "latitude": 28.6862, "longitude": 77.2056,
         "phone": "011-27466942", "working_hours": "Mon-Fri 9AM-5PM"},

        {"name": "RTO Delhi East", "code": "DL-02", "city": "New Delhi",
         "state_code": "DL", "address": "Surajmal Vihar, Delhi 110092",
         "latitude": 28.6729, "longitude": 77.3122,
         "phone": "011-22374023", "working_hours": "Mon-Fri 9AM-5PM"},

        {"name": "RTO Delhi West", "code": "DL-03", "city": "New Delhi",
         "state_code": "DL", "address": "Janakpuri, Delhi 110058",
         "latitude": 28.6289, "longitude": 77.0853,
         "phone": "011-25618029", "working_hours": "Mon-Fri 9AM-5PM"},

        # MAHARASHTRA
        {"name": "RTO Mumbai Central", "code": "MH-01", "city": "Mumbai",
         "state_code": "MH", "address": "Tardeo, Mumbai 400034",
         "latitude": 18.9647, "longitude": 72.8258,
         "phone": "022-23527044", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Mumbai West", "code": "MH-02", "city": "Mumbai",
         "state_code": "MH", "address": "Andheri West, Mumbai 400058",
         "latitude": 19.1197, "longitude": 72.8468,
         "phone": "022-26204515", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Pune", "code": "MH-12", "city": "Pune",
         "state_code": "MH", "address": "Shivajinagar, Pune 411005",
         "latitude": 18.5308, "longitude": 73.8474,
         "phone": "020-25536353", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Nagpur", "code": "MH-31", "city": "Nagpur",
         "state_code": "MH", "address": "Civil Lines, Nagpur 440001",
         "latitude": 21.1463, "longitude": 79.0826,
         "phone": "0712-2560532", "working_hours": "Mon-Sat 10AM-5PM"},

        # KARNATAKA
        {"name": "RTO Bengaluru Central", "code": "KA-01", "city": "Bengaluru",
         "state_code": "KA", "address": "Kasturba Road, Bengaluru 560001",
         "latitude": 12.9757, "longitude": 77.5931,
         "phone": "080-22371609", "working_hours": "Mon-Sat 10AM-5:30PM"},

        {"name": "RTO Bengaluru East", "code": "KA-02", "city": "Bengaluru",
         "state_code": "KA", "address": "Indiranagar, Bengaluru 560038",
         "latitude": 12.9784, "longitude": 77.6408,
         "phone": "080-25209622", "working_hours": "Mon-Sat 10AM-5:30PM"},

        {"name": "RTO Mysuru", "code": "KA-09", "city": "Mysuru",
         "state_code": "KA", "address": "Nazarbad, Mysuru 570010",
         "latitude": 12.3052, "longitude": 76.6552,
         "phone": "0821-2440908", "working_hours": "Mon-Sat 10AM-5PM"},

        # TAMIL NADU
        {"name": "RTO Chennai Central", "code": "TN-01", "city": "Chennai",
         "state_code": "TN", "address": "Ezhilagam, Chennai 600005",
         "latitude": 13.0632, "longitude": 80.2553,
         "phone": "044-28521076", "working_hours": "Mon-Fri 10AM-5:45PM"},

        {"name": "RTO Chennai North", "code": "TN-02", "city": "Chennai",
         "state_code": "TN", "address": "Ponneri High Road, Chennai 600081",
         "latitude": 13.1219, "longitude": 80.2453,
         "phone": "044-25930614", "working_hours": "Mon-Fri 10AM-5:45PM"},

        {"name": "RTO Coimbatore", "code": "TN-38", "city": "Coimbatore",
         "state_code": "TN", "address": "Race Course, Coimbatore 641018",
         "latitude": 11.0128, "longitude": 77.0058,
         "phone": "0422-2300148", "working_hours": "Mon-Fri 10AM-5:45PM"},

        {"name": "RTO Madurai", "code": "TN-58", "city": "Madurai",
         "state_code": "TN", "address": "KK Nagar, Madurai 625020",
         "latitude": 9.9195, "longitude": 78.1191,
         "phone": "0452-2580175", "working_hours": "Mon-Fri 10AM-5:45PM"},

        # UTTAR PRADESH
        {"name": "RTO Lucknow", "code": "UP-32", "city": "Lucknow",
         "state_code": "UP", "address": "Kaiserbagh, Lucknow 226001",
         "latitude": 26.8507, "longitude": 80.9462,
         "phone": "0522-2238785", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Kanpur", "code": "UP-78", "city": "Kanpur",
         "state_code": "UP", "address": "Collectorganj, Kanpur 208001",
         "latitude": 26.4675, "longitude": 80.3498,
         "phone": "0512-2550352", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Agra", "code": "UP-80", "city": "Agra",
         "state_code": "UP", "address": "Sanjay Place, Agra 282002",
         "latitude": 27.1963, "longitude": 78.0087,
         "phone": "0562-2226274", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Varanasi", "code": "UP-65", "city": "Varanasi",
         "state_code": "UP", "address": "Sigra, Varanasi 221010",
         "latitude": 25.3315, "longitude": 82.9870,
         "phone": "0542-2220024", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Noida", "code": "UP-16", "city": "Noida",
         "state_code": "UP", "address": "Sector 33, Noida 201301",
         "latitude": 28.5706, "longitude": 77.3210,
         "phone": "0120-2457106", "working_hours": "Mon-Sat 10AM-5PM"},

        {"name": "RTO Ghaziabad", "code": "UP-14", "city": "Ghaziabad",
         "state_code": "UP", "address": "Navyug Market, Ghaziabad 201001",
         "latitude": 28.6692, "longitude": 77.4538,
         "phone": "0120-2820010", "working_hours": "Mon-Sat 10AM-5PM"},
    ]

    count = 0
    for data in rto_data:
        existing = db.query(RTOOffice).filter(RTOOffice.code == data["code"]).first()
        if not existing:
            state = states.get(data["state_code"])
            rto = RTOOffice(
                name=data["name"],
                code=data["code"],
                city=data["city"],
                state_id=state.id if state else None,
                address=data["address"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                phone=data["phone"],
                working_hours=data["working_hours"]
            )
            db.add(rto)
            count += 1
            print(f"  ✅ Added RTO: {data['code']} - {data['name']}")
        else:
            print(f"  ⏭️  RTO exists: {data['code']}")

    db.commit()
    print(f"\n  Total RTOs added: {count}")


def main():
    """Run all seeders"""
    print("=" * 50)
    print("DriveLegal Database Seeder")
    print("=" * 50)

    db = SessionLocal()
    try:
        states = seed_states(db)
        laws = seed_laws(db)
        seed_fines(db, states, laws)
        seed_rto_offices(db, states)

        print("\n" + "=" * 50)
        print("✅ Database seeding complete!")
        print("=" * 50)

        # Print summary
        from app.models.models import State, Law, Fine, RTOOffice
        print(f"\nDatabase summary:")
        print(f"  States:      {db.query(State).count()}")
        print(f"  Laws:        {db.query(Law).count()}")
        print(f"  Fines:       {db.query(Fine).count()}")
        print(f"  RTO Offices: {db.query(RTOOffice).count()}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()