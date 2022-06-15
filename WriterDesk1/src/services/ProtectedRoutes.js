import { history } from "../helpers/history";
import { Navigate, Outlet, useOutletContext } from "react-router-dom";
import { AuthenticationService } from "./authenticationService";

/**
 * Check role from user, and authenticate access token
 * 
 * @returns 
 */
const getRole = () => {
    AuthenticationService.checkAuth().catch(() => {
        history.push("/Login");
        window.location.reload();
    });
    return AuthenticationService.getRole();
}

/**
 * Load pages for researchers when user has correct role
 * 
 * @returns 
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
 * @returns 
 */
const ProtectedA = () => {
    const role = getRole();
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    return (role === 'admin') ? <Outlet context={{ setTitle }}/> : <Navigate to="/" />;
}

export {ProtectedR, ProtectedA};