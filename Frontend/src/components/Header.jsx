import {
  useNavigate
} from "react-router-dom";

import {
  useAuth
} from "../context/AuthContext";


function Header() {

  const {
    user,
    logout
  } = useAuth();

  const navigate =
    useNavigate();


  function handleLogout() {

    logout();

    navigate(
      "/login"
    );
  }


  const initial =
    user?.name
      ? user.name.charAt(0)
          .toUpperCase()
      : "F";


  return (
    <header className="top-header">

      <div>

        <h3>
          Mango Cultivation Management
        </h3>

        <p>
          AI-powered support for healthier
          mango cultivation
        </p>

      </div>


      <div className="header-profile">

        <div className="profile-avatar">
          {initial}
        </div>


        <div className="profile-user-info">

          <strong>
            {user?.name || "Farmer"}
          </strong>

          <p>
            {user?.email}
          </p>

        </div>


        <button
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>

      </div>

    </header>
  );
}


export default Header;