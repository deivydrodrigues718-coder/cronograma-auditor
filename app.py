from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Usar PostgreSQL do Render se disponível, senão SQLite local
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///cronograma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== MODELS ====================
class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    modulo = db.Column(db.String(50))
    cor = db.Column(db.String(7), default='#1e88e5')

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(500), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    ordem = db.Column(db.Integer, default=0)
    questoes_resolvidas = db.Column(db.Integer, default=0)
    questoes_acertos = db.Column(db.Integer, default=0)
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

# ==================== INIT ====================
with app.app_context():
    try:
        db.create_all()
        print("✅ Banco criado")
    except Exception as e:
        print(f"❌ Erro: {e}")
        # ==================== SEED EDITAL COMPLETO ====================
def seed_database():
    try:
        if Disciplina.query.count() > 0:
            return
    except:
        pass
    
    print("🌱 Populando...")
    
    # TÓPICOS EXATOS DO ANEXO I - EDITAL RFB 1/2022
    edital_completo = {
        'Português': {
            'modulo': 'Básico', 'cor': '#e53935',
            'topicos': [
                'Compreensão e interpretação de textos',
                'Tipologia textual',
                'Ortografia oficial',
                'Acentuação gráfica',
                'Emprego das classes de palavras',
                'Emprego do sinal indicativo de crase',
                'Sintaxe da oração e do período',
                'Pontuação',
                'Concordância nominal e verbal',
                'Regência nominal e verbal',
                'Significação das palavras',
                'Redação de correspondências oficiais'
            ]
        },
        'Inglês': {
            'modulo': 'Básico', 'cor': '#1e88e5',
            'topicos': [
                'Compreensão de texto escrito em Língua Inglesa',
                'Itens gramaticais relevantes para compreensão dos conteúdos semânticos'
            ]
        },
        'Raciocínio Lógico-Matemático': {
            'modulo': 'Básico', 'cor': '#8e24aa',
            'topicos': [
                'Estruturas lógicas',
                'Lógica de argumentação',
                'Diagramas lógicos',
                'Trigonometria',
                'Matrizes, determinantes e sistemas lineares',
                'Álgebra',
                'Combinações, arranjos e permutação',
                'Probabilidade e variáveis aleatórias',
                'Estatística descritiva',
                'Números complexos',
                'Geometria básica',
                'Juros simples e compostos, taxas de juros, desconto, equivalência de capitais, anuidades e sistemas de amortização'
            ]
        },
        'Estatística': {
            'modulo': 'Básico', 'cor': '#fb8c00',
            'topicos': [
                'Estatística descritiva: medidas de posição',
                'Estatística descritiva: medidas de dispersão',
                'Distribuições de frequências: representação tabular e gráfica',
                'Probabilidade: conceitos básicos, variáveis aleatórias discretas e contínuas',
                'Distribuições de probabilidade: binomial, normal',
                'Amostragem',
                'Distribuições amostrais',
                'Inferência estatística: estimação pontual e intervalar',
                'Teste de hipóteses para médias e proporções',
                'Análise de regressão linear simples',
                'Análise de correlação'
            ]
        },
        'Economia e Finanças Públicas': {
            'modulo': 'Básico', 'cor': '#43a047',
            'topicos': [
                'Microeconomia: oferta e demanda',
                'Microeconomia: teoria do consumidor',
                'Microeconomia: teoria da firma',
                'Estruturas de mercado',
                'Macroeconomia: principais agregados macroeconômicos',
                'Macroeconomia: Sistema de Contas Nacionais',
                'Macroeconomia: modelo IS-LM',
                'Modelo OA-DA (oferta e demanda agregadas)',
                'Macroeconomia: inflação, desemprego',
                'Política monetária e fiscal',
                'Setor público: funções econômicas do governo',
                'Despesa pública: classificações e conceitos',
                'Receita pública: classificações e conceitos',
                'Déficit público e dívida pública'
            ]
        },
        'Administração Geral': {
            'modulo': 'Básico', 'cor': '#00acc1',
            'topicos': [
                'Evolução da administração: teorias e escolas',
                'Processo administrativo: planejamento',
                'Processo administrativo: organização',
                'Processo administrativo: direção',
                'Processo administrativo: controle',
                'Estrutura organizacional',
                'Cultura organizacional',
                'Gestão de pessoas: equilíbrio organizacional',
                'Objetivos, desafios e características da gestão de pessoas',
                'Comportamento organizacional: motivação',
                'Comportamento organizacional: liderança',
                'Comportamento organizacional: clima e comunicação',
                'Gestão da qualidade e modelo de excelência gerencial'
            ]
        },
        'Administração Pública': {
            'modulo': 'Básico', 'cor': '#5e35b1',
            'topicos': [
                'Características básicas das organizações formais modernas: Estado e Administração Pública',
                'Evolução da administração pública no Brasil',
                'Processo administrativo no âmbito da Administração Pública',
                'Princípios da administração pública',
                'Governança e governabilidade',
                'Orçamento público: conceitos e princípios orçamentários',
                'Ciclo orçamentário',
                'Lei nº 4.320/1964 e suas alterações',
                'Lei Complementar nº 101/2000 - LRF',
                'Plano Plurianual (PPA)',
                'Lei de Diretrizes Orçamentárias (LDO)',
                'Lei Orçamentária Anual (LOA)'
            ]
        }
        # ... continua com TODAS as outras disciplinas
    }
    
    try:
        for nome, dados in edital_completo.items():
            disc = Disciplina(nome=nome, modulo=dados['modulo'], cor=dados['cor'])
            db.session.add(disc)
            db.session.flush()
            
            for i, topico_nome in enumerate(dados['topicos']):
                top = Topico(nome=topico_nome, disciplina_id=disc.id, ordem=i+1)
                db.session.add(top)
        
        db.session.commit()
        
        # Gerar 30 dias
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
        print("✅ Populado!")
    except Exception as e:
        print(f"❌ {e}")
        db.session.rollback()

