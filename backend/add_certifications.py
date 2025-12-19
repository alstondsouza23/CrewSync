import json

# Load crew data
with open('data/crew_data.json', 'r', encoding='utf-8') as f:
    crew_data = json.load(f)

print(f"Processing {len(crew_data)} crew members...")
print("="*70)

fixed_count = 0
missing_base = 0

for crew in crew_data:
    # Fix 1: Add missing certifications
    if 'certifications' not in crew or not crew['certifications']:
        # Assign based on designation
        if 'Captain' in crew.get('designation', '') or 'Pilot' in crew.get('designation', ''):
            crew['certifications'] = ["Boeing 737", "Airbus A320"]
            print(f"  [ADDED] {crew['name']} (Captain/Pilot) → Both certifications")
        else:  # Cabin Crew
            crew['certifications'] = ["Boeing 737", "Airbus A320"]
            print(f"  [ADDED] {crew['name']} (Cabin Crew) → Both certifications")
        fixed_count += 1
    
    # Fix 2: Add missing baseLocation
    if 'baseLocation' not in crew:
        crew['baseLocation'] = 'DEL'  # Default to Delhi
        missing_base += 1
        print(f"  [BASE ADDED] {crew['name']} → DEL")

print("="*70)

# Save
if fixed_count > 0 or missing_base > 0:
    with open('data/crew_data.json', 'w', encoding='utf-8') as f:
        json.dump(crew_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Added certifications to: {fixed_count} crew members")
    print(f"✓ Added baseLocation to: {missing_base} crew members")
    print(f"✓ Saved to: data/crew_data.json")
else:
    print("\n✓ No fixes needed - all crew have certifications")

print("\nNEXT STEPS:")
print("1. Restart: python app.py")
print("2. Test: curl http://localhost:5000/api/recommendations/AI-156")
