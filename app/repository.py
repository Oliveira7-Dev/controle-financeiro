from .database import get_db


def listar_lancamentos(tipo=None):
    db = get_db()

    if tipo in ("receita", "despesa"):
        return db.execute(
            """
            SELECT id, descricao, valor, tipo, categoria, data
            FROM lancamentos
            WHERE tipo = ?
            ORDER BY data DESC, id DESC
            """,
            (tipo,),
        ).fetchall()

    return db.execute(
        """
        SELECT id, descricao, valor, tipo, categoria, data
        FROM lancamentos
        ORDER BY data DESC, id DESC
        """
    ).fetchall()


def buscar_lancamento(lancamento_id):
    return get_db().execute(
        "SELECT * FROM lancamentos WHERE id = ?",
        (lancamento_id,),
    ).fetchone()


def criar_lancamento(descricao, valor, tipo, categoria, data):
    db = get_db()
    cursor = db.execute(
        """
        INSERT INTO lancamentos (descricao, valor, tipo, categoria, data)
        VALUES (?, ?, ?, ?, ?)
        """,
        (descricao, valor, tipo, categoria, data),
    )
    db.commit()
    return cursor.lastrowid


def atualizar_lancamento(lancamento_id, descricao, valor, tipo, categoria, data):
    db = get_db()
    db.execute(
        """
        UPDATE lancamentos
        SET descricao = ?, valor = ?, tipo = ?, categoria = ?, data = ?
        WHERE id = ?
        """,
        (descricao, valor, tipo, categoria, data, lancamento_id),
    )
    db.commit()


def excluir_lancamento(lancamento_id):
    db = get_db()
    db.execute("DELETE FROM lancamentos WHERE id = ?", (lancamento_id,))
    db.commit()


def obter_resumo():
    db = get_db()

    receitas = db.execute(
        "SELECT COALESCE(SUM(valor), 0) FROM lancamentos WHERE tipo = 'receita'"
    ).fetchone()[0]

    despesas = db.execute(
        "SELECT COALESCE(SUM(valor), 0) FROM lancamentos WHERE tipo = 'despesa'"
    ).fetchone()[0]

    return {
        "receitas": float(receitas),
        "despesas": float(despesas),
        "saldo": float(receitas - despesas),
    }
