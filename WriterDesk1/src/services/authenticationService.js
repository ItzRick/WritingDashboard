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

/**
 * Request login to server using axios
 * 
 * @param username username for request
 * @param password password for request
 * @returns login page
 */
function login(username, password) {
    return axios.post(`${BASE_URL}/login`, {
        "username": username,
        "password": password,
    }).then(response => {
        localStorage.setItem('currentUser', JSON.stringify(response.data));

        if (JSON.parse(localStorage.getItem('currentUser')).access_token == null || JSON.parse(localStorage.getItem('currentUser')).access_token == "undefined") {
            return Promise.reject();
        }
    })
        .catch(error => {        
            return Promise.reject();   
        });
}

/**
 * Logout user
 */
function logout() {
    localStorage.removeItem('currentUser');
}

/**
 * 
 * @returns currentUser containing user id, access token, role
 */
function getCurrentUser() {
    return JSON.parse(localStorage.getItem('currentUser'));
}

/**
 * 
 * @returns user ID
 */
function getCurrentUserId() {
    if(JSON.parse(localStorage.getItem('currentUser')) !== null) {
        return JSON.parse(localStorage.getItem('currentUser')).id;
    } else {
        return Error("No user found");
    }
}

/**
 * Server checks if users access token is valid
 * 
 * @returns axios response, status 200 when user is authenticated
 */
function checkAuth () {
    return axios.get(`${BASE_URL}/protected`, {headers: authHeader()});
}

/**
 * 
 * @returns user role
 */
function getRole (){
    return JSON.parse(localStorage.getItem('currentUser')).role;
}
