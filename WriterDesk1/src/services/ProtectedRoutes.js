import { history } from "../helpers/history";
import { Navigate, Outlet, useOutletContext } from "react-router-dom";
import { AuthenticationService } from "./authenticationService";

const getRole = () => {
    AuthenticationService.checkAuth().catch(() => {
        history.push("/Login");
        window.location.reload();
    });
    return AuthenticationService.getRole();
}

const ProtectedR = () => {
    const role = getRole()
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    return (role === 'researcher' || role === 'admin') ? <Outlet context={{ setTitle }} /> : <Navigate to="/" />;
}

const ProtectedA = () => {
    const role = getRole();
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    return (role === 'admin') ? <Outlet context={{ setTitle }}/> : <Navigate to="/" />;
}

export {ProtectedR, ProtectedA};