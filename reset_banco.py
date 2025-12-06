import os
import shutil
import sys

def limpar_tudo():
    print("--- INICIANDO LIMPEZA TOTAL ---")
    
    # 1. Tentar apagar o banco de dados
    db_files = ['db.sqlite3', 'db_novo.sqlite3']
    for db in db_files:
        if os.path.exists(db):
            try:
                os.remove(db)
                print(f"Banco de dados '{db}' apagado com sucesso!")
            except PermissionError:
                print(f" ERRO CRÍTICO: Não foi possível apagar '{db}'.")
                print("   MOTIVO: O servidor (runserver) ainda está rodando ou o arquivo está aberto.")
                print("   SOLUÇÃO: Pare o servidor, feche terminais e tente de novo.")
                return False

    # 2. Limpar a pasta migrations do app 'app'
    # Ajuste o caminho se o nome da pasta do seu app não for 'app'
    app_name = 'app' 
    migrations_path = os.path.join(app_name, 'migrations')
    
    if os.path.exists(migrations_path):
        for filename in os.listdir(migrations_path):
            file_path = os.path.join(migrations_path, filename)
            # Apaga tudo que não for __init__.py e pastas __pycache__
            if filename != '__init__.py' and os.path.isfile(file_path):
                os.remove(file_path)
                print(f"🧹 Migração antiga removida: {filename}")
            elif filename == '__pycache__':
                shutil.rmtree(file_path)
                print("🧹 Cache de migração limpo.")
    
    print("\n--- LIMPEZA CONCLUÍDA ---")
    print("Agora vamos recriar o banco do zero...")
    return True

if __name__ == "__main__":
    if limpar_tudo():
        # Executa os comandos do Django automaticamente
        print("\n1. Criando novas migrações...")
        os.system("python manage.py makemigrations")
        
        print("\n2. Aplicando ao banco de dados...")
        os.system("python manage.py migrate")
        
        print("\n3. Criando superusuário...")
        os.system("python manage.py createsuperuser")
        
        print("\n✅ TUDO PRONTO! Pode rodar 'python manage.py runserver' agora.")