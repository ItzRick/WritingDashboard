import axios from 'axios'
const BASE_URL = "https://localhost:5000/loginapi";


export const AuthenticationService = {
    login,
    logout,
    getCurrentUser
}

function login(username, password) {
    axios.post(`${BASE_URL}/login`, {
        "username": username,
        "password": password,
    }).then(response => {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token)

        if (localStorage.getItem("access_token") !== null && localStorage.getItem("access_token") !== "undefined") {
            console.log("Inloggen gelukt!")
            // TODO go to new page
        } else {
            alert(response.data.error);
            setFormError(true);
        }
    })
        .catch(error => {
            console.error("Something went wrong:", error);
            setFormError(true);
        });
}

function logout() {
    localStorage.removeItem('currentUser');
}

function getCurrentUser() {
    return JSON.parse(localStorage.getItem('currentUser'));
}

export default new AuthenticationService();