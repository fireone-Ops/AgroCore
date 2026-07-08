import React from 'react';
import { 
  FaChartPie, FaSeedling, FaWarehouse, FaTractor, 
  FaShieldAlt, FaSignOutAlt 
} from 'react-icons/fa';

export default function Sidebar({ tabAtual, setTabAtual, onLogout }) {
  const menuItens = [
    { id: 'dashboard', label: 'Dashboard', icon: FaChartPie },
    { id: 'agricola', label: 'Módulo Agrícola', icon: FaSeedling },
    { id: 'almoxarifado', label: 'Almoxarifado', icon: FaWarehouse },
    { id: 'maquinario', label: 'Maquinário', icon: FaTractor },
  ];

  return (
    <aside className="w-64 backdrop-blur-xl border-r border-white/10 max-md:hidden md:flex md:flex-col md:justify-between md:shrink-0 z-10" style={{ backgroundColor: 'rgba(255,255,255,0.02)' }}>
      <div>
        {/* Brand/Logo */}
        <div className="p-5 flex items-center gap-3 border-b border-white/10">
          <FaShieldAlt className="text-2xl text-amber-500 drop-shadow-[0_0_8px_rgba(245,158,11,0.4)]" />
          <div>
            <h1 className="font-bold text-lg leading-tight tracking-wide">AgroCore</h1>
            <span className="text-xs text-lime-500/80 font-medium tracking-wider uppercase">Plataforma</span>
          </div>
        </div>
        
        {/* Navegação */}
        <nav className="p-4 space-y-1.5">
          {menuItens.map((item) => {
            const Icon = item.icon;
            const ativo = tabAtual === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setTabAtual(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all duration-300
                  ${ativo 
                    ? 'bg-lime-600/20 border border-lime-500/30 text-lime-400 shadow-[inset_0_1px_1px_rgba(255,255,255,0.1)]' 
                    : 'text-zinc-400 hover:bg-white/5 hover:text-white border border-transparent'
                  }`}
              >
                <Icon className={`text-base ${ativo ? 'text-lime-400' : 'text-zinc-400'}`} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Perfil do Produtor */}
      <div className="p-4 border-t border-white/10 bg-black/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-sm shadow-md" style={{ backgroundImage: 'linear-gradient(135deg, #65a30d 0%, #047857 100%)' }}>
            P
          </div>
          <div>
            <p className="text-sm font-semibold leading-tight">Produtor</p>
            <span className="text-[11px] text-lime-500/80 font-medium">Acesso Total</span>
          </div>
        </div>
        <button 
          onClick={onLogout}
          className="p-2 rounded-lg bg-white/5 hover:bg-red-900/40 border border-white/5 hover:border-red-500/30 text-zinc-400 hover:text-red-400 transition-all"
          title="Sair do Sistema"
        >
          <FaSignOutAlt size={14} />
        </button>
      </div>
    </aside>
  );
}