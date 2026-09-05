from app.database import get_db


def test_index_abre(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "Controle Financeiro" in resposta.get_data(as_text=True)


def test_criar_lancamento(client, app):
    resposta = client.post(
        "/novo",
        data={
            "descricao": "Salário",
            "valor": "3500.00",
            "tipo": "receita",
            "categoria": "Trabalho",
            "data": "2026-09-04",
        },
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert "Lançamento cadastrado com sucesso." in resposta.get_data(as_text=True)

    with app.app_context():
        item = get_db().execute(
            "SELECT descricao, valor, tipo FROM lancamentos"
        ).fetchone()

        assert item["descricao"] == "Salário"
        assert item["valor"] == 3500.00
        assert item["tipo"] == "receita"


def test_validacao_valor(client):
    resposta = client.post(
        "/novo",
        data={
            "descricao": "Teste",
            "valor": "-10",
            "tipo": "despesa",
            "categoria": "Outros",
            "data": "2026-09-04",
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert "O valor deve ser maior que zero." in texto


def test_editar_lancamento(client, app):
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO lancamentos (descricao, valor, tipo, categoria, data)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Mercado", 100, "despesa", "Alimentação", "2026-09-04"),
        )
        db.commit()
        lancamento_id = cursor.lastrowid

    resposta = client.post(
        f"/editar/{lancamento_id}",
        data={
            "descricao": "Supermercado",
            "valor": "150.50",
            "tipo": "despesa",
            "categoria": "Alimentação",
            "data": "2026-09-04",
        },
        follow_redirects=True,
    )

    assert resposta.status_code == 200

    with app.app_context():
        item = get_db().execute(
            "SELECT descricao, valor FROM lancamentos WHERE id = ?",
            (lancamento_id,),
        ).fetchone()

        assert item["descricao"] == "Supermercado"
        assert item["valor"] == 150.50


def test_excluir_lancamento(client, app):
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO lancamentos (descricao, valor, tipo, categoria, data)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Conta", 80, "despesa", "Casa", "2026-09-04"),
        )
        db.commit()
        lancamento_id = cursor.lastrowid

    resposta = client.post(
        f"/excluir/{lancamento_id}",
        follow_redirects=True,
    )

    assert resposta.status_code == 200

    with app.app_context():
        item = get_db().execute(
            "SELECT id FROM lancamentos WHERE id = ?",
            (lancamento_id,),
        ).fetchone()

        assert item is None
