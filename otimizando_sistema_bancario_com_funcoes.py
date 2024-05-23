import textwrap

def linha_completa(texto, largura=80, caractere='='):
    texto_centralizado = texto.center(largura, caractere)
    return texto_centralizado

def menu():
    menu_texto = f"""\n
    {linha_completa("\tHbank\t")}\n
    {linha_completa("\tMENU\t")}\n
    Bem-vindo ao Hbank, seu banco digital de toda hora!

    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tEmpréstimo
    [8]\tListar usuários
    [9]\tInativar conta
    [0]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


# Depositar
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n*** Operação falhou! O valor informado é inválido. ***")

    return saldo, extrato

# Sacar
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n*** Operação falhou! Você não tem saldo suficiente. ***")

    elif excedeu_limite:
        print("\n*** Operação falhou! O valor do saque excede o limite. ***")

    elif excedeu_saques:
        print("\n*** Operação falhou! Número máximo de saques excedido. ***")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n*** Operação falhou! O valor informado é inválido. ***")

    return saldo, extrato

# Extrato
def exibir_extrato(saldo, /, *, extrato, emprestimos_contratados):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    for emprestimo in emprestimos_contratados:
        print(f"Empréstimo:\tR$ {emprestimo['valor']:.2f} em {emprestimo['parcelas']} parcelas de R$ {emprestimo['valor_parcela']:.2f} com juros de {emprestimo['juros'] * 100:.2f}%")
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# Criar Usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n*** Já existe usuário com esse CPF! ***")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco, "ativo": True})

    print("=== Usuário criado com sucesso! ===")

# Listar Usuários
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Criar conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        if not usuario["ativo"]:
            print("\n*** Usuário está inativo e não pode criar conta! ***")
            return
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n*** Usuário não encontrado, fluxo de criação de conta encerrado! ***")

# Listar Contas
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Listar Usuários
def listar_usuarios(usuarios):
    for usuario in usuarios:
        linha = f"""\
            Nome:\t\t{usuario['nome']}
            CPF:\t\t{usuario['cpf']}
            Data Nasc.:\t{usuario['data_nascimento']}
            Endereço:\t{usuario['endereco']}
            Ativo:\t\t{'Sim' if usuario['ativo'] else 'Não'}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Inativar
def inativar_conta(contas):
    numero_conta = input("Informe o número da conta a ser inativada: ")
    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)

    if conta:
        contas.remove(conta)
        print("\n=== Conta inativada com sucesso! ===")
    else:
        print("\n*** Conta não encontrada! ***")

# Emprestimo
def emprestimo(saldo, extrato, emprestimos_contratados, limite_emprestimo, juros, /):
    valor = float(input("Informe o valor do empréstimo: "))
    parcelas = int(input("Informe o número de parcelas: "))

    if valor > 0 and valor <= limite_emprestimo and parcelas > 0:
        valor_parcela = valor * (1 + juros) / parcelas
        saldo += valor
        extrato += f"Empréstimo:\tR$ {valor:.2f}\n"
        emprestimos_contratados.append({
            "valor": valor,
            "juros": juros,
            "parcelas": parcelas,
            "valor_parcela": valor_parcela
        })
        print("\n=== Empréstimo realizado com sucesso! ===")
    else:
        print("\n*** Operação falhou! O valor ou o número de parcelas informado é inválido ou excede o limite de empréstimo. ***")

    return saldo, extrato


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    LIMITE_EMPRESTIMO = 1000
    JUROS = 0.05  # 5% de juros

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    emprestimos_contratados = []

    while True:
        opcao = menu()
# Depositar
        if opcao == '1':  
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == '2':  # Sacar
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
# Extrato
        elif opcao == '3':  
            exibir_extrato(saldo, extrato=extrato, emprestimos_contratados=emprestimos_contratados)

# Nova conta
        elif opcao == '4':  
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                
# Listar contas
        elif opcao == '5':  
            listar_contas(contas)

# Novo usuário
        elif opcao == '6':  
            criar_usuario(usuarios)

# Empréstimo
        elif opcao == '7':  
            saldo, extrato = emprestimo(
                saldo, extrato, emprestimos_contratados, 
                LIMITE_EMPRESTIMO, JUROS
            )

# Listar usuários
        elif opcao == '8':  
            listar_usuarios(usuarios)

# Inativar conta
        elif opcao == '9':  
            inativar_conta(contas)
            
# Sair
        elif opcao == '0':  
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
