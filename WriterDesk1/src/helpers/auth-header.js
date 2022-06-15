import { AuthenticationService } from "../services/authenticationService";

/**
 * Create authorization header for requests; 
 * Checks if there is a stored access token, this is used to write a header which can be used for requests to the server.
 *  * 
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