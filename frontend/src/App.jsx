// src/App.jsx
// Main app with bottom navigation between pages

import { useState } from "react";
import LawsPage from "./pages/LawsPage";
import ChallanPage from "./pages/ChalllanPage";

export default function App() {
  const [currentPage, setCurrentPage] = useState("home");

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <header className="bg-blue-700 text-white p-4 shadow-md sticky top-0 z-10">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <span className="text-2xl">🚦</span>
          <div>
            <h1 className="text-xl font-bold">DriveLegal</h1>
            <p className="text-blue-200 text-xs">
              AI-powered Indian Traffic Law Platform
            </p>
          </div>
        </div>
      </header>

      {/* Page Content */}
      <main className="pb-20 pt-4">
        {currentPage === "home" && <HomePage setCurrentPage={setCurrentPage} />}
        {currentPage === "laws" && <LawsPage />}
        {currentPage === "challan" && <ChallanPage />}
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t
                      border-gray-200 shadow-lg z-10">
        <div className="max-w-4xl mx-auto flex">

          <button
            onClick={() => setCurrentPage("home")}
            className={`flex-1 py-3 flex flex-col items-center gap-1
              ${currentPage === "home" ? "text-blue-700" : "text-gray-400"}`}
          >
            <span className="text-xl">🏠</span>
            <span className="text-xs font-medium">Home</span>
          </button>

          <button
            onClick={() => setCurrentPage("laws")}
            className={`flex-1 py-3 flex flex-col items-center gap-1
              ${currentPage === "laws" ? "text-blue-700" : "text-gray-400"}`}
          >
            <span className="text-xl">⚖️</span>
            <span className="text-xs font-medium">Laws</span>
          </button>

          <button
            onClick={() => setCurrentPage("challan")}
            className={`flex-1 py-3 flex flex-col items-center gap-1
              ${currentPage === "challan" ? "text-blue-700" : "text-gray-400"}`}
          >
            <span className="text-xl">💰</span>
            <span className="text-xs font-medium">Challan</span>
          </button>

          <button
            onClick={() => setCurrentPage("rto")}
            className={`flex-1 py-3 flex flex-col items-center gap-1
              ${currentPage === "rto" ? "text-blue-700" : "text-gray-400"}`}
          >
            <span className="text-xl">🏢</span>
            <span className="text-xs font-medium">RTO</span>
          </button>

        </div>
      </nav>

    </div>
  );
}

// Home Page Component
function HomePage({ setCurrentPage }) {
  return (
    <div className="max-w-4xl mx-auto p-4">

      {/* Hero */}
      <div className="bg-white rounded-2xl shadow p-6 mt-2 text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Know Your Traffic Laws
        </h2>
        <p className="text-gray-500 text-sm mb-4">
          Instant traffic law information, challan amounts,
          and your legal rights — powered by AI.
        </p>
        <button
          onClick={() => setCurrentPage("laws")}
          className="bg-blue-700 text-white px-6 py-3 rounded-xl
                     font-semibold hover:bg-blue-800 transition-colors"
        >
          Browse Traffic Laws
        </button>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 gap-4 mt-4">

        <button
          onClick={() => setCurrentPage("laws")}
          className="bg-white rounded-xl shadow p-4 text-left
                     hover:shadow-md transition-shadow"
        >
          <div className="flex items-center gap-4">
            <span className="text-3xl">⚖️</span>
            <div>
              <h3 className="font-bold text-gray-800">Traffic Laws</h3>
              <p className="text-gray-500 text-sm">
                20 MV Act sections with plain English explanations
              </p>
            </div>
            <span className="ml-auto text-gray-400">›</span>
          </div>
        </button>

        <button
          onClick={() => setCurrentPage("challan")}
          className="bg-white rounded-xl shadow p-4 text-left
                     hover:shadow-md transition-shadow"
        >
          <div className="flex items-center gap-4">
            <span className="text-3xl">💰</span>
            <div>
              <h3 className="font-bold text-gray-800">Challan Calculator</h3>
              <p className="text-gray-500 text-sm">
                Exact fine amounts for 5 states, all vehicle types
              </p>
            </div>
            <span className="ml-auto text-gray-400">›</span>
          </div>
        </button>

        <div className="bg-white rounded-xl shadow p-4 opacity-60">
          <div className="flex items-center gap-4">
            <span className="text-3xl">🛡️</span>
            <div>
              <h3 className="font-bold text-gray-800">Know Your Rights</h3>
              <p className="text-gray-500 text-sm">Coming soon...</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-4 opacity-60">
          <div className="flex items-center gap-4">
            <span className="text-3xl">🤖</span>
            <div>
              <h3 className="font-bold text-gray-800">AI Chat Assistant</h3>
              <p className="text-gray-500 text-sm">Coming soon...</p>
            </div>
          </div>
        </div>

      </div>

      {/* Footer */}
      <p className="text-center text-gray-400 text-xs mt-6 pb-4">
        Built for IITM Road Safety Hackathon 2026 🏆
      </p>

    </div>
  );
}