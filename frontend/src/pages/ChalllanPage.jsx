// src/pages/ChalllanPage.jsx
// Interactive challan calculator
// User selects violation, state, vehicle type → gets exact fine

import { useState } from "react";
import { finesAPI } from "../utils/api";

const STATES = [
  { code: "DL", name: "Delhi" },
  { code: "MH", name: "Maharashtra" },
  { code: "KA", name: "Karnataka" },
  { code: "TN", name: "Tamil Nadu" },
  { code: "UP", name: "Uttar Pradesh" },
];

const VIOLATIONS = [
  { section: "Section 185", title: "Drunk Driving / DUI" },
  { section: "Section 194C", title: "No Helmet" },
  { section: "Section 194B", title: "No Seat Belt" },
  { section: "Section 181", title: "Driving Without Licence" },
  { section: "Section 196", title: "Driving Without Insurance" },
  { section: "Section 183", title: "Over Speeding" },
  { section: "Section 184", title: "Dangerous Driving" },
  { section: "Section 177", title: "General Traffic Violation" },
  { section: "Section 194", title: "Vehicle Overloading" },
  { section: "Section 189", title: "Street Racing" },
];

const VEHICLE_TYPES = [
  { value: "two_wheeler", label: "Two Wheeler (Bike/Scooter)" },
  { value: "four_wheeler", label: "Four Wheeler (Car/SUV)" },
  { value: "three_wheeler", label: "Three Wheeler (Auto)" },
  { value: "commercial", label: "Commercial Vehicle" },
  { value: "heavy_vehicle", label: "Heavy Vehicle (Truck/Bus)" },
  { value: "all_vehicles", label: "All Vehicles" },
];

export default function ChallanPage() {
  const [section, setSection] = useState("");
  const [stateCode, setStateCode] = useState("");
  const [vehicleType, setVehicleType] = useState("all_vehicles");
  const [isRepeat, setIsRepeat] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const calculateChallan = async () => {
    if (!section || !stateCode) {
      setError("Please select a violation and state");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const data = await finesAPI.calculate(
        section, stateCode, vehicleType, isRepeat
      );
      setResult(data.data);
    } catch (err) {
      setError("Could not calculate fine. Try a different combination.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          💰 Challan Calculator
        </h1>
        <p className="text-gray-500 mt-1">
          Calculate exact fine amounts for any traffic violation
        </p>
      </div>

      {/* Calculator Form */}
      <div className="bg-white rounded-2xl shadow p-6 space-y-4">

        {/* Violation Selector */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Violation
          </label>
          <select
            value={section}
            onChange={(e) => setSection(e.target.value)}
            className="w-full border border-gray-300 rounded-xl px-4 py-3
                       focus:outline-none focus:ring-2 focus:ring-blue-500
                       text-gray-700"
          >
            <option value="">-- Choose a violation --</option>
            {VIOLATIONS.map((v) => (
              <option key={v.section} value={v.section}>
                {v.section} — {v.title}
              </option>
            ))}
          </select>
        </div>

        {/* State Selector */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select State
          </label>
          <select
            value={stateCode}
            onChange={(e) => setStateCode(e.target.value)}
            className="w-full border border-gray-300 rounded-xl px-4 py-3
                       focus:outline-none focus:ring-2 focus:ring-blue-500
                       text-gray-700"
          >
            <option value="">-- Choose a state --</option>
            {STATES.map((s) => (
              <option key={s.code} value={s.code}>
                {s.name}
              </option>
            ))}
          </select>
        </div>

        {/* Vehicle Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Vehicle Type
          </label>
          <select
            value={vehicleType}
            onChange={(e) => setVehicleType(e.target.value)}
            className="w-full border border-gray-300 rounded-xl px-4 py-3
                       focus:outline-none focus:ring-2 focus:ring-blue-500
                       text-gray-700"
          >
            {VEHICLE_TYPES.map((v) => (
              <option key={v.value} value={v.value}>
                {v.label}
              </option>
            ))}
          </select>
        </div>

        {/* Repeat Offence Toggle */}
        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            id="repeat"
            checked={isRepeat}
            onChange={(e) => setIsRepeat(e.target.checked)}
            className="w-4 h-4 text-blue-700"
          />
          <label htmlFor="repeat" className="text-gray-700 text-sm">
            This is a repeat offence (higher fine applies)
          </label>
        </div>

        {/* Error */}
        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}

        {/* Calculate Button */}
        <button
          onClick={calculateChallan}
          disabled={loading}
          className="w-full bg-blue-700 text-white py-3 rounded-xl
                     font-semibold hover:bg-blue-800 transition-colors
                     disabled:opacity-50"
        >
          {loading ? "Calculating..." : "Calculate Fine Amount"}
        </button>
      </div>

      {/* Result Card */}
      {result && (
        <div className="mt-6 bg-white rounded-2xl shadow overflow-hidden">

          {/* Result Header */}
          <div className="bg-blue-700 text-white p-4">
            <p className="text-blue-200 text-sm">{result.law_section}</p>
            <h2 className="text-xl font-bold">{result.law_title}</h2>
            <p className="text-blue-200 text-sm mt-1">
              {result.state_name} • {result.vehicle_type.replace("_", " ")}
            </p>
          </div>

          {/* Fine Amount */}
          <div className="p-6 text-center border-b border-gray-100">
            <p className="text-gray-500 text-sm mb-1">
              {result.is_repeat_offence ? "Repeat Offence Fine" : "First Offence Fine"}
            </p>
            <p className="text-4xl font-bold text-blue-700">
              ₹{result.fine_amount.toLocaleString("en-IN")}
            </p>
          </div>

          {/* Details */}
          <div className="p-4 space-y-3">

            {/* First vs Repeat */}
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">First Offence</span>
              <span className="font-medium text-gray-800">
                ₹{result.first_offence_amount.toLocaleString("en-IN")}
              </span>
            </div>
            {result.repeat_offence_amount && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Repeat Offence</span>
                <span className="font-medium text-red-600">
                  ₹{result.repeat_offence_amount.toLocaleString("en-IN")}
                </span>
              </div>
            )}

            {/* Legal Reference */}
            {result.mv_act_reference && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Legal Reference</span>
                <span className="font-medium text-gray-800">
                  {result.mv_act_reference}
                </span>
              </div>
            )}

            {/* Plain Language */}
            {result.plain_language && (
              <div className="bg-blue-50 rounded-lg p-3 mt-2">
                <p className="text-blue-800 text-sm">
                  💡 {result.plain_language}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}