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

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(300), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    ordem = db.Column(db.Integer, default=0)
    disciplina = db.relationship('Disciplina', backref='topicos')

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

class Revisao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topico_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
    tipo = db.Column(db.String(10))
    data_agendada = db.Column(db.DateTime)
    concluida = db.Column(db.Boolean, default=False)
    questoes = db.Column(db.Integer, default=0)
    acertos = db.Column(db.Integer, default=0)

# ==================== HELPERS ====================
def get_topico(topico_id):
    if topico_id:
        return Topico.query.get(topico_id)
    return None

# ==================== SEED ====================
def seed_database():
    if Disciplina.query.count() > 0:
        return
    
    disciplinas_data = [
        ('Português', 'Básico', '#e53935', ['Compreensão e interpretação de textos', 'Tipologia textual', 'Ortografia oficial', 'Acentuação gráfica', 'Emprego das classes de palavras', 'Emprego do sinal indicativo de crase', 'Sintaxe da oração e do período', 'Pontuação', 'Concordância nominal e verbal', 'Regência nominal e verbal', 'Significação das palavras', 'Redação de correspondências oficiais']),
        ('Inglês', 'Básico', '#1e88e5', ['Compreensão de texto escrito em Língua Inglesa', 'Itens gramaticais relevantes']),
        ('Raciocínio Lógico', 'Básico', '#8e24aa', ['Estruturas lógicas', 'Lógica de argumentação', 'Diagramas lógicos', 'Trigonometria', 'Matrizes e determinantes', 'Álgebra', 'Combinações e permutação', 'Probabilidade', 'Estatística descritiva', 'Números complexos', 'Geometria básica', 'Juros simples e compostos']),
        ('Estatística', 'Básico', '#fb8c00', ['Medidas de posição', 'Medidas de dispersão', 'Distribuições de frequências', 'Probabilidade', 'Distribuições: binomial e normal', 'Amostragem', 'Estimação', 'Teste de hipóteses', 'Regressão linear', 'Correlação']),
        ('Economia e Finanças', 'Básico', '#43a047', ['Oferta e demanda', 'Teoria do consumidor', 'Teoria da firma', 'Estruturas de mercado', 'Agregados macroeconômicos', 'IS-LM', 'OA-DA', 'Inflação', 'Política monetária e fiscal', 'Funções do governo', 'Despesa pública', 'Receita pública', 'Déficit e dívida']),
        ('Administração Geral', 'Básico', '#00acc1', ['Teorias administrativas', 'Planejamento', 'Organização', 'Direção', 'Controle', 'Estrutura organizacional', 'Cultura organizacional', 'Gestão de pessoas', 'Motivação', 'Liderança', 'Comunicação', 'Gestão da qualidade']),
        ('Administração Pública', 'Básico', '#5e35b1', ['Estado e Administração', 'Evolução no Brasil', 'Processo administrativo', 'Princípios', 'Governança', 'Orçamento público', 'Ciclo orçamentário', 'Lei 4.320/1964', 'LRF', 'PPA', 'LDO', 'LOA']),
        ('Auditoria', 'Básico', '#d81b60', ['Conceitos', 'Normas do auditor', 'Normas de execução', 'Normas do parecer', 'Ética', 'Planejamento', 'Risco', 'Relevância', 'Evidência', 'Procedimentos', 'Testes', 'Papéis de trabalho', 'Amostragem', 'Relatório']),
        ('Contabilidade Geral', 'Básico', '#f4511e', ['Estrutura conceitual', 'Patrimônio', 'Fatos contábeis', 'Contas', 'Regimes', 'Provisões', 'Ativo', 'Estoques', 'Imobilizado', 'Passivo', 'PL', 'Balanço', 'DRE', 'DFC', 'DVA', 'Análise', 'Custos']),
        ('Contabilidade Pública', 'Básico', '#f57c00', ['Conceito', 'Princípios', 'PCASP', 'DCASP', 'Balanço Orçamentário', 'Balanço Financeiro', 'Balanço Patrimonial', 'DVP', 'Procedimentos orçamentários', 'Procedimentos patrimoniais', 'Dívida ativa']),
        ('Fluência em TI', 'Básico', '#00897b', ['Sistemas computacionais', 'Arquitetura', 'SO', 'Redes', 'Segurança', 'Banco de dados', 'SQL', 'Big Data', 'ETL', 'Data warehouse', 'BI']),
        ('Direito Administrativo', 'Específico', '#3949ab', ['Estado e governo', 'Organização administrativa', 'Ato administrativo', 'Anulação e revogação', 'Poderes', 'Controle', 'Responsabilidade civil', 'Lei 8.429 - Improbidade', 'Lei 9.784 - PAF', 'Lei 14.133 - Licitações', 'Lei 8.112 - RJU']),
        ('Direito Constitucional', 'Específico', '#1976d2', ['Constituição', 'Poder constituinte', 'Princípios fundamentais', 'Direitos fundamentais', 'Nacionalidade', 'Direitos políticos', 'Organização do Estado', 'Poder Executivo', 'Poder Legislativo', 'Poder Judiciário', 'Controle de constitucionalidade', 'Sistema Tributário', 'Finanças públicas']),
        ('Direito Previdenciário', 'Específico', '#0288d1', ['Seguridade social', 'RGPS', 'Segurados', 'Salário-de-contribuição', 'Aposentadorias', 'Auxílios', 'Pensão', 'Salário-família', 'Carência', 'Cálculo', 'Custeio', 'Contribuições']),
        ('Direito Tributário', 'Específico', '#c62828', ['Competência tributária', 'Princípios', 'Imunidades', 'Tributos', 'Obrigação tributária', 'Fato gerador', 'Sujeição', 'Responsabilidade', 'Crédito tributário', 'Lançamento', 'Suspensão', 'Extinção', 'Garantias', 'Fiscalização']),
        ('Legislação Tributária', 'Específico', '#ad1457', ['IRPF', 'IRPJ', 'IPI', 'PIS/COFINS', 'CSLL', 'Simples Nacional', 'PAF', 'Ilícito tributário']),
        ('Comércio Internacional', 'Específico', '#6a1b9a', ['Teoria', 'Balança comercial', 'Vantagens comparativas', 'Políticas', 'Incoterms', 'OMC', 'Mercosul', 'Tarifas', 'NCM', 'SH']),
        ('Legislação Aduaneira', 'Específico', '#4a148c', ['Jurisdição aduaneira', 'Tributos', 'II e IE', 'Regimes especiais', 'Despacho de importação', 'Despacho de exportação', 'Infrações', 'Pena de perdimento', 'Processo administrativo'])
    ]
    
    for nome, modulo, cor, topicos_lista in disciplinas_data:
        disc = Disciplina(nome=nome, modulo=modulo, cor=cor)
        db.session.add(disc)
        db.session.flush()
        
        for i, topico_nome in enumerate(topicos_lista):
            top = Topico(nome=topico_nome, disciplina_id=disc.id, ordem=i+1)
            db.session.add(top)
    
    db.session.commit()
    
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
    
    # Adicionar tópicos ao dia_atual
    if dia_atual:
        dia_atual.topico1 = get_topico(dia_atual.topico1_id)
        dia_atual.topico2 = get_topico(dia_atual.topico2_id)
        dia_atual.topico3 = get_topico(dia_atual.topico3_id)
    
    return render_template('dashboard.html', dia_atual=dia_atual, total_horas=total_horas, total_questoes=total_questoes, taxa_acerto=taxa_acerto, dias_concluidos=dias_concluidos, revisoes_pendentes=revisoes_pendentes)

@app.route('/dia/<int:dia_id>')
def dia_detalhe(dia_id):
    dia = DiaCiclo.query.get_or_404(dia_id)
    dia.topico1 = get_topico(dia.topico1_id)
    dia.topico2 = get_topico(dia.topico2_id)
    dia.topico3 = get_topico(dia.topico3_id)
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
    for rev in revs:
        rev.topico = get_topico(rev.topico_id)
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
    
