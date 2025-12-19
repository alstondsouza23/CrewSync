import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import CrewManagement from './pages/CrewManagement';
import Recommendations from './pages/Recommendations';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/crew" element={<CrewManagement />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
