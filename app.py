from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cronograma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== MODELS ====================
class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    modulo = db.Column(db.String(50))
    cor = db.Column(db.String(7), default='#1e88e5')
    topicos = db.relationship('Topico', backref='disciplina', lazy=True)

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    ordem = db.Column(db.Integer, default=0)

class DiaCiclo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    topico1_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
    topico2_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
    topico3_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
    data_conclusao = db.Column(db.DateTime)
    questoes = db.Column(db.Integer, default=0)
    acertos = db.Column(db.Integer, default=0)
    minutos = db.Column(db.Integer, default=0)
    
    topico1 = db.relationship('Topico', foreign_keys=[topico1_id])
    topico2 = db.relationship('Topico', foreign_keys=[topico2_id])
    topico3 = db.relationship('Topico', foreign_keys=[topico3_id])

class Revisao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topico_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
    tipo = db.Column(db.String(10))
    data_agendada = db.Column(db.DateTime)
    concluida = db.Column(db.Boolean, default=False)
    questoes = db.Column(db.Integer, default=0)
    acertos = db.Column(db.Integer, default=0)
    
    topico = db.relationship('Topico', backref='revisoes')

# ==================== SEED ====================
def seed_database():
    if Disciplina.query.count() > 0:
        return
    
    # Português
    port = Disciplina(nome='Português', modulo='Básico', cor='#e53935')
    db.session.add(port)
    db.session.flush()
    for i, t in enumerate(['Compreensão e interpretação de textos', 'Tipologia textual', 'Ortografia oficial', 'Acentuação gráfica', 'Emprego das classes de palavras', 'Emprego do sinal indicativo de crase', 'Sintaxe da oração e do período', 'Pontuação', 'Concordância nominal e verbal', 'Regência nominal e verbal', 'Significação das palavras', 'Redação de correspondências oficiais']):
        db.session.add(Topico(nome=t, disciplina_id=port.id, ordem=i+1))
    
    # Inglês
    ing = Disciplina(nome='Inglês', modulo='Básico', cor='#1e88e5')
    db.session.add(ing)
    db.session.flush()
    for i, t in enumerate(['Compreensão de texto escrito em Língua Inglesa', 'Itens gramaticais relevantes para compreensão dos conteúdos semânticos']):
        db.session.add(Topico(nome=t, disciplina_id=ing.id, ordem=i+1))
    
    # RLM
    rlm = Disciplina(nome='Raciocínio Lógico-Matemático', modulo='Básico', cor='#8e24aa')
    db.session.add(rlm)
    db.session.flush()
    for i, t in enumerate(['Estruturas lógicas', 'Lógica de argumentação', 'Diagramas lógicos', 'Trigonometria', 'Matrizes, determinantes e sistemas lineares', 'Álgebra', 'Combinações, arranjos e permutação', 'Probabilidade e variáveis aleatórias', 'Estatística descritiva', 'Números complexos', 'Geometria básica', 'Juros simples e compostos']):
        db.session.add(Topico(nome=t, disciplina_id=rlm.id, ordem=i+1))
    
    # Estatística
    est = Disciplina(nome='Estatística', modulo='Básico', cor='#fb8c00')
    db.session.add(est)
    db.session.flush()
    for i, t in enumerate(['Medidas de posição', 'Medidas de dispersão', 'Distribuições de frequências', 'Probabilidade: conceitos básicos', 'Distribuições: binomial, normal', 'Amostragem', 'Distribuições amostrais', 'Estimação pontual e intervalar', 'Teste de hipóteses', 'Análise de regressão linear', 'Análise de correlação']):
        db.session.add(Topico(nome=t, disciplina_id=est.id, ordem=i+1))
    
    # Economia
    eco = Disciplina(nome='Economia e Finanças Públicas', modulo='Básico', cor='#43a047')
    db.session.add(eco)
    db.session.flush()
    for i, t in enumerate(['Oferta e demanda', 'Teoria do consumidor', 'Teoria da firma', 'Estruturas de mercado', 'Agregados macroeconômicos', 'Sistema de Contas Nacionais', 'Modelo IS-LM', 'Modelo OA-DA', 'Inflação e desemprego', 'Política monetária e fiscal', 'Funções do governo', 'Despesa pública', 'Receita pública', 'Déficit e dívida pública']):
        db.session.add(Topico(nome=t, disciplina_id=eco.id, ordem=i+1))
    
    # Adm Geral
    adm = Disciplina(nome='Administração Geral', modulo='Básico', cor='#00acc1')
    db.session.add(adm)
    db.session.flush()
    for i, t in enumerate(['Teorias e escolas', 'Planejamento', 'Organização', 'Direção', 'Controle', 'Estrutura organizacional', 'Cultura organizacional', 'Gestão de pessoas', 'Motivação', 'Liderança', 'Clima e comunicação', 'Gestão da qualidade']):
        db.session.add(Topico(nome=t, disciplina_id=adm.id, ordem=i+1))
    
    # Adm Pública
    adp = Disciplina(nome='Administração Pública', modulo='Básico', cor='#5e35b1')
    db.session.add(adp)
    db.session.flush()
    for i, t in enumerate(['Estado e Administração Pública', 'Evolução da administração pública no Brasil', 'Processo administrativo', 'Princípios da administração pública', 'Governança e governabilidade', 'Orçamento público', 'Ciclo orçamentário', 'Lei 4.320/1964', 'LRF - Lei 101/2000', 'PPA', 'LDO', 'LOA']):
        db.session.add(Topico(nome=t, disciplina_id=adp.id, ordem=i+1))
    
    # Auditoria
    aud = Disciplina(nome='Auditoria', modulo='Básico', cor='#d81b60')
    db.session.add(aud)
    db.session.flush()
    for i, t in enumerate(['Conceitos e objetivos', 'Normas da pessoa do auditor', 'Normas de execução', 'Normas do parecer', 'Ética profissional', 'Planejamento', 'Risco de auditoria', 'Relevância', 'Evidência', 'Procedimentos', 'Testes de observância', 'Testes substantivos', 'Papéis de trabalho', 'Amostragem', 'Eventos subsequentes', 'Revisão analítica', 'Relatório']):
        db.session.add(Topico(nome=t, disciplina_id=aud.id, ordem=i+1))
    
    # Contabilidade Geral
    ctg = Disciplina(nome='Contabilidade Geral e de Custos', modulo='Básico', cor='#f4511e')
    db.session.add(ctg)
    db.session.flush()
    for i, t in enumerate(['Estrutura conceitual', 'Patrimônio', 'Fatos contábeis', 'Contas', 'Apuração de resultados', 'Regimes: caixa e competência', 'Provisões e contingências', 'Políticas contábeis', 'Ativo circulante', 'Estoques', 'Despesas antecipadas', 'Imobilizado e intangível', 'Passivo exigível', 'Patrimônio líquido', 'Balancete', 'Balanço Patrimonial', 'DRE', 'DRA', 'DMPL', 'DFC', 'DVA', 'Análise das demonstrações', 'Contabilidade de custos', 'Custos para estoques', 'Custos para decisões', 'Sistemas de custos', 'Relação custo/volume/lucro']):
        db.session.add(Topico(nome=t, disciplina_id=ctg.id, ordem=i+1))
    
    # Contabilidade Pública
    ctp = Disciplina(nome='Contabilidade Pública', modulo='Básico', cor='#f57c00')
    db.session.add(ctp)
    db.session.flush()
    for i, t in enumerate(['Conceito e campo de aplicação', 'Princípios sob perspectiva pública', 'Sistema de Contabilidade Federal', 'PCASP', 'DCASP', 'Balanço Orçamentário', 'Balanço Financeiro', 'Balanço Patrimonial', 'DVP', 'DFC', 'DMPL', 'Procedimentos orçamentários', 'Procedimentos patrimoniais', 'Operações de crédito', 'RPPS', 'Dívida ativa']):
        db.session.add(Topico(nome=t, disciplina_id=ctp.id, ordem=i+1))
    
    # Fluência TI
    flu = Disciplina(nome='Fluência em TI e Gestão de Dados', modulo='Básico', cor='#00897b')
    db.session.add(flu)
    db.session.flush()
    for i, t in enumerate(['Sistemas computacionais', 'Arquitetura de computadores', 'Sistemas operacionais', 'Redes e Internet', 'Segurança da informação', 'Banco de dados', 'Modelo relacional', 'SQL', 'Big Data', 'ETL', 'Data warehouse', 'BI']):
        db.session.add(Topico(nome=t, disciplina_id=flu.id, ordem=i+1))
    
    # Dir Administrativo
    dad = Disciplina(nome='Direito Administrativo', modulo='Específico', cor='#3949ab')
    db.session.add(dad)
    db.session.flush()
    for i, t in enumerate(['Estado, governo e administração', 'Organização administrativa', 'Agências', 'Ato administrativo', 'Anulação e revogação', 'Prescrição', 'Poderes administrativos', 'Controle da administração', 'Responsabilidade civil do Estado', 'Lei 8.429/1992 - Improbidade', 'Lei 9.784/1999 - PAF', 'Lei 14.133/2021 - Licitações', 'Serviços públicos', 'Lei 8.112/1990 - RJU']):
        db.session.add(Topico(nome=t, disciplina_id=dad.id, ordem=i+1))
    
    # Dir Constitucional
    dco = Disciplina(nome='Direito Constitucional', modulo='Específico', cor='#1976d2')
    db.session.add(dco)
    db.session.flush()
    for i, t in enumerate(['Constituição', 'Supremacia', 'Aplicabilidade das normas', 'Interpretação', 'Poder constituinte', 'Princípios fundamentais', 'Direitos e garantias', 'Direitos individuais e coletivos', 'Direitos sociais', 'Nacionalidade', 'Direitos políticos', 'Organização do Estado', 'Federação', 'Administração pública', 'Poder executivo', 'Poder legislativo', 'Processo legislativo', 'Poder judiciário', 'Ministério Público', 'Advocacia Pública', 'Controle de constitucionalidade', 'Segurança pública', 'Ordem econômica', 'Sistema Tributário Nacional', 'Finanças públicas']):
        db.session.add(Topico(nome=t, disciplina_id=dco.id, ordem=i+1))
    
    # Dir Previdenciário
    dpv = Disciplina(nome='Direito Previdenciário', modulo='Específico', cor='#0288d1')
    db.session.add(dpv)
    db.session.flush()
    for i, t in enumerate(['Seguridade social', 'Conceituação', 'Organização e princípios', 'Legislação previdenciária', 'RGPS', 'Segurados obrigatórios', 'Filiação e inscrição', 'Empregado', 'Empregado doméstico', 'Contribuinte individual', 'Trabalhador avulso', 'Segurado especial', 'Segurado facultativo', 'Salário-de-contribuição', 'Benefícios: aposentadorias', 'Auxílios', 'Pensão por morte', 'Salário-família', 'Salário-maternidade', 'Carência', 'Cálculo de benefícios', 'Reajustamento', 'Acumulação', 'Prescrição e decadência', 'Custeio', 'Contribuições sociais']):
        db.session.add(Topico(nome=t, disciplina_id=dpv.id, ordem=i+1))
    
    # Dir Tributário
    dtr = Disciplina(nome='Direito Tributário', modulo='Específico', cor='#c62828')
    db.session.add(dtr)
    db.session.flush()
    for i, t in enumerate(['Sistema Tributário Nacional', 'Competência tributária', 'Limitações ao poder de tributar', 'Princípios tributários', 'Imunidades', 'Conceito e classificação dos tributos', 'Tributos de cada ente', 'CTN: normas gerais', 'Obrigação tributária', 'Fato gerador', 'Sujeição ativa e passiva', 'Solidariedade', 'Capacidade tributária', 'Domicílio tributário', 'Responsabilidade tributária', 'Responsabilidade dos sucessores', 'Responsabilidade de terceiros', 'Responsabilidade por infrações', 'Denúncia espontânea', 'Crédito tributário', 'Lançamento', 'Modalidades de lançamento', 'Suspensão do crédito', 'Extinção do crédito', 'Pagamento indevido', 'Exclusão do crédito', 'Garantias e privilégios', 'Fiscalização', 'Dívida ativa', 'Certidões negativas']):
        db.session.add(Topico(nome=t, disciplina_id=dtr.id, ordem=i+1))
    
    # Leg Tributária
    ltr = Disciplina(nome='Legislação Tributária', modulo='Específico', cor='#ad1457')
    db.session.add(ltr)
    db.session.flush()
    for i, t in enumerate(['IRPF', 'IRPJ', 'IPI', 'PIS/PASEP', 'COFINS', 'CSLL', 'Simples Nacional', 'Processo Administrativo Fiscal', 'Ilícito tributário']):
        db.session.add(Topico(nome=t, disciplina_id=ltr.id, ordem=i+1))
    
    # Comércio
    com = Disciplina(nome='Comércio Internacional', modulo='Específico', cor='#6a1b9a')
    db.session.add(com)
    db.session.flush()
    for i, t in enumerate(['Teoria do comércio exterior', 'Balança comercial', 'Vantagens comparativas', 'Políticas de comércio exterior', 'Incoterms', 'OMC e GATT', 'Blocos econômicos', 'Mercosul', 'Tarifas aduaneiras', 'Barreiras não tarifárias', 'NCM', 'Sistema Harmonizado']):
        db.session.add(Topico(nome=t, disciplina_id=com.id, ordem=i+1))
    
    # Leg Aduaneira
    lad = Disciplina(nome='Legislação Aduaneira', modulo='Específico', cor='#4a148c')
    db.session.add(lad)
    db.session.flush()
    for i, t in enumerate(['Jurisdição aduaneira', 'Controle de veículos', 'Tributos sobre comércio exterior', 'Imposto de Importação', 'Imposto de Exportação', 'Regimes aduaneiros especiais', 'Áreas especiais', 'Despacho de importação', 'Despacho de exportação', 'Infrações e penalidades', 'Pena de perdimento', 'Aplicação de penalidades', 'Processo administrativo']):
        db.session.add(Topico(nome=t, disciplina_id=lad.id, ordem=i+1))
    
    db.session.commit()
    
    # Gerar primeiros 30 dias
    topicos = Topico.query.all()
    for dia in range(1, 31):
        idx = ((dia-1) * 3) % len(topicos)
        d = DiaCiclo(
            numero=dia,
            topico1_id=topicos[idx].id,
            topico2_id=topicos[(idx+1) % len(topicos)].id,
            topico3_id=topicos[(idx+2) % len(topicos)].id
        )
        db.session.add(d)
    
    db.session.commit()

