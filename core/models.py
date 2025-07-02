from django.db import models

class Cadastro(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    nome = models.TextField(null=True, blank=True, max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)
    prematuro = models.CharField(max_length=3, choices=[('sim', 'Sim'), ('nao', 'Não')], blank=True, null=True)
    semanasCorrigidas = models.IntegerField(null=True, blank=True)
    diasCorrigidos = models.IntegerField(null=True, blank=True)
    sexo = models.TextField(max_length=10, null=True, blank=True, choices=[
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('outro', 'Outro'),
    ])
    tipo_sanguineo = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ])
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    responsavel = models.CharField(max_length=255, blank=True, null=True)
    cpf_responsavel = models.CharField(max_length=14, blank=True, null=True, default='')
    rg_responsavel = models.CharField(max_length=20, blank=True, null=True, default='')
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.nome.lower()
        if self.responsavel:
            self.responsavel = self.responsavel.lower()
        if self.endereco:
            self.endereco = self.endereco.lower()
        super().save(*args, **kwargs)

    @property
    def semanaCorrigida(self):
        if self.prematuro and self.semanasCorrigidas:
            return 40 - self.semanasCorrigidas
        return ""
    
    @property
    def diaCorrigido(self):
        if self.prematuro and self.diasCorrigidos:
            return 30 - self.diasCorrigidos
        return ""

class NovaConsulta(models.Model):
    # Informações do paciente
    paciente = models.ForeignKey(Cadastro, on_delete=models.CASCADE,  null=True, blank=True)
    nome = models.CharField(max_length=255)
    dataConsulta = models.DateField()
    idade = models.CharField(max_length=50, blank=True, null=True) 
    idadeMeses = models.IntegerField(blank=True, null=True)  # idade em meses
    idadeCorrigida = models.TextField(blank=True, null=True)
    doencaPrevia = models.CharField(max_length=3, choices=[('sim', 'Sim'), ('nao', 'Não')], blank=True, null=True)
    especificacaoDoencaPrevia = models.TextField(blank=True, null=True)
    medicamentoUso = models.CharField(max_length=3, choices=[('sim', 'Sim'), ('nao', 'Não')], blank=True, null=True)
    especificacaoMedicamentoUso = models.TextField(blank=True, null=True)
    historicoGestacional = models.TextField(blank=True, null=True)
    anamnese = models.TextField(blank=True, null=True)

    # Dados objetivos
    peso = models.FloatField(blank=True, null=True)
    estatura = models.FloatField(blank=True, null=True)
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    perimetroCefalico = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    testeReflexoVermelho = models.TextField(blank=True, null=True)
    auscultaCardiaca = models.TextField(blank=True, null=True)
    frequenciaCardiaca = models.IntegerField(blank=True, null=True)
    pressaoArterial = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    auscultaPulmonar = models.TextField(blank=True, null=True)
    frequenciaRespiratoria = models.IntegerField(blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    oroscopia = models.TextField(blank=True, null=True)
    otoscopia = models.TextField(blank=True, null=True)
    exameAbdominal = models.TextField(blank=True, null=True)
    genituPelve = models.TextField(blank=True, null=True)
    tanner = models.TextField(blank=True, null=True)
    membrosInferiores = models.TextField(blank=True, null=True)
    pele = models.TextField(blank=True, null=True)
    outrosExames = models.TextField(blank=True, null=True)

    # Avaliação e plano de conduta
    avaliacao = models.TextField(blank=True, null=True)
    cid = models.CharField(max_length=20, blank=True, null=True)
    planoConduta = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consulta de {self.nome} em {self.dataConsulta}"
    
    def save(self, *args, **kwargs):
        if self.especificacaoDoencaPrevia:
            self.especificacaoDoencaPrevia = self.especificacaoDoencaPrevia.lower()
        if self.especificacaoMedicamentoUso:
            self.especificacaoMedicamentoUso = self.especificacaoMedicamentoUso.lower()
        if self.historicoGestacional:
            self.historicoGestacional = self.historicoGestacional.lower()
        if self.anamnese:
            self.anamnese = self.anamnese.lower()
        if self.testeReflexoVermelho:
            self.testeReflexoVermelho = self.testeReflexoVermelho.lower()
        if self.auscultaCardiaca:
            self.auscultaCardiaca = self.auscultaCardiaca.lower()
        if self.auscultaPulmonar:
            self.auscultaPulmonar = self.auscultaPulmonar.lower()
        if self.otoscopia:
            self.otoscopia = self.otoscopia.lower()
        if self.oroscopia:
            self.oroscopia = self.oroscopia.lower()
        if self.exameAbdominal:
            self.exameAbdominal = self.exameAbdominal.lower()
        if self.genituPelve:
            self.genituPelve = self.genituPelve.lower()
        if self.membrosInferiores:
            self.membrosInferiores = self.membrosInferiores.lower()
        if self.pele:
            self.pele = self.pele.lower()
        if self.outrosExames:
            self.outrosExames = self.outrosExames.lower()
        if self.tanner:
            self.tanner = self.tanner.lower()
        if self.avaliacao:
            self.avaliacao = self.avaliacao.lower()
        if self.planoConduta:   
            self.planoConduta = self.planoConduta.lower()
        super().save(*args, **kwargs)
    
    