-- INTEGRANTES EM COMENTARIO--

-- CREATE TABLE integrantes (
-- nome VARCHAR(50),
-- rm CHAR(6)
--);
-- INSERT INTO integrantes VALUES ('Giovanna Revito Roz','558981');
-- INSERT INTO integrantes VALUES ('Kaian Gustavo','558986');
-- INSERT INTO integrantes VALUES ('Lucas Kenji Kikushi','554424');

drop table usuario cascade constraints; 
drop table veiculo cascade constraints; 
drop table orcamento cascade constraints;
drop table servico cascade constraints;
drop table peca cascade constraints;
drop table centro_automotivo cascade constraints;
drop table funcionario cascade constraints;
drop table cargo cascade constraints;
drop table diagnostico cascade constraints;
drop table agendamento cascade constraints;
drop table oferece cascade constraints;
drop table fornece cascade constraints;

CREATE TABLE usuario
(
    cpf_usuario CHAR(11) CONSTRAINT usuario_cpf_pk PRIMARY KEY,
    nome_usuario VARCHAR(80) CONSTRAINT usuario_nm_nn NOT NULL
                          CONSTRAINT usuario_nm_unique UNIQUE,
    email VARCHAR(255) CONSTRAINT usuario_mail_nn NOT NULL,
    telefone CHAR(11) CONSTRAINT usuario_tel_nn NOT NULL,
    senha VARCHAR(30) CONSTRAINT usuario_sen_nn NOT NULL,
    CONSTRAINT chk_senha_usuario CHECK (LENGTH(senha) > 6)
);

CREATE TABLE veiculo
(
    placa CHAR(7) CONSTRAINT veic_pl_pk PRIMARY KEY,
    marca VARCHAR(50) CONSTRAINT veic_mrc_nn NOT NULL,
    modelo VARCHAR(50) CONSTRAINT veic_mdl_nn NOT NULL,
    ano NUMBER(4) CONSTRAINT veic_ano_nn NOT NULL, 
    quilometragem NUMBER(10,2) CONSTRAINT veic_quil_nn NOT NULL, 
    CONSTRAINT chk_quil_veiculo CHECK (quilometragem > 0),
    usuario_cpf_usuario CHAR(11) CONSTRAINT veic_cpf_fk REFERENCES usuario(cpf_usuario) ON DELETE CASCADE    
);
 
CREATE TABLE orcamento 
(
    id_orcamento CHAR(36) CONSTRAINT orc_id_pk PRIMARY KEY,
    descricao_orcamento VARCHAR(255) CONSTRAINT orc_desc_nn NOT NULL,
    valor_total NUMBER(9,2) CONSTRAINT orc_vt_nn NOT NULL,
    status_orcamento VARCHAR(50) CONSTRAINT orc_stts_nn NOT NULL,
    CONSTRAINT chk_status_orcamento CHECK (status_orcamento IN ('PENDENTE', 'APROVADO', 'REJEITADO'))
);
CREATE TABLE servico
(
    id_servico CHAR(6) CONSTRAINT serv_id_pk PRIMARY KEY,
    tipo_servico VARCHAR(50) CONSTRAINT serv_tp_nn NOT NULL,
    descricao_servico VARCHAR(255) CONSTRAINT serv_desc_nn NOT NULL, 
    preco_servico NUMBER(9,2) CONSTRAINT serv_prec_nn NOT NULL,
    duracao NUMBER(4) CONSTRAINT serv_dur_nn NOT NULL
);
CREATE TABLE peca
(
    id_peca CHAR(6) CONSTRAINT peca_id_pk PRIMARY KEY,  
    disponibilidade_peca NUMBER(8) CONSTRAINT peca_disp_nn NOT NULL, CONSTRAINT chk_disponibilidade_peca CHECK (disponibilidade_peca > 0),
    nome_peca VARCHAR(255) CONSTRAINT peca_nm_nn NOT NULL
                          CONSTRAINT peca_nm_unique UNIQUE,
    preco_peca NUMBER(9,2) CONSTRAINT peca_pc_nn NOT NULL,
    CONSTRAINT chk_preco_peca CHECK (preco_peca > 0)
);

CREATE TABLE centro_automotivo
(
    id_centro CHAR(4) CONSTRAINT centro_id_pk PRIMARY KEY,  
    nome_centro VARCHAR(155) CONSTRAINT centro_nm_nn NOT NULL,
    endereco_centro VARCHAR(255) CONSTRAINT centro_end_nn NOT NULL, 
    CONSTRAINT chk_end_centro CHECK (LENGTH(endereco_centro) > 5),
    telefone_centro CHAR(11) CONSTRAINT centro_tel_nn NOT NULL,
    horario_funcionamento VARCHAR(70) CONSTRAINT centro_hr_func_nn NOT NULL 
);

CREATE TABLE cargo
(
    id_cargo CHAR(4) CONSTRAINT cargo_id_pk PRIMARY KEY,
    nome_cargo VARCHAR(50) CONSTRAINT cargo_nm_nn NOT NULL,
    area_cargo VARCHAR(50) CONSTRAINT cargo_area_nn NOT NULL,
    descricao_cargo VARCHAR(255) CONSTRAINT cargo_desc_nn NOT NULL,
    salario_cargo NUMBER(9,2) CONSTRAINT cargo_sal_nn NOT NULL
                      CONSTRAINT cargo_sal_unique UNIQUE,
    CONSTRAINT chk_salario_cargo CHECK (salario_cargo > 0)
);

