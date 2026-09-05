from datetime import date
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from .repository import (
    atualizar_lancamento,
    buscar_lancamento,
    criar_lancamento,
    excluir_lancamento,
    listar_lancamentos,
    obter_resumo,
)

bp = Blueprint("financeiro", __name__)


def validar_formulario(form):
    descricao = form.get("descricao", "").strip()
    categoria = form.get("categoria", "").strip()
    tipo = form.get("tipo", "").strip()
    data_lancamento = form.get("data", "").strip()

    erros = []

    if not descricao:
        erros.append("A descrição é obrigatória.")

    if not categoria:
        erros.append("A categoria é obrigatória.")

    if tipo not in ("receita", "despesa"):
        erros.append("O tipo deve ser receita ou despesa.")

    try:
        valor = float(form.get("valor", "").replace(",", "."))
        if valor <= 0:
            erros.append("O valor deve ser maior que zero.")
    except ValueError:
        valor = None
        erros.append("Informe um valor válido.")

    if not data_lancamento:
        data_lancamento = date.today().isoformat()

    return {
        "descricao": descricao,
        "categoria": categoria,
        "tipo": tipo,
        "valor": valor,
        "data": data_lancamento,
    }, erros


@bp.route("/")
def index():
    filtro = request.args.get("tipo", "").strip()
    lancamentos = listar_lancamentos(filtro or None)
    resumo = obter_resumo()

    return render_template(
        "index.html",
        lancamentos=lancamentos,
        resumo=resumo,
        filtro=filtro,
    )


@bp.route("/novo", methods=("GET", "POST"))
def novo():
    if request.method == "POST":
        dados, erros = validar_formulario(request.form)

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("form.html", titulo="Novo lançamento", dados=dados)

        criar_lancamento(**dados)
        flash("Lançamento cadastrado com sucesso.", "sucesso")
        return redirect(url_for("financeiro.index"))

    return render_template(
        "form.html",
        titulo="Novo lançamento",
        dados={"data": date.today().isoformat()},
    )


@bp.route("/editar/<int:lancamento_id>", methods=("GET", "POST"))
def editar(lancamento_id):
    lancamento = buscar_lancamento(lancamento_id)

    if lancamento is None:
        abort(404)

    if request.method == "POST":
        dados, erros = validar_formulario(request.form)

        if erros:
            for erro in erros:
                flash(erro, "erro")
            return render_template("form.html", titulo="Editar lançamento", dados=dados)

        atualizar_lancamento(lancamento_id=lancamento_id, **dados)
        flash("Lançamento atualizado com sucesso.", "sucesso")
        return redirect(url_for("financeiro.index"))

    return render_template(
        "form.html",
        titulo="Editar lançamento",
        dados=dict(lancamento),
    )


@bp.post("/excluir/<int:lancamento_id>")
def excluir(lancamento_id):
    if buscar_lancamento(lancamento_id) is None:
        abort(404)

    excluir_lancamento(lancamento_id)
    flash("Lançamento excluído.", "sucesso")
    return redirect(url_for("financeiro.index"))
