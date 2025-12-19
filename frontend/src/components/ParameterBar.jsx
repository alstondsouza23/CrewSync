export default function ParameterBar({ name, value, weight }) {
  const getColor = (val) => {
    if (val >= 85) return 'bg-green-500';
    if (val >= 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-700">{name}</span>
        <div className="flex items-center gap-2">
          <span className="text-gray-500">({Math.round(weight * 100)}%)</span>
          <span className="font-bold text-gray-900">{value.toFixed(1)}</span>
        </div>
      </div>
      <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full ${getColor(value)} transition-all duration-300`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}
