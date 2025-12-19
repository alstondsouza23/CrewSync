import json
import shutil
from datetime import datetime

print("="*70)
print("CREW AVAILABILITY FIX UTILITY")
print("="*70)

# Create backup first
backup_file = f"data/crew_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
shutil.copy('data/crew_data.json', backup_file)
print(f"\n✓ Created backup: {backup_file}")

# Load crew data
with open('data/crew_data.json', 'r', encoding='utf-8') as f:
    crew_data = json.load(f)

print(f"✓ Loaded {len(crew_data)} crew members\n")

print("-"*70)
print("ANALYZING AND FIXING...")
print("-"*70)

fixed_count = 0
added_count = 0
case_fixed_count = 0

for crew in crew_data:
    # Fix 1: Add missing availability
    if 'availability' not in crew:
        crew['availability'] = 'Available'
        added_count += 1
        fixed_count += 1
        print(f"  [ADDED] {crew['name']} (ID: {crew['emp_id']})")
    
    # Fix 2: Correct case (e.g., 'available' → 'Available')
    elif crew['availability']:
        old_value = crew['availability']
        
        # Standardize values
        if old_value.lower() == 'available':
            crew['availability'] = 'Available'
        elif old_value.lower() == 'fatigued':
            crew['availability'] = 'Fatigued'
        elif old_value.lower() in ['on leave', 'onleave', 'leave']:
            crew['availability'] = 'On Leave'
        elif old_value.lower() == 'backup':
            crew['availability'] = 'Backup'
        
        # Check if changed
        if crew['availability'] != old_value:
            case_fixed_count += 1
            fixed_count += 1
            print(f"  [FIXED] {crew['name']}: '{old_value}' → '{crew['availability']}'")

print("-"*70)

# Save fixed data
if fixed_count > 0:
    with open('data/crew_data.json', 'w', encoding='utf-8') as f:
        json.dump(crew_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ FIXES APPLIED:")
    print(f"  • Added availability: {added_count}")
    print(f"  • Fixed case issues: {case_fixed_count}")
    print(f"  • Total fixes: {fixed_count}")
    print(f"\n✓ Saved to: data/crew_data.json")
    print(f"✓ Backup saved to: {backup_file}")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Restart your backend:")
    print("   python app.py")
    print("\n2. Test recommendations:")
    print("   curl http://localhost:5000/api/recommendations/AI-202")
    print("\n3. Or run verification:")
    print("   python check_crew_availability.py")
else:
    print("\n✓ NO FIXES NEEDED")
    print("  All crew members already have correct 'availability' values")

print("="*70)
