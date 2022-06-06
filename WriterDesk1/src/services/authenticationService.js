import axios from 'axios'
import { authHeader } from '../helpers/auth-header';
const BASE_URL = "https://localhost:5000/loginapi";


export const AuthenticationService = {
    login,
    logout,
    getCurrentUser,
    checkAuth,
    getRole
}

function login(username, password) {
    axios.post(`${BASE_URL}/login`, {
        "username": username,
        "password": password,
    }).then(response => {
        localStorage.setItem('currentUser', JSON.stringify(response.data));

        if (JSON.parse(localStorage.getItem('currentUser')).access_token !== null && JSON.parse(localStorage.getItem('currentUser')).access_token !== "undefined") {
            console.log("Inloggen gelukt!")
            // TODO go to new page
        } else {
            alert(response.data.error);
            // setFormError(true);
        }
    })
        .catch(error => {
            console.error("Something went wrong:", error);
            logout();
        });
}

function logout() {
    localStorage.removeItem('currentUser');
}

function getCurrentUser() {
    return JSON.parse(localStorage.getItem('currentUser'));
}

function checkAuth () {
    return axios.get(`${BASE_URL}/protected`, {headers: authHeader()});
}

function getRole (){
    return axios.get(`${BASE_URL}/protected`, {headers: authHeader()
        }).then(response => {
            return response.data.role;
            localStorage.setItem('currentUser', JSON.stringify(response.data));
        }).catch(error => {
            AuthenticationService.logout();
            console.error("Couldn't recieve role:", error);
        });
}
