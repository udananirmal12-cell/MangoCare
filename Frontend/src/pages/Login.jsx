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


function Login() {

  const navigate =
    useNavigate();

  const {
    login
  } = useAuth();


  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  async function handleSubmit(
    event
  ) {

    event.preventDefault();

    try {

      setLoading(true);
      setError("");


      await login(
        email,
        password
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

        <h1>
          Welcome Back
        </h1>

        <p className="auth-description">
          Sign in to your MangoCare account.
        </p>


        <form
          onSubmit={handleSubmit}
        >

          <div className="form-group">

            <label>
              Email Address
            </label>

            <input
              type="email"
              value={email}
              onChange={
                (event) =>
                  setEmail(
                    event.target.value
                  )
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
              value={password}
              onChange={
                (event) =>
                  setPassword(
                    event.target.value
                  )
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
                ? "Signing In..."
                : "Sign In"
            }

          </button>

        </form>


        <p className="auth-footer">

          Don't have an account?

          {" "}

          <Link to="/register">
            Create Account
          </Link>

        </p>

      </div>

    </div>
  );
}


export default Login;