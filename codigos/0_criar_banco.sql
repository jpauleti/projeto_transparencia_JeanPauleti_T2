-- PROJETO: Transparência em Viagens a Serviço
-- AUTOR: Jean Pauleti
-- TURMA: T2
-- SGBD: MySQL
-- SCHEMA: transparencia

DROP DATABASE IF EXISTS transparencia;

CREATE DATABASE transparencia
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE transparencia;

-- CAMADA RAW
-- Cópia fiel dos arquivos CSV.
-- Todas as colunas permanecem como texto e sem constraints.

-- Tabela: raw_viagem
-- Origem: 2025_Viagem.csv

CREATE TABLE raw_viagem (
    id_viagem VARCHAR(255),
    num_proposta VARCHAR(255),
    situacao VARCHAR(255),
    viagem_urgente VARCHAR(255),
    justificativa_urgencia TEXT,
    cod_orgao_superior VARCHAR(255),
    nome_orgao_superior VARCHAR(500),
    cod_orgao_solicitante VARCHAR(255),
    nome_orgao_solicitante VARCHAR(500),
    cpf_viajante VARCHAR(255),
    nome_viajante VARCHAR(500),
    cargo VARCHAR(500),
    funcao VARCHAR(500),
    descricao_funcao TEXT,
    data_inicio VARCHAR(255),
    data_fim VARCHAR(255),
    destinos TEXT,
    motivo TEXT,
    valor_diarias VARCHAR(255),
    valor_passagens VARCHAR(255),
    valor_devolucao VARCHAR(255),
    valor_outros_gastos VARCHAR(255)
);

-- Tabela: raw_pagamento
-- Origem: 2025_Pagamento.csv

CREATE TABLE raw_pagamento (
    id_viagem VARCHAR(255),
    num_proposta VARCHAR(255),
    cod_orgao_superior VARCHAR(255),
    nome_orgao_superior VARCHAR(500),
    cod_orgao_pagador VARCHAR(255),
    nome_orgao_pagador VARCHAR(500),
    cod_ug_pagadora VARCHAR(255),
    nome_ug_pagadora VARCHAR(500),
    tipo_pagamento VARCHAR(255),
    valor VARCHAR(255)
);

-- Tabela: raw_passagem
-- Origem: 2025_Passagem.csv

CREATE TABLE raw_passagem (
    id_viagem VARCHAR(255),
    num_proposta VARCHAR(255),
    meio_transporte VARCHAR(255),
    pais_origem_ida VARCHAR(255),
    uf_origem_ida VARCHAR(255),
    cidade_origem_ida VARCHAR(500),
    pais_destino_ida VARCHAR(255),
    uf_destino_ida VARCHAR(255),
    cidade_destino_ida VARCHAR(500),
    pais_origem_volta VARCHAR(255),
    uf_origem_volta VARCHAR(255),
    cidade_origem_volta VARCHAR(500),
    pais_destino_volta VARCHAR(255),
    uf_destino_volta VARCHAR(255),
    cidade_destino_volta VARCHAR(500),
    valor_passagem VARCHAR(255),
    taxa_servico VARCHAR(255),
    data_emissao VARCHAR(255),
    hora_emissao VARCHAR(255)
);

-- Tabela: raw_trecho
-- Origem: 2025_Trecho.csv

CREATE TABLE raw_trecho (
    id_viagem VARCHAR(255),
    num_proposta VARCHAR(255),
    sequencia_trecho VARCHAR(255),
    origem_data VARCHAR(255),
    origem_pais VARCHAR(255),
    origem_uf VARCHAR(255),
    origem_cidade VARCHAR(500),
    destino_data VARCHAR(255),
    destino_pais VARCHAR(255),
    destino_uf VARCHAR(255),
    destino_cidade VARCHAR(500),
    meio_transporte VARCHAR(255),
    numero_diarias VARCHAR(255),
    missao VARCHAR(255)
);