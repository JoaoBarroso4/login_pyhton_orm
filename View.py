from Controller import ControllerCadastro, ControllerLogin

while True:
    print("====== MENU ======")
    escolha = input("Digite 1 para cadastrar\nDigite 2 para logar\nDigite 3 para sair\n")

    if escolha == "1":
        nome = input("Digite o nome: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        retorno = ControllerCadastro.cadastrar(nome, email, senha)

        if retorno == 1:
            print("Cadastrado com sucesso!")
        elif retorno == 2:
            print("Nome inválido!")
        elif retorno == 3:
            print("Email inválido!")
        elif retorno == 4:
            print("Senha inválida! (Mínimo de 6 caracteres)")
        elif retorno == 5:
            print("Email já cadastrado!")
        else:
            print("Erro desconhecido!")
    elif escolha == "2":
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        retorno = ControllerLogin.login(email, senha)

        if not retorno:
            print("Email ou senha inválidos!")
        else:
            print(retorno)
    else:
        break
