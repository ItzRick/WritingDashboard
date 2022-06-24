import { history } from "../helpers/history";
import { Navigate, Outlet, useOutletContext } from "react-router-dom";
import { AuthenticationService } from "./authenticationService";

/**
 * Check role from user, and authenticate access token
 * 
 * @returns Role of current user, if there isn't a current user the user will be send to login page
 */
const getRole = () => {
    AuthenticationService.checkAuth().catch(() => {
        history.push("/Login");
    });
    return AuthenticationService.getRole();
}

/**
 * Load pages when user is logged in
 * 
 * @returns protected page when user is logged in, else user will be send to homepage
 */
 const ProtectedU = () => {
    const role = getRole();
    //set title in parent 'base'     
    const { setTitle } = useOutletContext();
    return (role === 'student' || role === 'participant' || role === 'researcher' || role === 'admin') ? <Outlet context={{ setTitle }} /> : <Navigate to="/" />;
}

/**
 * Load pages for researchers when user has correct role
 * 
 * @returns protected page when user has access to protected pages, else user will be send to homepage
 */
const ProtectedR = () => {
    const role = getRole()
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    return (role === 'researcher' || role === 'admin') ? <Outlet context={{ setTitle }} /> : <Navigate to="/" />;
}

/**
 * * Load pages for admins when user has correct role
 * 
 * @returns protected page when user has access to protected pages, else user will be send to homepage
 */
const ProtectedA = () => {
    const role = getRole();
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    return (role === 'admin') ? <Outlet context={{ setTitle }}/> : <Navigate to="/" />;
}

export {ProtectedU, ProtectedR, ProtectedA};