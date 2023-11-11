import React, { useContext } from "react";
import './Header.css';
import { UserContext } from "../context/UserContext";
import Profile from "./Profile";
import {Link, useNavigate} from "react-router-dom";

const Header = ({ title }) => {
  const navigate = useNavigate();
  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
    navigate("/auth/login")
  };

  return (
    <div className="has-text-centered m-6">
      <h1 className="title">{title}</h1>
      {token && (
          <div>
            <div className="links">
              <Link to="profile" >Profile</Link>
              <Link to="services">Services</Link>
              <button className="button1" onClick={handleLogout}>
                Logout
              </button>
            </div>

              <hr className="horizontal-line" />
          </div>

      )}

    </div>
  );
};

export default Header;