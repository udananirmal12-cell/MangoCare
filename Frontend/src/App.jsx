import {
  Routes,
  Route
} from "react-router-dom";

import Sidebar
  from "./components/Sidebar";

import Header
  from "./components/Header";

import ProtectedRoute
  from "./components/ProtectedRoute";


import Dashboard
  from "./pages/Dashboard";

import LeafDetection
  from "./pages/LeafDetection";

import FruitDetection
  from "./pages/FruitDetection";

import Advisory
  from "./pages/Advisory";

import History
  from "./pages/History";

import Profile
  from "./pages/Profile";

import Login
  from "./pages/Login";

import Register
  from "./pages/Register";


function AppLayout() {

  return (
    <div className="app-container">

      <Sidebar />

      <div className="main-area">

        <Header />

        <main className="page-content">

          <Routes>

            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/leaf"
              element={<LeafDetection />}
            />

            <Route
              path="/fruit"
              element={<FruitDetection />}
            />

            <Route
              path="/advisory"
              element={<Advisory />}
            />

            <Route
              path="/history"
              element={<History />}
            />

            <Route
              path="/profile"
              element={<Profile />}
            />

          </Routes>

        </main>

      </div>

    </div>
  );
}


function App() {

  return (
    <Routes>

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />


      <Route
        path="/*"
        element={
          <ProtectedRoute>

            <AppLayout />

          </ProtectedRoute>
        }
      />

    </Routes>
  );
}


export default App;