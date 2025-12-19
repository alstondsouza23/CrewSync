import json

# Load crew data
with open('data/crew_data.json', 'r', encoding='utf-8') as f:
    crew_data = json.load(f)

# Load flights data
with open('data/flights_data.json', 'r', encoding='utf-8') as f:
    flights_data = json.load(f)

print("="*70)
print("CREW AVAILABILITY ANALYSIS")
print("="*70)
print(f"\nTotal crew members: {len(crew_data)}")
print(f"Total flights: {len(flights_data)}")

# Count availability statuses
availability_counts = {}
missing_availability = []
wrong_case = []

for crew in crew_data:
    if 'availability' not in crew:
        missing_availability.append(crew['name'])
        status = 'MISSING'
    else:
        status = crew['availability']
        
        # Check for wrong case
        if status and status.lower() == 'available' and status != 'Available':
            wrong_case.append((crew['name'], status))
    
    availability_counts[status] = availability_counts.get(status, 0) + 1

print("\n" + "-"*70)
print("AVAILABILITY DISTRIBUTION")
print("-"*70)
for status, count in sorted(availability_counts.items()):
    percentage = (count/len(crew_data)*100)
    print(f"  {status:20s}: {count:3d} ({percentage:5.1f}%)")

if missing_availability:
    print("\n" + "!"*70)
    print(f"⚠ WARNING: {len(missing_availability)} crew MISSING 'availability' key")
    print("!"*70)
    for name in missing_availability[:10]:
        print(f"  ✗ {name}")
    if len(missing_availability) > 10:
        print(f"  ... and {len(missing_availability) - 10} more")
    print("\n→ Run: python fix_all_availability.py")

if wrong_case:
    print("\n" + "!"*70)
    print(f"⚠ WARNING: {len(wrong_case)} crew with WRONG CASE")
    print("!"*70)
    for name, status in wrong_case[:10]:
        print(f"  ✗ {name}: '{status}' (should be 'Available')")
    if len(wrong_case) > 10:
        print(f"  ... and {len(wrong_case) - 10} more")
    print("\n→ Run: python fix_all_availability.py")

# Analyze each flight
print("\n" + "="*70)
print("FLIGHT-SPECIFIC ANALYSIS")
print("="*70)

for flight in flights_data:
    print(f"\n--- {flight['flightNumber']}: {flight['route']} ---")
    print(f"Aircraft: {flight['aircraft']}")
    print(f"Status: {flight['status']}")
    
    # Find crew certified for this aircraft
    certified_crew = [
        c for c in crew_data 
        if flight['aircraft'] in c.get('certifications', [])
    ]
    print(f"Crew with {flight['aircraft']} certification: {len(certified_crew)}")
    
    # Find available crew
    available_certified = [
        c for c in certified_crew 
        if c.get('availability', '').lower() == 'available'
    ]
    print(f"Available certified crew: {len(available_certified)}")
    
    if len(available_certified) == 0:
        print(f"  ⚠ NO RECOMMENDATIONS POSSIBLE - No available crew!")
    elif len(available_certified) < 5:
        print(f"  ⚠ Only {len(available_certified)} recommendations possible")
    else:
        print(f"  ✓ Can provide 5+ recommendations")
    
    # Show sample crew
    if len(available_certified) > 0:
        print(f"\n  Sample available crew:")
        for crew in available_certified[:3]:
            print(f"    • {crew['name']} ({crew.get('designation', 'N/A')}) - {crew.get('baseLocation', 'N/A')}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

issues_found = len(missing_availability) + len(wrong_case)

if issues_found == 0:
    print("✓ All crew members have correct 'availability' values")
    print("✓ No fixes needed")
    print("\nYour backend should work correctly!")
else:
    print(f"✗ Found {issues_found} issues with availability data")
    print("\n→ RECOMMENDED ACTION:")
    print("  1. Run: python fix_all_availability.py")
    print("  2. Restart backend: python app.py")
    print("  3. Test: curl http://localhost:5000/api/recommendations/AI-202")

print("="*70)
