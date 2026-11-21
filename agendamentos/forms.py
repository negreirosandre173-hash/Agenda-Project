from django import forms
from .models import Servico, Profissional, Disponibilidade

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'preco', 'duracao_minutos']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Corte Masculino, Consulta Urgência...'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Ex: 50.00'}),
            'duracao_minutos': forms.NumberInput(attrs={'step': '5', 'placeholder': 'Ex: 30'}),
        }

class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ['nome', 'telefone', 'servicos']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Dr. Carlos, Ana Manicure...'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Ex: (61) 99999-9999'}),
            'servicos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra apenas os serviços ativos da empresa logada
        self.fields['servicos'].queryset = Servico.objects.filter(empresa=user, ativo=True).order_by('nome')

class DisponibilidadeForm(forms.ModelForm):
    class Meta:
        model = Disponibilidade
        fields = ['profissional', 'dia_semana', 'hora_inicio', 'hora_fim']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['profissional'].queryset = Profissional.objects.filter(empresa=user, ativo=True).order_by('nome')
        self.fields['profissional'].empty_label = "Profissional"
        
        self.fields['dia_semana'].choices = [('','Dia da semana')] + list(Disponibilidade.DIAS_SEMANA)