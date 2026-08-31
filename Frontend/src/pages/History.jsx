import {
  useEffect,
  useState
} from "react";

import {
  getHistory,
  API_BASE_URL
} from "../services/api";


function History() {

  const [history, setHistory] =
    useState([]);

  const [filter, setFilter] =
    useState("all");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  useEffect(() => {

    loadHistory();

  }, []);


  async function loadHistory() {

    try {

      setLoading(true);

      const data =
        await getHistory();

      setHistory(
        data.history || []
      );

    } catch (err) {

      setError(
        err.message
      );

    } finally {

      setLoading(false);

    }
  }


  const filteredHistory =
    filter === "all"
      ? history
      : history.filter(
          item =>
            item.type === filter
        );


  return (
    <div className="page">

      <span className="page-badge">
        Previous Analysis
      </span>

      <h1>
        History
      </h1>

      <p className="page-description">
        View your previous leaf scans,
        fruit scans and cultivation advisories.
      </p>


      <div className="history-filters">

        {[
          ["all", "All"],
          ["leaf", "Leaf"],
          ["fruit", "Fruit"],
          ["advisory", "Advisory"]
        ].map(([value, label]) => (

          <button
            key={value}
            className={
              filter === value
                ? "history-filter active"
                : "history-filter"
            }
            onClick={() =>
              setFilter(value)
            }
          >
            {label}
          </button>

        ))}

      </div>


      {loading && (
        <p>
          Loading history...
        </p>
      )}


      {error && (
        <div className="error-message">
          {error}
        </div>
      )}


      {!loading &&
        filteredHistory.length === 0 && (

        <div className="placeholder-box">

          <div className="large-icon">
            ◷
          </div>

          <h3>
            No records found
          </h3>

          <p>
            Your MangoCare analyses
            will appear here.
          </p>

        </div>

      )}


      <div className="history-list">

        {filteredHistory.map(
          item => (

            <HistoryItem
              key={
                `${item.type}-${item.id}`
              }
              item={item}
            />

          )
        )}

      </div>

    </div>
  );
}


function HistoryItem({
  item
}) {

  const date = new Date(
    item.created_at
  ).toLocaleString();


  return (
    <div className="history-card">

      <div className="history-icon">

        {item.type === "leaf" && "🌿"}
        {item.type === "fruit" && "🥭"}
        {item.type === "advisory" && "🌱"}

      </div>


      <div className="history-content">

        <div className="history-heading">

          <div>

            <h3>
              {item.title}
            </h3>

            <p>
              {date}
            </p>

          </div>


          <span className="history-type">
            {item.type}
          </span>

        </div>


        {item.type !== "advisory" ? (

          <>

            <strong className="history-result">
              {item.prediction}
            </strong>

            <p>
              Confidence:{" "}
              {
                (
                  item.confidence * 100
                ).toFixed(2)
              }%
            </p>


            {item.image_path && (

              <a
                href={
                  `${API_BASE_URL}/${item.image_path}`
                }
                target="_blank"
                rel="noreferrer"
                className="image-link"
              >
                View Image
              </a>

            )}

          </>

        ) : (

          <div className="history-advisory-grid">

            <span>
              Suitability:
              <strong>
                {" "}
                {item.suitability}
              </strong>
            </span>

            <span>
              Irrigation:
              <strong>
                {" "}
                {item.irrigation_need}
              </strong>
            </span>

            <span>
              Drought:
              <strong>
                {" "}
                {item.drought_risk}
              </strong>
            </span>

            <span>
              Nutrients:
              <strong>
                {" "}
                {item.nutrient_condition}
              </strong>
            </span>

          </div>

        )}

      </div>

    </div>
  );
}


export default History;