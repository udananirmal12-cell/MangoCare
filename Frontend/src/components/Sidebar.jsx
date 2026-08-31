import { NavLink } from "react-router-dom";


function Sidebar() {

  const getLinkClass = ({ isActive }) =>
    isActive
      ? "sidebar-link active"
      : "sidebar-link";


  return (
    <aside className="sidebar">

      <div className="brand">

        <div>
          <h2>MangoCare</h2>
          <p>AI Cultivation Assistant</p>
        </div>

      </div>


      <nav className="sidebar-nav">

        <NavLink
          to="/"
          className={getLinkClass}
        >
          Dashboard
        </NavLink>


        <NavLink
          to="/leaf"
          className={getLinkClass}
        >
          Leaf Detection
        </NavLink>


        <NavLink
          to="/fruit"
          className={getLinkClass}
        >
          Fruit Detection
        </NavLink>


        <NavLink
          to="/advisory"
          className={getLinkClass}
        >
          Smart Advisory
        </NavLink>


        <NavLink
          to="/history"
          className={getLinkClass}
        >
          History
        </NavLink>


        <NavLink
          to="/profile"
          className={getLinkClass}
        >
          Profile
        </NavLink>

      </nav>


      <div className="sidebar-footer">

        <p>MangoCare</p>

        <small>
          AI-powered decision support
        </small>

      </div>

    </aside>
  );
}


export default Sidebar;