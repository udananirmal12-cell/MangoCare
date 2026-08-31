import {
  useEffect,
  useState
} from "react";

import {
  getProfile,
  updateProfile
} from "../services/api";

import {
  useAuth
} from "../context/AuthContext";


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


function Profile() {

  const {
    loadUser
  } = useAuth();


  const [formData, setFormData] =
    useState({
      name: "",
      email: "",
      district: "",
      soil_ph: "",
      nitrogen: "",
      phosphorus: "",
      potassium: ""
    });


  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");


  useEffect(() => {

    loadProfile();

  }, []);


  async function loadProfile() {

    try {

      setLoading(true);

      const data =
        await getProfile();


      setFormData({

        name:
          data.name || "",

        email:
          data.email || "",

        district:
          data.district || "",

        soil_ph:
          data.soil_ph ?? "",

        nitrogen:
          data.nitrogen ?? "",

        phosphorus:
          data.phosphorus ?? "",

        potassium:
          data.potassium ?? ""

      });

    } catch (err) {

      setError(
        err.message
      );

    } finally {

      setLoading(false);

    }
  }


  function handleChange(
    event
  ) {

    const {
      name,
      value
    } = event.target;


    setFormData({
      ...formData,
      [name]: value
    });
  }


  async function handleSubmit(
    event
  ) {

    event.preventDefault();


    try {

      setSaving(true);
      setError("");
      setMessage("");


      const profileData = {

        name:
          formData.name,

        district:
          formData.district || null,

        soil_ph:
          formData.soil_ph === ""
            ? null
            : Number(
                formData.soil_ph
              ),

        nitrogen:
          formData.nitrogen === ""
            ? null
            : Number(
                formData.nitrogen
              ),

        phosphorus:
          formData.phosphorus === ""
            ? null
            : Number(
                formData.phosphorus
              ),

        potassium:
          formData.potassium === ""
            ? null
            : Number(
                formData.potassium
              )
      };


      await updateProfile(
        profileData
      );


      await loadUser();


      setMessage(
        "Profile updated successfully."
      );

    } catch (err) {

      setError(
        err.message
      );

    } finally {

      setSaving(false);

    }
  }


  if (loading) {

    return (
      <div className="page">
        Loading profile...
      </div>
    );
  }


  return (
    <div className="page">

      <span className="page-badge">
        Farmer Account
      </span>

      <h1>
        Farmer Profile
      </h1>

      <p className="page-description">
        Manage your account and cultivation
        information.
      </p>


      <form
        className="profile-form-card"
        onSubmit={handleSubmit}
      >

        <div className="profile-section">

          <h3>
            Account Information
          </h3>


          <div className="form-group">

            <label>
              Full Name
            </label>

            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />

          </div>


          <div className="form-group">

            <label>
              Email
            </label>

            <input
              type="email"
              value={formData.email}
              disabled
            />

          </div>

        </div>


        <div className="profile-section">

          <h3>
            Cultivation Information
          </h3>


          <div className="form-group">

            <label>
              Location
            </label>

            <select
              name="district"
              value={formData.district}
              onChange={handleChange}
            >

              <option value="">
                Select District
              </option>

              {
                districts.map(
                  district => (

                    <option
                      key={district}
                      value={district}
                    >
                      {district}
                    </option>

                  )
                )
              }

            </select>

          </div>


          <div className="form-row">

            <div className="form-group">

              <label>
                Nitrogen (N)
              </label>

              <input
                type="number"
                name="nitrogen"
                min="0"
                max="200"
                value={
                  formData.nitrogen
                }
                onChange={
                  handleChange
                }
              />

            </div>


            <div className="form-group">

              <label>
                Phosphorus (P)
              </label>

              <input
                type="number"
                name="phosphorus"
                min="0"
                max="200"
                value={
                  formData.phosphorus
                }
                onChange={
                  handleChange
                }
              />

            </div>

          </div>


          <div className="form-row">

            <div className="form-group">

              <label>
                Potassium (K)
              </label>

              <input
                type="number"
                name="potassium"
                min="0"
                max="200"
                value={
                  formData.potassium
                }
                onChange={
                  handleChange
                }
              />

            </div>


            <div className="form-group">

              <label>
                Soil pH
              </label>

              <input
                type="number"
                name="soil_ph"
                min="3.5"
                max="9"
                step="0.1"
                value={
                  formData.soil_ph
                }
                onChange={
                  handleChange
                }
              />

            </div>

          </div>

        </div>


        {message && (

          <div className="success-message">
            {message}
          </div>

        )}


        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        <button
          className="primary-button"
          type="submit"
          disabled={saving}
        >

          {
            saving
              ? "Saving..."
              : "Save Profile"
          }

        </button>

      </form>

    </div>
  );
}


export default Profile;