CREATE TABLE diagnostico 
(
    id_diagnostico CHAR(36) CONSTRAINT diag_id_pk PRIMARY KEY,
    descricao_sintomas VARCHAR(255) CONSTRAINT diag_desc_nn NOT NULL,
    categoria_problema VARCHAR(50) CONSTRAINT diag_cat_nn NOT NULL,
    solucao VARCHAR(255) CONSTRAINT diag_sol_nn NOT NULL,
    status_diagnostico VARCHAR(50) CONSTRAINT diag_stt_nn NOT NULL,
    CONSTRAINT chk_status_diagnostico CHECK (status_diagnostico IN ('EM AN�LISE', 'ANALISADO')),
    veiculo_placa CHAR(7) CONSTRAINT diag_veiculo_fk REFERENCES veiculo(placa) ON DELETE CASCADE,
    orcamento_id_orcamento CHAR(36) CONSTRAINT diag_orcamento_fk REFERENCES orcamento(id_orcamento) ON DELETE CASCADE, 
    servico_id_servico CHAR(6) CONSTRAINT diag_servico_fk REFERENCES servico(id_servico) ON DELETE CASCADE
);

CREATE TABLE agendamento
(
    id_agendamento CHAR(36) CONSTRAINT agend_id_pk PRIMARY KEY,
    data_agendamento DATE CONSTRAINT agend_dt_nn NOT NULL,
    horario_agendamento CHAR(5) CONSTRAINT agend_hr_nn NOT NULL,
    descricao_agendamento VARCHAR(255) CONSTRAINT agend_desc_nn NOT NULL,
    servico_id_servico CHAR(6) CONSTRAINT agend_id_serv_fk REFERENCES servico(id_servico) ON DELETE CASCADE,
    centro_automotivo_id_centro CHAR(4) CONSTRAINT agend_id_centro_fk REFERENCES centro_automotivo(id_centro) ON DELETE CASCADE,  
    veiculo_placa CHAR(7) CONSTRAINT agend_veiculo_fk REFERENCES veiculo(placa) ON DELETE CASCADE
);

CREATE TABLE funcionario(
    matricula_func CHAR(6) CONSTRAINT func_matric_pk PRIMARY KEY,
    nome_func VARCHAR(70) CONSTRAINT func_nome_nn NOT NULL,
    horario_trabalho VARCHAR(70) CONSTRAINT func_horario_nn NOT NULL,
    disponibilidade_func CHAR(1) CONSTRAINT func_disp_nn NOT NULL CHECK (disponibilidade_func IN ('S', 'N')),
    centro_automotivo_id_centro CHAR(4) CONSTRAINT func_id_centro_fk REFERENCES centro_automotivo(id_centro) ON DELETE SET NULL, 
    cargo_id_cargo CHAR(4) CONSTRAINT func_id_cargo_fk REFERENCES cargo(id_cargo) ON DELETE SET NULL
);
 
CREATE TABLE oferece 
(
    servico_id_servico CHAR(6),
    centro_automotivo_id_centro CHAR(4),
    CONSTRAINT oferece_pk PRIMARY KEY (servico_id_servico, centro_automotivo_id_centro),
    CONSTRAINT oferece_servico_fk FOREIGN KEY (servico_id_servico) REFERENCES servico(id_servico) ON DELETE CASCADE,
    CONSTRAINT oferece_id_centro_fk FOREIGN KEY (centro_automotivo_id_centro) REFERENCES centro_automotivo(id_centro) ON DELETE CASCADE 
);
 
CREATE TABLE fornece
(
    peca_id_peca CHAR(6),
    servico_id_servico CHAR(6),
    CONSTRAINT fornece_pk PRIMARY KEY (peca_id_peca, servico_id_servico),
    CONSTRAINT fornece_peca_fk FOREIGN KEY (peca_id_peca) REFERENCES peca(id_peca) ON DELETE CASCADE, 
    CONSTRAINT fornece_servico_fk FOREIGN KEY (servico_id_servico) REFERENCES servico(id_servico) ON DELETE CASCADE
);

-- SCRIPT DML - CRIA��O DA ESTRUTURA E DADOS PARA POPULAR AS TABELAS PARA OS TESTES DA APLICA��O --

