import json

# Load the data
with open('data/crew_data.json', 'r', encoding='utf-8') as f:
    crew_data = json.load(f)

print(f"Loaded {len(crew_data)} crew members")
print("\nChecking first entry keys:")
print(crew_data[0].keys())

# Check if keys need fixing
needs_fix = False
if 'baselocation' in crew_data[0]:
    print("\n⚠ Found lowercase 'baselocation' - needs fixing to 'baseLocation'")
    needs_fix = True

if needs_fix:
    # Fix all entries
    for crew in crew_data:
        if 'baselocation' in crew and 'baseLocation' not in crew:
            crew['baseLocation'] = crew.pop('baselocation')
    
    # Save fixed data
    with open('data/crew_data_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(crew_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Fixed {len(crew_data)} entries")
    print("✓ Saved to: data/crew_data_fixed.json")
    print("\nRename the file:")
    print("  1. Delete or rename old crew_data.json")
    print("  2. Rename crew_data_fixed.json to crew_data.json")
else:
    print("\n✓ Keys are correct - using camelCase 'baseLocation'")
