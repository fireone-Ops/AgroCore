import React, { useEffect, useMemo, useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import api from '../services/api';
import {
  FaSeedling,
  FaWarehouse,
  FaTractor,
  FaExclamationCircle,
  FaCheckCircle,
  FaTrash,
  FaEdit,
} from 'react-icons/fa';

export default function DashboardHome({ onLogout }) {
  const [tabAtual, setTabAtual] = useState('dashboard');
  const [fazendas, setFazendas] = useState([]);
  const [acessos, setAcessos] = useState([]);
  const [plantios, setPlantios] = useState([]);
  const [estoque, setEstoque] = useState([]);
  const [maquinarios, setMaquinarios] = useState([]);
  const [alertas, setAlertas] = useState([]);
  const [fazendaAtual, setFazendaAtual] = useState('');
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ nome: '', localizacao: '', cidade: '', estado: '', area_total: '' });
  const [editandoFazendaId, setEditandoFazendaId] = useState(null);
  const [acessoForm, setAcessoForm] = useState({ fazenda: '', email: '', perfil: 'operador' });
  const [feedback, setFeedback] = useState('');

  const carregarAlertas = async (fazendaId) => {
    if (!fazendaId) {
      setAlertas([]);
      return;
    }

    try {
      const response = await api.get('/alertas/alertas/', {
        params: { fazenda: fazendaId, nao_lidos: 'true' },
      });
      setAlertas(response.data || []);
    } catch (error) {
      console.error('Erro ao carregar alertas:', error);
      setAlertas([]);
    }
  };

  const carregarDados = async () => {
    try {
      const [fazendasRes, acessosRes, plantiosRes, estoqueRes] = await Promise.all([
        api.get('/fazendas/'),
        api.get('/fazendas/acessos/'),
        api.get('/culturas/plantios/'),
        api.get('/estoque/itens/'),
      ]);
      setFazendas(fazendasRes.data || []);
      setAcessos(acessosRes.data || []);
      setPlantios(plantiosRes.data || []);
      setEstoque(estoqueRes.data || []);
      if ((fazendasRes.data || []).length) {
        const primeira = fazendasRes.data[0];
        setFazendaAtual(primeira.id.toString());
        setAcessoForm((prev) => ({ ...prev, fazenda: primeira.id.toString() }));
      }
    } catch (error) {
      console.error(error);
      setFeedback('Não foi possível carregar todos os dados do backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  useEffect(() => {
    carregarAlertas(fazendaAtual);
  }, [fazendaAtual]);

  const totalArea = useMemo(() => {
    return fazendas.reduce((acc, item) => acc + Number(item.area_total || 0), 0);
  }, [fazendas]);

  const salvarFazenda = async (event) => {
    event.preventDefault();
    try {
      const payload = {
        nome: form.nome,
        localizacao: form.localizacao,
        cidade: form.cidade,
        estado: form.estado,
        area_total: Number(form.area_total || 0),
      };
      if (editandoFazendaId) {
        const response = await api.patch(`/fazendas/${editandoFazendaId}/`, payload);
        setFazendas((prev) => prev.map((item) => (item.id === editandoFazendaId ? response.data : item)));
        setFeedback('Fazenda atualizada com sucesso.');
      } else {
        const response = await api.post('/fazendas/', payload);
        setFazendas((prev) => [response.data, ...prev]);
        setFeedback('Fazenda criada com sucesso.');
      }
      setForm({ nome: '', localizacao: '', cidade: '', estado: '', area_total: '' });
      setEditandoFazendaId(null);
    } catch (error) {
      setFeedback('Erro ao salvar fazenda.');
    }
  };

  const editarFazenda = (fazenda) => {
    setEditandoFazendaId(fazenda.id);
    setForm({
      nome: fazenda.nome,
      localizacao: fazenda.localizacao || '',
      cidade: fazenda.cidade || '',
      estado: fazenda.estado || '',
      area_total: fazenda.area_total || '',
    });
  };

  const removerFazenda = async (id) => {
    try {
      await api.delete(`/fazendas/${id}/`);
      setFazendas((prev) => prev.filter((item) => item.id !== id));
      setFeedback('Fazenda removida com sucesso.');
    } catch (error) {
      setFeedback('Erro ao remover fazenda.');
    }
  };

  const criarAcesso = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post('/fazendas/acessos/', {
        fazenda: Number(acessoForm.fazenda),
        email: acessoForm.email,
        perfil: acessoForm.perfil,
      });
      setAcessos((prev) => [response.data, ...prev]);
      setAcessoForm((prev) => ({ ...prev, email: '' }));
      setFeedback('Acesso criado com sucesso.');
    } catch (error) {
      setFeedback('Erro ao criar acesso.');
    }
  };

  const removerAcesso = async (id) => {
    try {
      await api.delete(`/fazendas/acessos/${id}/`);
      setAcessos((prev) => prev.filter((item) => item.id !== id));
      setFeedback('Acesso removido com sucesso.');
    } catch (error) {
      setFeedback('Erro ao remover acesso.');
    }
  };

  return (
    <div className="min-h-screen w-full text-white font-sans flex overflow-hidden relative" style={{ backgroundImage: 'linear-gradient(135deg, #0c1f14 0%, #142d1e 50%, #08140e 100%)' }}>
      
      {/* Luzes orgânicas de fundo */}
      <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-emerald-700/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[45vw] h-[45vw] rounded-full bg-amber-600/5 blur-[120px] pointer-events-none" />

      {/* COMPONENTE DA SIDEBAR */}
      <Sidebar tabAtual={tabAtual} setTabAtual={setTabAtual} onLogout={onLogout} />

      {/* CONTAINER CONTEÚDO DIREITO */}
      <div className="flex-1 flex flex-col overflow-hidden z-10">
        
        {/* COMPONENTE DO HEADER */}
<Header fazenda={fazendaAtual} setFazenda={setFazendaAtual} fazendas={fazendas} />

        {/* CONTEÚDO PRINCIPAL (MÓDULOS) */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6">

          {/* TAB 1: DASHBOARD CENTRAL */}
          {tabAtual === 'dashboard' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl flex items-center justify-between shadow-xl">
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Fazendas</span>
                    <h3 className="text-2xl font-bold text-white mt-1">{fazendas.length}</h3>
                  </div>
                  <div className="w-12 h-12 rounded-xl bg-lime-500/10 border border-lime-500/20 text-lime-400 flex items-center justify-center text-xl shadow-inner"><FaSeedling /></div>
                </div>
                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl flex items-center justify-between shadow-xl">
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Área Total</span>
                    <h3 className="text-2xl font-bold text-white mt-1">{totalArea.toFixed(2)} ha</h3>
                  </div>
                  <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center text-xl shadow-inner"><FaWarehouse /></div>
                </div>
                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl flex items-center justify-between shadow-xl">
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Colaboradores</span>
                    <h3 className="text-2xl font-bold text-white mt-1">{acessos.length}</h3>
                  </div>
                  <div className="w-12 h-12 rounded-xl bg-sky-500/10 border border-sky-500/20 text-sky-400 flex items-center justify-center text-xl shadow-inner"><FaTractor /></div>
                </div>
              </div>
              {alertas.length > 0 && (
                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl shadow-xl">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h2 className="text-white font-bold text-base">Alertas recentes</h2>
                      <p className="text-zinc-400 text-sm">Somente alertas reais emitidos pelo sistema.</p>
                    </div>
                    <span className="text-xs uppercase tracking-wider text-amber-400 font-semibold">{alertas.length} não lido(s)</span>
                  </div>
                  <div className="space-y-3">
                    {alertas.map((item) => (
                      <div key={item.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <div className="text-sm font-semibold text-white">{item.titulo}</div>
                            <p className="text-zinc-400 text-sm mt-1">{item.descricao}</p>
                          </div>
                          <div className="flex flex-col items-end gap-2 text-right">
                            <span className="inline-flex items-center gap-2 text-amber-300 text-sm font-semibold"><FaExclamationCircle />{item.severidade}</span>
                            <span className="text-xs uppercase tracking-wider text-zinc-400">{item.status.replace('_', ' ')}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl shadow-xl">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-white font-bold text-base tracking-wide">Cadastrar fazenda</h2>
                  </div>
                  <form className="space-y-3" onSubmit={salvarFazenda}>
                    <input className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm" placeholder="Nome da fazenda" value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} required />
                    <input className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm" placeholder="Localização" value={form.localizacao} onChange={(e) => setForm({ ...form, localizacao: e.target.value })} />
                    <div className="grid grid-cols-2 gap-3">
                      <input className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm" placeholder="Cidade" value={form.cidade} onChange={(e) => setForm({ ...form, cidade: e.target.value })} />
                      <input className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm" placeholder="Estado" value={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.value })} />
                    </div>
                    <input className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm" placeholder="Área total (ha)" type="number" value={form.area_total} onChange={(e) => setForm({ ...form, area_total: e.target.value })} />
                    <button type="submit" className="w-full rounded-xl bg-lime-600 px-3 py-2 text-sm font-semibold">{editandoFazendaId ? 'Salvar alterações' : 'Criar fazenda'}</button>
                  </form>
                </div>

                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl shadow-xl">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-white font-bold text-base tracking-wide">Conceder acesso a colaborador</h2>
                  </div>
                  <form className="space-y-3" onSubmit={criarAcesso}>
                    <select className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm" value={acessoForm.fazenda} onChange={(e) => setAcessoForm({ ...acessoForm, fazenda: e.target.value })}>
                      {fazendas.map((item) => (
                        <option value={item.id} key={item.id}>{item.nome}</option>
                      ))}
                    </select>
                    <input className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-sm" placeholder="E-mail do colaborador" value={acessoForm.email} onChange={(e) => setAcessoForm({ ...acessoForm, email: e.target.value })} required />
                    <select className="w-full rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-white text-sm" value={acessoForm.perfil} onChange={(e) => setAcessoForm({ ...acessoForm, perfil: e.target.value })}>
                      <option value="operador" className="text-black">Operador</option>
                      <option value="agronomo" className="text-black">Agrônomo</option>
                      <option value="gerente" className="text-black">Gerente</option>
                    </select>
                    <button type="submit" className="w-full rounded-xl bg-amber-600 px-3 py-2 text-sm font-semibold">Adicionar acesso</button>
                  </form>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl shadow-xl">
                  <h2 className="text-white font-bold text-base tracking-wide border-b border-white/5 pb-3">Fazendas cadastradas</h2>
                  {fazendas.length === 0 ? (
                    <p className="text-zinc-400 text-sm mt-3">Nenhuma fazenda cadastrada ainda.</p>
                  ) : (
                    <ul className="mt-3 space-y-2">
                      {fazendas.map((item) => (
                        <li key={item.id} className="rounded-xl border border-white/10 bg-white/5 p-3 text-sm flex items-start justify-between gap-3">
                          <div>
                            <div className="font-semibold text-white">{item.nome}</div>
                            <div className="text-zinc-400">{item.cidade || 'Cidade não informada'} / {item.estado || 'UF'}</div>
                            <div className="text-zinc-400">{item.area_total || 0} ha</div>
                          </div>
                          <div className="flex gap-2">
                            <button onClick={() => editarFazenda(item)} className="rounded-lg border border-white/10 bg-white/10 p-2 text-white"><FaEdit /></button>
                            <button onClick={() => removerFazenda(item.id)} className="rounded-lg border border-red-500/20 bg-red-500/10 p-2 text-red-400"><FaTrash /></button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>

                <div className="bg-white/2 backdrop-blur-md border border-white/10 p-5 rounded-2xl shadow-xl">
                  <h2 className="text-white font-bold text-base tracking-wide border-b border-white/5 pb-3">Acessos de colaboradores</h2>
                  {acessos.length === 0 ? (
                    <p className="text-zinc-400 text-sm mt-3">Nenhum acesso cadastrado.</p>
                  ) : (
                    <ul className="mt-3 space-y-2">
                      {acessos.map((item) => (
                        <li key={item.id} className="rounded-xl border border-white/10 bg-white/5 p-3 text-sm flex items-center justify-between gap-3">
                          <div>
                            <div className="font-semibold text-white">{item.usuario_nome || item.usuario_email}</div>
                            <div className="text-zinc-400">{item.usuario_email}</div>
                            <div className="text-zinc-400">{item.perfil}</div>
                          </div>
                          <button onClick={() => removerAcesso(item.id)} className="rounded-lg border border-red-500/20 bg-red-500/10 p-2 text-red-400"><FaTrash /></button>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: MÓDULO AGRÍCOLA */}
          {tabAtual === 'agricola' && (
            <div className="bg-white/2 backdrop-blur-md border border-white/10 p-6 rounded-2xl shadow-xl">
              <h2 className="text-white font-bold text-lg mb-4 tracking-wide border-b border-white/5 pb-2">Gerenciamento de Plantio e Colheita</h2>
              {plantios.length === 0 ? (
                <div className="text-zinc-400 text-sm">Nenhum plantio cadastrado ainda. Cadastre uma fazenda e adicione plantios para ver os dados aqui.</div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="border-b border-white/10 text-zinc-400 text-xs uppercase tracking-wider font-semibold">
                        <th className="p-3">Cultura</th>
                        <th className="p-3">Área (ha)</th>
                        <th className="p-3">Início do Plantio</th>
                        <th className="p-3">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5 text-zinc-300">
                      {plantios.map((item) => (
                        <tr key={item.id} className="hover:bg-white/1 transition-colors">
                          <td className="p-3 font-medium text-white">{item.cultura || '—'}</td>
                          <td className="p-3">{item.area_plantada || '—'} ha</td>
                          <td className="p-3">{item.data_plantio || '—'}</td>
                          <td className="p-3"><span className="bg-amber-500/10 text-amber-300 border border-amber-500/20 px-2.5 py-0.5 rounded-full text-xs font-medium">{item.status || '—'}</span></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: ALMOXARIFADO */}
          {tabAtual === 'almoxarifado' && (
            <div className="bg-white/2 backdrop-blur-md border border-white/10 p-6 rounded-2xl shadow-xl">
              <h2 className="text-white font-bold text-lg mb-4 tracking-wide border-b border-white/5 pb-2">Controle de Estoque (Insumos)</h2>
              {estoque.length === 0 ? (
                <div className="text-zinc-400 text-sm">Nenhum item de estoque registrado ainda. Registre insumos para acompanhar níveis e alertas.</div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {estoque.map((item) => (
                    <div key={item.id} className="p-4 rounded-xl border border-white/5 bg-white/1 flex justify-between items-center shadow-inner">
                      <div>
                        <h4 className="font-bold text-zinc-200">{item.nome}</h4>
                        <p className="text-xs text-zinc-500 mt-0.5">Mínimo exigido: {item.estoque_minimo || 0} {item.unidade}</p>
                      </div>
                      <span className={`font-bold text-sm px-3 py-1 rounded-xl ${item.estoque_minimo && item.estoque_atual <= item.estoque_minimo ? 'text-red-400 bg-red-500/10 border border-red-500/20' : 'text-lime-400 bg-lime-500/10 border border-lime-500/20'}`}>
                        {(item.estoque_atual || 0).toFixed(1)} {item.unidade}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 4: MAQUINÁRIO */}
          {tabAtual === 'maquinario' && (
            <div className="bg-white/2 backdrop-blur-md border border-white/10 p-6 rounded-2xl shadow-xl">
              <div className="mb-4 border-b border-white/5 pb-2">
                <h2 className="text-white font-bold text-lg tracking-wide">Módulo de Maquinário Ativo</h2>
                <p className="text-xs text-zinc-500 mt-0.5">Rastreamento de telemetria e conectividade em campo.</p>
              </div>
              <div className="text-zinc-400 text-sm">Nenhum maquinário cadastrado ainda. Quando houver máquinas registradas, você verá o status e a telemetria aqui.</div>
            </div>
          )}

        </main>
      </div>
    </div>
  );
}