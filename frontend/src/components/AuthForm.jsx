import React, { useState } from 'react';
import {
  FaGoogle,
  FaFacebookF,
  FaLinkedinIn,
  FaUser,
  FaEnvelope,
  FaLock,
  FaSeedling,
} from 'react-icons/fa';
import api from '../services/api';

const initialFormState = {
  nome: '',
  email: '',
  password: '',
  password_confirm: '',
};

function getErrorMessage(error) {
  const data = error?.response?.data;

  if (typeof data === 'string') return data;
  if (data?.erro) return data.erro;
  if (data?.mensagem) return data.mensagem;
  if (data?.detail) return data.detail;

  if (data && typeof data === 'object') {
    const [firstValue] = Object.values(data);
    if (Array.isArray(firstValue)) return firstValue[0];
    if (typeof firstValue === 'string') return firstValue;
  }

  return 'Não foi possível completar a operação.';
}

export default function AuthForm({ onLoginSuccess }) {
  const [isSignIn, setIsSignIn] = useState(true);
  const [formData, setFormData] = useState(initialFormState);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState({ type: '', message: '' });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (feedback.message) {
      setFeedback({ type: '', message: '' });
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setFeedback({ type: '', message: '' });

    try {
      if (isSignIn) {
        const response = await api.post('/accounts/login/', {
          email: formData.email,
          password: formData.password,
        });

        localStorage.setItem('token_access', response.data.access);
        localStorage.setItem('token_refresh', response.data.refresh);
        onLoginSuccess?.();
        return;
      }

      const response = await api.post('/accounts/registro/', {
        nome: formData.nome,
        email: formData.email,
        password: formData.password,
        password_confirm: formData.password_confirm,
        perfil: 'produtor',
      });

      setFeedback({
        type: 'success',
        message: response.data.mensagem || 'Cadastro realizado com sucesso.',
      });
      setFormData(initialFormState);
      setIsSignIn(true);
    } catch (error) {
      setFeedback({
        type: 'error',
        message: getErrorMessage(error),
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden font-sans p-4" style={{ backgroundImage: 'linear-gradient(135deg, #1b3d2b 0%, #2c4c38 50%, #0f2619 100%)' }}>
      <div className="absolute top-[-10%] left-[-10%] w-[40vw] h-[40vw] rounded-full opacity-30 blur-3xl animate-pulse" style={{ backgroundImage: 'linear-gradient(135deg, #91a030 0%, #b3c14a 100%)' }} />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50vw] h-[50vw] rounded-full opacity-20 blur-3xl" style={{ backgroundImage: 'linear-gradient(135deg, #d4af37 0%, #aa8010 100%)' }} />

      <div className="relative w-full rounded-3xl overflow-hidden flex shadow-[0_25px_50px_-12px_rgba(0,0,0,0.5)] border border-white/10 backdrop-blur-[25px]" style={{ maxWidth: '850px', minHeight: '550px', backgroundColor: 'rgba(255,255,255,0.03)' }}>
        <div className="w-full md:w-1/2 flex flex-col justify-center items-center p-8 lg:p-12 transition-all duration-700 ease-in-out">
          {isSignIn ? (
            <div className="w-full text-center flex flex-col items-center animate-fadeIn">
              <div className="flex items-center gap-2 mb-2 text-[#91a030]">
                <FaSeedling className="text-2xl" />
                <span className="text-sm font-semibold tracking-widest uppercase">AgroCore</span>
              </div>
              <h2 className="text-3xl font-bold text-white mb-6">Entrar na Conta</h2>

              <div className="flex gap-3 mb-6">
                <button className="w-10 h-10 rounded-full flex items-center justify-center bg-white/5 border border-white/10 text-white hover:bg-[#91a030] hover:border-[#91a030] transition-all duration-300">
                  <FaGoogle size={16} />
                </button>
                <button className="w-10 h-10 rounded-full flex items-center justify-center bg-white/5 border border-white/10 text-white hover:bg-[#3b5998] hover:border-[#3b5998] transition-all duration-300">
                  <FaFacebookF size={16} />
                </button>
                <button className="w-10 h-10 rounded-full flex items-center justify-center bg-white/5 border border-white/10 text-white hover:bg-[#0077b5] hover:border-[#0077b5] transition-all duration-300">
                  <FaLinkedinIn size={16} />
                </button>
              </div>

              <span className="text-xs text-stone-400 mb-6">ou use suas credenciais de produtor</span>

              <form className="w-full flex flex-col gap-4" onSubmit={handleSubmit}>
                <div className="relative w-full">
                  <FaEnvelope className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="E-mail ou Usuário"
                    className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-stone-400 focus:outline-none focus:border-[#91a030] focus:bg-white/10 transition-all text-sm shadow-[inset_0_1px_2px_rgba(255,255,255,0.05)]"
                    required
                  />
                </div>
                <div className="relative w-full">
                  <FaLock className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Senha"
                    className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-stone-400 focus:outline-none focus:border-[#91a030] focus:bg-white/10 transition-all text-sm shadow-[inset_0_1px_2px_rgba(255,255,255,0.05)]"
                    required
                  />
                </div>

                {feedback.message && (
                  <p className={`text-sm ${feedback.type === 'error' ? 'text-red-400' : 'text-emerald-400'}`}>
                    {feedback.message}
                  </p>
                )}

                <a href="#" className="text-xs text-stone-400 hover:text-white transition-colors text-right self-end mt-1">Esqueceu sua senha?</a>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full mt-4 py-3 rounded-xl text-white font-semibold shadow-lg shadow-[#91a030]/20 hover:shadow-[#91a030]/40 active:scale-[0.98] transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
                  style={{ backgroundImage: 'linear-gradient(90deg, #91a030 0%, #5d6b18 100%)' }}
                >
                  {loading ? 'Aguarde...' : 'Acessar Painel'}
                </button>
              </form>
            </div>
          ) : (
            <div className="w-full text-center flex flex-col items-center animate-fadeIn">
              <div className="flex items-center gap-2 mb-2 text-[#91a030]">
                <FaSeedling className="text-2xl" />
                <span className="text-sm font-semibold tracking-widest uppercase">Cultive Conosco</span>
              </div>
              <h2 className="text-3xl font-bold text-white mb-6">Criar Conta Agro</h2>

              <form className="w-full flex flex-col gap-4" onSubmit={handleSubmit}>
                <div className="relative w-full">
                  <FaUser className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
                  <input
                    type="text"
                    name="nome"
                    value={formData.nome}
                    onChange={handleChange}
                    placeholder="Nome Completo"
                    className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-stone-400 focus:outline-none focus:border-[#91a030] focus:bg-white/10 transition-all text-sm shadow-[inset_0_1px_2px_rgba(255,255,255,0.05)]"
                    required
                  />
                </div>
                <div className="relative w-full">
                  <FaEnvelope className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="E-mail Agrícola"
                    className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-stone-400 focus:outline-none focus:border-[#91a030] focus:bg-white/10 transition-all text-sm shadow-[inset_0_1px_2px_rgba(255,255,255,0.05)]"
                    required
                  />
                </div>
                <div className="relative w-full">
                  <FaLock className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Defina uma Senha"
                    className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-stone-400 focus:outline-none focus:border-[#91a030] focus:bg-white/10 transition-all text-sm shadow-[inset_0_1px_2px_rgba(255,255,255,0.05)]"
                    required
                  />
                </div>
                <div className="relative w-full">
                  <FaLock className="absolute left-4 top-1/2 -translate-y-1/2 text-stone-400" />
                  <input
                    type="password"
                    name="password_confirm"
                    value={formData.password_confirm}
                    onChange={handleChange}
                    placeholder="Confirme a Senha"
                    className="w-full pl-12 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-stone-400 focus:outline-none focus:border-[#91a030] focus:bg-white/10 transition-all text-sm shadow-[inset_0_1px_2px_rgba(255,255,255,0.05)]"
                    required
                  />
                </div>

                {feedback.message && (
                  <p className={`text-sm ${feedback.type === 'error' ? 'text-red-400' : 'text-emerald-400'}`}>
                    {feedback.message}
                  </p>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full mt-4 py-3 rounded-xl text-white font-semibold shadow-lg shadow-[#91a030]/20 hover:shadow-[#91a030]/40 active:scale-[0.98] transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
                  style={{ backgroundImage: 'linear-gradient(90deg, #91a030 0%, #5d6b18 100%)' }}
                >
                  {loading ? 'Aguarde...' : 'Cadastrar Agora'}
                </button>
              </form>
            </div>
          )}

          <div className="mt-6 text-sm text-stone-400 md:hidden">
            {isSignIn ? 'Novo por aqui?' : 'Já possui conta?'}{' '}
            <button
              onClick={() => {
                setIsSignIn(!isSignIn);
                setFeedback({ type: '', message: '' });
              }}
              className="text-[#91a030] font-semibold underline"
            >
              {isSignIn ? 'Cadastre-se' : 'Entre aqui'}
            </button>
          </div>
        </div>

        <div
          className={`max-md:hidden md:flex w-1/2 flex-col justify-center items-center text-center p-12 transition-all duration-700 ease-in-out relative border-l border-white/10
            ${isSignIn
              ? ''
              : '-translate-x-full border-r border-l-0 border-white/10 order-first'
            }`}
          style={{
            backgroundImage: 'linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.01) 100%)',
            boxShadow: 'inset 0 20px 40px rgba(255,255,255,0.05), inset 0 -20px 40px rgba(0,0,0,0.2)'
          }}
        >
          {isSignIn ? (
            <div className="animate-fadeIn flex flex-col items-center">
              <h2 className="text-3xl font-bold text-white mb-4">Olá, Amigo do Campo!</h2>
              <p className="text-stone-300 text-sm leading-relaxed mb-8 max-w-70">
                Entre com seus dados para gerenciar sua colheita, monitorar o gado e acessar nosso ecossistema agro.
              </p>
              <button
                onClick={() => {
                  setIsSignIn(false);
                  setFeedback({ type: '', message: '' });
                }}
                className="px-10 py-3 rounded-xl border border-white/30 text-white font-medium backdrop-blur-md bg-white/5 hover:bg-white/10 active:scale-[0.98] transition-all duration-200 shadow-md"
              >
                Criar Conta
              </button>
            </div>
          ) : (
            <div className="animate-fadeIn flex flex-col items-center">
              <h2 className="text-3xl font-bold text-white mb-4">Bem-vindo de Volta!</h2>
              <p className="text-stone-300 text-sm leading-relaxed mb-8 max-w-70">
                Mantenha-se conectado com a sua terra. Faça login para continuar acompanhando sua produção.
              </p>
              <button
                onClick={() => {
                  setIsSignIn(true);
                  setFeedback({ type: '', message: '' });
                }}
                className="px-10 py-3 rounded-xl border border-white/30 text-white font-medium backdrop-blur-md bg-white/5 hover:bg-white/10 active:scale-[0.98] transition-all duration-200 shadow-md"
              >
                Já sou Cliente
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}