-- tabela usuario
INSERT INTO usuario VALUES ('12345678901', 'Jo�o Silva', 'joao.silva@gmail.com', '11987654321', 'senha1234');
INSERT INTO usuario VALUES ('23456789012', 'Maria Oliveira', 'mariaoliveira@yahoo.com.br', '11987654322', 'senha1234');
INSERT INTO usuario VALUES ('34567890123', 'Pedro Santos', 'pedro_santos@gmail.com', '11987654323', 'senha1234');
INSERT INTO usuario VALUES ('45678901234', 'Ana Costa', 'anacosta2114@hotmail.com', '11987654324', 'senha1234');
INSERT INTO usuario VALUES ('56789012345', 'Lucas Pereira', 'lucas.pereira@outlook.com', '11987654325', 'senha1234');
INSERT INTO usuario VALUES ('67890123456', 'Fernanda Lima', 'fernandalima@outlook.com', '11987654326', 'senha1234');
INSERT INTO usuario  VALUES ('78901234567', 'Rafael Almeida', 'rafaelalmeida@hotmail.com', '11987654327', 'senha1234');
INSERT INTO usuario VALUES ('89012345678', 'Cl�udia Mendes', 'claudiamendes@gmail.com', '11987654328', 'senha1234');
INSERT INTO usuario VALUES ('90123456789', 'Ricardo Rocha', 'ricardorocha@gmail.com', '11987654329', 'senha1234');
INSERT INTO usuario  VALUES ('01234567890', 'Juliana Martins', 'julianamartins@gmail.com', '11987654330', 'senha1234');

-- tabela veiculo
INSERT INTO veiculo VALUES ('ABC1D34', 'Fiat', 'Palio', 2017, 50000, '12345678901');
INSERT INTO veiculo VALUES ('DEF5F78', 'Volkswagen', 'Gol', 2018, 30000, '23456789012');
INSERT INTO veiculo VALUES ('GHI9B12', 'Ford', 'Fiesta', 2019, 20000, '34567890123');
INSERT INTO veiculo VALUES ('JKL3J56', 'Chevrolet', 'Onix', 2020, 15000, '45678901234');
INSERT INTO veiculo VALUES ('MNO7L90', 'Toyota', 'Corolla', 2021, 10000, '56789012345');
INSERT INTO veiculo VALUES ('PQR1E34', 'Honda', 'Civic', 2022, 5000, '67890123456');
INSERT INTO veiculo VALUES ('STU5M78', 'Hyundai', 'HB20', 2020, 25000, '78901234567');
INSERT INTO veiculo  VALUES ('VWX9W12', 'Peugeot', '208', 2021, 7000, '89012345678');
INSERT INTO veiculo  VALUES ('YZA3Z56', 'Renault', 'Sandero', 2022, 4000, '90123456789');
INSERT INTO veiculo  VALUES ('BCD7L90', 'Nissan', 'Kicks', 2023, 1000, '01234567890');

