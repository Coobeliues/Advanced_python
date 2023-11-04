import React from "react";
import {Link, useNavigate} from "react-router-dom";

const Profile = () => {
    const navigate = useNavigate();
    const f = () => {
        navigate('/services');
    }
    return(
        <>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"></link>
            <nav className="navbar navbar-expand-lg navbar-custom">
                <div className="container">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <Link to="services">Services</Link>
                        </li>
                        <li className="nav-item">
                            <Link to="profile">Profile</Link>
                        </li>
                    </ul>
                    <ul className="navbar-nav ml-auto">
                        <li className="nav-item">
                            <button onClick={() => f()}><Link to="auth/login">Logout</Link></button>.
                        </li>
                    </ul>
                </div>
            </nav>

            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </>
    )
}

export default Profile;