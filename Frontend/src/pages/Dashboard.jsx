import {
  useEffect,
  useState
} from "react";

import {
  Link
} from "react-router-dom";

import {
  getDashboardWeather,
  getHistory
} from "../services/api";

import {
  useAuth
} from "../context/AuthContext";


function Dashboard() {

  const {
    user
  } = useAuth();


  const [weather, setWeather] =
    useState(null);

  const [weatherError, setWeatherError] =
    useState("");

  const [recentHistory, setRecentHistory] =
    useState([]);


  useEffect(() => {

    loadDashboard();

  }, []);


  async function loadDashboard() {

    // ------------------------------------------
    // Load current weather
    // ------------------------------------------

    try {

      const weatherData =
        await getDashboardWeather();

      setWeather(
        weatherData.weather
      );

    } catch (error) {

      setWeatherError(
        error.message
      );

    }


    // ------------------------------------------
    // Load recent activity
    // ------------------------------------------

    try {

      const historyData =
        await getHistory();

      setRecentHistory(
        (
          historyData.history || []
        ).slice(0, 4)
      );

    } catch (error) {

      console.error(
        "Could not load recent activity:",
        error
      );

    }
  }


  return (
    <div>

      {/* ======================================
          WELCOME SECTION
      ====================================== */}

      <section className="welcome-section">

        <div>

          <span className="page-badge">
            MangoCare AI
          </span>

          <h1>
            Welcome, {
              user?.name || "Farmer"
            }
          </h1>

          <p>
            Monitor mango health,
            detect diseases and receive
            intelligent cultivation advice.
          </p>

        </div>

      </section>


      {/* ======================================
          AI SERVICES
      ====================================== */}

      <div className="section-heading">

        <div>

          <h2>
            AI Services
          </h2>

          <p>
            Select a MangoCare service to begin.
          </p>

        </div>

      </div>


      <section className="service-grid">

        <ServiceCard
          title="Leaf Disease Detection"
          text="Analyse mango leaves using the trained AI model."
          link="/leaf"
          button="Check Leaf"
        />


        <ServiceCard
          title="Fruit Condition Detection"
          text="Analyse mango fruits for diseases and healthy conditions."
          link="/fruit"
          button="Check Fruit"
        />


        <ServiceCard
          title="Smart Advisory"
          text="Receive AI-supported cultivation and environmental advice."
          link="/advisory"
          button="Get Advisory"
        />

      </section>


      {/* ======================================
          WEATHER + RECENT ACTIVITY
      ====================================== */}

      <section className="dashboard-bottom-grid">

        {/* ==================================
            CURRENT WEATHER
        ================================== */}

        <div className="info-panel">

          <div className="panel-title">

            <div>

              <h3>
                Current Weather
              </h3>

              <p>
                Based on your saved profile location.
              </p>

            </div>

          </div>


          {weather ? (

            <div className="dashboard-weather">

              <div className="dashboard-weather-main">

                <div>

                  <strong>
                    {
                      weather.temperature_c
                    }°C
                  </strong>

                  <p>
                    {
                      weather.district
                    }
                  </p>

                </div>

              </div>


              <div className="dashboard-weather-grid">

                <div>

                  <span>
                    Humidity
                  </span>

                  <strong>
                    {
                      weather.humidity
                    }%
                  </strong>

                </div>


                <div>

                  <span>
                    Rainfall
                  </span>

                  <strong>
                    {
                      weather.rainfall_1h_mm
                    } mm
                  </strong>

                </div>


                <div>

                  <span>
                    Wind Speed
                  </span>

                  <strong>
                    {
                      weather.wind_speed_mps
                    } m/s
                  </strong>

                </div>


                <div>

                  <span>
                    Condition
                  </span>

                  <strong>
                    {
                      weather.description
                    }
                  </strong>

                </div>

              </div>

            </div>

          ) : (

            <div className="empty-state">

              <p>
                {
                  weatherError ||
                  "Weather information unavailable."
                }
              </p>


              {weatherError && (

                <Link
                  to="/profile"
                  className="image-link"
                >
                  Update Profile Location
                </Link>

              )}

            </div>

          )}

        </div>


        {/* ==================================
            RECENT ACTIVITY
        ================================== */}

        <div className="info-panel">

          <div className="panel-title">

            <div>

              <h3>
                Recent Activity
              </h3>

              <p>
                Your latest MangoCare analyses.
              </p>

            </div>


            <Link
              to="/history"
              className="image-link"
            >
              View All
            </Link>

          </div>


          {recentHistory.length === 0 ? (

            <div className="empty-state">

              <p>
                No recent activity yet.
              </p>

            </div>

          ) : (

            <div className="recent-list">

              {recentHistory.map(
                item => (

                  <div
                    className="recent-item"
                    key={
                      `${item.type}-${item.id}`
                    }
                  >

                    {/* Keep icons only here */}

                    <span className="recent-icon">

                      {
                        item.type === "leaf"
                          ? "🌿"
                          : item.type === "fruit"
                          ? "🥭"
                          : "🌱"
                      }

                    </span>


                    <div>

                      <strong>
                        {
                          item.title
                        }
                      </strong>

                      <p>

                        {
                          item.type ===
                          "advisory"
                            ? item.suitability
                            : item.prediction
                        }

                      </p>

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      </section>

    </div>
  );
}


/* ==========================================
   SERVICE CARD COMPONENT
========================================== */

function ServiceCard({
  title,
  text,
  link,
  button
}) {

  return (
    <div className="service-card">

      <h3>
        {title}
      </h3>

      <p>
        {text}
      </p>

      <Link
        to={link}
        className="primary-button"
      >
        {button}
      </Link>

    </div>
  );
}


export default Dashboard;