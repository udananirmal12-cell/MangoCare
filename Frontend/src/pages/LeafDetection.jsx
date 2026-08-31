import { useState } from "react";

import {
  predictLeaf,
  API_BASE_URL
} from "../services/api";


function LeafDetection() {

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  function handleFileChange(event) {

    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);

    setPreview(
      URL.createObjectURL(selectedFile)
    );

    setResult(null);
    setError("");
  }


  async function handlePrediction() {

    if (!file) {

      setError(
        "Please select a mango leaf image."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");

      const data = await predictLeaf(file);

      setResult(data);

    } catch (err) {

      setError(err.message);

    } finally {

      setLoading(false);

    }
  }


  return (
    <div className="page">

      <span className="page-badge">
        AI Image Analysis
      </span>

      <h1>
        Leaf Disease Detection
      </h1>

      <p className="page-description">
        Upload a clear mango leaf photograph and
        MangoCare will analyse it using the trained
        AI disease detection model.
      </p>


      <div className="analysis-layout">

        <div className="upload-card">

          <h3>
            Upload Mango Leaf
          </h3>

          <label className="upload-area">

            {preview ? (

              <img
                src={preview}
                alt="Leaf preview"
                className="image-preview"
              />

            ) : (

              <>
                <strong>
                  Select Leaf Image
                </strong>

                <p>
                  JPG, JPEG or PNG
                </p>
              </>

            )}

            <input
              type="file"
              accept="image/png,image/jpeg"
              onChange={handleFileChange}
              hidden
            />

          </label>


          {file && (
            <p className="selected-file">
              {file.name}
            </p>
          )}


          <button
            className="primary-button full-button"
            onClick={handlePrediction}
            disabled={loading}
          >

            {loading
              ? "Analysing..."
              : "Analyse Leaf"}

          </button>


          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

        </div>


        <div className="result-card">

          {!result ? (

            <div className="result-empty">

              <h3>
                AI Result
              </h3>

              <p>
                Your prediction will appear here
                after the image is analysed.
              </p>

            </div>

          ) : (

            <>

              <span className="result-label">
                Detected Condition
              </span>

              <h2 className="prediction-name">
                {result.result.prediction}
              </h2>


              <div className="confidence-section">

                <div className="confidence-header">

                  <span>
                    AI Confidence
                  </span>

                  <strong>
                    {
                      result.result
                        .confidence_percentage
                    }%
                  </strong>

                </div>


                <div className="confidence-bar">

                  <div
                    className="confidence-fill"
                    style={{
                      width:
                        `${
                          result.result
                            .confidence_percentage
                        }%`
                    }}
                  />

                </div>

              </div>


              <div className="result-info">

                <strong>
                  Analysis completed successfully
                </strong>

                <p>
                  MangoCare classified the uploaded
                  leaf using the trained CNN model.
                </p>

              </div>

              {result.disease_information && (

                <DiseaseInformation
                  info={result.disease_information}
                />

              )}

              {result.image_path && (

                <a
                  className="image-link"
                  href={
                    `${API_BASE_URL}/${result.image_path}`
                  }
                  target="_blank"
                  rel="noreferrer"
                >
                  View stored image
                </a>

              )}

            </>

          )}

        </div>

      </div>

    </div>
  );
}


function DiseaseInformation({
  info
}) {

  return (
    <div className="disease-info">

      <h3>
        Disease Information
      </h3>


      <div className="disease-info-section">

        <h4>
          About this condition
        </h4>

        <p>
          {info.description}
        </p>

      </div>


      {info.causes &&
        info.causes.length > 0 && (

        <div className="disease-info-section">

          <h4>
            Possible Causes
          </h4>

          <ul>

            {info.causes.map(
              (item, index) => (

                <li key={index}>
                  {item}
                </li>

              )
            )}

          </ul>

        </div>

      )}


      <div className="disease-info-section">

        <h4>
          Recommended Management
        </h4>

        <ul>

          {info.management.map(
            (item, index) => (

              <li key={index}>
                {item}
              </li>

            )
          )}

        </ul>

      </div>


      <div className="disease-info-section">

        <h4>
          Prevention
        </h4>

        <ul>

          {info.prevention.map(
            (item, index) => (

              <li key={index}>
                {item}
              </li>

            )
          )}

        </ul>

      </div>


      <div className="advisory-disclaimer">

        AI-supported management guidance.
        Consult an agricultural specialist
        when symptoms are severe or uncertain.

      </div>

    </div>
  );
}

export default LeafDetection;