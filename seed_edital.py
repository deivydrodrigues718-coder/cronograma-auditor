# seed_edital.py - Tópicos EXATOS do Anexo I - Edital RFB 1/2022

DISCIPLINAS_TOPICOS = {
    'Português': {
        'modulo': 'Básico',
        'cor': '#e53935',
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
        'modulo': 'Básico',
        'cor': '#1e88e5',
        'topicos': [
            'Compreensão de texto escrito em Língua Inglesa',
            'Itens gramaticais relevantes para compreensão dos conteúdos semânticos'
        ]
    },
    'Raciocínio Lógico-Matemático': {
        'modulo': 'Básico',
        'cor': '#8e24aa',
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
        'modulo': 'Básico',
        'cor': '#fb8c00',
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
        'modulo': 'Básico',
        'cor': '#43a047',
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
        'modulo': 'Básico',
        'cor': '#00acc1',
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
        'modulo': 'Básico',
        'cor': '#5e35b1',
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
        'modulo': 'Básico',
        'cor': '#d81b60',
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
        'modulo': 'Básico',
        'cor': '#f4511e',
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
            'Passivos: exigível a longo prazo, fornecedores, obrigações fiscais e outras',
            'Patrimônio líquido: capital social, adiantamentos, reservas de capital, ajustes de avaliação patrimonial, reservas de lucros, ações em tesouraria, prejuízos acumulados',
            'Balancete de verificação',
            'Demonstrações contábeis: Balanço Patrimonial',
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
        'modulo': 'Básico',
        'cor': '#f57c00',
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
            'Procedimentos contábeis específicos: operações de crédito, regime próprio de previdência social, dívida ativa'
        ]
    },
    'Fluência em Tecnologias de Informação e Gestão de Dados': {
        'modulo': 'Básico',
        'cor': '#00897b',
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
        'modulo': 'Específico',
        'cor': '#3949ab',
        'topicos': [
            'Estado, governo e administração pública: conceitos, elementos, poderes e organização; natureza, fins e princípios',
            'Organização administrativa da União: administração direta e indireta',
            'Agências executivas e reguladoras',
            'Ato administrativo: conceito, requisitos, atributos, classificação, espécies e invalidação',
            'Anulação e revogação',
            'Prescrição',
            'Poderes administrativos: poder hierárquico, disciplinar, regulamentar e poder de polícia',
            'Controle e responsabilização da administração: controle administrativo, controle judicial, controle legislativo',
            'Responsabilidade civil do Estado',
            'Lei nº 8.429/1992 - Lei de Improbidade Administrativa',
            'Lei nº 9.784/1999 - Processo administrativo federal',
            'Licitações e contratos administrativos - Lei nº 14.133/2021',
            'Serviços públicos',
            'Regime jurídico peculiar aos servidores públicos federais - Lei nº 8.112/1990'
        ]
    },
    'Direito Constitucional': {
        'modulo': 'Específico',
        'cor': '#1976d2',
        'topicos': [
            'Constituição: conceito, origens, conteúdo, estrutura e classificação',
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
            'Estado federal brasileiro, União, estados, Distrito Federal, municípios e territórios',
            'Administração pública: disposições gerais, servidores públicos',
            'Poder executivo: atribuições e responsabilidades do presidente da República',
            'Poder legislativo: estrutura, funcionamento e atribuições, processo legislativo',
            'Poder judiciário: disposições gerais, órgãos do Poder Judiciário',
            'Funções essenciais à Justiça: Ministério Público, Advocacia Pública',
            'Controle de constitucionalidade',
            'Defesa do Estado e das instituições democráticas: segurança pública, organização da segurança pública',
            'Ordem econômica e financeira: princípios gerais da atividade econômica',
            'Sistema Tributário Nacional: princípios gerais, limitações do poder de tributar, impostos da União, dos Estados, do Distrito Federal e dos Municípios',
            'Finanças públicas: normas gerais, orçamentos'
        ]
    },
    'Direito Previdenciário': {
        'modulo': 'Específico',
        'cor': '#0288d1',
        'topicos': [
            'Seguridade social: origem e evolução legislativa no Brasil',
            'Conceituação',
            'Organização e princípios constitucionais',
            'Legislação previdenciária: conteúdo, fontes, autonomia',
            'Regime Geral de Previdência Social',
            'Segurados obrigatórios',
            'Filiação e inscrição',
            'Conceito, características e abrangência: empregado, empregado doméstico, contribuinte individual, trabalhador avulso e segurado especial',
            'Segurado facultativo: conceito, características, filiação e inscrição',
            'Salário-de-contribuição: conceito, parcelas integrantes e excluídas, limites mínimo e máximo',
            'Benefícios do Regime Geral de Previdência Social: aposentadorias, auxílios, pensão por morte, salário-família e salário-maternidade',
            'Carência',
            'Cálculo de benefícios',
            'Reajustamento e revisão de benefícios',
            'Acumulação de benefícios',
            'Prescrição e decadência',
            'Custeio da Seguridade Social: receitas da União, receitas das contribuições sociais',
            'Salário-de-contribuição',
            'Contribuições sociais: dos segurados, das empresas, do empregador doméstico e do produtor rural'
        ]
    },
    'Direito Tributário': {
        'modulo': 'Específico',
        'cor': '#c62828',
        'topicos': [
            'Sistema Tributário Nacional: competência tributária',
            'Limitações constitucionais ao poder de tributar: princípios constitucionais tributários',
            'Imunidades tributárias',
            'Conceito e classificação dos tributos',
            'Tributos de competência da União, dos Estados, do Distrito Federal e dos Municípios',
            'Código Tributário Nacional: normas gerais de direito tributário',
            'Obrigação tributária principal e acessória',
            'Fato gerador da obrigação tributária',
            'Sujeição ativa e passiva',
            'Solidariedade',
            'Capacidade tributária',
            'Domicílio tributário',
            'Responsabilidade tributária: conceito e modalidades',
            'Responsabilidade dos sucessores',
            'Responsabilidade de terceiros',
            'Responsabilidade por infrações',
            'Denúncia espontânea',
            'Crédito tributário: conceito',
            'Constituição do crédito tributário: lançamento, modalidades de lançamento',
            'Suspensão do crédito tributário: conceito e modalidades',
            'Extinção do crédito tributário: modalidades',
            'Pagamento indevido',
            'Exclusão do crédito tributário: isenção e anistia',
            'Garantias e privilégios do crédito tributário',
            'Administração tributária: fiscalização, dívida ativa, certidões negativas'
        ]
    },
    'Legislação Tributária': {
        'modulo': 'Específico',
        'cor': '#ad1457',
        'topicos': [
            'Imposto sobre a Renda e Proventos de Qualquer Natureza - Pessoa Física',
            'Imposto sobre a Renda e Proventos de Qualquer Natureza - Pessoa Jurídica',
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
        'modulo': 'Específico',
        'cor': '#6a1b9a',
        'topicos': [
            'Comércio exterior: teoria do comércio exterior, balança comercial',
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
        'modulo': 'Específico',
        'cor': '#4a148c',
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
