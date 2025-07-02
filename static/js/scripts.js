function calcularIdade(dataNascimento, idadeSpanId) {
    const idadeSpan = document.getElementById(idadeSpanId);
    if (idadeSpan && dataNascimento) {
        const hoje = new Date();
        const nascimento = new Date(dataNascimento);
        let anos = hoje.getFullYear() - nascimento.getFullYear();
        let meses = hoje.getMonth() - nascimento.getMonth();
        let dias = hoje.getDate() - nascimento.getDate();
        if (meses < 0 || (meses === 0 && dias < 0)) {
            anos--;
            meses += 12;
        }
        if (dias < 0) {
            const ultimoDiaMesAnterior = new Date(
                hoje.getFullYear(),
                hoje.getMonth(),
                0
            ).getDate();
            dias += ultimoDiaMesAnterior;
            meses--;
        }
        idadeSpan.textContent = `${anos} anos ${meses} meses ${dias} dias`;
    } else if (idadeSpan) {
        idadeSpan.textContent = "Data de nascimento não disponível";
    }
}

// Funções de formatação
function formatarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

function formatarRG(rg) {
    rg = rg.replace(/\D/g, '');
    return rg.replace(/(\d{1})(\d{3})(\d{3})/, '$1.$2.$3');
}

function formatarTelefone(telefone) {
    telefone = telefone.replace(/\D/g, '');
    if (telefone.length === 11) {
        return telefone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (telefone.length === 10) {
        return telefone.replace(/(\d{5})(\d{4})/, '$1-$2');
    }
    return telefone;
}

// Função de validação de CPF
function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
        return false;
    }
    let soma = 0;
    let resto;
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) {
        resto = 0;
    }
    if (resto !== parseInt(cpf.substring(9, 10))) {
        return false;
    }
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }
    resto = (soma * 10) % 11;
    if ((resto === 10) || (resto === 11)) {
        resto = 0;
    }
    return resto === parseInt(cpf.substring(10, 11));
}

// Funções para verificar CPF único (requisição AJAX)
async function validarCPFUnico(cpf) {
    const response = await fetch(`/verificar_cpf/?cpf=${cpf}`);
    const data = await response.json();
    return !data.cpf_existe;
}

async function validarCPFResponsavelUnico(cpfResponsavel) {
    const response = await fetch(`/verificar_cpf_responsavel/?cpf_responsavel=${cpfResponsavel}`);
    const data = await response.json();
    return !data.cpf_responsavel_existe;
}

// Validação do formulário de cadastro de paciente
function inicializarCadastroPaciente() {
    const form = document.getElementById('formCadastroPaciente');
    if (!form) return;
    const nomePacienteInput = document.getElementById('nome');
    const nomeResponsavelInput = document.getElementById('responsavel');
    const dataNascimentoInput = document.getElementById('data_nascimento');
    const telefoneInput = document.getElementById('telefone');
    const cpfInput = document.getElementById('cpf');
    const cpfResponsavelInput = document.getElementById('cpf_responsavel');

    form.addEventListener('submit', async function (event) {
        // Validação do Nome do Paciente
        if (!nomePacienteInput.value.trim()) {
            event.preventDefault();
            alert('Por favor, preencha o nome do paciente.');
            nomePacienteInput.focus();
            return;
        }
        // Validação do Nome do Responsável
        if (!nomeResponsavelInput.value.trim()) {
            event.preventDefault();
            alert('Por favor, preencha o nome do responsável.');
            nomeResponsavelInput.focus();
            return;
        }
        // Validação de Data de Nascimento
        if (!dataNascimentoInput.value.trim()) {
            event.preventDefault();
            alert('Por favor, preencha a data de nascimento.');
            dataNascimentoInput.focus();
            return;
        }
        // Validação de Telefone
        if (!telefoneInput.value.trim()) {
            event.preventDefault();
            alert('Por favor, preencha o telefone.');
            telefoneInput.focus();
            return;
        }
        // Validação de CPF do paciente (agora opcional)
        let cpfFormatado = '';
        if (cpfInput.value.trim()) {
            cpfFormatado = formatarCPF(cpfInput.value);
            if (!validarCPF(cpfFormatado)) {
                event.preventDefault();
                alert('CPF do paciente inválido.');
                cpfInput.focus();
                return;
            }
            // Verificar CPF único apenas se informado
            const cpfValido = await validarCPFUnico(cpfFormatado);
            if (!cpfValido) {
                event.preventDefault();
                alert('CPF de paciente já cadastrado.');
                return;
            }
        }
        // Validação de CPF do responsável (obrigatório)
        const cpfResponsavelFormatado = formatarCPF(cpfResponsavelInput.value);
        if (!validarCPF(cpfResponsavelFormatado)) {
            event.preventDefault();
            alert('CPF do responsável inválido.');
            cpfResponsavelInput.focus();
            return;
        }
        if (cpfFormatado && cpfFormatado === cpfResponsavelFormatado) {
            event.preventDefault();
            alert('O CPF do paciente não pode ser igual ao CPF do responsável.');
            return;
        }
        const cpfResponsavelValido = await validarCPFResponsavelUnico(cpfResponsavelFormatado);
        if (!cpfResponsavelValido) {
            event.preventDefault();
            alert('CPF do responsável já cadastrado como CPF de paciente.');
            return;
        }
        // Atualiza os valores dos campos com os formatos corretos
        if (cpfFormatado) cpfInput.value = cpfFormatado;
        cpfResponsavelInput.value = cpfResponsavelFormatado;
        // O form será submetido normalmente
    });
}

