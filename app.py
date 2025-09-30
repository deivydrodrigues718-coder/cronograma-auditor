from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from seed_edital import DISCIPLINAS_TOPICOS

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

# ==================== SEED COM EDITAL COMPLETO ====================
def seed_database():
    if Disciplina.query.count() == 0:
        for nome_disc, dados in DISCIPLINAS_TOPICOS.items():
            disc = Disciplina(
                nome=nome_disc,
                modulo=dados['modulo'],
                cor=dados['cor']
            )
            db.session.add(disc)
            db.session.flush()
            
            for i, nome_topico in enumerate(dados['topicos']):
                top = Topico(
                    nome=nome_topico,
                    disciplina_id=disc.id,
                    ordem=i+1
                )
                db.session.add(top)
        
        db.session.commit()
        
        # Gerar primeiros 30 dias de ciclo
        topicos_disponiveis = Topico.query.all()
        for dia in range(1, 31):
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
    dia_atual = DiaCiclo.query.filter_by(data_conclusao=None).first()
    
    if not dia_atual:
        dia_atual = DiaCiclo.query.order_by(DiaCiclo.numero).first()
    
    total_minutos = db.session.query(db.func.sum(DiaCiclo.minutos)).scalar() or 0
    total_horas = total_minutos // 60
    total_questoes = db.session.query(db.func.sum(DiaCiclo.questoes)).scalar() or 0
    total_acertos = db.session.query(db.func.sum(DiaCiclo.acertos)).scalar() or 0
    taxa_acerto = round((total_acertos / total_questoes * 100) if total_questoes > 0 else 0, 1)
    
    dias_concluidos = DiaCiclo.query.filter(DiaCiclo.data_conclusao != None).count()
    
    revisoes_pendentes = Revisao.query.filter_by(concluida=False).filter(
        Revisao.data_agendada <= datetime.now()
    ).count()
    
    return render_template('dashboard.html',
                         dia_atual=dia_atual,
                         total_horas=total_horas,
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
    
    for topico_id in [dia.topico1_id, dia.topico2_id, dia.topico3_id]:
        if topico_id:
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(host='0.0.0.0', port=5000)
            
