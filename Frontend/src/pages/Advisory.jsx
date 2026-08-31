import {
  useEffect,
  useState
} from "react";

import {
  getAdvisory,
  getProfile
} from "../services/api";

function Advisory() {

  const [mode, setMode] = useState("new");

  // Initial state set to empty values
  const [formData, setFormData] = useState({
    district: "",
    N: "",
    P: "",
    K: "",
    ph: ""
  });
    
  const [profileLoaded, setProfileLoaded] = useState(false);

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const districts = [
  "Athurugiriya",
  "Badulla",
  "Bentota",
  "Colombo",
  "Galle",
  "Gampaha",
  "Hambantota",
  "Hatton",
  "Jaffna",
  "Kalmunai",
  "Kalutara",
  "Kandy",
  "Kesbewa",
  "Kolonnawa",
  "Kurunegala",
  "Mabole",
  "Maharagama",
  "Mannar",
  "Matale",
  "Matara",
  "Moratuwa",
  "Mount Lavinia",
  "Negombo",
  "Oruwala",
  "Pothuhera",
  "Puttalam",
  "Ratnapura",
  "Sri Jayewardenepura Kotte",
  "Trincomalee",
  "Weligama"
  ];

  async function loadProfileData() {
    try {
      const profile = await getProfile();

      setFormData({
        district: profile.district || "Kandy",
        N: profile.nitrogen ?? 80,
        P: profile.phosphorus ?? 40,
        K: profile.potassium ?? 50,
        ph: profile.soil_ph ?? 6.2
      });

      setProfileLoaded(true);
    } catch (error) {
      console.error(
        "Could not load profile data:",
        error
      );
    }
  }

  useEffect(() => {
    if (mode === "existing") {
      loadProfileData();
    }
  }, [mode]);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const requestData = {
        mode: mode,
        district: formData.district,
        N: Number(formData.N),
        P: Number(formData.P),
        K: Number(formData.K),
        ph: Number(formData.ph)
      };

      const data = await getAdvisory(requestData);
      setResult(data);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // Updated changeMode function
  function changeMode(newMode) {
    setMode(newMode);
    setResult(null);
    setError("");
    setProfileLoaded(false);

    if (newMode === "new") {
      setFormData({
        district: "",
        N: "",
        P: "",
        K: "",
        ph: ""
      });
    }
  }

  return (
    <div className="page">

      <span className="page-badge">
        AI Cultivation Support
      </span>

      <h1>
        Smart Mango Advisory
      </h1>

      <p className="page-description">
        Select your cultivation situation and provide
        basic soil information. MangoCare automatically
        analyses historical climate information and,
        for existing plants, current weather conditions.
      </p>

      <div className="advisory-tabs">
        <button
          className={
            mode === "new"
              ? "advisory-tab active"
              : "advisory-tab"
          }
          onClick={() => changeMode("new")}
        >
           New Cultivation
        </button>

        <button
          className={
            mode === "existing"
              ? "advisory-tab active"
              : "advisory-tab"
          }
          onClick={() => changeMode("existing")}
        >
           Existing Plants
        </button>
      </div>

      <div className="advisory-layout">

        <form
          className="advisory-form"
          onSubmit={handleSubmit}
        >
          <h3>
            {
              mode === "new"
                ? "New Cultivation Analysis"
                : "Existing Plant Analysis"
            }
          </h3>

          {mode === "existing" && profileLoaded && (
            <div className="profile-data-notice">
              Saved cultivation information from your
              profile has been loaded automatically.
              You can change any value before analysis.
            </div>
          )}

          <div className="form-group">
            <label>Location</label>
            {/* Updated select with empty default option */}
            <select
              name="district"
              value={formData.district}
              onChange={handleChange}
              required
            >
              <option value="">
                Select District
              </option>

              {districts.map((district) => (
                <option key={district} value={district}>
                  {district}
                </option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Nitrogen (N)</label>
              <input
                type="number"
                name="N"
                value={formData.N}
                onChange={handleChange}
                min="0"
                max="200"
                step="1"
                required
              />
            </div>

            <div className="form-group">
              <label>Phosphorus (P)</label>
              <input
                type="number"
                name="P"
                value={formData.P}
                onChange={handleChange}
                min="0"
                max="200"
                step="1"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Potassium (K)</label>
              <input
                type="number"
                name="K"
                value={formData.K}
                onChange={handleChange}
                min="0"
                max="200"
                step="1"
                required
              />
            </div>

            <div className="form-group">
              <label>Soil pH</label>
              <input
                type="number"
                step="0.1"
                name="ph"
                value={formData.ph}
                onChange={handleChange}
                min="3.5"
                max="9"
                required
              />
            </div>
          </div>

          <button
            className="primary-button full-button"
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Analysing Conditions..."
              : "Generate Advisory"}
          </button>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </form>

        <div className="advisory-results">
          {!result ? (
            <div className="result-empty">
              <h3>Advisory Results</h3>
              <p>
                Complete the form to receive
                AI-supported cultivation advice.
              </p>
            </div>
          ) : (
            <AdvisoryResults
              result={result}
              mode={mode}
            />
          )}
        </div>

      </div>

    </div>
  );
}

function AdvisoryResults({ result, mode }) {
  const prediction = result.prediction;

  return (
    <div>
      <div className="results-heading">
        <div>
          <span className="result-label">
            Analysis for
          </span>
          <h2>{result.district}</h2>
        </div>

        <span className="mode-badge">
          {mode === "new" ? "New Cultivation" : "Existing Plants"}
        </span>
      </div>

      <div className="metric-grid">
        <MetricCard title="Suitability" value={prediction.suitability} />
        <MetricCard title="Irrigation" value={prediction.irrigation_need} />
        <MetricCard title="Drought Risk" value={prediction.drought_risk} />
        <MetricCard title="Nutrient Condition" value={prediction.nutrient_condition} />
      </div>

      {mode === "existing" && result.current_weather && (
        <div className="weather-result-card">
          <h3>Current Weather</h3>
          <div className="weather-metrics">
            <div>
              <strong>{result.current_weather.temperature_c}°C</strong>
              <span>Temperature</span>
            </div>
            <div>
              <strong>{result.current_weather.humidity}%</strong>
              <span>Humidity</span>
            </div>
            <div>
              <strong>{result.current_weather.rainfall_1h_mm} mm</strong>
              <span>Current Rain</span>
            </div>
            <div>
              <strong>{result.current_weather.description}</strong>
              <span>Condition</span>
            </div>
          </div>
        </div>
      )}

      <RecommendationSection result={result} mode={mode} />
    </div>
  );
}

function MetricCard({ title, value }) {
  return (
    <div className="metric-card">
      <span>{title}</span>
      <strong>{value}</strong>
    </div>
  );
}

function RecommendationSection({ result, mode }) {
  const recommendations = result.advisory?.recommendations || [];

  return (
    <>
      <div className="recommendation-card">
        <h3>Farmer Recommendations</h3>
        {recommendations.length > 0 ? (
          <ul>
            {recommendations.map((recommendation, index) => (
              <li key={index}>{recommendation}</li>
            ))}
          </ul>
        ) : (
          <p>No additional recommendations.</p>
        )}
      </div>

      {mode === "existing" && result.live_weather_advisory && (
        <div className="live-advisory-card">
          <h3>Live Weather Advice</h3>
          <AdviceItem
            title="Irrigation"
            data={result.live_weather_advisory.irrigation}
          />
          <AdviceItem
            title="Environmental Disease Risk"
            data={result.live_weather_advisory.disease_environment}
          />
          <AdviceItem
            title="Heat Stress"
            data={result.live_weather_advisory.heat_stress}
          />
        </div>
      )}
    </>
  );
}

function AdviceItem({ title, data }) {
  if (!data) return null;

  return (
    <div className="advice-item">
      <div className="advice-heading">
        <strong>{title}</strong>
        <span>{data.level}</span>
      </div>
      <p>{data.message}</p>
      <small>{data.action}</small>
    </div>
  );
}

export default Advisory;