import { combineReducers } from 'redux';
import notes from "./notes";
import auth from "./auth";


const ponyApp = combineReducers({
    notes, auth,
})

const rootReducer = (state, action) => {
    switch (action.type) {
        case 'AUTHENTICATION_ERROR':
        case 'LOGIN_FAILED':
        case 'REGISTRATION_FAILED':
        case 'LOGOUT_SUCCESSFUL':
            state = {...state, 'notes': []};
            break;
        
        default:
            break;
    }
    
    return ponyApp(state, action);
};
    
export default rootReducer;

//export default ponyApp;
