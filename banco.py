import sqlite3

def conectar():
    return sqlite3.connect('escola.db')

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aluno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nascimento TEXT,
            idade INTEGER,
            media REAL,
            curso TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matricula (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            nascimento TEXT,
            idade INTEGER,
            turma INTEGER,
            curso TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disciplina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma INTEGER,
            UNIQUE(nome, turma)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aluno_disciplina (
            aluno_nome TEXT,
            disciplina_nome TEXT,
            turma INTEGER,
            PRIMARY KEY (aluno_nome, disciplina_nome, turma)
        )
    ''')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aluno_nota(
                   aluno_nome TEXT,
                   disciplina TEXT,
                   trimestre TEXT,
                   nota1 REAL,
                   nota2 REAL,
                   nota3 REAL   
        )
    """)
    conn.commit()
    conn.close()
