
import {Link} from "react-router-dom";

const Home = () => {
    return (

        <>
                <div className="container">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <Link to="services">Services</Link>
                        </li>
                        <li className="nav-item">
                            <Link to="profile">Profile</Link>
                        </li>
                    </ul>
                </div>

        </>
    )
}

export default Home;