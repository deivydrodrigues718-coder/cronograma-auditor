from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder="static", template_folder="templates")

# Fila simples de "Dias" (MVP sem banco)
DIAS = []

def gerar_dia(topicos):
    return {"topicos": topicos, "status": "pendente"}

@app.route("/")
def home():
    # Primeiro acesso: cria Dia N com 3 tópicos exemplo
    if not DIAS:
        DIAS.append(gerar_dia([
            "Português – Interpretação de textos",
            "CTN – Obrigação/Crédito",
            "Aduaneira – Regimes Aduaneiros"
        ]))
    return render_template("hoje.html", dia=DIAS[0])

@app.route("/concluir", methods=["POST"])
def concluir():
    # Conclui o Dia atual e gera o próximo Dia com 3 novos tópicos exemplo
    if DIAS:
        DIAS.pop(0)
    DIAS.append(gerar_dia([
        "Contabilidade – Ativo/Passivo",
        "RLM – Proposições",
        "Inglês – Reading técnico"
    ]))
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
