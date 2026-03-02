import React, { createContext, useContext, useState, useEffect } from "react";
import { getStoredUser, logout as logoutService } from "../backend_connection/auth";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const storedUser = getStoredUser();
        if (storedUser) {
            setUser(storedUser);
        }
        setLoading(false);
    }, []);

    const login = (userData) => {
        setUser(userData);
    };

    const logout = () => {
        logoutService();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);