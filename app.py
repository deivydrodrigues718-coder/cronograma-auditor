from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Configuração do banco
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cronograma.db')
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

# ==================== INICIALIZAÇÃO ====================
with app.app_context():
    try:
        db.create_all()
        print("✅ Banco de dados criado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar banco: {e}")

# ==================== HELPERS ====================
def get_topico(topico_id):
    if topico_id:
        try:
            return Topico.query.get(topico_id)
        except:
            return None
    return None

# ==================== SEED ====================
def seed_database():
    try:
        if Disciplina.query.count() > 0:
            print("✅ Banco já populado.")
            return
    except:
        pass
    
    print("🌱 Populando banco de dados...")
    
    disciplinas_data = [
        ('Português', 'Básico', '#e53935', ['Compreensão de textos', 'Ortografia', 'Acentuação', 'Classes de palavras', 'Crase', 'Sintaxe', 'Pontuação', 'Concordância', 'Regência']),
        ('Inglês', 'Básico', '#1e88e5', ['Reading', 'Gramática']),
        ('Raciocínio Lógico', 'Básico', '#8e24aa', ['Estruturas lógicas', 'Argumentação', 'Diagramas', 'Trigonometria', 'Matrizes', 'Álgebra', 'Combinatória', 'Probabilidade', 'Geometria', 'Juros']),
        ('Estatística', 'Básico', '#fb8c00', ['Medidas de posição', 'Dispersão', 'Distribuições', 'Probabilidade', 'Binomial e Normal', 'Amostragem', 'Estimação', 'Hipóteses', 'Regressão', 'Correlação']),
        ('Economia e Finanças', 'Básico', '#43a047', ['Oferta e demanda', 'Consumidor', 'Firma', 'Mercados', 'Agregados macro', 'IS-LM', 'OA-DA', 'Inflação', 'Política monetária', 'Despesa pública', 'Receita', 'Déficit']),
        ('Administração Geral', 'Básico', '#00acc1', ['Teorias', 'Planejamento', 'Organização', 'Direção', 'Controle', 'Estrutura', 'Cultura', 'Pessoas', 'Motivação', 'Liderança', 'Qualidade']),
        ('Administração Pública', 'Básico', '#5e35b1', ['Estado', 'Evolução no Brasil', 'Processo adm', 'Princípios', 'Governança', 'Orçamento', 'Ciclo orçamentário', 'Lei 4.320', 'LRF', 'PPA/LDO/LOA']),
        ('Auditoria', 'Básico', '#d81b60', ['Conceitos', 'Normas', 'Ética', 'Planejamento', 'Risco', 'Evidência', 'Procedimentos', 'Testes', 'Papéis', 'Amostragem', 'Relatório']),
        ('Contabilidade Geral', 'Básico', '#f4511e', ['Estrutura conceitual', 'Patrimônio', 'Contas', 'Regimes', 'Ativo', 'Estoques', 'Imobilizado', 'Passivo', 'PL', 'Balanço', 'DRE', 'DFC', 'Custos']),
        ('Contabilidade Pública', 'Básico', '#f57c00', ['Conceito', 'PCASP', 'DCASP', 'Balanços', 'DVP', 'Procedimentos']),
        ('Fluência em TI', 'Básico', '#00897b', ['Computação', 'Arquitetura', 'SO', 'Redes', 'Segurança', 'BD', 'SQL', 'Big Data', 'ETL', 'BI']),
        ('Direito Administrativo', 'Específico', '#3949ab', ['Estado', 'Organização', 'Ato adm', 'Poderes', 'Controle', 'Responsabilidade', 'Improbidade', 'PAF', 'Licitações', 'RJU']),
        ('Direito Constitucional', 'Específico', '#1976d2', ['Constituição', 'Poder constituinte', 'Princípios', 'Direitos fundamentais', 'Organização', 'Executivo', 'Legislativo', 'Judiciário', 'Controle', 'Sistema Tributário']),
        ('Direito Previdenciário', 'Específico', '#0288d1', ['Seguridade', 'RGPS', 'Segurados', 'Salário-contribuição', 'Aposentadorias', 'Auxílios', 'Pensão', 'Carência', 'Custeio']),
        ('Direito Tributário', 'Específico', '#c62828', ['Competência', 'Princípios', 'Imunidades', 'Tributos', 'Obrigação', 'Fato gerador', 'Responsabilidade', 'Crédito', 'Lançamento', 'Suspensão', 'Extinção', 'Fiscalização']),
        ('Legislação Tributária', 'Específico', '#ad1457', ['IRPF', 'IRPJ', 'IPI', 'PIS/COFINS', 'CSLL', 'Simples', 'PAF']),
        ('Comércio Internacional', 'Específico', '#6a1b9a', ['Teoria', 'Balança', 'Vantagens', 'Políticas', 'Incoterms', 'OMC', 'Mercosul', 'Tarifas', 'NCM']),
        ('Legislação Aduaneira', 'Específico', '#4a148c', ['Jurisdição', 'Tributos', 'II e IE', 'Regimes', 'Despachos', 'Infrações', 'Perdimento'])
    ]
    
    try:
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
        print("✅ Banco populado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao popular: {e}")
        db.session.rollback()

# Executar seed na inicialização
with app.app_context():
    seed_database()

# ==================== ROTAS ====================
@app.route('/')
def home():
    try:
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
        
        if dia_atual:
            dia_atual.topico1 = get_topico(dia_atual.topico1_id)
            dia_atual.topico2 = get_topico(dia_atual.topico2_id)
            dia_atual.topico3 = get_topico(dia_atual.topico3_id)
        
        return render_template('dashboard.html', dia_atual=dia_atual, total_horas=total_horas, total_questoes=total_questoes, taxa_acerto=taxa_acerto, dias_concluidos=dias_concluidos, revisoes_pendentes=revisoes_pendentes)
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/dia/<int:dia_id>')
def dia_detalhe(dia_id):
    try:
        dia = DiaCiclo.query.get_or_404(dia_id)
        dia.topico1 = get_topico(dia.topico1_id)
        dia.topico2 = get_topico(dia.topico2_id)
        dia.topico3 = get_topico(dia.topico3_id)
        return render_template('dia.html', dia=dia)
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/concluir_dia/<int:dia_id>', methods=['POST'])
def concluir_dia(dia_id):
    try:
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
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/disciplinas')
def disciplinas():
    try:
        discs = Disciplina.query.all()
        return render_template('disciplinas.html', disciplinas=discs)
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/revisoes')
def revisoes():
    try:
        revs = Revisao.query.filter_by(concluida=False).order_by(Revisao.data_agendada).all()
        for rev in revs:
            rev.topico = get_topico(rev.topico_id)
        return render_template('revisoes.html', revisoes=revs)
    except Exception as e:
        return f"Erro: {str(e)}", 500

@app.route('/estatisticas')
def estatisticas():
    try:
        discs = Disciplina.query.all()
        return render_template('estatisticas.html', disciplinas=discs)
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