-- tabela servico
INSERT INTO servico VALUES ('S00001', 'Troca de Bateria', 'Verificar e substituir a bateria se necess�rio, verificar o sistema de carregamento.', 150.00, 120);
INSERT INTO servico VALUES('S00002', 'Substitui��o do Filtro de Ar', 'Substituir o filtro de ar para melhorar o desempenho do motor e a efici�ncia do combust�vel.', 80.00, 60);
INSERT INTO servico VALUES('S00003', 'Troca das Velas de Igni��o', 'Substituir as velas de igni��o e verificar o sistema de igni��o para garantir uma partida eficiente do motor.', 100.00, 120);
INSERT INTO servico VALUES('S00004', 'Calibra��o e Alinhamento de Pneus', 'Calibrar os pneus e verificar o alinhamento.', 120.00, 120);
INSERT INTO servico VALUES('S00005', 'Substitui��o do Alternador', 'Testar e substituir o alternador se necess�rio para garantir o funcionamento correto dos sistemas el�tricos.', 250.00, 240);
INSERT INTO servico VALUES('S00006', 'Troca de �leo', 'Verificar e completar o n�vel de �leo ou realizar troca completa do �leo do motor.', 90.00, 60);
INSERT INTO servico VALUES('S00007', 'Reparo do Radiador', 'Reparar ou substituir o radiador e completar o fluido de arrefecimento para evitar o superaquecimento do motor.', 300.00, 180);
INSERT INTO servico VALUES('S00008', 'Substitui��o da Correia Dentada', 'Substituir a correia dentada e verificar o tensionamento para evitar problemas no motor.', 250.00, 180);
INSERT INTO servico VALUES('S00009', 'Reparo da Transmiss�o', 'Verificar e reparar a transmiss�o, trocar o fluido de transmiss�o para garantir uma troca de marchas suave.', 350.00, 240);
INSERT INTO servico VALUES('S00010', 'Substitui��o da Bomba de Combust�vel', 'Testar e substituir a bomba de combust�vel para garantir que o motor receba o combust�vel adequado.', 200.00, 120);
INSERT INTO servico VALUES('S00011', 'Substitui��o dos Discos de Freio', 'Substituir os discos de freio e as pastilhas se necess�rio para garantir a efici�ncia dos freios.', 250.00, 180);
INSERT INTO servico VALUES('S00012', 'Reparo da Suspens�o', 'Verificar e substituir os componentes da suspens�o para garantir uma condu��o est�vel e segura.', 300.00, 180);
INSERT INTO servico VALUES('S00013', 'Substitui��o da Bomba de �gua', 'Substituir a bomba de �gua e verificar o sistema de arrefecimento para evitar o superaquecimento do motor.', 200.00, 120);
INSERT INTO servico VALUES('S00014', 'Substitui��o do Sensor de Oxig�nio', 'Substituir o sensor de oxig�nio para manter o desempenho do motor e reduzir as emiss�es.', 130.00, 90);
INSERT INTO servico VALUES('S00015', 'Reparo do Sistema de Escapamento', 'Verificar e reparar o sistema de escapamento para garantir a elimina��o adequada dos gases do motor.', 200.00, 120);
INSERT INTO servico VALUES ('S00016', 'Substitui��o da Embreagem', 'Substituir o conjunto da embreagem para garantir o funcionamento adequado das marchas.', 400.00, 240);
INSERT INTO servico VALUES ('S00017', 'Substitui��o dos Amortecedores', 'Substituir os amortecedores para melhorar a estabilidade e o conforto da condu��o.', 350.00, 180);
INSERT INTO servico VALUES('S00018', 'Reparo da Bomba de Dire��o', 'Verificar e reparar a bomba de dire��o hidr�ulica, completar fluido para garantir a dire��o suave.', 150.00, 90);
INSERT INTO servico VALUES('S00019', 'Substitui��o do Sensor de Temperatura', 'Substituir o sensor de temperatura para evitar problemas de superaquecimento e garantir o funcionamento correto do motor.', 120.00, 90);
INSERT INTO servico VALUES('S00020', 'Reparo de Vazamento de �leo', 'Identificar e reparar o vazamento de �leo, completar o n�vel de �leo para evitar danos ao motor.', 180.00, 120);
INSERT INTO servico VALUES('S00021', 'Substitui��o do Filtro de Combust�vel', 'Verificar e substituir o filtro de combust�vel para garantir o fluxo de combust�vel adequado para o motor.', 100.00, 90);
INSERT INTO servico VALUES('S00022', 'Substitui��o do Sensor de Press�o dos Pneus', 'Verificar e substituir o sensor de press�o dos pneus para garantir leituras precisas e evitar problemas com os pneus.', 120.00, 90);
INSERT INTO servico VALUES('S00023', 'Substitui��o da Bobina de Igni��o', 'Substituir a bobina de igni��o para garantir uma igni��o eficiente e melhorar o desempenho do motor.', 140.00, 90);
INSERT INTO servico VALUES('S00024', 'Reparo do M�dulo ABS', 'Reparar ou substituir o m�dulo ABS para garantir a funcionalidade adequada do sistema de frenagem.', 350.00, 180);
INSERT INTO servico VALUES('S00025', 'Substitui��o do Termostato', 'Substituir o termostato para garantir a regula��o correta da temperatura do motor e evitar superaquecimento.', 130.00, 90);
INSERT INTO servico VALUES ('S00026', 'Substitui��o da Bomba de V�cuo', 'Substituir a bomba de v�cuo para garantir a assist�ncia adequada aos freios e evitar problemas na frenagem.', 180.00, 90);
INSERT INTO servico VALUES ('S00027', 'Reparo do Sistema de Exaust�o', 'Reparar o vazamento no sistema de exaust�o para garantir a elimina��o adequada dos gases e reduzir o ru�do.', 200.00, 120);
INSERT INTO servico VALUES ('S00028', 'Limpeza ou Substitui��o da V�lvula EGR', 'Limpar ou substituir a v�lvula EGR para melhorar a efici�ncia do motor e reduzir as emiss�es.', 150.00, 90);
INSERT INTO servico VALUES('S00029', 'Reparo do Sistema de Arrefecimento', 'Verificar e reparar o sistema de arrefecimento, substituir componentes defeituosos para evitar o superaquecimento do motor.', 300.00, 180);
INSERT INTO servico VALUES('S00030', 'Reparo do Sistema de Ar Condicionado', 'Verificar e reparar o sistema de ar condicionado, incluindo checagem de vazamentos, substitui��o de filtros, e manuten��o dos componentes do sistema.', 250.00, 180);
INSERT INTO servico VALUES('S00031', 'Ajuste da Geometria/Alinhamento', 'Verificar e ajustar o alinhamento e a geometria das rodas para garantir uma dire��o est�vel e uniforme. Se necess�rio, substituir componentes desgastados.', 170.00, 120);
INSERT INTO servico VALUES ('S00032', 'Manuten��o Completa do Motor', 'Inclui troca de �leo, verifica��o do sistema de inje��o, substitui��o da correia dentada, limpeza do sistema de arrefecimento e ajuste das v�lvulas. Ideal para garantir a performance e a durabilidade do motor.', 950.00, 360);

