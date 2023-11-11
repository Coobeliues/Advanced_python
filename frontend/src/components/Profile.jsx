import React, {useEffect, useState} from "react";


const Profile = () => {
    const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"));
    var name;
    useEffect(() => {
        const fetchUser = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
            };

            const response = await fetch("/users/me/", requestOptions);

            if (!response.ok) {
                setToken(null);
            }
            localStorage.setItem("awesomeLeadsToken", token);
            console.log(response.json())
            // name = await response.json()["username"];
            // console.log(name)
        };
        // fetchUser();
    }, [token]);
    return(
        <>
            <h2>Profile</h2>
        </>
    )
}

export default Profile;