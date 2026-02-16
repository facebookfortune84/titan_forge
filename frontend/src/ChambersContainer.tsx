import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import ArsenalManager from './components/chambers/ArsenalManager';
import ArtifactStudio from './components/chambers/ArtifactStudio';
import NeuralLattice from './components/chambers/NeuralLattice';
import WarRoom from './components/chambers/WarRoom';

const ChambersContainer: React.FC = () => {
  const location = useLocation();

  return (
    <div className="chambers-container" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <nav style={{ padding: '10px 20px', backgroundColor: '#333', color: 'white' }}>
        <ul style={{ display: 'flex', listStyle: 'none', margin: 0, padding: 0 }}>
          <li style={{ marginRight: '20px' }}>
            <Link to="/chambers/arsenal" style={{ color: location.pathname === "/chambers/arsenal" ? '#00f2ff' : 'white', textDecoration: 'none' }}>
              Arsenal Manager
            </Link>
          </li>
          <li style={{ marginRight: '20px' }}>
            <Link to="/chambers/artifacts" style={{ color: location.pathname === "/chambers/artifacts" ? '#00f2ff' : 'white', textDecoration: 'none' }}>
              Artifact Studio
            </Link>
          </li>
          <li style={{ marginRight: '20px' }}>
            <Link to="/chambers/neural-lattice" style={{ color: location.pathname === "/chambers/neural-lattice" ? '#00f2ff' : 'white', textDecoration: 'none' }}>
              Neural Lattice
            </Link>
          </li>
          <li>
            <Link to="/chambers/war-room" style={{ color: location.pathname === "/chambers/war-room" ? '#00f2ff' : 'white', textDecoration: 'none' }}>
              War Room
            </Link>
          </li>
        </ul>
      </nav>
      <div style={{ flexGrow: 1, padding: '20px', overflow: 'auto' }}>
        <Routes>
          <Route path="arsenal" element={<ArsenalManager />} />
          <Route path="artifacts" element={<ArtifactStudio />} />
          <Route path="neural-lattice" element={<NeuralLattice />} />
          <Route path="war-room" element={<WarRoom logs={[]} activeDept="" activeAgent="" isProcessing={false} onSend={() => {}} unlockAudio={() => {}} audioUnlocked={false} />} />
          <Route path="/" element={<h2>Select a Chamber from the navigation above.</h2>} />
        </Routes>
      </div>
    </div>
  );
};

export default ChambersContainer;