-- tabela centro_automotivo
INSERT INTO centro_automotivo VALUES ('C001', 'Auto Center ABC', 'Rua das Flores, 123', '11987654321', '08:00 - 18:00');
INSERT INTO centro_automotivo VALUES ('C002', 'Oficina XYZ', 'Av. Paulista, 1000', '11987654322', '09:00 - 19:00');
INSERT INTO centro_automotivo VALUES ('C003', 'Mec�nica R�pida', 'Rua do Carmo, 456', '11987654323', '08:30 - 18:30');
INSERT INTO centro_automotivo VALUES ('C004', 'Centro Automotivo Alfa', 'Rua Jo�o Paulo, 789', '11987654324', '08:00 - 17:30');
INSERT INTO centro_automotivo VALUES ('C005', 'Oficina Porto', 'Av. Santos Dumont, 555', '11987654325', '08:00 - 18:00');
INSERT INTO centro_automotivo VALUES ('C006', 'Auto Mec�nica Sul', 'Rua Vit�ria, 321', '11987654326', '09:00 - 18:30');
INSERT INTO centro_automotivo VALUES ('C007', 'Mec�nica Avenida', 'Av. Brasil, 200', '11987654327', '08:30 - 17:30');
INSERT INTO centro_automotivo VALUES ('C008', 'Oficina Central', 'Pra�a da S�, 10', '11987654328', '07:30 - 18:00');
INSERT INTO centro_automotivo VALUES ('C009', 'Repara��o Veicular Omega', 'Rua Marechal, 999', '11987654329', '08:00 - 17:00');
INSERT INTO centro_automotivo VALUES ('C010', 'Centro Automotivo Delta', 'Av. Get�lio Vargas, 400', '11987654330', '08:00 - 18:00');

-- Inser��es na tabela cargo
INSERT INTO cargo VALUES ('CG01', 'Mec�nico', 'Oficina', 'Respons�vel pela manuten��o de ve�culos', 3000.00);
INSERT INTO cargo VALUES ('CG02', 'Gerente', 'Administra��o', 'Gerencia o centro automotivo', 5000.00);
INSERT INTO cargo VALUES ('CG03', 'Atendente', 'Recep��o', 'Atendimento ao cliente no balc�o', 1800.00);
INSERT INTO cargo VALUES ('CG04', 'Supervisor', 'Oficina', 'Supervisiona as atividades da oficina', 4000.00);
INSERT INTO cargo VALUES ('CG05', 'Eletricista', 'Oficina', 'Respons�vel pela manuten��o el�trica dos ve�culos', 3200.00);
INSERT INTO cargo VALUES ('CG06', 'Auxiliar de Mec�nico', 'Oficina', 'Auxilia os mec�nicos na manuten��o de ve�culos', 2200.00);
INSERT INTO cargo VALUES ('CG07', 'Vendedor de Pe�as', 'Comercial', 'Respons�vel pela venda de pe�as e acess�rios', 2500.00);
INSERT INTO cargo VALUES ('CG08', 'Assistente Administrativo', 'Administra��o', 'Auxilia nas tarefas administrativas do centro automotivo', 2700.00);
INSERT INTO cargo VALUES ('CG09', 'Consultor T�cnico', 'Oficina', 'Realiza consultoria t�cnica sobre reparos automotivos', 3800.00);
INSERT INTO cargo VALUES ('CG10', 'Lavador de Ve�culos', 'Servi�os Gerais', 'Respons�vel pela lavagem e limpeza dos ve�culos', 1500.00);

-- tabela peca
INSERT INTO peca VALUES ('P00001', 10, 'Filtro de �leo', 25.00);
INSERT INTO peca VALUES ('P00002', 15, 'Filtro de ar', 30.00);
INSERT INTO peca VALUES ('P00003', 20, 'Correia dentada', 120.00);
INSERT INTO peca VALUES ('P00004', 5, 'Bateria', 400.00);
INSERT INTO peca VALUES ('P00005', 8, 'Pastilha de freio', 150.00);
INSERT INTO peca VALUES ('P00006', 12, 'Pneu', 300.00);
INSERT INTO peca VALUES ('P00007', 7, 'Amortecedor', 250.00);
INSERT INTO peca VALUES ('P00008', 18, 'Velas de igni��o', 40.00);
INSERT INTO peca VALUES ('P00009', 6, 'Bico injetor', 450.00);
INSERT INTO peca VALUES ('P00010', 10, 'Correia poly-v', 85.00);
INSERT INTO peca VALUES ('P00011', 14, 'Filtro de combust�vel', 35.00);
INSERT INTO peca VALUES ('P00012', 9, 'Disco de freio', 220.00);
INSERT INTO peca VALUES ('P00013', 6, 'Radiador', 500.00);
INSERT INTO peca VALUES ('P00014', 11, 'Bomba de combust�vel', 350.00);
INSERT INTO peca VALUES ('P00015', 8, 'Alternador', 650.00);
INSERT INTO peca VALUES ('P00016', 7, 'Motor de partida', 700.00);
INSERT INTO peca VALUES ('P00017', 13, 'Cabo de vela', 60.00);
INSERT INTO peca VALUES ('P00018', 10, 'Kit de embreagem', 950.00);
INSERT INTO peca VALUES ('P00019', 5, 'Sensor de oxig�nio', 180.00);
INSERT INTO peca VALUES ('P00020', 4, 'Sensor de temperatura', 90.00);

