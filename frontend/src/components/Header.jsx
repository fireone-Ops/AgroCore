import React from 'react';
import { FaChevronDown } from 'react-icons/fa';

export default function Header({ fazenda, setFazenda, fazendas = [] }) {
  return (
    <header className="backdrop-blur-md border-b border-white/10 px-6 py-4 flex items-center justify-between shrink-0" style={{ backgroundColor: 'rgba(255,255,255,0.1)' }}>
      <div className="relative">
        <select 
          value={fazenda || ''}
          onChange={(e) => setFazenda(e.target.value)}
          className="appearance-none bg-white/5 border border-white/10 text-white text-sm rounded-xl pl-4 pr-10 py-2 font-medium focus:outline-none focus:border-lime-500 cursor-pointer transition-all"
          disabled={fazendas.length === 0}
        >
          <option value="" disabled className="bg-[#142d1e] text-zinc-400">
            {fazendas.length ? 'Selecione uma fazenda' : 'Nenhuma fazenda cadastrada'}
          </option>
          {fazendas.map((item) => (
            <option key={item.id} value={item.id} className="bg-[#142d1e]">
              {item.nome}
            </option>
          ))}
        </select>
        <FaChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none text-xs" />
      </div>
      <div className="flex items-center gap-4">
        <span className="text-xs tracking-wider uppercase text-zinc-400">
          Perfil: <strong className="text-white font-semibold">Administrador</strong>
        </span>
      </div>
    </header>
  );
}