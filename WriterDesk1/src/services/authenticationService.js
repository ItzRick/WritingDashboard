import axios from 'axios'
import { authHeader } from '../helpers/auth-header';
const BASE_URL = "https://localhost:5000/loginapi";


export const AuthenticationService = {
    login,
    logout,
    getCurrentUser,
    getCurrentUserId,
    checkAuth,
    getRole
}

function login(username, password) {
    return axios.post(`${BASE_URL}/login`, {
        "username": username,
        "password": password,
    }).then(response => {
        localStorage.setItem('currentUser', JSON.stringify(response.data));

        if (JSON.parse(localStorage.getItem('currentUser')).access_token !== null && JSON.parse(localStorage.getItem('currentUser')).access_token !== "undefined") {
            console.log("Inloggen gelukt!");
        } else {
            return Promise.reject();
        }
    })
        .catch(error => {        
            return Promise.reject();   
        });
}

function logout() {
    localStorage.removeItem('currentUser');
}

function getCurrentUser() {
    return JSON.parse(localStorage.getItem('currentUser'));
}

function getCurrentUserId() {
    if(JSON.parse(localStorage.getItem('currentUser')) !== null) {
        return JSON.parse(localStorage.getItem('currentUser')).id;
    } else {
        return Error("No user found");
    }
}

function checkAuth () {
    return axios.get(`${BASE_URL}/protected`, {headers: authHeader()});
}

function getRole (){
    return JSON.parse(localStorage.getItem('currentUser')).role;
}