-- tabela funcionario
INSERT INTO funcionario VALUES ('M85234', 'Carlos Almeida', '08:00 - 17:00', 'S', 'C001', 'CG01');
INSERT INTO funcionario VALUES ('M65412', 'Fernanda Sousa', '09:00 - 18:00', 'S', 'C002', 'CG03');
INSERT INTO funcionario VALUES ('M33583', 'Jo�o Pereira', '08:30 - 17:30', 'S', 'C003', 'CG02');
INSERT INTO funcionario VALUES ('M22242', 'Ana Costa', '08:00 - 16:00', 'N', 'C001', 'CG04');
INSERT INTO funcionario VALUES ('M00005', 'Luiz Melo', '10:00 - 19:00', 'S', 'C004', 'CG01');
INSERT INTO funcionario VALUES ('M00006', 'Pedro Silva', '07:30 - 16:30', 'N', 'C002', 'CG02');
INSERT INTO funcionario VALUES ('M00007', 'Mariana Rocha', '08:00 - 17:00', 'S', 'C003', 'CG03');
INSERT INTO funcionario VALUES ('M00008', 'Lucas Moreira', '08:30 - 17:30', 'S', 'C004', 'CG04');
INSERT INTO funcionario VALUES ('M00009', 'Beatriz Lima', '09:00 - 18:00', 'S', 'C001', 'CG01');
INSERT INTO funcionario VALUES ('M00010', 'Rafael Oliveira', '07:00 - 16:00', 'S', 'C002', 'CG02');

-- tabela orcamento
INSERT INTO orcamento VALUES ('dff9082b-b150-405c-be5b-508016668287', 'Conserto dos amortecedores', 350.00, 'PENDENTE'); --ok
INSERT INTO orcamento VALUES ('63f67511-2dac-4b90-b1f0-8eeb47025da7', 'Alinhamento e balanceamento', 170.00, 'APROVADO'); --ok
INSERT INTO orcamento VALUES ('4cd95553-a5f3-40ac-acd9-843f0b86da15', 'Calibramento dos pneus', 120.0, 'REJEITADO'); --ok
INSERT INTO orcamento VALUES ('7929d0ec-c875-4062-bd01-9ab4676d88fa', 'Troca de pastilhas de freio', 250.00, 'PENDENTE'); --ok
INSERT INTO orcamento VALUES ('2b4d29f6-cba0-4699-ac2c-8a3f7ab2f062', 'Conserto do sistema de ar-condicionado', 250.00, 'APROVADO'); --ok
INSERT INTO orcamento VALUES ('e900daec-6a71-48d8-ae09-3f578e55c734', 'Troca da correia dentada', 250.00, 'PENDENTE'); --ok
INSERT INTO orcamento VALUES ('39f0f5db-687f-4190-a0e5-8faa25c40b4f', 'Repara��o do escapemento', 200.00, 'REJEITADO'); --ok
INSERT INTO orcamento VALUES ('9f01c149-fb36-453a-afb5-805ce3935e0b', 'Substitui��o da bomba de combust�vel', 200.00, 'APROVADO'); --ok
INSERT INTO orcamento VALUES ('53312f65-d349-49a6-b500-632c67180ca8', 'Limpeza ou substitui��o do filtro de ar', 80.0, 'PENDENTE'); --ok
INSERT INTO orcamento VALUES ('ada3552b-f72c-4a1a-b28e-3264506882a5', 'Troca do sistema de suspens�o', 300.00, 'APROVADO'); --ok

-- tabela diagnostico
INSERT INTO diagnostico VALUES ('2a7b9758-e057-4901-9e3b-62610dd3480a', 'Ru�dos ao frear', 'Problema no sistema de freios', 'Substituir os discos de freio e as pastilhas se necess�rio para garantir a efici�ncia dos freios.', 'ANALISADO', 'ABC1D34', '7929d0ec-c875-4062-bd01-9ab4676d88fa', 'S00011');
INSERT INTO diagnostico VALUES ('30f8d3d2-c0c7-4add-a21b-c023da029202', 'Carro puxando para o lado', 'Desalinhamento', 'Verificar e ajustar o alinhamento e a geometria das rodas para garantir uma dire��o est�vel e uniforme. Se necess�rio, substituir componentes desgastados.', 'EM AN�LISE', 'DEF5F78', '63f67511-2dac-4b90-b1f0-8eeb47025da7', 'S00031');
INSERT INTO diagnostico VALUES ('76b64318-9713-472e-b134-4b4c71b64dc3', 'Vibra��o ao acelerar', 'Pneus descalibrados', 'Calibrar os pneus e verificar o alinhamento.', 'ANALISADO', 'GHI9B12', '4cd95553-a5f3-40ac-acd9-843f0b86da15', 'S00004');
INSERT INTO diagnostico VALUES ('39dc1dc7-9974-496c-9042-a10ae9052309', 'Ar-condicionado n�o gela', 'Falha no compressor', 'Verificar e reparar o sistema de ar condicionado, incluindo checagem de vazamentos, substitui��o de filtros, e manuten��o dos componentes do sistema.', 'EM AN�LISE', 'JKL3J56', '2b4d29f6-cba0-4699-ac2c-8a3f7ab2f062', 'S00030');
INSERT INTO diagnostico VALUES ('08c76548-b131-4a81-9633-fcbb6a5ec02e', 'Desempenho ruim do motor', 'Filtro de ar sujo', 'Substituir o filtro de ar para melhorar o desempenho do motor e a efici�ncia do combust�vel.', 'ANALISADO', 'MNO7L90', '53312f65-d349-49a6-b500-632c67180ca8', 'S00002');
INSERT INTO diagnostico VALUES ('4569c33f-fb58-4df8-add6-6b438805afdf', 'Ru�do no motor', 'Correia dentada desgastada', 'Substituir a correia dentada e verificar o tensionamento para evitar problemas no motor.', 'EM AN�LISE', 'PQR1E34', 'e900daec-6a71-48d8-ae09-3f578e55c734', 'S00008');
INSERT INTO diagnostico VALUES ('41ca953d-f2dc-45e9-bc3e-1d3658d6151f', 'Carro n�o liga', 'Falha na bomba de combust�vel', 'Testar e substituir a bomba de combust�vel para garantir que o motor receba o combust�vel adequado.', 'ANALISADO', 'STU5M78', '9f01c149-fb36-453a-afb5-805ce3935e0b', 'S00010');
INSERT INTO diagnostico VALUES ('1e365374-0461-4fd2-bbf6-9b463fbb736f', 'Fuma�a no escapamento', 'Mistura rica de combust�vel', 'Verificar e reparar o sistema de escapamento para garantir a elimina��o adequada dos gases do motor.', 'EM AN�LISE', 'VWX9W12', '39f0f5db-687f-4190-a0e5-8faa25c40b4f', 'S00015');
INSERT INTO diagnostico VALUES ('0040bfc5-ac3e-4733-99b7-18a0c53823cb', 'Suspens�o barulhenta', 'Desgaste nos amortecedores', 'Substituir os amortecedores para melhorar a estabilidade e o conforto da condu��o.', 'ANALISADO', 'YZA3Z56', 'dff9082b-b150-405c-be5b-508016668287', 'S00017');
INSERT INTO diagnostico VALUES ('6f2817ef-349c-4a18-968e-3d6066a03f12', 'Barulho ao passar em lombadas', 'Desgaste nas molas da suspens�o', 'Verificar e substituir os componentes da suspens�o para garantir uma condu��o est�vel e segura.', 'EM AN�LISE', 'BCD7L90', 'ada3552b-f72c-4a1a-b28e-3264506882a5', 'S00012');
 
