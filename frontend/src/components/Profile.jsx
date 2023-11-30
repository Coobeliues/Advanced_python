import React, {useEffect, useState, useContext} from "react";
import {UserContext} from "../context/UserContext" 


const Profile = () => {
    const [user, setUser] = useState(null);
    const [token] = useContext(UserContext);
    useEffect(() => {
        const fetchUser = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
            },
        };

        const response = await fetch("http://localhost:8000/users/profile/", requestOptions);

    
        const userData = await response.json(); // Parse the JSON response

        setUser(userData);
        };
        fetchUser();
    }, [token]);
    return(
        <>
            <h2>Profile</h2>
            {user && (
                <div>
                    <h3>Name: {user.username}</h3>
                    {/* Display other user information here */}
                </div>
            )}
        </>
    )
}

export default Profile;