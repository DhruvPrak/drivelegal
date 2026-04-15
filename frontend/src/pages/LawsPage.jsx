// src/pages/LawsPage.jsx
// Displays all traffic laws fetched from the backend
// Has search and category filter functionality

import { useState, useEffect } from "react";
import { lawsAPI } from "../utils/api";

export default function LawsPage() {
  // State variables — React re-renders when these change
  const [laws, setLaws] = useState([]);           // list of laws
  const [categories, setCategories] = useState([]); // list of categories
  const [loading, setLoading] = useState(true);   // loading state
  const [error, setError] = useState(null);       // error state
  const [search, setSearch] = useState("");       // search input
  const [selectedCategory, setSelectedCategory] = useState(""); // filter

  // useEffect runs when component loads
  // Fetches categories from API once
  useEffect(() => {
    fetchCategories();
  }, []);

  // useEffect runs when search or category changes
  // Fetches filtered laws
  useEffect(() => {
    fetchLaws();
  }, [search, selectedCategory]);

  const fetchCategories = async () => {
    try {
      const data = await lawsAPI.getCategories();
      setCategories(data.data);
    } catch (err) {
      console.error("Failed to fetch categories:", err);
    }
  };

  const fetchLaws = async () => {
    try {
      setLoading(true);
      setError(null);

      // Build filters object
      const filters = {};
      if (search) filters.search = search;
      if (selectedCategory) filters.category = selectedCategory;

      const data = await lawsAPI.getAll(filters);
      setLaws(data.data);
    } catch (err) {
      setError("Failed to load laws. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  // Category color mapping for visual distinction
  const categoryColors = {
    "Speed": "bg-red-100 text-red-700",
    "Safety": "bg-yellow-100 text-yellow-700",
    "Documents": "bg-blue-100 text-blue-700",
    "Drunk Driving": "bg-purple-100 text-purple-700",
    "Dangerous Driving": "bg-orange-100 text-orange-700",
    "Overloading": "bg-green-100 text-green-700",
    "General": "bg-gray-100 text-gray-700",
  };

  return (
    <div className="max-w-4xl mx-auto p-4">

      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          ⚖️ Traffic Laws
        </h1>
        <p className="text-gray-500 mt-1">
          Motor Vehicles Act 1988 — All Sections
        </p>
      </div>

      {/* Search Bar */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search laws by title, section or keyword..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full border border-gray-300 rounded-xl px-4 py-3
                     focus:outline-none focus:ring-2 focus:ring-blue-500
                     text-gray-700"
        />
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedCategory("")}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors
            ${selectedCategory === ""
              ? "bg-blue-700 text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
        >
          All
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors
              ${selectedCategory === cat
                ? "bg-blue-700 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="text-4xl mb-3">⏳</div>
          <p className="text-gray-500">Loading laws...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-4">
          <p className="text-red-600">❌ {error}</p>
          <p className="text-red-400 text-sm mt-1">
            Make sure the backend is running on port 8000
          </p>
        </div>
      )}

      {/* Laws Count */}
      {!loading && !error && (
        <p className="text-gray-400 text-sm mb-4">
          Showing {laws.length} laws
          {selectedCategory && ` in ${selectedCategory}`}
          {search && ` matching "${search}"`}
        </p>
      )}

      {/* Laws List */}
      <div className="space-y-4">
        {laws.map((law) => (
          <div
            key={law.id}
            className="bg-white rounded-xl shadow-sm border border-gray-100
                       p-5 hover:shadow-md transition-shadow"
          >
            {/* Law Header */}
            <div className="flex items-start justify-between mb-2">
              <div>
                <span className="text-blue-700 font-bold text-sm">
                  {law.section}
                </span>
                <h3 className="font-bold text-gray-800 mt-0.5">
                  {law.title}
                </h3>
              </div>
              {law.category && (
                <span className={`text-xs px-2 py-1 rounded-full font-medium
                  ${categoryColors[law.category] || "bg-gray-100 text-gray-600"}`}>
                  {law.category}
                </span>
              )}
            </div>

            {/* Plain Language */}
            {law.plain_language && (
              <div className="bg-blue-50 rounded-lg p-3 mb-3">
                <p className="text-blue-800 text-sm">
                  💡 <strong>In simple words:</strong> {law.plain_language}
                </p>
              </div>
            )}

            {/* Full Legal Text */}
            <p className="text-gray-500 text-sm leading-relaxed">
              {law.description}
            </p>

            {/* National Badge */}
            {law.is_national && (
              <div className="mt-3">
                <span className="text-xs bg-green-50 text-green-700
                                 px-2 py-1 rounded-full">
                  🇮🇳 National Law
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Empty State */}
      {!loading && !error && laws.length === 0 && (
        <div className="text-center py-12">
          <div className="text-4xl mb-3">🔍</div>
          <p className="text-gray-500">No laws found matching your search</p>
        </div>
      )}

    </div>
  );
}