-- tabela agendamento
INSERT INTO agendamento VALUES ('6ce37502-f32d-444b-ad70-e897c8414b7d', TO_DATE('2024-10-25', 'YYYY-MM-DD'), '09:30', 'Agendamento para troca de pastilhas de freio', 'S00011', 'C001', 'ABC1D34');
INSERT INTO agendamento VALUES ('7f53d587-885d-4e53-bf0c-720b65204de9', TO_DATE('2024-11-03', 'YYYY-MM-DD'), '14:00', 'Agendamento para alinhamento e balanceamento', 'S00031', 'C002', 'DEF5F78');
INSERT INTO agendamento VALUES ('a2547171-b99b-4db0-9ccc-5086a31387ec', TO_DATE('2024-11-10', 'YYYY-MM-DD'), '10:30', 'Agendamento para troca de �leo e filtros', 'S00006', 'C003', 'GHI9B12');
INSERT INTO agendamento VALUES ('80357e49-2b58-4024-a6a3-cff4dd47560e', TO_DATE('2024-11-12', 'YYYY-MM-DD'), '13:00', 'Agendamento para revis�o completa', 'S00032', 'C001', 'JKL3J56');
INSERT INTO agendamento VALUES ('9323305f-3c10-403d-b8bb-63e2b8f198d9', TO_DATE('2024-11-15', 'YYYY-MM-DD'), '11:00', 'Agendamento para conserto do ar-condicionado', 'S00030', 'C002', 'MNO7L90');
INSERT INTO agendamento VALUES ('f1b39845-2174-4f67-9c36-f2fb1f5a4c36', TO_DATE('2024-11-20', 'YYYY-MM-DD'), '09:00', 'Agendamento para troca da correia dentada', 'S00008', 'C003', 'PQR1E34');
INSERT INTO agendamento VALUES ('ac54768b-e87f-4632-b941-8418e337f0f8', TO_DATE('2024-11-25', 'YYYY-MM-DD'), '15:00', 'Agendamento para substitui��o da bomba de combust�vel', 'S00010', 'C001', 'STU5M78');
INSERT INTO agendamento VALUES ('6a0fe502-f876-401d-831a-5acf3fc56dd4', TO_DATE('2024-11-28', 'YYYY-MM-DD'), '12:30', 'Agendamento para substitui��o do filtro de combust�vel', 'S00021', 'C002', 'VWX9W12');
INSERT INTO agendamento VALUES ('a11d715a-adda-4c89-b256-1a651a2ee108', TO_DATE('2024-12-02', 'YYYY-MM-DD'), '16:00', 'Agendamento para troca do sistema de suspens�o', 'S00012', 'C003', 'YZA3Z56');
INSERT INTO agendamento VALUES ('0fc8fad6-1780-465c-900d-cb51dde92b06', TO_DATE('2024-12-05', 'YYYY-MM-DD'), '17:30', 'Agendamento para repara��o el�trica', 'S00005', 'C001', 'BCD7L90');
 
