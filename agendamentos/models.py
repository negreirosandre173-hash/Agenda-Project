from django.db import models
from django.contrib.auth.models import User

class Servico(models.Model):
    empresa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos')
    nome = models.CharField(max_length=100, verbose_name="Nome do Serviço")
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço (R$)")
    duracao_minutos = models.PositiveIntegerField(default=30, verbose_name="Duração (minutos)")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

class Profissional(models.Model):
    empresa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profissionais')
    nome = models.CharField(max_length=100, verbose_name="Nome do Profissional")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp (opcional)")
    servicos = models.ManyToManyField(Servico, related_name='profissionais', verbose_name="Serviços que realiza")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Disponibilidade(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='disponibilidades')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA, verbose_name="Dia da Semana")
    hora_inicio = models.TimeField(verbose_name="Início")
    hora_fim = models.TimeField(verbose_name="Fim")

    class Meta:
        ordering = ['profissional', 'dia_semana', 'hora_inicio']

    def __str__(self):
        return f"{self.profissional.nome} - {self.get_dia_semana_display()} ({self.hora_inicio} às {self.hora_fim})"
