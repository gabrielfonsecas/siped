from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Cadastro
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect


# from django.urls import reverse_lazy


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
        # Cria um novo paciente
        novo_paciente = Cadastro(
            nome=request.POST.get('nome'),
            data_nascimento=request.POST.get('data_nascimento'),
            prematuro = request.POST.get('prematuro'),
            semanasCorrigidas = request.POST.get('semanasCorrigidas') or None,
            diasCorrigidos = request.POST.get('diasCorrigidos') or None,
            sexo=request.POST.get('sexo'),
            tipo_sanguineo=request.POST.get('tipo_sanguineo'),
            telefone=request.POST.get('telefone'),
            cpf=request.POST.get('cpf'),
            rg=request.POST.get('rg'),
            endereco=request.POST.get('endereco'),
            responsavel=request.POST.get('responsavel'),
            cpf_responsavel=request.POST.get('cpf_responsavel'),
            rg_responsavel=request.POST.get('rg_responsavel'),
        )
        novo_paciente.save()
        messages.success(request, 'Paciente cadastrado com sucesso!')
        return redirect('listar_pacientes')  # Redireciona para o próprio formulário

    return render(request, 'core/cadastroPaciente.html')


@login_required
def paciente(request):
    pacientes = Cadastro.objects.all().order_by('nome')  # Busca todos os pacientes
    paciente_selecionado = None

    if request.method == 'POST':
        paciente_id = request.POST.get('id_paciente')  # Obtém o id_paciente do formulário
        if paciente_id:
            paciente_selecionado = get_object_or_404(Cadastro, id_paciente=paciente_id)  # Use id_paciente
        else:
            return redirect('paciente')  # Redireciona se nenhum paciente for selecionado

    return render(request, 'core/paciente.html', {
        'pacientes': pacientes,
        'paciente': paciente_selecionado
    })

@login_required
# Busca o paciente pelo ID ou retorna um erro 404 se não for encontrado
def paciente_view(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)
    return render(request, 'core/paciente.html', {'paciente': paciente})

@login_required
def apagar_paciente(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)  # Use id_paciente
    paciente.delete()
    return redirect('paciente')

@login_required
def editarPaciente(request, id_paciente):
    paciente = get_object_or_404(Cadastro, id_paciente=id_paciente)

    if request.method == 'POST':
        paciente.nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        if data_nascimento:  # Só atualiza se vier preenchido
            paciente.data_nascimento = data_nascimento
        paciente.sexo = request.POST.get('sexo')
        paciente.tipo_sanguineo = request.POST.get('tipo_sanguineo')
        paciente.telefone = request.POST.get('telefone')
        paciente.cpf = request.POST.get('cpf')
        paciente.rg = request.POST.get('rg')
        paciente.endereco = request.POST.get('endereco')
        paciente.responsavel = request.POST.get('responsavel')
        paciente.cpf_responsavel = request.POST.get('cpf_responsavel')
        paciente.rg_responsavel = request.POST.get('rg_responsavel')
        paciente.save()
        return redirect('paciente', id_paciente=id_paciente)

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

    # Busca o histórico de consultas do paciente
    consultaAnterior = NovaConsulta.objects.filter(nome=paciente.nome).order_by('-dataConsulta').first()


    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        dataConsulta = request.POST.get('dataConsulta')
        if not dataConsulta:
            return render(request, 'core/novaConsulta.html', {
                'paciente': paciente,
                'consulta_anterior': consultaAnterior,
                'error': 'A data da consulta é obrigatória.'
            })

        novaConsulta = NovaConsulta(
            paciente=paciente, 
            nome=paciente.nome,
            dataConsulta=dataConsulta,
            idade=request.POST.get('idade'), 
            idadeMeses=request.POST.get('idadeMeses'),
            idadeCorrigida=request.POST.get('idadeCorrigida'),
            doencaPrevia=request.POST.get('doencaPrevia'),
            especificacaoDoencaPrevia=request.POST.get('especificacaoDoencaPrevia') or '',
            medicamentoUso=request.POST.get('medicamentoUso') or '',
            especificacaoMedicamentoUso=request.POST.get('especificacaoMedicamentoUso') or '',
            historicoGestacional=request.POST.get('historicoGestacional') or '',
            anamnese=request.POST.get('anamnese') or '',
            peso=request.POST.get('peso') or '0',
            estatura=request.POST.get('estatura') or '0',
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
        novaConsulta.save()
        messages.success(request, 'Consulta cadastrada com sucesso!')
        return redirect('nova_consulta_listar_pacientes')  # Redireciona para a lista de consultas ou outra página

    return render(request, 'core/novaConsulta.html', {
        'paciente': paciente,
        'consultaAnterior': consultaAnterior
    })

@login_required
def consulta_view(request, consulta_id):
    # Obtém a consulta pelo ID ou retorna 404 se não existir
    consulta = get_object_or_404(NovaConsulta, id=consulta_id)
    
    # Renderiza o template com os dados da consulta
    return render(request, 'core/consulta.html', {'consulta': consulta})


@login_required
def listar_consultas(request):
    # Obtém o parâmetro de busca
    nome = request.GET.get('nome', '')

    # Filtra as consultas pelo nome do paciente e ordena por data (mais recentes primeiro)
    if nome:
        consultas = NovaConsulta.objects.filter(paciente__nome__icontains=nome).select_related('paciente').order_by('-dataConsulta')
    else:
        consultas = NovaConsulta.objects.all().order_by('-dataConsulta')

    paginator = Paginator(consultas, 10)  # 10 pacientes por página
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
    # Obtém o parâmetro de busca
    nome = request.GET.get('nome', '')

    # Filtra os pacientes pelo nome e ordena por nome (alfabético)
    if nome:
        pacientes_list = Cadastro.objects.filter(nome__icontains=nome).order_by('nome')
    else:
        pacientes_list = Cadastro.objects.all().order_by('nome')

    paginator = Paginator(pacientes_list, 10)  # 10 pacientes por página
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)   

    return render(request, 'core/listar_pacientes.html', {'pacientes': pacientes})


@login_required
def nova_consulta_listar_pacientes(request):
    nome = request.GET.get('nome', '')
    if nome:
        pacientes_list = Cadastro.objects.filter(nome__icontains=nome).order_by('nome')
    else:
        pacientes_list = Cadastro.objects.all().order_by('nome')

    paginator = Paginator(pacientes_list, 10)  # 10 pacientes por página
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)

    return render(request, 'core/nova_consulta_listar_pacientes.html', {'pacientes': pacientes})


@login_required
def listar_paciente_grafico(request):
    nome = request.GET.get('nome', '')
    if nome:
        pacientes_list = Cadastro.objects.filter(nome__icontains=nome).order_by('nome')
    else:
        pacientes_list = Cadastro.objects.all().order_by('nome')

    paginator = Paginator(pacientes_list, 10)  # 10 pacientes por página
    page_number = request.GET.get('page')
    pacientes = paginator.get_page(page_number)

    return render(request, 'core/listar_paciente_grafico.html', {'pacientes': pacientes})