# ==================== ROTAS ====================
@app.route('/')
def home():
    dia_atual = DiaCiclo.query.filter_by(data_conclusao=None).first()
    if not dia_atual:
        dia_atual = DiaCiclo.query.order_by(DiaCiclo.numero).first()
    
    total_minutos = db.session.query(db.func.sum(DiaCiclo.minutos)).scalar() or 0
    total_horas = total_minutos // 60
    total_questoes = db.session.query(db.func.sum(DiaCiclo.questoes)).scalar() or 0
    total_acertos = db.session.query(db.func.sum(DiaCiclo.acertos)).scalar() or 0
    taxa_acerto = round((total_acertos / total_questoes * 100) if total_questoes > 0 else 0, 1)
    dias_concluidos = DiaCiclo.query.filter(DiaCiclo.data_conclusao != None).count()
    revisoes_pendentes = Revisao.query.filter_by(concluida=False).filter(Revisao.data_agendada <= datetime.now()).count()
    
    return render_template('dashboard.html', dia_atual=dia_atual, total_horas=total_horas, total_questoes=total_questoes, taxa_acerto=taxa_acerto, dias_concluidos=dias_concluidos, revisoes_pendentes=revisoes_pendentes)

@app.route('/dia/<int:dia_id>')
def dia_detalhe(dia_id):
    dia = DiaCiclo.query.get_or_404(dia_id)
    return render_template('dia.html', dia=dia)

