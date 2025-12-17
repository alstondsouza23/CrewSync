from data_structures import *

class CrewRecommendationEngine:
    """
    17-Parameter Algorithmic Recommendation System
    NO ML/AI - Pure data structure-driven decision making
    """
    
    # Parameter weights (total = 100%)
    WEIGHTS = {
        'fatigueScore': 0.15,           # 15% - Most critical
        'restPeriodScore': 0.10,        # 10%
        'consecutiveDutyScore': 0.08,   # 8%
        'medicalStatusScore': 0.07,     # 7%
        'performanceScore': 0.10,       # 10% - High priority
        'onTimeRecordScore': 0.08,      # 8%
        'skillProficiencyScore': 0.07,  # 7%
        'reliabilityScore': 0.08,       # 8%
        'backoutHistoryScore': 0.07,    # 7%
        'seniorityScore': 0.05,         # 5%
        'flightHoursScore': 0.05,       # 5%
        'locationScore': 0.03,          # 3%
        'availabilityScore': 0.02,      # 2%
        'dutyComplianceScore': 0.02,    # 2%
        'certificationValidityScore': 0.01,  # 1%
        'languageProficiencyScore': 0.01,    # 1%
        'routeFamiliarityScore': 0.01        # 1%
    }
    
    def __init__(self, crew_data):
        self.crew_members = [CrewMember(c) for c in crew_data]
        
        # Initialize all data structures
        self.cert_hashmap = CertificationHashMap()
        self.location_graph = LocationGraph()
        self.fatigue_heap = MinHeapCrewScheduler()
        self.backup_queue = BackupCrewQueue()
        
        self._initialize_data_structures()
    
    def _initialize_data_structures(self):
        """Populate all data structures with crew data"""
        print("\n" + "="*70)
        print("INITIALIZING DATA STRUCTURES")
        print("="*70)
        
        print("\n[1] HASH MAP - Certification Index")
        for crew in self.crew_members:
            self.cert_hashmap.add_crew(crew)
        
        print("\n[2] MIN-HEAP - Fatigue Monitoring")
        for crew in self.crew_members:
            self.fatigue_heap.insert(crew, crew.data.get('fatigueScore', 50))
        
        print("\n[3] QUEUE - Backup Crew Management")
        for crew in self.crew_members:
            if crew.data.get('availability') == 'Backup':
                self.backup_queue.enqueue(crew)
        
        print("\n[4] GRAPH - Location Network")
        locations = ['DEL', 'BOM', 'BLR', 'HYD', 'GOI']
        for loc1 in locations:
            for loc2 in locations:
                if loc1 != loc2:
                    self.location_graph.add_route(loc1, loc2)
        
        print("\n" + "="*70)
        print(f"✓ Initialized {len(self.crew_members)} crew members across all data structures")
        print("="*70 + "\n")
    
    def calculate_composite_score(self, crew_data):
        """Calculate weighted composite score from all 17 parameters"""
        score = 0
        for param, weight in self.WEIGHTS.items():
            param_score = crew_data.get(param, 0)
            score += param_score * weight
        return round(score, 2)
    
    def get_recommendations(self, flight_data, top_k=5):
        """
        Main recommendation algorithm using multiple data structures
        Returns top K crew recommendations for a flight
        """
        print("\n" + "="*70)
        print(f"RECOMMENDATION ENGINE: {flight_data['flightNumber']} ({flight_data['route']})")
        print("="*70)
        
        # STEP 1: Filter by certification using Hash Map (O(1))
        print(f"\n[STEP 1] HASH MAP FILTERING - Aircraft: {flight_data['aircraft']}")
        print("-" * 70)
        eligible_crew = self.cert_hashmap.get_by_certification(flight_data['aircraft'])
        print(f"   Result: {len(eligible_crew)} crew members certified for {flight_data['aircraft']}")
        
        # STEP 2: Filter by availability
        print(f"\n[STEP 2] AVAILABILITY FILTERING")
        print("-" * 70)
        available_crew = [c for c in eligible_crew if c.data.get('availability') == 'Available']
        print(f"   Available crew: {len(available_crew)} out of {len(eligible_crew)}")
        for crew in available_crew:
            print(f"   ✓ {crew.name} - {crew.base_location}")
        
        if len(available_crew) == 0:
            print(f"\n   ⚠ WARNING: No available crew found!")
            return []
        
        # STEP 3: Check location feasibility using Graph (O(1) per check)
        print(f"\n[STEP 3] GRAPH CONNECTIVITY CHECK")
        print("-" * 70)
        origin = flight_data['origin']
        reachable_crew = []
        for crew in available_crew:
            can_reach = self.location_graph.can_reach(crew.base_location, origin)
            if can_reach:
                reachable_crew.append(crew)
        print(f"   Result: {len(reachable_crew)} crew can reach {origin}")
        
        # STEP 4: Build BST with composite scores and extract top K
        print(f"\n[STEP 4] BST RANKING - Building tree and extracting top {top_k}")
        print("-" * 70)
        ranking_tree = BSTRankingTree()
        
        for crew in reachable_crew:
            composite_score = self.calculate_composite_score(crew.data)
            ranking_tree.insert(crew, composite_score)
        
        # STEP 5: Extract top K performers (O(k + log n))
        print(f"\n[STEP 5] TOP-K EXTRACTION")
        print("-" * 70)
        top_recommendations = ranking_tree.get_top_k(top_k)
        
        # Format recommendations
        recommendations = []
        for idx, (crew, score) in enumerate(top_recommendations, 1):
            rec = {
                'rank': idx,
                'emp_id': crew.emp_id,
                'name': crew.name,
                'designation': crew.designation,
                'baseLocation': crew.base_location,
                'compositeScore': score,
                'parameters': {k: crew.data.get(k, 0) for k in self.WEIGHTS.keys()},
                'weights': self.WEIGHTS,
                'keyStrengths': [
                    k.replace('Score', '').replace(/([A-Z])/g, ' $1').strip() 
                    for k, v in crew.data.items() 
                    if k.endswith('Score') and v > 85
                ]
            }
            recommendations.append(rec)
            print(f"   #{idx} {crew.name} - Score: {score:.2f}")
        
        print("\n" + "="*70)
        print(f"✓ RECOMMENDATION COMPLETE - {len(recommendations)} candidates ranked")
        print("="*70 + "\n")
        
        return recommendations
    
    def demonstrate_heap_operation(self):
        """Demonstrate min-heap fatigue extraction"""
        print("\n" + "="*70)
        print("DEMONSTRATING MIN-HEAP - Get Least Fatigued Crew")
        print("="*70)
        print(f"\nHeap size: {self.fatigue_heap.size()}")
        print("Extracting top 3 least fatigued crew members:\n")
        
        for i in range(min(3, self.fatigue_heap.size())):
            crew = self.fatigue_heap.get_least_fatigued()
            if crew:
                print(f"   Position {i+1}: {crew.name}")
        
        print("\n" + "="*70 + "\n")
