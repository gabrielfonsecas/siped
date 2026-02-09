from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Cadastro, NovaConsulta
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

class index(LoginView):
    template_name = 'index.html'

class CustomLogoutView(auth_views.LogoutView):
    template_name = 'logout.html'

@login_required
def menu(request):
    if request.user.is_authenticated:
        return render(request, 'core/menu.html')
    else:
        return redirect('login')
    

@login_required
def cadastroPaciente(request):
    if request.method == 'POST':
        # Captura os dados
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        cpf_responsavel = request.POST.get('cpf_responsavel')
        rg = request.POST.get('rg')
        rg_responsavel = request.POST.get('rg_responsavel')
        
        # Dicionário para repopular o formulário em caso de erro
        dados_preenchidos = {
            'nome': nome,
            'data_nascimento': request.POST.get('data_nascimento'),
            'prematuro': request.POST.get('prematuro'),
            'semanasCorrigidas': request.POST.get('semanasCorrigidas'),
            'diasCorrigidos': request.POST.get('diasCorrigidos'),
            'sexo': request.POST.get('sexo'),
            'tipo_sanguineo': request.POST.get('tipo_sanguineo'),
            'telefone': request.POST.get('telefone'),
            'cpf': cpf,
            'rg': rg,
            'endereco': request.POST.get('endereco'),
            'responsavel': request.POST.get('responsavel'),
            'cpf_responsavel': cpf_responsavel,
            'rg_responsavel': rg_responsavel,
        }

        # --- VALIDAÇÃO DE CPF (DUPLICIDADE E CRUZAMENTO) ---
        if cpf:
            if Cadastro.objects.filter(cpf=cpf).exists():
                messages.error(request, 'Erro: Já existe um paciente cadastrado com este CPF.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})
            
            if Cadastro.objects.filter(cpf_responsavel=cpf).exists():
                messages.error(request, 'Erro: Este CPF já está cadastrado como Responsável. Não pode ser usado para um Paciente.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})

        if cpf_responsavel:
            if Cadastro.objects.filter(cpf_responsavel=cpf_responsavel).exists():
                messages.error(request, 'Erro: Já existe um responsável cadastrado com este CPF.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})

            if Cadastro.objects.filter(cpf=cpf_responsavel).exists():
                messages.error(request, 'Erro: Este CPF já pertence a um Paciente. Não pode ser usado como Responsável.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})

        # --- VALIDAÇÃO DE RG (DUPLICIDADE E CRUZAMENTO) [NOVO] ---
        if rg:
            # Verifica se já é RG de Paciente
            if Cadastro.objects.filter(rg=rg).exists():
                messages.error(request, 'Erro: Já existe um paciente cadastrado com este RG.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})
            
            # Verifica se já é RG de Responsável (Cruzamento)
            if Cadastro.objects.filter(rg_responsavel=rg).exists():
                messages.error(request, 'Erro: Este RG já está cadastrado como Responsável. Não pode ser usado para um Paciente.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})

        if rg_responsavel:
            # Verifica se já é RG de Responsável
            if Cadastro.objects.filter(rg_responsavel=rg_responsavel).exists():
                messages.error(request, 'Erro: Já existe um responsável cadastrado com este RG.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})

            # Verifica se já é RG de Paciente (Cruzamento)
            if Cadastro.objects.filter(rg=rg_responsavel).exists():
                messages.error(request, 'Erro: Este RG já pertence a um Paciente. Não pode ser usado como Responsável.')
                return render(request, 'core/cadastroPaciente.html', {'values': dados_preenchidos})

        # --- FIM DA VALIDAÇÃO ---

        # Se passou por tudo, cria o objeto
        novo_paciente = Cadastro(
            nome=nome,
            data_nascimento=dados_preenchidos['data_nascimento'],
            prematuro=dados_preenchidos['prematuro'],
            semanasCorrigidas=dados_preenchidos['semanasCorrigidas'] or None,
            diasCorrigidos=dados_preenchidos['diasCorrigidos'] or None,
            sexo=dados_preenchidos['sexo'],
            tipo_sanguineo=dados_preenchidos['tipo_sanguineo'],
            telefone=dados_preenchidos['telefone'],
            cpf=cpf,
            rg=rg,
            endereco=dados_preenchidos['endereco'],
            responsavel=dados_preenchidos['responsavel'],
            cpf_responsavel=cpf_responsavel,
            rg_responsavel=rg_responsavel,
        )
        novo_paciente.save()
        messages.success(request, 'Paciente cadastrado com sucesso!')
        return redirect('listar_pacientes') 

    return render(request, 'core/cadastroPaciente.html')


@login_required
def paciente(request):
    pacientes = Cadastro.objects.all().order_by('nome') 
    paciente_selecionado = None

    if request.method == 'POST':
        paciente_id = request.POST.get('id_paciente') 
        if paciente_id:
            paciente_selecionado = get_object_or_404(Cadastro, id_paciente=paciente_id) 
        else:
            return redirect('paciente') 

    return render(request, 'core/paciente.html', {
        'pacientes': pacientes,
        'paciente': paciente_selecionado
    })

@login_required
def paciente_view(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)
    return render(request, 'core/paciente.html', {'paciente': paciente})

@login_required
def apagar_paciente(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente) 
    paciente.delete()
    return redirect('paciente')

@login_required
def editarPaciente(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)

    if request.method == 'POST':
        
        # Captura os dados
        novo_cpf = request.POST.get('cpf')
        novo_cpf_resp = request.POST.get('cpf_responsavel')
        novo_rg = request.POST.get('rg')
        novo_rg_resp = request.POST.get('rg_responsavel')
        
        # --- ATUALIZAÇÃO EM MEMÓRIA (Para manter o form preenchido se der erro) ---
        paciente.nome = request.POST.get('nome')
        
        data_nascimento = request.POST.get('data_nascimento')
        if data_nascimento:
            paciente.data_nascimento = data_nascimento

        paciente.prematuro = request.POST.get('prematuro')
        
        semanas_str = request.POST.get('semanasCorrigidas')
        dias_str = request.POST.get('diasCorrigidos')
        paciente.semanasCorrigidas = int(semanas_str) if semanas_str else None
        paciente.diasCorrigidos = int(dias_str) if dias_str else None

        paciente.sexo = request.POST.get('sexo')
        paciente.tipo_sanguineo = request.POST.get('tipo_sanguineo')
        paciente.telefone = request.POST.get('telefone')
        
        paciente.cpf = novo_cpf
        paciente.cpf_responsavel = novo_cpf_resp
        
        paciente.rg = novo_rg
        paciente.rg_responsavel = novo_rg_resp
        
        paciente.endereco = request.POST.get('endereco')
        paciente.responsavel = request.POST.get('responsavel')

        # --- VALIDAÇÃO DE DUPLICIDADE (CPF) ---
        erro_encontrado = False

        if novo_cpf:
            if Cadastro.objects.filter(cpf=novo_cpf).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: Este CPF de paciente já está em uso.')
                erro_encontrado = True
            elif Cadastro.objects.filter(cpf_responsavel=novo_cpf).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: Este CPF já está cadastrado como Responsável de outra pessoa.')
                erro_encontrado = True

        if not erro_encontrado and novo_cpf_resp:
            if Cadastro.objects.filter(cpf_responsavel=novo_cpf_resp).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: Este CPF de responsável já está vinculado a outro paciente.')
                erro_encontrado = True
            elif Cadastro.objects.filter(cpf=novo_cpf_resp).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: O CPF inserido para o responsável pertence a um Paciente cadastrado.')
                erro_encontrado = True
        
        # --- VALIDAÇÃO DE DUPLICIDADE (RG) [NOVO] ---
        if not erro_encontrado and novo_rg:
            # RG Paciente x RG Paciente (Outro)
            if Cadastro.objects.filter(rg=novo_rg).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: Este RG de paciente já está em uso.')
                erro_encontrado = True
            # RG Paciente x RG Responsável (Qualquer um)
            elif Cadastro.objects.filter(rg_responsavel=novo_rg).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: Este RG já está cadastrado como Responsável de outra pessoa.')
                erro_encontrado = True

        if not erro_encontrado and novo_rg_resp:
            # RG Responsável x RG Responsável (Outro)
            if Cadastro.objects.filter(rg_responsavel=novo_rg_resp).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: Este RG de responsável já está vinculado a outro paciente.')
                erro_encontrado = True
            # RG Responsável x RG Paciente (Qualquer um)
            elif Cadastro.objects.filter(rg=novo_rg_resp).exclude(id_paciente=id_paciente).exists():
                messages.error(request, 'Erro: O RG inserido para o responsável pertence a um Paciente cadastrado.')
                erro_encontrado = True

        # Se encontrou erro (CPF ou RG), renderiza novamente
        if erro_encontrado:
            return render(request, 'core/editarPaciente.html', {'paciente': paciente})

        # --- FIM DA VALIDAÇÃO ---

        # Se não houve erro, salva
        paciente.save()
        messages.success(request, 'Paciente atualizado com sucesso!')
        return redirect('listar_pacientes') 

    return render(request, 'core/editarPaciente.html', {'paciente': paciente})

@login_required
def excluirPaciente(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)

    if request.method == 'POST':
        paciente.delete()
        return redirect('core/menu.html')  # Redireciona para a lista de pacientes

    return render(request, 'core/confirmarExclusao.html', {'paciente': paciente})

from core.models import NovaConsulta  # Certifique-se de que o modelo está importado

@login_required
def novaConsulta(request, id_paciente=None):
    if id_paciente is None:
    # Caso sem id_paciente: Exibir a lista de pacientes para seleção
        pacientes = Cadastro.objects.all()
        return render(request, 'core/novaConsulta.html', {'pacientes': pacientes})

    # Caso com id_paciente: Exibir o formulário de nova consulta
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)

    # --- LÓGICA CORRIGIDA DO HISTÓRICO GESTACIONAL (GET) ---
    # 1. Buscamos o OBJETO da primeira consulta que tenha o histórico preenchido
    historicoExistenteObj = NovaConsulta.objects.filter(
        paciente=paciente
    ).exclude(
        historicoGestacional__exact=''
    ).first()
    
    # 2. A flag para mostrar o campo no template será True apenas se NENHUM histórico for encontrado
    campoHistorico = not bool(historicoExistenteObj)
    # --- FIM DA LÓGICA (GET) ---

    consultaAnterior = NovaConsulta.objects.filter(paciente=paciente).order_by('-dataConsulta').first()

    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        dataConsulta = request.POST.get('dataConsulta')
        if not dataConsulta:
            return render(request, 'core/novaConsulta.html', {
                'paciente': paciente,
                'consultaAnterior': consultaAnterior,
                'campoHistorico': campoHistorico,
                'error': 'A data da consulta é obrigatória.'
            })
        
        # --- LÓGICA CORRIGIDA PARA SALVAR O HISTÓRICO (POST) ---
        historicoGestacionalParaSalvar = ''
        if campoHistorico:
            # Se o campo estava visível, pegamos o valor do formulário.
            historicoGestacionalParaSalvar = request.POST.get('historicoGestacional', '')
        # CORREÇÃO: Usamos o objeto que buscamos antes (historicoExistenteObj)
        elif historicoExistenteObj:
            # Se o campo estava oculto, copiamos o valor do histórico já existente.
            historicoGestacionalParaSalvar = historicoExistenteObj.historicoGestacional
        # --- FIM DA LÓGICA (POST) ---

        novaConsultaObj = NovaConsulta(
            paciente=paciente, 
            nome=paciente.nome,
            dataConsulta=dataConsulta,
            idade=request.POST.get('idade'), 
            idadeMeses=request.POST.get('idadeMeses') or None,
            idadeCorrigida=request.POST.get('idadeCorrigida'),
            doencaPrevia=request.POST.get('doencaPrevia'),
            especificacaoDoencaPrevia=request.POST.get('especificacaoDoencaPrevia') or '',
            medicamentoUso=request.POST.get('medicamentoUso') or '',
            especificacaoMedicamentoUso=request.POST.get('especificacaoMedicamentoUso') or '',
            historicoGestacional=historicoGestacionalParaSalvar,
            anamnese=request.POST.get('anamnese') or '',
            peso=request.POST.get('peso') or '0',
            estatura=request.POST.get('estatura') or '0',
            avaliacaoEstatura=request.POST.get('avaliacaoEstatura') or '',
            avaliacaoPeso=request.POST.get('avaliacaoPeso') or '',
            imc=request.POST.get('imc') or '0',
            perimetroCefalico=request.POST.get('perimetroCefalico') or '0',
            testeReflexoVermelho=request.POST.get('testeReflexoVermelho') or '0',
            auscultaCardiaca=request.POST.get('auscultaCardiaca') or '',
            frequenciaCardiaca=request.POST.get('frequenciaCardiaca') or '0',
            pressaoArterial=request.POST.get('pressaoArterial') or '0',
            auscultaPulmonar=request.POST.get('auscultaPulmonar') or '',
            frequenciaRespiratoria=request.POST.get('frequenciaRespiratoria') or '0',
            temperatura=request.POST.get('temperatura') or '0',
            oroscopia=request.POST.get('oroscopia') or '',
            otoscopia=request.POST.get('otoscopia') or '',
            exameAbdominal=request.POST.get('exameAbdominal') or '',
            genituPelve=request.POST.get('genituPelve'),
            tanner=request.POST.get('tanner') or '',
            membrosInferiores=request.POST.get('membrosInferiores') or '',
            pele=request.POST.get('pele') or '',
            outrosExames=request.POST.get('outrosExames') or '',
            avaliacao=request.POST.get('avaliacao')or '',
            cid=request.POST.get('cid') or '',
            planoConduta=request.POST.get('planoConduta') or '',
        )
        novaConsultaObj.save()
        messages.success(request, 'Consulta cadastrada com sucesso!')
        return redirect('nova_consulta_listar_pacientes')

    context = {
        'paciente': paciente,
        'consultaAnterior': consultaAnterior,
        'campoHistorico': campoHistorico,
    }
    return render(request, 'core/novaConsulta.html', context)

@login_required
def consulta_view(request, consulta_id):
    # Obtém a consulta pelo ID ou retorna 404 se não existir
    consulta = get_object_or_404(NovaConsulta, id=consulta_id)
    
    # Renderiza o template com os dados da consulta
    return render(request, 'core/consulta.html', {'consulta': consulta})


@login_required
def listar_consultas(request):
    texto_busca = request.GET.get('nome', '').strip()

    if texto_busca:
        palavras = texto_busca.split()

        # Query para o NOME do paciente (dentro da consulta)
        query_nome = Q()
        for palavra in palavras:
            query_nome &= Q(paciente__nome__icontains=palavra)
        
        # Query para o CPF do responsável
        query_cpf = Q(paciente__cpf_responsavel__icontains=texto_busca)

        consultas = NovaConsulta.objects.filter(
            query_nome | query_cpf
        ).select_related('paciente').order_by('-dataConsulta')
    else:
        consultas = NovaConsulta.objects.all().order_by('-dataConsulta')

    paginator = Paginator(consultas, 10)
    page_number = request.GET.get('page')
    consultas = paginator.get_page(page_number)   
    return render(request, 'core/listar_consultas.html', {'consultas': consultas})


@login_required
def grafico_crescimento(request, id_paciente):
    consultas = NovaConsulta.objects.filter(
        paciente_id=id_paciente,
        estatura__isnull=False
    ).order_by('dataConsulta')

    historico = []
    for c in consultas:
        estatura_val = c.estatura
        if estatura_val is not None and str(estatura_val).strip() != '':
            try:
                idade_meses = c.idadeMeses
                historico.append({
                    'idade_meses': idade_meses,
                    'estatura': float(estatura_val),
                    'data': c.dataConsulta.strftime('%d/%m/%Y'),
                })
            except Exception:
                pass

    # Adiciona ponto da consulta atual (se vier via GET, ex: de novaConsulta)
    idade_meses_atual = request.GET.get('idade_meses')
    estatura_atual = request.GET.get('estatura')
    sexo_atual = request.GET.get('sexo')  # <-- Novo: pega sexo via GET, se vier

    if idade_meses_atual and estatura_atual:
        try:
            idade_meses_atual = int(idade_meses_atual)
            estatura_atual = float(estatura_atual)
            historico.append({
                'idade_meses': idade_meses_atual,
                'estatura': estatura_atual,
                'data': 'Consulta Atual'
            })
            idade_meses = idade_meses_atual
            altura = estatura_atual
            # Formata idade_exibicao para "X anos Y meses"
            anos = idade_meses_atual // 12
            meses = idade_meses_atual % 12
            idade_exibicao = f"{anos} anos {meses} meses" if anos else f"{meses} meses"
        except Exception:
            idade_meses = ''
            altura = ''
            idade_exibicao = ''
    else:
        idade_meses = ''
        altura = ''
        idade_exibicao = ''
        if consultas:
            ultima = consultas.last()
            idade_meses = ultima.idadeMeses
            idade_exibicao = ultima.idade
            altura = ultima.estatura

    # Busca o paciente normalmente
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)


    # Define o sexo: prioriza o GET, senão usa do paciente
    if sexo_atual:
        sexo = sexo_atual
    else:
        sexo = paciente.sexo if paciente else ''

    return render(request, 'core/graficoCrescimento.html', {
        'historico': historico,
        'paciente': paciente,
        'sexo': sexo,
        'idade_meses': idade_meses,
        'idade_exibicao': idade_exibicao,
        'altura': altura,
    })

@login_required
def paciente_view(request, id_paciente):
    # Obtém o paciente pelo ID ou retorna 404 se não existir
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)
    # Renderiza o template com os dados do paciente
    return render(request, 'core/paciente.html', {'paciente': paciente})

@login_required
def listar_pacientes(request):
    # Obtém o parâmetro de busca e remove espaços extras
    texto_busca = request.GET.get('nome', '').strip()

    if texto_busca:
        # Separa o texto em palavras (ex: "João Moraes" vira ["João", "Moraes"])
        palavras = texto_busca.split()

        # Monta a query para o NOME: O nome deve conter TODAS as palavras digitadas
        query_nome = Q()
        for palavra in palavras:
            query_nome &= Q(nome__icontains=palavra)

        # Monta a query para o CPF (busca simples pelo termo digitado)
        query_cpf = Q(cpf_responsavel__icontains=texto_busca)

        # Filtra: (Contém todas as palavras no nome) OU (Contém o termo no CPF)
        pacientes_list = Cadastro.objects.filter(
            query_nome | query_cpf
        ).order_by('nome')
    else:
        pacientes_list = Cadastro.objects.all().order_by('nome')

    paginator = Paginator(pacientes_list, 10)
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)   

    return render(request, 'core/listar_pacientes.html', {'pacientes': pacientes})


@login_required
def nova_consulta_listar_pacientes(request):
    texto_busca = request.GET.get('nome', '').strip()
    
    if texto_busca:
        palavras = texto_busca.split()

        query_nome = Q()
        for palavra in palavras:
            query_nome &= Q(nome__icontains=palavra)

        query_cpf = Q(cpf_responsavel__icontains=texto_busca)

        pacientes_list = Cadastro.objects.filter(
            query_nome | query_cpf
        ).order_by('nome')
    else:
        pacientes_list = Cadastro.objects.all().order_by('nome')

    paginator = Paginator(pacientes_list, 10)
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)

    return render(request, 'core/nova_consulta_listar_pacientes.html', {'pacientes': pacientes})


@login_required
def listar_paciente_grafico(request):
    texto_busca = request.GET.get('nome', '').strip()
    
    if texto_busca:
        palavras = texto_busca.split()

        query_nome = Q()
        for palavra in palavras:
            query_nome &= Q(nome__icontains=palavra)

        query_cpf = Q(cpf_responsavel__icontains=texto_busca)

        pacientes_list = Cadastro.objects.filter(
            query_nome | query_cpf
        ).order_by('nome')
    else:
        pacientes_list = Cadastro.objects.all().order_by('nome')

    paginator = Paginator(pacientes_list, 10)
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)

    return render(request, 'core/listar_paciente_grafico.html', {'pacientes': pacientes})