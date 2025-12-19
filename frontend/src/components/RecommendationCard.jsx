import { MapPin, Star, Award } from 'lucide-react';
import ParameterBar from './ParameterBar';

export default function RecommendationCard({ recommendation, rank, onAssign }) {
  const { emp_id, name, designation, baseLocation, compositeScore, parameters, weights, keyStrengths } = recommendation;

  return (
    <div className="bg-white rounded-xl shadow-lg border-l-4 border-blue-500 p-6 hover:shadow-xl transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-blue-600 text-white flex items-center justify-center text-2xl font-bold">
            #{rank}
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900">{name}</h3>
            <p className="text-gray-600">{designation}</p>
            <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
              <span className="flex items-center gap-1">
                <MapPin className="w-4 h-4" />
                {baseLocation}
              </span>
              <span className="flex items-center gap-1">
                <Star className="w-4 h-4 text-yellow-500" />
                {(compositeScore / 20).toFixed(1)}/5
              </span>
            </div>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Composite Score</p>
          <div className="relative w-24 h-24">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="48"
                cy="48"
                r="40"
                stroke="#e5e7eb"
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="48"
                cy="48"
                r="40"
                stroke="#2563eb"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${(compositeScore / 100) * 251.2} 251.2`}
                className="transition-all duration-1000"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl font-bold text-blue-600">{compositeScore.toFixed(1)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="border-t pt-4 mb-4">
        <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
          <Award className="w-5 h-5 text-blue-600" />
          17 Parameter Breakdown
        </h4>
        <div className="grid grid-cols-3 gap-4">
          {Object.entries(parameters).map(([key, value]) => (
            <ParameterBar
              key={key}
              name={key.replace(/Score$/, '').replace(/([A-Z])/g, ' $1').trim()}
              value={value}
              weight={weights[key]}
            />
          ))}
        </div>
      </div>

      <div className="border-t pt-4 mb-4">
        <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
          ✓ Key Strengths (Score ≥ 85)
        </h4>
        <div className="flex flex-wrap gap-2">
          {keyStrengths.map((strength, idx) => (
            <span
              key={idx}
              className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium border border-green-200"
            >
              ✓ {strength}
            </span>
          ))}
        </div>
      </div>

      <button
        onClick={() => onAssign(recommendation)}
        className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
      >
        ✓ Assign to Flight
      </button>
    </div>
  );
}
