import json
import boto3
import uuid
import bcrypt

def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    def calcular_digito(cpf, fator_inicial):
        soma = 0
        for i in range(fator_inicial - 1):
            soma += int(cpf[i]) * (fator_inicial - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calcular_digito(cpf, 10)
    digito2 = calcular_digito(cpf, 11)

    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])

def cpf_ja_cadastrado(table, cpf, user_id=None):
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('cpf').eq(cpf)
    )
    if user_id:
        for item in response['Items']:
            if item['id'] != user_id:
                return True
        return False
    return len(response['Items']) > 0

def normalize_field_names(data):
    return {key[0].lower() + key[1:]: value for key, value in data.items()}

def denormalize_field_names(data):
    return {
        'nome': data.get('nome'),
        'email': data.get('email'),
        'cpf': data.get('cpf'),
        'dataNascimento': data.get('dataNascimento'),
        'telefone': data.get('telefone'),
        'cep': data.get('cep'),
        'logradouro': data.get('logradouro'),
        'numero': data.get('numero'),
        'complemento': data.get('complemento'),
        'bairro': data.get('bairro'),
        'cidade': data.get('cidade'),
        'uf': data.get('uf'),
        'id': data.get('id'),
        'anamnese': data.get('anamnese'),
        'orientacoes': data.get('orientacoes'),
        'profile_picture': data.get('profile_picture'),
        # Campos adicionados
        'rg': data.get('rg'),
        'orgaoExpedidorRg': data.get('orgaoExpedidorRg'),
        'ufOrgaoExpedidorRg': data.get('ufOrgaoExpedidorRg'),
        'pronome': data.get('pronome'),
        'corRaca': data.get('corRaca'),
        'etnia': data.get('etnia'),
        'rendaMensalIndividual': data.get('rendaMensalIndividual'),
        'rendaMensalFamiliar': data.get('rendaMensalFamiliar'),
        'genero': data.get('genero'),
        'escolaridade': data.get('escolaridade'),
        'quantasPessoasCasa': data.get('quantasPessoasCasa'),
        'estadoCivil': data.get('estadoCivil'),
        'planoSaude': data.get('planoSaude'),
        'orientacaoSexual': data.get('orientacaoSexual'),
        'religiosidade': data.get('religiosidade'),
        'nacionalidade': data.get('nacionalidade'),
        'profissao': data.get('profissao'),
        'cpfUrl': data.get('cpfUrl'),
        'rgUrl': data.get('rgUrl'),
        'laudoMedicoUrl': data.get('laudoMedicoUrl'),
        'receitaMedicaUrl': data.get('receitaMedicaUrl'),
        'termoAjuizamentoUrl': data.get('termoAjuizamentoUrl'),
        'comprovanteResidenciaUrl': data.get('comprovanteResidenciaUrl'),
        'nomeProfissionalSaude': data.get('nomeProfissionalSaude'),
        'numeroRegistroProfissional': data.get('numeroRegistroProfissional'),
        'conquistas': data.get('conquistas')
    }

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    print("Evento recebido:", json.dumps(event))  # Log inicial do evento recebido

    headers = event.get('headers', {})
    user_agent = headers.get('User-Agent', '')

    is_browser = any(keyword in user_agent for keyword in ['Mozilla', 'Chrome', 'Safari', 'Firefox', 'Edge'])

    print("Requisição vinda de navegador:", is_browser)

    http_method = event.get('httpMethod')

    if http_method == 'POST':
        body = normalize_field_names(json.loads(event.get('body', '{}')))
        user_id = str(uuid.uuid4())

        required_fields = ['nome', 'email', 'cpf', 'senha', 'dataNascimento']
        for field in required_fields:
            if not body.get(field):
                print(f"Campo obrigatório ausente: {field}")
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                    },
                    'body': json.dumps(f'O campo {field} é obrigatório.')
                }

        nome = body['nome']
        email = body['email']
        cpf = body['cpf']
        senha = body['senha']
        data_nascimento = body['dataNascimento']
        telefone = body['telefone']

        if not validar_cpf(cpf):
            print("CPF inválido:", cpf)
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                },
                'body': json.dumps('CPF inválido.')
            }

        if cpf_ja_cadastrado(table, cpf):
            print("CPF já cadastrado:", cpf)
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                },
                'body': json.dumps('CPF já cadastrado.')
            }

        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        item = {
            'id': user_id,
            'nome': nome,
            'email': email,
            'cpf': cpf,
            'dataNascimento': data_nascimento,
            'senha': hashed_senha,
            'telefone': telefone,
            'conquistas': {
                'Onboarding': {
                    'Cadastro': True,
                    'Endereco': False,
                    'InfoPessoal': False,
                    'Anamnese': False,
                    'Docs': False
                },
                'OnboardingOk': False,
                'Farmacia': False,
                'Consulta': False,
                'BemEstar': False
            }
        }
        print("Item a ser inserido:", item)
        table.put_item(Item=item)
        return {
            'statusCode': 201,
            'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
            },
            'body': json.dumps('Usuário cadastrado com sucesso!')
        }

    elif http_method == 'GET':
        params = event.get('queryStringParameters', {})
        if 'id' in params:
            user_id = params['id']
            response = table.get_item(Key={'id': user_id})
            if 'Item' in response:
                item = response['Item']
                item.pop('senha', None)
                item = denormalize_field_names(normalize_field_names(item))
                print("Item encontrado:", item)
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                    },
                    'body': json.dumps(item)
                }
            print("Usuário não encontrado:", user_id)
            return {
                'statusCode': 404,
                'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                },
                'body': json.dumps('Usuário não encontrado.')
            }
        elif 'cpf' in params:
            cpf = params['cpf']
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('cpf').eq(cpf)
            )
            if len(response['Items']) > 0:
                print("CPF já cadastrado:", cpf)
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                    },
                    'body': json.dumps({'cpfJaCadastrado': True})
                }
            print("CPF não cadastrado:", cpf)
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                },
                'body': json.dumps({'cpfJaCadastrado': False})
            }
        print("Parâmetros de consulta não fornecidos.")
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
            },
            'body': json.dumps('Parâmetros de consulta não fornecidos.')
        }

    elif http_method == 'PATCH':
        user_id = event.get('queryStringParameters', {}).get('id')
        if user_id:
            body = normalize_field_names(json.loads(event.get('body', '{}')))
            print("Corpo da requisição PATCH:", body)
            response = table.get_item(Key={'id': user_id})
            if 'Item' in response:
                update_expression = 'SET '
                expression_attribute_values = {}

                # Checar se cada campo está presente no corpo da requisição e adicionar à expressão de atualização
                if 'nome' in body:
                    update_expression += 'nome = :n, '
                    expression_attribute_values[':n'] = body['nome']
                if 'email' in body:
                    update_expression += 'email = :e, '
                    expression_attribute_values[':e'] = body['email']
                if 'dataNascimento' in body:
                    update_expression += 'dataNascimento = :d, '
                    expression_attribute_values[':d'] = body['dataNascimento']
                if 'senha' in body:
                    hashed_senha = bcrypt.hashpw(body['senha'].encode('utf-8'), bcrypt.gensalt())
                    update_expression += 'senha = :s, '
                    expression_attribute_values[':s'] = hashed_senha.decode('utf-8')
                if 'telefone' in body:
                    update_expression += 'telefone = :t, '
                    expression_attribute_values[':t'] = body['telefone']
                if 'cep' in body:
                    update_expression += 'cep = :cep, '
                    expression_attribute_values[':cep'] = body['cep']
                if 'logradouro' in body:
                    update_expression += 'logradouro = :logradouro, '
                    expression_attribute_values[':logradouro'] = body['logradouro']
                if 'numero' in body:
                    update_expression += 'numero = :numero, '
                    expression_attribute_values[':numero'] = body['numero']
                if 'complemento' in body:
                    update_expression += 'complemento = :complemento, '
                    expression_attribute_values[':complemento'] = body['complemento']
                if 'bairro' in body:
                    update_expression += 'bairro = :bairro, '
                    expression_attribute_values[':bairro'] = body['bairro']
                if 'cidade' in body:
                    update_expression += 'cidade = :cidade, '
                    expression_attribute_values[':cidade'] = body['cidade']
                if 'uf' in body:
                    update_expression += 'uf = :uf, '
                    expression_attribute_values[':uf'] = body['uf']
                if 'anamnese' in body:
                    update_expression += 'anamnese = :a, '
                    expression_attribute_values[':a'] = body['anamnese']
                if 'orientacoes' in body:
                    update_expression += 'orientacoes = :o, '
                    expression_attribute_values[':o'] = body['orientacoes']
                if 'profile_picture' in body:
                    update_expression += 'profile_picture = :p, '
                    expression_attribute_values[':p'] = body['profile_picture']
                
                # Novos campos do formulário de onboarding
                if 'rg' in body:
                    update_expression += 'rg = :rg, '
                    expression_attribute_values[':rg'] = body['rg']
                if 'orgaoExpedidorRg' in body:
                    update_expression += 'orgaoExpedidorRg = :orgaoExpedidorRg, '
                    expression_attribute_values[':orgaoExpedidorRg'] = body['orgaoExpedidorRg']
                if 'ufOrgaoExpedidorRg' in body:
                    update_expression += 'ufOrgaoExpedidorRg = :ufOrgaoExpedidorRg, '
                    expression_attribute_values[':ufOrgaoExpedidorRg'] = body['ufOrgaoExpedidorRg']
                if 'pronome' in body:
                    update_expression += 'pronome = :pronome, '
                    expression_attribute_values[':pronome'] = body['pronome']
                if 'corRaca' in body:
                    update_expression += 'corRaca = :corRaca, '
                    expression_attribute_values[':corRaca'] = body['corRaca']
                if 'etnia' in body:
                    update_expression += 'etnia = :etnia, '
                    expression_attribute_values[':etnia'] = body['etnia']
                if 'rendaMensalIndividual' in body:
                    update_expression += 'rendaMensalIndividual = :rendaMensalIndividual, '
                    expression_attribute_values[':rendaMensalIndividual'] = body['rendaMensalIndividual']
                if 'rendaMensalFamiliar' in body:
                    update_expression += 'rendaMensalFamiliar = :rendaMensalFamiliar, '
                    expression_attribute_values[':rendaMensalFamiliar'] = body['rendaMensalFamiliar']
                if 'genero' in body:
                    update_expression += 'genero = :genero, '
                    expression_attribute_values[':genero'] = body['genero']
                if 'escolaridade' in body:
                    update_expression += 'escolaridade = :escolaridade, '
                    expression_attribute_values[':escolaridade'] = body['escolaridade']
                if 'quantasPessoasCasa' in body:
                    update_expression += 'quantasPessoasCasa = :quantasPessoasCasa, '
                    expression_attribute_values[':quantasPessoasCasa'] = body['quantasPessoasCasa']
                if 'estadoCivil' in body:
                    update_expression += 'estadoCivil = :estadoCivil, '
                    expression_attribute_values[':estadoCivil'] = body['estadoCivil']
                if 'planoSaude' in body:
                    update_expression += 'planoSaude = :planoSaude, '
                    expression_attribute_values[':planoSaude'] = body['planoSaude']
                if 'orientacaoSexual' in body:
                    update_expression += 'orientacaoSexual = :orientacaoSexual, '
                    expression_attribute_values[':orientacaoSexual'] = body['orientacaoSexual']
                if 'religiosidade' in body:
                    update_expression += 'religiosidade = :religiosidade, '
                    expression_attribute_values[':religiosidade'] = body['religiosidade']
                if 'nacionalidade' in body:
                    update_expression += 'nacionalidade = :nacionalidade, '
                    expression_attribute_values[':nacionalidade'] = body['nacionalidade']
                if 'profissao' in body:
                    update_expression += 'profissao = :profissao, '
                    expression_attribute_values[':profissao'] = body['profissao']
                if 'cpfUrl' in body:
                    update_expression += 'cpfUrl = :cpfUrl, '
                    expression_attribute_values[':cpfUrl'] = body['cpfUrl']
                if 'rgUrl' in body:
                    update_expression += 'rgUrl = :rgUrl, '
                    expression_attribute_values[':rgUrl'] = body['rgUrl']
                if 'laudoMedicoUrl' in body:
                    update_expression += 'laudoMedicoUrl = :laudoMedicoUrl, '
                    expression_attribute_values[':laudoMedicoUrl'] = body['laudoMedicoUrl']
                if 'receitaMedicaUrl' in body:
                    update_expression += 'receitaMedicaUrl = :receitaMedicaUrl, '
                    expression_attribute_values[':receitaMedicaUrl'] = body['receitaMedicaUrl']
                if 'termoAjuizamentoUrl' in body:
                    update_expression += 'termoAjuizamentoUrl = :termoAjuizamentoUrl, '
                    expression_attribute_values[':termoAjuizamentoUrl'] = body['termoAjuizamentoUrl']
                if 'comprovanteResidenciaUrl' in body:
                    update_expression += 'comprovanteResidenciaUrl = :comprovanteResidenciaUrl, '
                    expression_attribute_values[':comprovanteResidenciaUrl'] = body['comprovanteResidenciaUrl']
                if 'nomeProfissionalSaude' in body:
                    update_expression += 'nomeProfissionalSaude = :nomeProfissionalSaude, '
                    expression_attribute_values[':nomeProfissionalSaude'] = body['nomeProfissionalSaude']
                if 'numeroRegistroProfissional' in body:
                    update_expression += 'numeroRegistroProfissional = :numeroRegistroProfissional, '
                    expression_attribute_values[':numeroRegistroProfissional'] = body['numeroRegistroProfissional']
                if 'conquistas' in body:
                    update_expression += 'conquistas = :conquistas, '
                    expression_attribute_values[':conquistas'] = body['conquistas']
                 
                # Atualizar campos aninhados
                if 'conquistas.Onboarding.Cadastro' in body:
                    update_expression += 'conquistas.Onboarding.Cadastro = :cadastro, '
                    expression_attribute_values[':cadastro'] = body['conquistas.Onboarding.Cadastro']
                if 'conquistas.Onboarding.Endereco' in body:
                    update_expression += 'conquistas.Onboarding.Endereco = :endereco, '
                    expression_attribute_values[':endereco'] = body['conquistas.Onboarding.Endereco']
                if 'conquistas.Onboarding.InfoPessoal' in body:
                    update_expression += 'conquistas.Onboarding.InfoPessoal = :infopessoal, '
                    expression_attribute_values[':infopessoal'] = body['conquistas.Onboarding.InfoPessoal']
                if 'conquistas.Onboarding.Anamnese' in body:
                    update_expression += 'conquistas.Onboarding.Anamnese = :anamnese, '
                    expression_attribute_values[':anamnese'] = body['conquistas.Onboarding.Anamnese']
                if 'conquistas.Onboarding.Docs' in body:
                    update_expression += 'conquistas.Onboarding.Docs = :docs, '
                    expression_attribute_values[':docs'] = body['conquistas.Onboarding.Docs']
                if 'conquistas.OnboardingOk' in body:
                    update_expression += 'conquistas.OnboardingOk = :onboardingok, '
                    expression_attribute_values[':onboardingok'] = body['conquistas.OnboardingOk']
                if 'conquistas.Farmacia' in body:
                    update_expression += 'conquistas.Farmacia = :farmacia, '
                    expression_attribute_values[':farmacia'] = body['conquistas.Farmacia']
                if 'conquistas.Consulta' in body:
                    update_expression += 'conquistas.Consulta = :consulta, '
                    expression_attribute_values[':consulta'] = body['conquistas.Consulta']
                if 'conquistas.BemEstar' in body:
                    update_expression += 'conquistas.BemEstar = :bemestar, '
                    expression_attribute_values[':bemestar'] = body['conquistas.BemEstar']


                # Remover a última vírgula e espaço da expressão de atualização
                if update_expression.endswith(', '):
                    update_expression = update_expression[:-2]

                print("Expressão de atualização:", update_expression)
                print("Valores de atributos de atualização:", expression_attribute_values)

                if not expression_attribute_values:
                    print("Nenhum dado para atualizar.")
                    return {
                        'statusCode': 400,
                        'headers': {
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                            'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                        },
                        'body': json.dumps('Nenhum dado para atualizar.')
                    }

                # Atualizar o item no DynamoDB
                table.update_item(
                    Key={'id': user_id},
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_attribute_values,
                    ReturnValues="ALL_NEW"
                )

                # Recuperar o item atualizado
                updated_response = table.get_item(Key={'id': user_id})
                updated_item = updated_response.get('Item', {})
                updated_item.pop('senha', None)  # Remover a senha do item retornado
                updated_item = denormalize_field_names(normalize_field_names(updated_item))

                print("Item atualizado:", updated_item)
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                    },
                    'body': json.dumps(updated_item)
                }
            print("Usuário não encontrado para atualização:", user_id)
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
                },
                'body': json.dumps('Usuário não encontrado.')
            }
        print("ID do usuário não fornecido para atualização.")
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
            },
            'body': json.dumps('ID do usuário não fornecido.')
        }

    return {
        'statusCode': 405,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
        },
        'body': json.dumps('Método não permitido')
    }