// --- Scripts de novaConsulta ---
function calcularIMC() {
    // Obtém os valores de peso e estatura
    const peso = parseFloat(document.getElementById('pesoInput').value);
    const estatura = parseFloat(document.getElementById('estaturaInput').value) / 100; // Converte cm para metros

    // Verifica se os valores são válidos
    if (!isNaN(peso) && !isNaN(estatura) && estatura > 0) {
        // Calcula o IMC
        const imc = (peso / (estatura * estatura)).toFixed(2);
        document.getElementById('imcResult').value = imc;

        // Determina a classificação do IMC
        let classificacao;
        if (imc < 18.5) {
            classificacao = "Abaixo do peso - Menor que 18.5";
        } else if (imc >= 18.5 && imc <= 24.9) {
            classificacao = "Peso normal - Entre 18.5 e 24.9";
        } else if (imc >= 25 && imc <= 29.9) {
            classificacao = "Sobrepeso - Entre 25 e 29.9";
        } else if (imc >= 30 && imc <= 34.9) {
            classificacao = "Obesidade grau I - Entre 30 e 34.9";
        } else if (imc >= 35 && imc <= 39.9) {
            classificacao = "Obesidade grau II - Entre 35 e 39.9";
        } else {
            classificacao = "Obesidade grau III - Maior ou igual a 40";
        }

        // Exibe a classificação e a tabela de IMC
        document.getElementById('imcClassificacao').textContent = classificacao;
        document.getElementById('imcTable').style.display = 'block';
    } else {
        // Exibe um alerta se os valores forem inválidos
        alert('Por favor, preencha os campos de peso e estatura corretamente.');
    }
}

function redirecionar(event) {
    event.preventDefault(); // Impede o envio padrão do formulário
    const select = document.getElementById('id_paciente');
    const idPaciente = select.value; // Obtém o ID do paciente selecionado
    if (idPaciente) {
        window.location.href = `/novaConsulta/${idPaciente}/`;
    } else {
        alert('Por favor, selecione um paciente.');
    }
}

function inicializarNovaConsultaScripts() {
    // Impede submit com Enter exceto em textarea
    const form = document.getElementById('nova-consulta-form');
    if (form) {
        form.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                const activeElement = document.activeElement;
                if (activeElement.tagName.toLowerCase() === 'textarea') {
                    return;
                }
                event.preventDefault();
                const formElements = Array.from(form.elements);
                const currentIndex = formElements.indexOf(activeElement);
                const nextElement = formElements[currentIndex + 1];
                if (nextElement) {
                    nextElement.focus();
                }
            }
        });
    }

    // Select2
    if (window.jQuery && $('.js-example-basic-single').length) {
        $('.js-example-basic-single').select2({
            placeholder: "Selecione o paciente",
            allowClear: true
        });
    }

    // Mostrar/ocultar campos de doenças prévias e medicamentos
    const doencaPrevias = document.querySelectorAll('input[name="doencaPrevia"]');
    const medicamentoUso = document.querySelectorAll('input[name="medicamentoUso"]');
    doencaPrevias.forEach(input => {
        input.addEventListener('change', function () {
            const campoDoencaPrevias = document.getElementById('campoDoencaPrevia');
            campoDoencaPrevias.style.display = this.value === 'sim' ? 'block' : 'none';
        });
    });
    medicamentoUso.forEach(input => {
        input.addEventListener('change', function () {
            const campoMedicamentoUso = document.getElementById('campoMedicamentoUso');
            campoMedicamentoUso.style.display = this.value === 'sim' ? 'block' : 'none';
        });
    });

    // Preencher data da consulta com data atual
    const dataConsultaInput = document.querySelector('input[name="dataConsulta"]');
    if (dataConsultaInput) {
        const hoje = new Date();
        const dia = String(hoje.getDate()).padStart(2, '0');
        const mes = String(hoje.getMonth() + 1).padStart(2, '0');
        const ano = hoje.getFullYear();
        const dataAtual = `${ano}-${mes}-${dia}`;
        dataConsultaInput.value = dataAtual;
    }
}

// Inicialização centralizada para cadastro de paciente e nova consulta
document.addEventListener('DOMContentLoaded', function () {
    inicializarCadastroPaciente();
    inicializarNovaConsultaScripts();
});

