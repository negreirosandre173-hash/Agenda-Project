from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Servico, Profissional, Disponibilidade
from .forms import ServicoForm, ProfissionalForm, DisponibilidadeForm

@login_required
def painel_admin(request):
    return redirect('gerenciar_servicos')

@login_required
def gerenciar_servicos(request):
    servicos = Servico.objects.filter(empresa=request.user, ativo=True).order_by('nome')
    
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.empresa = request.user
            servico.save()
            return redirect('gerenciar_servicos')
    else:
        form = ServicoForm()

    return render(request, 'agendamentos/servicos.html', {
        'form': form,
        'servicos': servicos
    })

@login_required
def desativar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id, empresa=request.user)
    servico.ativo = False
    servico.save()
    return redirect('gerenciar_servicos')

@login_required
def gerenciar_profissionais(request):
    profissionais = Profissional.objects.filter(empresa=request.user, ativo=True).order_by('nome')
    
    if request.method == 'POST':
        form = ProfissionalForm(request.user, request.POST)
        if form.is_valid():
            profissional = form.save(commit=False)
            profissional.empresa = request.user
            profissional.save()
            form.save_m2m()  # Salva os serviços marcados nas caixinhas
            return redirect('gerenciar_profissionais')
    else:
        form = ProfissionalForm(request.user)

    return render(request, 'agendamentos/profissionais.html', {
        'form': form,
        'profissionais': profissionais
    })

@login_required
def desativar_profissional(request, profissional_id):
    profissional = get_object_or_404(Profissional, id=profissional_id, empresa=request.user)
    profissional.ativo = False
    profissional.save()
    return redirect('gerenciar_profissionais')


@login_required
def gerenciar_horarios(request):
    horarios = Disponibilidade.objects.filter(
        profissional__empresa=request.user,
        profissional__ativo=True
    )
    
    if request.method == 'POST':
        form = DisponibilidadeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_horarios')
    else:
        form = DisponibilidadeForm(request.user)

    return render(request, 'agendamentos/horarios.html', {
        'form': form,
        'horarios': horarios
    })

@login_required
def remover_horario(request, horario_id):
    horario = get_object_or_404(Disponibilidade, id=horario_id, profissional__empresa=request.user)
    horario.delete()
    return redirect('gerenciar_horarios')