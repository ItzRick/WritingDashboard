import { AuthenticationService } from "../services/authenticationService";

/**
 * Create authorization header for requests
 * 
 * @returns Authorization header
 */
export function authHeader() {
    const currentUser = AuthenticationService.getCurrentUser();
    if (currentUser && currentUser.access_token){
        return {Authorization: `Bearer ${currentUser.access_token}`};
    } else {
        return {};
    }
}