@app.route('/concluir_dia/<int:dia_id>', methods=['POST'])
def concluir_dia(dia_id):
    dia = DiaCiclo.query.get_or_404(dia_id)
    dia.data_conclusao = datetime.now()
    dia.questoes = int(request.form.get('questoes', 0))
    dia.acertos = int(request.form.get('acertos', 0))
    dia.minutos = int(request.form.get('minutos', 150))
    
    for topico_id in [dia.topico1_id, dia.topico2_id, dia.topico3_id]:
        if topico_id:
            db.session.add(Revisao(topico_id=topico_id, tipo='24h', data_agendada=datetime.now() + timedelta(hours=24)))
            db.session.add(Revisao(topico_id=topico_id, tipo='7d', data_agendada=datetime.now() + timedelta(days=7)))
            db.session.add(Revisao(topico_id=topico_id, tipo='30d', data_agendada=datetime.now() + timedelta(days=30)))
    
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/disciplinas')
def disciplinas():
    discs = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=discs)

@app.route('/revisoes')
def revisoes():
    revs = Revisao.query.filter_by(concluida=False).order_by(Revisao.data_agendada).all()
    return render_template('revisoes.html', revisoes=revs)

@app.route('/estatisticas')
def estatisticas():
    discs = Disciplina.query.all()
    return render_template('estatisticas.html', disciplinas=discs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(host='0.0.0.0', port=5000)
    
