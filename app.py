from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

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
    nome = db.Column(db.String(200), nullable=False)
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

class Revisao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topico_id = db.Column(db.Integer, db.ForeignKey('topico.id'))
    tipo = db.Column(db.String(10))  # 24h, 7d, 30d
    data_agendada = db.Column(db.DateTime)
    concluida = db.Column(db.Boolean, default=False)
    questoes = db.Column(db.Integer, default=0)
    acertos = db.Column(db.Integer, default=0)

# ==================== SEED INICIAL ====================
def seed_database():
    if Disciplina.query.count() == 0:
        disciplinas = [
            {'nome': 'Português', 'modulo': 'Básico', 'cor': '#e53935'},
            {'nome': 'Inglês', 'modulo': 'Básico', 'cor': '#1e88e5'},
            {'nome': 'Raciocínio Lógico', 'modulo': 'Básico', 'cor': '#8e24aa'},
            {'nome': 'Estatística', 'modulo': 'Básico', 'cor': '#fb8c00'},
            {'nome': 'Economia e Finanças Públicas', 'modulo': 'Básico', 'cor': '#43a047'},
            {'nome': 'Administração Geral', 'modulo': 'Básico', 'cor': '#00acc1'},
            {'nome': 'Administração Pública', 'modulo': 'Básico', 'cor': '#5e35b1'},
            {'nome': 'Auditoria', 'modulo': 'Básico', 'cor': '#d81b60'},
            {'nome': 'Contabilidade Geral e Pública', 'modulo': 'Básico', 'cor': '#f4511e'},
            {'nome': 'Fluência em Dados', 'modulo': 'Básico', 'cor': '#00897b'},
            {'nome': 'Direito Administrativo', 'modulo': 'Específico', 'cor': '#3949ab'},
            {'nome': 'Direito Constitucional', 'modulo': 'Específico', 'cor': '#1976d2'},
            {'nome': 'Direito Previdenciário', 'modulo': 'Específico', 'cor': '#0288d1'},
            {'nome': 'Direito Tributário', 'modulo': 'Específico', 'cor': '#c62828'},
            {'nome': 'Legislação Tributária', 'modulo': 'Específico', 'cor': '#ad1457'},
            {'nome': 'Legislação Aduaneira', 'modulo': 'Específico', 'cor': '#6a1b9a'},
        ]
        
        for d in disciplinas:
            disc = Disciplina(nome=d['nome'], modulo=d['modulo'], cor=d['cor'])
            db.session.add(disc)
        
        db.session.commit()
        
        # Adicionar tópicos exemplo para Português
        port = Disciplina.query.filter_by(nome='Português').first()
        topicos_port = [
            'Interpretação de textos',
            'Ortografia oficial',
            'Acentuação gráfica',
            'Pontuação',
            'Classes de palavras',
            'Sintaxe da oração e do período',
            'Concordância nominal e verbal',
            'Regência nominal e verbal',
            'Emprego do sinal indicativo de crase',
            'Colocação dos pronomes átonos'
        ]
        
        for i, nome in enumerate(topicos_port):
            top = Topico(nome=nome, disciplina_id=port.id, ordem=i+1)
            db.session.add(top)
        
        db.session.commit()
        
        # Gerar primeiros 14 dias de ciclo
        topicos_disponiveis = Topico.query.all()
        for dia in range(1, 15):
            idx = ((dia-1) * 3) % len(topicos_disponiveis)
            d = DiaCiclo(
                numero=dia,
                topico1_id=topicos_disponiveis[idx].id,
                topico2_id=topicos_disponiveis[(idx+1) % len(topicos_disponiveis)].id,
                topico3_id=topicos_disponiveis[(idx+2) % len(topicos_disponiveis)].id
            )
            db.session.add(d)
        
        db.session.commit()

# ==================== ROTAS ====================
@app.route('/')
def home():
    dias = DiaCiclo.query.order_by(DiaCiclo.numero).all()
    dia_atual = DiaCiclo.query.filter_by(data_conclusao=None).first()
    
    if not dia_atual:
        dia_atual = dias[0] if dias else None
    
    # Estatísticas
    total_horas = db.session.query(db.func.sum(DiaCiclo.minutos)).scalar() or 0
    total_questoes = db.session.query(db.func.sum(DiaCiclo.questoes)).scalar() or 0
    total_acertos = db.session.query(db.func.sum(DiaCiclo.acertos)).scalar() or 0
    taxa_acerto = round((total_acertos / total_questoes * 100) if total_questoes > 0 else 0, 1)
    
    dias_concluidos = DiaCiclo.query.filter(DiaCiclo.data_conclusao != None).count()
    
    revisoes_pendentes = Revisao.query.filter_by(concluida=False).filter(
        Revisao.data_agendada <= datetime.now()
    ).count()
    
    return render_template('dashboard.html',
                         dia_atual=dia_atual,
                         total_horas=total_horas // 60,
                         total_questoes=total_questoes,
                         taxa_acerto=taxa_acerto,
                         dias_concluidos=dias_concluidos,
                         revisoes_pendentes=revisoes_pendentes)

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
    
    # Agendar revisões 24h/7d/30d
    for topico_id in [dia.topico1_id, dia.topico2_id, dia.topico3_id]:
        rev_24h = Revisao(topico_id=topico_id, tipo='24h', 
                         data_agendada=datetime.now() + timedelta(hours=24))
        rev_7d = Revisao(topico_id=topico_id, tipo='7d', 
                        data_agendada=datetime.now() + timedelta(days=7))
        rev_30d = Revisao(topico_id=topico_id, tipo='30d', 
                         data_agendada=datetime.now() + timedelta(days=30))
        db.session.add_all([rev_24h, rev_7d, rev_30d])
    
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

@app.route('/api/stats')
def api_stats():
    # Dados para gráficos
    return jsonify({
        'labels': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
        'horas': [2.5, 2.5, 0, 2.5, 2.5, 2.5]
    })

# ==================== INICIALIZAÇÃO ====================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(host='0.0.0.0', port=5000)
             
