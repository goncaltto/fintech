// URL base da API Python (Flask). Ajuste quando hospedar o backend.
const API_BASE_URL = "http://127.0.0.1:5000";

const form = document.getElementById("form-cashback");
const resultadoSecao = document.getElementById("resultado");
const resultadoTexto = document.getElementById("resultado-texto");
const erroMensagem = document.getElementById("erro-mensagem");

const tabelaCorpo = document.getElementById("tabela-historico-corpo");
const historicoVazio = document.getElementById("historico-vazio");

// Esconde resultado/erro antes de uma nova tentativa
function limparMensagens() {
  resultadoSecao.hidden = true;
  erroMensagem.hidden = true;
  erroMensagem.textContent = "";
}

function mostrarErro(mensagem) {
  erroMensagem.textContent = mensagem;
  erroMensagem.hidden = false;
}

// Envia os dados do formulário para a API e calcula o cashback
async function calcularCashback(event) {
  event.preventDefault();
  limparMensagens();

  const tipoCliente = document.getElementById("tipo_cliente").value;
  const valorCompra = parseFloat(document.getElementById("valor_compra").value);
  const descontoPercentual = parseFloat(document.getElementById("desconto").value) || 0;
  const desconto = descontoPercentual / 100; // o backend espera decimal (ex: 0.20)

  try {
    const resposta = await fetch(`${API_BASE_URL}/cashback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tipo_cliente: tipoCliente,
        valor_compra: valorCompra,
        desconto: desconto
      })
    });

    if (!resposta.ok) {
      const erroData = await resposta.json().catch(() => null);
      throw new Error(erroData?.erro || "Erro ao calcular o cashback.");
    }

    const dados = await resposta.json();

    resultadoTexto.textContent =
      `Cashback calculado: R$ ${dados.cashback.toFixed(2)}`;
    resultadoSecao.hidden = false;

    // Atualiza o histórico após um novo cálculo
    carregarHistorico();
  } catch (erro) {
    mostrarErro(erro.message || "Não foi possível conectar à API.");
  }
}

// Busca o histórico de consultas do IP do usuário
async function carregarHistorico() {
  try {
    const resposta = await fetch(`${API_BASE_URL}/historico`);

    if (!resposta.ok) {
      throw new Error("Erro ao carregar o histórico.");
    }

    const consultas = await resposta.json();
    renderizarHistorico(consultas);
  } catch (erro) {
    mostrarErro(erro.message || "Não foi possível carregar o histórico.");
  }
}

// Monta as linhas da tabela de histórico
function renderizarHistorico(consultas) {
  tabelaCorpo.innerHTML = "";

  if (!consultas || consultas.length === 0) {
    historicoVazio.hidden = false;
    return;
  }

  historicoVazio.hidden = true;

  consultas.forEach((consulta) => {
    const linha = document.createElement("tr");

    const tdTipo = document.createElement("td");
    tdTipo.textContent = consulta.tipo_cliente;

    const tdValor = document.createElement("td");
    tdValor.textContent = `R$ ${Number(consulta.valor_compra).toFixed(2)}`;

    const tdCashback = document.createElement("td");
    tdCashback.textContent = `R$ ${Number(consulta.cashback).toFixed(2)}`;

    const tdData = document.createElement("td");
    tdData.textContent = consulta.criado_em || "";

    linha.append(tdTipo, tdValor, tdCashback, tdData);
    tabelaCorpo.appendChild(linha);
  });
}

form.addEventListener("submit", calcularCashback);

// Carrega o histórico assim que a página abre
document.addEventListener("DOMContentLoaded", carregarHistorico);