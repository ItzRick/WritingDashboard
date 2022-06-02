import { AuthenticationService } from "../services/authenticationService";

export function authHeader() {
    const currentUser = AuthenticationService.getCurrentUser();
    if (currentUser && currentUser.access_token){
        return { Authorization: 'Bearer' + currentUser.access_token };
    } else {
        return {};
    }
}