import React, { useState, useEffect } from 'react';
import AuthForm from './components/AuthForm';
import DashboardHome from './components/DashboardHome';
import api from './services/api';

export default function App() {
    const [telaAtual, setTelaAtual] = useState('login');

    useEffect(() => {
        const tokenValido = localStorage.getItem('token_access');
        if (tokenValido) {
            setTelaAtual('dashboard');
        }
    }, []);

    const handleLogout = async () => {
        try {
            const refreshToken = localStorage.getItem('token_refresh');
            if (refreshToken) {
                await api.post('/accounts/logout/', { refresh: refreshToken });
            }
        } catch (error) {
            console.error('Erro ao encerrar sessão:', error);
        } finally {
            localStorage.clear();
            setTelaAtual('login');
        }
    };

    return (
        <>
            {telaAtual !== 'dashboard' ? (
                <AuthForm onLoginSuccess={() => setTelaAtual('dashboard')} />
            ) : (
                <DashboardHome onLogout={handleLogout} />
            )}
        </>
    );
}