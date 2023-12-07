import {Link} from "react-router-dom";
import React, { useContext } from "react";
import "./Services.css";
import { UserContext } from "../context/UserContext";
const Services = () => {
    const [token] = useContext(UserContext);
    return (

        <>
            {token && (
                <><Link to="/"><button>Back</button>
                </Link><h2>Services</h2>
                <Link to="editInfo">Service1</Link>
                <Link to="service2">Service2</Link></>
            )};
        </>
    )
}

export default Services;