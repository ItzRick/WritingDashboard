import axios from 'axios'
const BASE_URL = "https://localhost:5000/loginapi";

const authProvider = {
    login: ({ username, password }) =>  {
        axios.post(`${BASE_URL}/login`, {
            "username": username,
            "password": password,
        }).then(response => {
            if (response.status < 200 || response.status >= 300) {
                throw new Error(response.statusText);
            }
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
    
            if (localStorage.getItem("access_token") !== null && localStorage.getItem("access_token") !== "undefined") {

            } else {
                alert(response.data.error);
                setFormError(true);
            }
        }).catch(() => {
                throw new Error('Network error')
                setFormError(true);
            });
    },
    checkError: (error) => {
        const status = error.status;
        if (status === 401 || status === 403) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            return Promise.reject();
        }
        // other error code (404, 500, etc): no need to log out
        return Promise.resolve();
    },
    checkAuth: () => {
        axios.get(`${BASE_URL}/protected`, {
             headers: {"Authorization" : `Bearer ${localStorage.getItem(access_token)}`}
            }).then(response => {
                if (response.status < 200 || response.status >= 300) {
                    throw new Error(response.statusText);
                }
                return Promise.resolve()
            });
        return Promise.resolve();
    },
    getIdentity: () => {
        try {
            const { id } = JSON.parse(localStorage.getItem('id'));
            return Promise.resolve({ id });
        } catch (error) {
            return Promise.reject(error);
        }
    },
    getPermissions: () => {
        const access_token = localStorage.getItem('access_token');
        const role = localStorage.getItem('role')
        if (access_token && role){
            return Promise.resolve(role)
        } else {
            return Promise.reject;
        }
    },
};

export default authProvider;