from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from recommendation_engine import CrewRecommendationEngine

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# ============================================
# LOAD DATA
# ============================================

print("\n" + "="*70)
print(" "*15 + "CrewSync Backend Server")
print(" "*10 + "Data Structures-Driven Crew Scheduling")
print("="*70)
print("\nLoading data files...")

with open('data/crew_data.json', 'r', encoding='utf-8') as f:
    CREW_DATA = json.load(f)
    print(f"✓ Loaded {len(CREW_DATA)} crew members")

with open('data/flights_data.json', 'r', encoding='utf-8') as f:
    FLIGHTS_DATA = json.load(f)
    print(f"✓ Loaded {len(FLIGHTS_DATA)} flights")

# Initialize recommendation engine
print("\nInitializing recommendation engine...")
engine = CrewRecommendationEngine(CREW_DATA)

print("\n" + "="*70)
print("Data Structures Implementation:")
print("="*70)
print("1. Hash Map      - O(1) certification filtering")
print("2. Min-Heap      - O(log n) fatigue-based selection")
print("3. BST           - O(k + log n) top-K performer extraction")
print("4. Graph         - O(1) connection feasibility check")
print("5. Queue         - O(1) backup crew management (FIFO)")
print("="*70)

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/crew', methods=['GET'])
def get_crew():
    """Get all crew members"""
    return jsonify(CREW_DATA)

@app.route('/api/crew/<emp_id>', methods=['GET'])
def get_crew_by_id(emp_id):
    """Get specific crew member details"""
    # Try to find by string first, then try as integer
    crew = next((c for c in CREW_DATA if str(c['emp_id']) == str(emp_id)), None)
    if not crew:
        return jsonify({'error': 'Crew member not found'}), 404
    return jsonify(crew)


@app.route('/api/flights', methods=['GET'])
def get_flights():
    """Get all flights"""
    return jsonify(FLIGHTS_DATA)

@app.route('/api/flights/<flight_number>', methods=['GET'])
def get_flight_by_number(flight_number):
    """Get specific flight details"""
    flight = next((f for f in FLIGHTS_DATA if f['flightNumber'] == flight_number), None)
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    return jsonify(flight)

@app.route('/api/recommendations/<flight_number>', methods=['GET'])
def get_recommendations(flight_number):
    """
    Get crew recommendations for a specific flight
    This endpoint triggers the full data structure pipeline
    """
    flight = next((f for f in FLIGHTS_DATA if f['flightNumber'] == flight_number), None)
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    
    # Run recommendation engine (will print DS operations to terminal)
    recommendations = engine.get_recommendations(flight, top_k=5)
    return jsonify(recommendations)

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    # Use .get() to handle missing 'availability' key
    available_crew = sum(1 for c in CREW_DATA if c.get('availability', 'Available') == 'Available')
    needs_assignment = sum(1 for f in FLIGHTS_DATA if f.get('status', '') == 'Crew Needed')
    
    # Calculate average performance
    total_performance = sum(c.get('performanceScore', 0) for c in CREW_DATA)
    avg_performance = round(total_performance / len(CREW_DATA), 1) if CREW_DATA else 0
    
    return jsonify({
        'totalFlights': len(FLIGHTS_DATA),
        'availableCrew': available_crew,
        'needsAssignment': needs_assignment,
        'avgPerformance': avg_performance
    })

@app.route('/api/demo/heap', methods=['GET'])
def demo_heap():
    """Demonstrate heap operations"""
    engine.demonstrate_heap_operation()
    return jsonify({'message': 'Check terminal for heap demonstration'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'crew_count': len(CREW_DATA),
        'flights_count': len(FLIGHTS_DATA)
    })

# ============================================
# RUN SERVER
# ============================================

if __name__ == '__main__':
    import os
    
    print("\n" + "="*70)
    print("Flask server starting...")
    print("="*70)
    print("\nAvailable endpoints:")
    print("  GET  /api/crew")
    print("  GET  /api/crew/<emp_id>")
    print("  GET  /api/flights")
    print("  GET  /api/flights/<flight_number>")
    print("  GET  /api/recommendations/<flight_number>")
    print("  GET  /api/dashboard/stats")
    print("  GET  /api/demo/heap")
    print("  GET  /api/health")
    print("\nPress CTRL+C to stop the server")
    print("="*70 + "\n")
    
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    
    # Use 0.0.0.0 to make server accessible externally
    app.run(host='0.0.0.0', port=port, debug=False)
