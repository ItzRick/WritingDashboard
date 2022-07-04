import axios from 'axios'
import { authHeader } from '../helpers/auth-header';


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
    return axios.post(`/api/loginapi/login`, {
        "username": username,
        "password": password,
    }).then(response => {
        localStorage.setItem('currentUser', JSON.stringify(response.data));

        if (JSON.parse(localStorage.getItem('currentUser')).access_token == null || JSON.parse(localStorage.getItem('currentUser')).access_token === "undefined") {
            return Promise.reject();
        }
    })
        .catch(error => {   
            return Promise.reject();   
        });
}

/**
 * Logout current user
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
 * @returns userID of current user
 */
function getCurrentUserId() {
    if(JSON.parse(localStorage.getItem('currentUser')) !== null) {
        return JSON.parse(localStorage.getItem('currentUser')).user_id;
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
    return axios.get(`/api/loginapi/protected`, {headers: authHeader()});
}

/**
 * 
 * @returns role of current user
 */
function getRole (){
    const  user = getCurrentUser();
    return user === null ? null : user.role;
}