with app.app_context():
    seed_database()
    @app.route('/progresso')
def progresso():
    try:
        disciplinas = Disciplina.query.all()
        dados = []
        
        for disc in disciplinas:
            topicos = Topico.query.filter_by(disciplina_id=disc.id).all()
            total_questoes = sum(t.questoes_resolvidas for t in topicos)
            total_acertos = sum(t.questoes_acertos for t in topicos)
            taxa = round((total_acertos / total_questoes * 100) if total_questoes > 0 else 0, 1)
            
            dados.append({
                'disciplina': disc,
                'topicos': topicos,
                'total_questoes': total_questoes,
                'total_acertos': total_acertos,
                'taxa': taxa
            })
        
        return render_template('progresso.html', dados=dados)
    except Exception as e:
        return f"Erro: {e}", 500
        @app.route('/concluir_dia/<int:dia_id>', methods=['POST'])
def concluir_dia(dia_id):
    try:
        dia = DiaCiclo.query.get_or_404(dia_id)
        dia.data_conclusao = datetime.now()
        
        questoes_totais = int(request.form.get('questoes', 0))
        acertos_totais = int(request.form.get('acertos', 0))
        minutos_totais = int(request.form.get('minutos', 150))
        
        dia.questoes = questoes_totais
        dia.acertos = acertos_totais
        dia.minutos = minutos_totais
        
        # Distribuir questões entre os 3 tópicos
        questoes_por_topico = questoes_totais // 3
        acertos_por_topico = acertos_totais // 3
        
        for topico_id in [dia.topico1_id, dia.topico2_id, dia.topico3_id]:
            if topico_id:
                topico = Topico.query.get(topico_id)
                if topico:
                    topico.questoes_resolvidas += questoes_por_topico
                    topico.questoes_acertos += acertos_por_topico
                
                # Revisões
                db.session.add(Revisao(topico_id=topico_id, tipo='24h', data_agendada=datetime.now() + timedelta(hours=24)))
                db.session.add(Revisao(topico_id=topico_id, tipo='7d', data_agendada=datetime.now() + timedelta(days=7)))
                db.session.add(Revisao(topico_id=topico_id, tipo='30d', data_agendada=datetime.now() + timedelta(days=30)))
        
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Erro: {e}", 500
        # SEED COMPLETO - adicionar após a parte anterior
