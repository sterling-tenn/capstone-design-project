import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Homepage from './Homepage/Homepage';
import UploadComponent from './Upload/Upload';

function App() {
  return (
    <div className="App">
      <Router>
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/upload" element={<UploadComponent />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;
