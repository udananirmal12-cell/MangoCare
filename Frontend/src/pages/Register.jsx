import {
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../context/AuthContext";


function Register() {

  const navigate =
    useNavigate();

  const {
    register
  } = useAuth();


  const [formData, setFormData] =
    useState({
      name: "",
      email: "",
      password: "",
      confirmPassword: ""
    });


  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


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


    if (
      formData.password
      !==
      formData.confirmPassword
    ) {

      setError(
        "Passwords do not match."
      );

      return;
    }


    try {

      setLoading(true);
      setError("");


      await register(
        formData.name,
        formData.email,
        formData.password
      );


      navigate("/");

    } catch (err) {

      setError(
        err.message
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-logo">
          🥭
        </div>

        <h1>
          Create Account
        </h1>

        <p className="auth-description">
          Register as a MangoCare farmer.
        </p>


        <form
          onSubmit={handleSubmit}
        >

          <div className="form-group">

            <label>
              Full Name
            </label>

            <input
              type="text"
              name="name"
              value={
                formData.name
              }
              onChange={
                handleChange
              }
              required
            />

          </div>


          <div className="form-group">

            <label>
              Email Address
            </label>

            <input
              type="email"
              name="email"
              value={
                formData.email
              }
              onChange={
                handleChange
              }
              required
            />

          </div>


          <div className="form-group">

            <label>
              Password
            </label>

            <input
              type="password"
              name="password"
              minLength="6"
              value={
                formData.password
              }
              onChange={
                handleChange
              }
              required
            />

          </div>


          <div className="form-group">

            <label>
              Confirm Password
            </label>

            <input
              type="password"
              name="confirmPassword"
              value={
                formData.confirmPassword
              }
              onChange={
                handleChange
              }
              required
            />

          </div>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}


          <button
            type="submit"
            className="primary-button full-button"
            disabled={loading}
          >

            {
              loading
                ? "Creating Account..."
                : "Create Account"
            }

          </button>

        </form>


        <p className="auth-footer">

          Already have an account?

          {" "}

          <Link to="/login">
            Sign In
          </Link>

        </p>

      </div>

    </div>
  );
}


export default Register;