export default function FlightCard({ flight, onClick }) {
  const statusColors = {
    'Crew Needed': 'bg-red-500',
    'Partially Assigned': 'bg-yellow-500',
    'Fully Assigned': 'bg-green-500',
  };

  const priorityColors = {
    'High': 'bg-red-100 text-red-700',
    'Medium': 'bg-yellow-100 text-yellow-700',
    'Low': 'bg-gray-100 text-gray-700',
  };

  return (
    <tr className="border-b hover:bg-gray-50 cursor-pointer" onClick={onClick}>
      <td className="px-6 py-4 font-semibold text-blue-600">{flight.flightNumber}</td>
      <td className="px-6 py-4">{flight.route}</td>
      <td className="px-6 py-4">{flight.aircraft}</td>
      <td className="px-6 py-4">{flight.departure}</td>
      <td className="px-6 py-4">
        <span className={`px-3 py-1 rounded-full text-sm font-medium text-white ${statusColors[flight.status]}`}>
          {flight.status}
        </span>
      </td>
      <td className="px-6 py-4">
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${priorityColors[flight.priority]}`}>
          {flight.priority}
        </span>
      </td>
      <td className="px-6 py-4 text-center">
        <span className="font-semibold">{flight.crewAssigned}/{flight.crewRequired}</span>
      </td>
    </tr>
  );
}
