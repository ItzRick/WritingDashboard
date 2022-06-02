import axios from 'axios';
import authHeader from './auth-header';
const BASE_URL = "https://localhost:5000/loginapi";

class UserService{
    getPrivateContent() {
        return axios.get(`${BASE_URL}/protected`, { headers: authHeader() });
    }
}

export default new UserService();