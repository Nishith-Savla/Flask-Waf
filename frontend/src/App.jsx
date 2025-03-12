import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import WAFDashboard from "./WAFDashboard";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/waf-dashboard" element={<WAFDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
