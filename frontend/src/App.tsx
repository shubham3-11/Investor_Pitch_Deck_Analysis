import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import StartupList from './pages/StartupList';
import StartupDetail from './pages/StartupDetail';
import DeckAnalysis from './pages/DeckAnalysis';

function App() {
  return (
    <Router>
      <div className="app-header">
        <h1>Pitch Deck Analyst</h1>
      </div>
      <Routes>
        <Route path="/" element={<StartupList />} />
        <Route path="/startups/:id" element={<StartupDetail />} />
        <Route path="/decks/:deckId" element={<DeckAnalysis />} />
      </Routes>
    </Router>
  );
}

export default App;