def seed_database():
    try:
        if Disciplina.query.count() > 0:
            return
    except:
        pass
    
    edital_completo = {
        'Português': {
            'modulo': 'Básico', 'cor': '#e53935',
            'topicos': [
                'Compreensão e interpretação de textos',
                'Tipologia textual',
                'Ortografia oficial',
                'Acentuação gráfica',
                'Emprego das classes de palavras',
                'Emprego do sinal indicativo de crase',
                'Sintaxe da oração e do período',
                'Pontuação',
                'Concordância nominal e verbal',
                'Regência nominal e verbal',
                'Significação das palavras',
                'Redação de correspondências oficiais'
            ]
        },
        'Inglês': {
            'modulo': 'Básico', 'cor': '#1e88e5',
            'topicos': [
                'Compreensão de texto escrito em Língua Inglesa',
                'Itens gramaticais relevantes para compreensão dos conteúdos semânticos'
            ]
        },
        'Raciocínio Lógico-Matemático': {
            'modulo': 'Básico', 'cor': '#8e24aa',
            'topicos': [
                'Estruturas lógicas',
                'Lógica de argumentação',
                'Diagramas lógicos',
                'Trigonometria',
                'Matrizes, determinantes e sistemas lineares',
                'Álgebra',
                'Combinações, arranjos e permutação',
                'Probabilidade e variáveis aleatórias',
                'Estatística descritiva',
                'Números complexos',
                'Geometria básica',
                'Juros simples e compostos, taxas de juros, desconto, equivalência de capitais, anuidades e sistemas de amortização'
            ]
        },
        'Estatística': {
            'modulo': 'Básico', 'cor': '#fb8c00',
            'topicos': [
                'Estatística descritiva: medidas de posição',
                'Estatística descritiva: medidas de dispersão',
                'Distribuições de frequências: representação tabular e gráfica',
                'Probabilidade: conceitos básicos, variáveis aleatórias discretas e contínuas',
                'Distribuições de probabilidade: binomial, normal',
                'Amostragem',
                'Distribuições amostrais',
                'Inferência estatística: estimação pontual e intervalar',
                'Teste de hipóteses para médias e proporções',
                'Análise de regressão linear simples',
                'Análise de correlação'
            ]
        },
        'Economia e Finanças Públicas': {
            'modulo': 'Básico', 'cor': '#43a047',
            'topicos': [
                'Microeconomia: oferta e demanda',
                'Microeconomia: teoria do consumidor',
                'Microeconomia: teoria da firma',
                'Estruturas de mercado',
                'Macroeconomia: principais agregados macroeconômicos',
                'Macroeconomia: Sistema de Contas Nacionais',
                'Macroeconomia: modelo IS-LM',
                'Modelo OA-DA (oferta e demanda agregadas)',
                'Macroeconomia: inflação, desemprego',
                'Política monetária e fiscal',
                'Setor público: funções econômicas do governo',
                'Despesa pública: classificações e conceitos',
                'Receita pública: classificações e conceitos',
                'Déficit público e dívida pública'
            ]
        },
        'Administração Geral': {
            'modulo': 'Básico', 'cor': '#00acc1',
            'topicos': [
                'Evolução da administração: teorias e escolas',
                'Processo administrativo: planejamento',
                'Processo administrativo: organização',
                'Processo administrativo: direção',
                'Processo administrativo: controle',
                'Estrutura organizacional',
                'Cultura organizacional',
                'Gestão de pessoas: equilíbrio organizacional',
                'Objetivos, desafios e características da gestão de pessoas',
                'Comportamento organizacional: motivação',
                'Comportamento organizacional: liderança',
                'Comportamento organizacional: clima e comunicação',
                'Gestão da qualidade e modelo de excelência gerencial'
            ]
        },
        'Administração Pública': {
            'modulo': 'Básico', 'cor': '#5e35b1',
            'topicos': [
                'Características básicas das organizações formais modernas: Estado e Administração Pública',
                'Evolução da administração pública no Brasil',
                'Processo administrativo no âmbito da Administração Pública',
                'Princípios da administração pública',
                'Governança e governabilidade',
                'Orçamento público: conceitos e princípios orçamentários',
                'Ciclo orçamentário',
                'Lei nº 4.320/1964 e suas alterações',
                'Lei Complementar nº 101/2000 - LRF',
                'Plano Plurianual (PPA)',
                'Lei de Diretrizes Orçamentárias (LDO)',
                'Lei Orçamentária Anual (LOA)'
            ]
        },
        'Auditoria': {
            'modulo': 'Básico', 'cor': '#d81b60',
            'topicos': [
                'Auditoria: conceitos, objetivos, tipos',
                'Normas relativas à pessoa do auditor',
                'Normas relativas à execução do trabalho',
                'Normas relativas ao parecer',
                'Ética profissional e responsabilidade legal',
                'Planejamento de auditoria',
                'Risco de auditoria',
                'Relevância na auditoria',
                'Evidência de auditoria',
                'Procedimentos de auditoria',
                'Testes de observância',
                'Testes substantivos',
                'Papéis de trabalho',
                'Amostragem estatística em auditoria',
                'Eventos subsequentes',
                'Revisão analítica',
                'Relatório de auditoria'
            ]
        },
        'Contabilidade Geral e de Custos': {
            'modulo': 'Básico', 'cor': '#f4511e',
            'topicos': [
                'Estrutura conceitual para elaboração das demonstrações contábeis',
                'Patrimônio: Ativo, Passivo e Patrimônio Líquido',
                'Fatos contábeis e respectivas variações patrimoniais',
                'Contas patrimoniais e de resultado',
                'Apuração de resultados',
                'Regimes de apuração: caixa e competência',
                'Provisões, ativos e passivos contingentes',
                'Políticas contábeis, mudança de estimativa e retificação de erro',
                'Ativos: disponibilidades, aplicações financeiras, contas a receber',
                'Estoques',
                'Despesas antecipadas',
                'Propriedades para investimento',
                'Imobilizado e intangível',
                'Passivos: exigível a longo prazo, fornecedores, obrigações fiscais',
                'Patrimônio líquido: capital social, reservas, ações em tesouraria',
                'Balancete de verificação',
                'Balanço Patrimonial',
                'Demonstração do Resultado do Exercício',
                'Demonstração do Resultado Abrangente',
                'Demonstração das Mutações do Patrimônio Líquido',
                'Demonstração dos Fluxos de Caixa',
                'Demonstração do Valor Adicionado',
                'Análise das demonstrações contábeis',
                'Conceitos de contabilidade de custos',
                'Custos para avaliação de estoques',
                'Custos para tomada de decisões',
                'Sistemas de custos e informações gerenciais',
                'Estudo da relação custo/volume/lucro'
            ]
        },
        'Contabilidade Pública': {
            'modulo': 'Básico', 'cor': '#f57c00',
            'topicos': [
                'Conceito, objeto e campo de aplicação',
                'Princípios de contabilidade sob a perspectiva do setor público',
                'Sistema de Contabilidade Federal',
                'Plano de Contas Aplicado ao Setor Público – PCASP',
                'Demonstrações Contábeis Aplicadas ao Setor Público – DCASP',
                'Balanço Orçamentário',
                'Balanço Financeiro',
                'Balanço Patrimonial',
                'Demonstração das Variações Patrimoniais',
                'Demonstração dos Fluxos de Caixa',
                'Demonstração das Mutações do Patrimônio Líquido',
                'Procedimentos contábeis orçamentários',
                'Procedimentos contábeis patrimoniais',
                'Procedimentos contábeis específicos'
            ]
        },
        'Fluência em Tecnologias de Informação e Gestão de Dados': {
            'modulo': 'Básico', 'cor': '#00897b',
            'topicos': [
                'Conceitos básicos de sistemas computacionais',
                'Arquitetura de computadores',
                'Sistemas operacionais',
                'Redes de computadores e Internet',
                'Segurança da informação',
                'Banco de dados: conceitos básicos',
                'Modelo relacional',
                'Linguagem SQL',
                'Gestão de dados: conceitos de Big Data',
                'Processo de ETL (Extract, Transform, Load)',
                'Data warehouse',
                'Análise de dados e Business Intelligence'
            ]
        },
        'Direito Administrativo': {
            'modulo': 'Específico', 'cor': '#3949ab',
            'topicos': [
                'Estado, governo e administração pública: conceitos, elementos, poderes e organização',
                'Organização administrativa da União: administração direta e indireta',
                'Agências executivas e reguladoras',
                'Ato administrativo: conceito, requisitos, atributos, classificação',
                'Anulação e revogação',
                'Prescrição',
                'Poderes administrativos',
                'Controle e responsabilização da administração',
                'Responsabilidade civil do Estado',
                'Lei nº 8.429/1992 - Improbidade Administrativa',
                'Lei nº 9.784/1999 - Processo administrativo federal',
                'Lei nº 14.133/2021 - Licitações e contratos',
                'Serviços públicos',
                'Lei nº 8.112/1990 - Regime jurídico dos servidores'
            ]
        },
        'Direito Constitucional': {
            'modulo': 'Específico', 'cor': '#1976d2',
            'topicos': [
                'Constituição: conceito, origens, conteúdo, estrutura',
                'Supremacia da Constituição',
                'Aplicabilidade das normas constitucionais',
                'Interpretação das normas constitucionais',
                'Poder constituinte',
                'Princípios fundamentais',
                'Direitos e garantias fundamentais',
                'Direitos e deveres individuais e coletivos',
                'Direitos sociais',
                'Nacionalidade',
                'Direitos políticos',
                'Organização político-administrativa do Estado',
                'Administração pública: disposições gerais',
                'Poder executivo',
                'Poder legislativo',
                'Processo legislativo',
                'Poder judiciário',
                'Funções essenciais à Justiça',
                'Controle de constitucionalidade',
                'Defesa do Estado e das instituições democráticas',
                'Ordem econômica e financeira',
                'Sistema Tributário Nacional',
                'Finanças públicas'
            ]
        },
        'Direito Previdenciário': {
            'modulo': 'Específico', 'cor': '#0288d1',
            'topicos': [
                'Seguridade social: origem e evolução legislativa no Brasil',
                'Conceituação',
                'Organização e princípios constitucionais',
                'Legislação previdenciária',
                'Regime Geral de Previdência Social',
                'Segurados obrigatórios',
                'Filiação e inscrição',
                'Empregado',
                'Empregado doméstico',
                'Contribuinte individual',
                'Trabalhador avulso',
                'Segurado especial',
                'Segurado facultativo',
                'Salário-de-contribuição',
                'Benefícios: aposentadorias',
                'Auxílios',
                'Pensão por morte',
                'Salário-família e salário-maternidade',
                'Carência',
                'Cálculo de benefícios',
                'Reajustamento e revisão de benefícios',
                'Acumulação de benefícios',
                'Prescrição e decadência',
                'Custeio da Seguridade Social',
                'Contribuições sociais'
            ]
        },
        'Direito Tributário': {
            'modulo': 'Específico', 'cor': '#c62828',
            'topicos': [
                'Sistema Tributário Nacional: competência tributária',
                'Limitações constitucionais ao poder de tributar',
                'Imunidades tributárias',
                'Conceito e classificação dos tributos',
                'Tributos de competência da União, Estados, DF e Municípios',
                'Código Tributário Nacional',
                'Obrigação tributária principal e acessória',
                'Fato gerador da obrigação tributária',
                'Sujeição ativa e passiva',
                'Solidariedade',
                'Capacidade tributária',
                'Domicílio tributário',
                'Responsabilidade tributária',
                'Responsabilidade dos sucessores',
                'Responsabilidade de terceiros',
                'Responsabilidade por infrações',
                'Denúncia espontânea',
                'Crédito tributário: conceito',
                'Constituição do crédito tributário: lançamento',
                'Suspensão do crédito tributário',
                'Extinção do crédito tributário',
                'Pagamento indevido',
                'Exclusão do crédito tributário',
                'Garantias e privilégios do crédito tributário',
                'Administração tributária: fiscalização, dívida ativa'
            ]
        },
        'Legislação Tributária': {
            'modulo': 'Específico', 'cor': '#ad1457',
            'topicos': [
                'Imposto sobre a Renda - Pessoa Física',
                'Imposto sobre a Renda - Pessoa Jurídica',
                'Imposto sobre Produtos Industrializados - IPI',
                'Contribuição para o PIS/PASEP',
                'Contribuição para o Financiamento da Seguridade Social - COFINS',
                'Contribuição Social sobre o Lucro Líquido - CSLL',
                'Simples Nacional',
                'Processo Administrativo Fiscal',
                'Ilícito tributário e sanções administrativas'
            ]
        },
        'Comércio Internacional': {
            'modulo': 'Específico', 'cor': '#6a1b9a',
            'topicos': [
                'Comércio exterior: teoria, balança comercial',
                'Teoria das vantagens comparativas',
                'Políticas de comércio exterior',
                'Termos internacionais de comércio - Incoterms',
                'Organizações internacionais: OMC, GATT',
                'Blocos econômicos e acordos comerciais',
                'Mercosul',
                'Tarifas aduaneiras',
                'Barreiras não tarifárias',
                'Nomenclatura Comum do Mercosul - NCM',
                'Sistema Harmonizado - SH'
            ]
        },
        'Legislação Aduaneira': {
            'modulo': 'Específico', 'cor': '#4a148c',
            'topicos': [
                'Jurisdição aduaneira',
                'Controle aduaneiro de veículos',
                'Tributos incidentes sobre o comércio exterior',
                'Imposto de Importação',
                'Imposto de Exportação',
                'Regimes aduaneiros especiais',
                'Regimes aduaneiros aplicados em áreas especiais',
                'Despacho aduaneiro de importação',
                'Despacho aduaneiro de exportação',
                'Infrações e penalidades aduaneiras',
                'Pena de perdimento',
                'Aplicação da pena de perdimento',
                'Processo administrativo de aplicação de penalidades'
            ]
        }
    }
    
    try:
        for nome, dados in edital_completo.items():
            disc = Disciplina(nome=nome, modulo=dados['modulo'], cor=dados['cor'])
            db.session.add(disc)
            db.session.flush()
            
            for i, topico_nome in enumerate(dados['topicos']):
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
        print("✅ Seed completo!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.session.rollback()
                              
