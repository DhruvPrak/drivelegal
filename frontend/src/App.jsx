function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-700 text-white p-4 shadow-md">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <span className="text-3xl">🚦</span>
          <div>
            <h1 className="text-2xl font-bold">DriveLegal</h1>
            <p className="text-blue-200 text-sm">
              AI-powered Indian Traffic Law Platform
            </p>
          </div>
        </div>
      </header>
      <main className="max-w-4xl mx-auto p-6">
        <div className="bg-white rounded-2xl shadow p-8 mt-6 text-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-3">
            Know Your Traffic Laws
          </h2>
          <p className="text-gray-500 mb-6">
            Get instant, location-aware traffic law information,
            challan amounts, and your legal rights in plain English.
          </p>
          <button className="bg-blue-700 text-white px-8 py-3 rounded-xl text-lg font-semibold hover:bg-blue-800 transition-colors">
            Detect My Location
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="bg-white rounded-xl shadow p-5 text-center">
            <div className="text-4xl mb-3">⚖️</div>
            <h3 className="font-bold text-gray-800 mb-1">Traffic Laws</h3>
            <p className="text-gray-500 text-sm">
              Laws specific to your state and city
            </p>
          </div>
          <div className="bg-white rounded-xl shadow p-5 text-center">
            <div className="text-4xl mb-3">💰</div>
            <h3 className="font-bold text-gray-800 mb-1">Challan Calculator</h3>
            <p className="text-gray-500 text-sm">
              Exact fine amounts for any violation
            </p>
          </div>
          <div className="bg-white rounded-xl shadow p-5 text-center">
            <div className="text-4xl mb-3">🛡️</div>
            <h3 className="font-bold text-gray-800 mb-1">Know Your Rights</h3>
            <p className="text-gray-500 text-sm">
              What to do when stopped by police
            </p>
          </div>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mt-6 text-center text-blue-700 font-medium">
          AI Chat Assistant - Hindi and Tamil Support - Works Offline - Coming Soon!
        </div>
      </main>
      <footer className="text-center text-gray-400 text-sm p-6 mt-8">
        Built for IITM Road Safety Hackathon 2026
      </footer>
    </div>
  )
}

export default App