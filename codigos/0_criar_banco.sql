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
    justificativa_urgencia VARCHAR(1000),
    cod_orgao_superior VARCHAR(255),
    nome_orgao_superior VARCHAR(500),
    cod_orgao_solicitante VARCHAR(255),
    nome_orgao_solicitante VARCHAR(500),
    cpf_viajante VARCHAR(255),
    nome_viajante VARCHAR(500),
    cargo VARCHAR(500),
    funcao VARCHAR(500),
    descricao_funcao VARCHAR(1000),
    data_inicio VARCHAR(255),
    data_fim VARCHAR(255),
    destinos VARCHAR(1000),
    motivo VARCHAR(1000),
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

-- CAMADA SILVER
-- Dados limpos, tipados e relacionados.

-- Tabela: silver_viagem
-- Origem: raw_viagem

CREATE TABLE silver_viagem (
    id_viagem VARCHAR(20) PRIMARY KEY,
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias DECIMAL(10,2),
    valor_passagens DECIMAL(10,2),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    duracao_dias INT,

    CONSTRAINT chk_viagem_valor_diarias
        CHECK (valor_diarias >= 0)
);


-- Tabela: silver_pagamento
-- Origem: raw_pagamento

CREATE TABLE silver_pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2),

    CONSTRAINT fk_pagamento_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem (id_viagem),

    CONSTRAINT chk_pagamento_valor
        CHECK (valor >= 0)
);


-- Tabela: silver_passagem
-- Origem: raw_passagem

CREATE TABLE silver_passagem (
    id_passagem INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    meio_transporte VARCHAR(50),
    pais_origem_ida VARCHAR(60),
    uf_origem_ida VARCHAR(40),
    cidade_origem_ida VARCHAR(80),
    pais_destino_ida VARCHAR(60),
    uf_destino_ida VARCHAR(40),
    cidade_destino_ida VARCHAR(80),
    valor_passagem DECIMAL(10,2),
    taxa_servico DECIMAL(10,2),
    data_emissao DATE,

    CONSTRAINT fk_passagem_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem (id_viagem),

    CONSTRAINT chk_passagem_valor
        CHECK (valor_passagem >= 0),

    CONSTRAINT chk_passagem_taxa
        CHECK (taxa_servico >= 0)
);

-- Tabela: silver_trecho
-- Origem: raw_trecho

CREATE TABLE silver_trecho (
    id_trecho INT AUTO_INCREMENT PRIMARY KEY,
    id_viagem VARCHAR(20) NOT NULL,
    sequencia_trecho INT,
    origem_data DATE,
    origem_uf VARCHAR(40),
    origem_cidade VARCHAR(80),
    destino_data DATE,
    destino_uf VARCHAR(40),
    destino_cidade VARCHAR(80),
    meio_transporte VARCHAR(50),
    numero_diarias DECIMAL(10,2),

    CONSTRAINT fk_trecho_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem (id_viagem),

    CONSTRAINT chk_trecho_numero_diarias
        CHECK (numero_diarias >= 0),

    CONSTRAINT uq_trecho_viagem_sequencia
        UNIQUE (id_viagem, sequencia_trecho)
);