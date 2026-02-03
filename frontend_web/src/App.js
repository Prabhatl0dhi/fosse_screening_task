import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title,
} from "chart.js";
import { useState } from "react";
import { Bar } from "react-chartjs-2";
import "./App.css"; // Make sure to create this file (see Step 2)

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title
);

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    setError(null);
    setResult(null);

    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Simulate network delay for better UX feel or remove in prod
      // await new Promise(r => setTimeout(r, 800)); 

      const response = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Server responded with an error");
      }

      const text = await response.text();
      try {
        const data = JSON.parse(text);
        setResult(data);
      } catch {
        setResult({ message: "Upload successful", raw: text });
      }
    } catch (err) {
      setError(err.message || "Connection failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    window.open("http://127.0.0.1:8000/api/report/", "_blank");
  };


  // CHART CONFIGURATION
  const getEquipmentChartData = () => {
    if (!result || !result.equipment_type_distribution) return null;

    const labels = Object.keys(result.equipment_type_distribution);
    const values = Object.values(result.equipment_type_distribution);

    return {
      labels,
      datasets: [
        {
          label: "Equipment Count",
          data: values,
          backgroundColor: "#2E8B57", // Modern Indigo
          hoverBackgroundColor: "#047a37",
          borderRadius: 6, // Rounded bars
          barThickness: 40,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: "Equipment Distribution",
        font: { size: 16, weight: '600' },
        padding: { bottom: 20 }
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: { color: "#f3f4f6" }, // Subtle grid
        ticks: { font: { family: "sans-serif" } },
        border: { display: false }
      },
      x: {
        grid: { display: false },
        ticks: { font: { family: "sans-serif" } },
        border: { display: false }
      },
    },
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Analytics Dashboard</h1>
        <p>Upload your CSV data to visualize equipment stats.</p>
      </header>

      <main className="main-content">
        {/* Upload Card */}
        <div className="card upload-card">
          <div className="file-drop-area">
            <span className="file-msg">
              {file ? `Selected: ${file.name}` : "Drag & drop CSV here or click to upload"}
            </span>
            <input
              className="file-input"
              type="file"
              accept=".csv"
              onChange={handleFileChange}
            />
          </div>

          <button
            className={`btn-primary ${loading ? 'loading' : ''}`}
            onClick={handleUpload}
            disabled={loading || !file}
          >
            {loading ? "Processing..." : "Analyze Data"}
          </button>

          {error && <div className="alert error">{error}</div>}
        </div>

        {/* Results Section */}
        {result && (
          <div className="results-grid">
            {/* Chart Card */}
            {result.equipment_type_distribution && (
              <div className="card chart-card">
                <div style={{ height: "300px", width: "100%" }}>
                  <Bar data={getEquipmentChartData()} options={chartOptions} />
                </div>
              </div>
            )}

            {/* Summary Data Card */}
            <div className="card summary-card">
              <h3>Data Summary</h3>
              <div className="json-viewer">
                {Object.entries(result).map(([key, value]) => {
                  if (typeof value === 'object') return null; // Skip nested objects for this view
                  return (
                    <div key={key} className="stat-row">
                      <span className="stat-key">{key.replace(/_/g, ' ')}</span>
                      <span className="stat-value">{value}</span>
                    </div>
                  )
                })}
                {/* Fallback if it's just raw text */}
                {!result.equipment_type_distribution && <pre>{JSON.stringify(result, null, 2)}</pre>}
              </div>
              <div >
                <h3>Report</h3>
                <button
                  className="btn-primary"
                  onClick={handleDownloadPDF}
                >
                  Download PDF Report
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;