INSERT INTO oferece VALUES ('S00001', 'C001');
INSERT INTO oferece VALUES ('S00002', 'C002');
INSERT INTO oferece VALUES ('S00003', 'C003');
INSERT INTO oferece VALUES ('S00004', 'C004');
INSERT INTO oferece VALUES ('S00005', 'C005');
INSERT INTO oferece VALUES ('S00006', 'C006');
INSERT INTO oferece VALUES ('S00007', 'C007');
INSERT INTO oferece VALUES ('S00008', 'C008');
INSERT INTO oferece VALUES ('S00009', 'C009');
INSERT INTO oferece VALUES ('S00010', 'C001');
INSERT INTO oferece VALUES ('S00011', 'C002');
INSERT INTO oferece VALUES ('S00012', 'C003');
INSERT INTO oferece VALUES ('S00013', 'C004');
INSERT INTO oferece VALUES ('S00014', 'C005');
INSERT INTO oferece VALUES ('S00015', 'C006');
INSERT INTO oferece VALUES ('S00016', 'C007');
INSERT INTO oferece VALUES ('S00017', 'C008');
INSERT INTO oferece VALUES ('S00018', 'C009');
INSERT INTO oferece VALUES ('S00019', 'C001');
INSERT INTO oferece VALUES ('S00020', 'C002');

INSERT INTO fornece VALUES ('P00001', 'S00001');
INSERT INTO fornece VALUES ('P00002', 'S00002');
INSERT INTO fornece VALUES ('P00003', 'S00003');
INSERT INTO fornece VALUES ('P00004', 'S00004');
INSERT INTO fornece VALUES ('P00005', 'S00005');
INSERT INTO fornece VALUES ('P00006', 'S00006');
INSERT INTO fornece VALUES ('P00007', 'S00007');
INSERT INTO fornece VALUES ('P00008', 'S00008');
INSERT INTO fornece VALUES ('P00009', 'S00009');
INSERT INTO fornece VALUES ('P00010', 'S00010');
INSERT INTO fornece VALUES ('P00011', 'S00011');
INSERT INTO fornece VALUES ('P00012', 'S00012');
INSERT INTO fornece VALUES ('P00013', 'S00013');
INSERT INTO fornece VALUES ('P00014', 'S00014');
INSERT INTO fornece VALUES ('P00015', 'S00015');
INSERT INTO fornece VALUES ('P00016', 'S00016');
INSERT INTO fornece VALUES ('P00017', 'S00017');
INSERT INTO fornece VALUES ('P00018', 'S00018');
INSERT INTO fornece VALUES ('P00019', 'S00019');
INSERT INTO fornece VALUES ('P00020', 'S00020');

-- SCRIPT DQL - CONSULTAR AS TABELAS PARA OS TESTES DA APLICA��O --

-- Relat�rio das tabelas --
SELECT * FROM usuario; 
SELECT * FROM veiculo;
SELECT * FROM orcamento;
SELECT * FROM servico;
SELECT * FROM peca;
SELECT * FROM centro_automotivo;
SELECT * FROM funcionario;
SELECT * FROM cargo;
SELECT * FROM diagnostico;
SELECT * FROM agendamento;
SELECT * FROM oferece;
SELECT * FROM fornece;

-- Relat�rio utilizando classifica��o de dados --
SELECT preco_servico FROM servico order by preco_servico;
SELECT duracao FROM servico order by duracao desc;

-- 
SELECT MAX(preco_servico) AS "MAIOR PRE�O" FROM servico;
SELECT SUM(disponibilidade_peca * preco_peca) AS "VALOR TOTAL EM ESTOQUE" FROM peca;

-- Relat�rio utilizando alguma fun��o de grupo
SELECT tipo_servico, AVG(preco_servico) AS "PRE�O M�DIO" FROM servico group by tipo_servico;
SELECT horario_funcionamento, COUNT(*) AS "QUANTIDADE DE SERVI�OS" FROM centro_automotivo group by horario_funcionamento;

--Relat�rio utilizando sub consulta
SELECT d.id_diagnostico, d.descricao_sintomas, d.solucao, s.preco_servico FROM diagnostico d
INNER JOIN servico s ON d.servico_id_servico = s.id_servico
WHERE s.preco_servico > (SELECT AVG(preco_servico) FROM servico);

SELECT f.matricula_func, f.nome_func, ca.nome_centro FROM funcionario f
INNER JOIN centro_automotivo ca ON f.centro_automotivo_id_centro = ca.id_centro
WHERE ca.id_centro IN (SELECT centro_automotivo_id_centro FROM oferece
                       GROUP BY centro_automotivo_id_centro
                       HAVING COUNT(servico_id_servico) > 2);

--Relat�rio utilizando jun��o de tabelas
SELECT v.placa, v.modelo, d.descricao_sintomas, o.valor_total, o.status_orcamento FROM veiculo v 
INNER JOIN diagnostico d ON v.placa = d.veiculo_placa
INNER JOIN orcamento o ON d.orcamento_id_orcamento = o.id_orcamento;

SELECT ca.nome_centro, ca.endereco_centro, s.tipo_servico, s.preco_servico FROM centro_automotivo ca
INNER JOIN oferece o ON ca.id_centro = o.centro_automotivo_id_centro
INNER JOIN servico s ON o.servico_id_servico = s.id_servico;

commit;