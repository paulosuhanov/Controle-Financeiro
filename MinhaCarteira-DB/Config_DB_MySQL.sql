###############################
#####  Criação de Tabelas #####
###############################

USE MinhaCarteira;

CREATE TABLE Usuario(
    IdUsuario VARCHAR ( 20 ) NOT NULL,
    Senha VARCHAR (30),
    DtExpiracao DATE NOT NULL DEFAULT '1900-01-01' ,
    CONSTRAINT PK_Usuario PRIMARY KEY (IdUsuario)
);

CREATE TABLE DadosUsuario (
    Id INT AUTO_INCREMENT NOT NULL,
    IdUsuario VARCHAR ( 20 ) NOT NULL,
    Nome VARCHAR ( 50 ) NOT NULL,
    Sobrenome VARCHAR ( 50 ) NOT NULL,
    DtNascimento DATE NOT NULL DEFAULT '1900-01-01',
    Email VARCHAR ( 50 ) NOT NULL ,
    Celular VARCHAR ( 11 ) NOT NULL,
    Foto VARCHAR (255),
    CONSTRAINT PK_Usuario PRIMARY KEY (Id),
    CONSTRAINT FK_IdUsuario FOREIGN KEY (IdUsuario)
        REFERENCES Usuario (IdUsuario) ,
    CONSTRAINT UQ_Celular UNIQUE ( Celular ),
    CONSTRAINT UQ_Email UNIQUE ( Email ),
    CONSTRAINT UQ_UsuarioId UNIQUE ( IdUsuario )
);

CREATE TABLE Banco (
    IdBanco CHAR ( 4 ) NOT NULL,
    NomeBanco VARCHAR ( 100 ) NOT NULL ,
    CONSTRAINT PK_Banco PRIMARY KEY ( IdBanco ),
    CONSTRAINT UQ_IdBanco UNIQUE (IdBanco)
);

CREATE TABLE Conta (
    IdConta VARCHAR ( 40 ) NOT NULL , # a soma do CodBanco + CodAgencia + Conta
    NomeConta VARCHAR ( 30 ) NOT NULL ,
    IdUsuario VARCHAR ( 20 ) NOT NULL ,
    IdBanco CHAR ( 4 ) NOT NULL ,
    CodAgencia CHAR ( 5 ) NOT NULL ,
    CodConta CHAR ( 11 ) NOT NULL ,
    Gerente VARCHAR ( 50 ) ,
    TelGerente VARCHAR ( 11 ) ,
    EmailGerente VARCHAR ( 50 ),
    CONSTRAINT PK_Conta PRIMARY KEY (IdConta),
    CONSTRAINT FK_IdUsuario_Conta FOREIGN KEY ( IdUsuario )
        REFERENCES Usuario (IdUsuario),
    CONSTRAINT FK_Banco FOREIGN KEY ( IdBanco )
        REFERENCES Banco ( IdBanco ),
    CONSTRAINT UQ_Conta UNIQUE ( IdUsuario , IdBanco , CodAgencia , CodConta )
);

CREATE TABLE Categoria (
    IdCategoria INT NOT NULL AUTO_INCREMENT,
    NomeCategoria VARCHAR ( 30 ),
    TipoCategoria VARCHAR ( 10 ),
    CONSTRAINT PK_Categoria PRIMARY KEY ( IdCategoria ),
    CONSTRAINT CK_TipoCategoria CHECK
        ( TipoCategoria='Debito' or
          TipoCategoria='Receita' )
);

Create Table Recorrente (
    IdRecorrente INT NOT NULL AUTO_INCREMENT,
    NomeRecorrente VARCHAR ( 30 ) NOT NULL,
    CONSTRAINT PK_Recorrencia PRIMARY KEY ( IdRecorrente )
);

CREATE TABLE Receita (
    ID INT NOT NULL AUTO_INCREMENT,
    IdUsuario VARCHAR ( 20 ) ,
    Data DATE NOT NULL DEFAULT '1900-01-01',
    Valor DECIMAL ( 10,2 ) NOT NULL,
    IdConta VARCHAR ( 40 ),
    IdCategoria INT NOT NULL ,
    IdRecorrente INT DEFAULT 0 NOT NULL,
    Efetuado INT DEFAULT 0 NOT NULL,
    Descricao LONGTEXT,
    CONSTRAINT PK_Receita PRIMARY KEY ( ID ),
    CONSTRAINT FK_IdUsuarioReceita FOREIGN KEY ( IdUsuario )
        REFERENCES Usuario( IdUsuario ),
    CONSTRAINT FK_IdContaRec FOREIGN KEY (IdConta)
        REFERENCES  Conta (IdConta),
    CONSTRAINT FK_IdCatReceita FOREIGN KEY ( IdCategoria )
        REFERENCES Categoria ( IdCategoria ),
    CONSTRAINT FK_IdRecReceita FOREIGN KEY ( IdRecorrente )
        REFERENCES Recorrente ( IdRecorrente )
);

CREATE TABLE Debito (
    ID INT NOT NULL AUTO_INCREMENT,
    IdUsuario VARCHAR ( 20 ) ,
    Data DATE NOT NULL DEFAULT '1900-01-01',
    Valor DECIMAL ( 10,2 ) NOT NULL,
    IdConta VARCHAR ( 40 ) ,
    IdCategoria INT NOT NULL ,
    IdRecorrente INT DEFAULT 0,
    Efetuado INT DEFAULT 0,
    Descricao LONGTEXT,
    CONSTRAINT PK_Debito PRIMARY KEY ( ID ),
    CONSTRAINT FK_IdUsuarioDebito FOREIGN KEY ( IdUsuario )
        REFERENCES Usuario ( IdUsuario ),
    CONSTRAINT FK_IdContaDeb FOREIGN KEY (IdConta)
        REFERENCES  Conta (IdConta),
    CONSTRAINT FK_IdCatDebito FOREIGN KEY ( IdCategoria)
        REFERENCES Categoria ( IdCategoria ),
    CONSTRAINT FK_IdRecDebito FOREIGN KEY ( IdRecorrente )
        REFERENCES Recorrente ( IdRecorrente )
);

##################################
#####  Criação de Procedures #####
##################################

DELIMITER //
CREATE PROCEDURE sp_criaUsuario
(
    IN v_usuario VARCHAR( 20 ),
    IN v_senha VARCHAR( 30 ))
    BEGIN
        IF ( select exists (select 1 from Usuario where IdUsuario = v_usuario) )
        THEN
            select 'Usuário Existente !!';
        ELSE
            insert into Usuario
                (
                    IdUsuario,
                    Senha
                )
                values
                (
                    v_usuario,
                    v_senha
                );
        END IF;
    END
// DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_DadosUsuarios
(
    IN v_id_usuario VARCHAR( 20 ),
    IN v_nome VARCHAR(50),
    IN v_sobrenome VARCHAR(50),
    IN v_dt_nascimento DATE,
    IN v_email VARCHAR ( 50),
    IN v_celular VARCHAR (11) )
    BEGIN
    IF ( select exists (select 1 from DadosUsuario where IdUsuario = v_id_usuario and Nome != NULL) )
        THEN
            update DadosUsuario
                SET
                    Nome = v_nome,
                    Sobrenome = v_sobrenome,
                    DtNascimento = v_dt_nascimento,
                    Email = v_email,
                    Celular = v_celular
                where
                    IdUsuario = v_id_usuario;
        ELSE
            insert into DadosUsuario
                (
                    IdUsuario,
                    Nome,
                    Sobrenome,
                    DtNascimento,
                    Email,
                    Celular
                )
                values
                (
                    v_id_usuario,
                    v_nome,
                    v_sobrenome,
                    v_dt_nascimento,
                    v_email,
                    v_celular
                );
        END IF;
    END
// DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_criaBanco
(
    IN v_id_banco INT,
    IN v_nome_banco VARCHAR(20))
    BEGIN
        IF ( select exists (select 1 from Banco where IdBanco = v_id_banco) )
        THEN
            select 'Banco Existente.';
        ELSE
            insert into Banco
                (
                    IdBanco,
                    NomeBanco
                )
                values
                (
                    v_id_banco,
                    v_nome_banco
                );
        END IF;
    END
// DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_Conta
(
    IN v_id_usuario VARCHAR( 20 ),
    IN v_cod_banco CHAR ( 4 ),
    IN v_cod_agencia CHAR ( 5 ),
    IN v_cod_conta CHAR ( 11 ),
    IN v_gerente VARCHAR (50),
    IN v_tel_gerente VARCHAR ( 11 ),
    IN v_email_gerente VARCHAR( 50 ))
    BEGIN
    IF ( select exists (select 1 from Conta where IdUsuario = v_id_usuario and CodConta = v_cod_conta ) )
        THEN
            update Conta
                SET
                    IdBanco = v_cod_banco,
                    CodAgencia = v_cod_agencia,
                    CodConta = v_cod_conta,
                    Gerente = v_gerente,
                    TelGerente = v_tel_gerente,
                    EmailGerente = v_email_gerente
                where
                    IdUsuario = v_id_usuario and CodConta = v_cod_conta;
        ELSE
            insert into Conta
                (IdConta,IdUsuario,IdBanco,CodAgencia,CodConta,Gerente,TelGerente,EmailGerente)
                values
                (
                    (v_id_usuario + v_cod_banco + v_cod_agencia + v_cod_conta),
                    v_id_usuario,
                    v_cod_banco,
                    v_cod_agencia,
                    v_cod_conta,
                    v_gerente,
                    v_tel_gerente,
                    v_email_gerente
                );
        END IF;
    END
// DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_CriaCategoria
(
    IN v_nomecategoria VARCHAR ( 30 ),
    IN v_tipoCategoria VARCHAR ( 10 ))
    BEGIN
        IF ( select exists (
            select 1 from Categoria where NomeCategoria = v_nomecategoria and TipoCategoria = v_tipoCategoria)
        )
        THEN
            select 'Categoria Existente.';
        ELSE
            insert into Categoria
                (
                    NomeCategoria,
                    TipoCategoria
                )
                values
                (
                    v_nomecategoria,
                    v_tipocategoria
                );
        END IF;
    END
// DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_Receita
(
    IN v_id_usuario VARCHAR( 20 ),
    IN v_data DATE,
    IN v_valor DECIMAL (10,2),
    IN v_id_conta VARCHAR ( 40 ),
    IN v_id_categoria VARCHAR (50),
    IN v_recorrente INT,
    IN v_efetuado INT,
    IN v_descricao LONGTEXT)
    BEGIN
    IF ( select exists (select 1 from Receita
        where
        IdUsuario = v_id_usuario and
        IdConta   = v_id_conta and
        Valor     = v_valor and
        Data      = v_data ) )
        THEN
            update Receita
                SET
                    Data       = v_data,
                    Valor       = v_valor,
                    IdConta     = v_id_conta ,
                    IdCategoria = v_id_categoria ,
                    IdRecorrente  = v_recorrente ,
                    Efetuado    = v_efetuado ,
                    Descricao   = v_descricao
                where
                    IdUsuario   = v_id_usuario  and
                    IdConta     = v_id_conta    and
                    Valor       = v_valor  and
                    Data        = v_data;
        ELSE
            insert into Receita
                (
                    IdUsuario,
                    Data,
                    Valor,
                    IdConta,
                    IdCategoria,
                    IdRecorrente,
                    Efetuado,
                    Descricao
                )
                values
                (
                    v_id_usuario,
                    v_data,
                    v_valor,
                    v_id_conta,
                    v_id_categoria,
                    v_recorrente,
                    v_efetuado,
                    v_descricao
                );
        END IF;
    END
// DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_Debito
(
    IN v_id_usuario VARCHAR( 20 ),
    IN v_data DATE,
    IN v_valor DECIMAL (10,2),
    IN v_id_conta VARCHAR ( 40 ),
    IN v_id_categoria VARCHAR (50),
    IN v_recorrente INT,
    IN v_efetuado INT,
    IN v_descricao LONGTEXT)
    BEGIN
    IF ( select exists (select 1 from Debito
        where
        IdUsuario = v_id_usuario and
        IdConta   = v_id_conta and
        Valor     = v_valor and
        Data      = v_data ) )
        THEN
            update Debito
                SET
                    Data          = v_data,
                    Valor         = v_valor,
                    IdConta       = v_id_conta ,
                    IdCategoria   = v_id_categoria ,
                    IdRecorrente  = v_recorrente ,
                    Efetuado      = v_efetuado ,
                    Descricao     = v_descricao
                where
                    IdUsuario   = v_id_usuario  and
                    IdConta     = v_id_conta    and
                    Valor       = v_valor       and
                    Data        = v_data;
        ELSE
            insert into Debito
                (
                    IdUsuario,
                    Data,
                    Valor,
                    IdConta,
                    IdCategoria,
                    IdRecorrente,
                    Efetuado,
                    Descricao
                )
                values
                (
                    v_id_usuario,
                    v_data,
                    v_valor,
                    v_id_conta,
                    v_id_categoria,
                    v_recorrente,
                    v_efetuado,
                    v_descricao
                );
        END IF;
    END
// DELIMITER ;

##################################################
#####  Inserção de Dados Essenciais e Modelo #####
##################################################

INSERT INTO Usuario (
	IdUsuario,
	Senha
	)
	VALUES (
	'jsilva',
	'123@mudar'
);

INSERT INTO DadosUsuario (
	IdUsuario,
	Nome,
	Sobrenome,
	DtNascimento,
	Email,
	Celular
	)
	VALUES (
	'jsilva',
	'Joaquim',
	'Silva',
	'1985-05-10',
	'joaquim.silva@gmail.com',
	'11912345678'
);

INSERT INTO Banco (
	IdBanco, NomeBanco
	)
	VALUES
	(001,'BANCO DO BRASIL S.A (BB)'),
	(237,'BRADESCO S.A'),
	(335,'Banco Digio S.A'),
	(260,'NU PAGAMENTOS S.A (NUBANK)'),
	(290,'Pagseguro Internet S.A (PagBank)'),
	(380,'PicPay Servicos S.A.'),
	(323,'Mercado Pago - conta do Mercado Livre'),
	(637,'BANCO SOFISA S.A (SOFISA DIRETO)'),
	(077,'BANCO INTER S.A'),
	(341,'ITAÚ UNIBANCO S.A'),
	(104,'CAIXA ECONÔMICA FEDERAL (CEF)'),
	(033,'BANCO SANTANDER BRASIL S.A'),
	(212,'BANCO ORIGINAL S.A'),
	(756,'BANCOOB (BANCO COOPERATIVO DO BRASIL)'),
	(655,'BANCO VOTORANTIM S.A'),
	(041,'BANRISUL (BANCO DO ESTADO DO RIO GRANDE DO SUL S.A)'),
	(389,'BANCO MERCANTIL DO BRASIL S.A'),
	(422,'BANCO SAFRA S.A'),
	(070,'BANCO DE BRASÍLIA (BRB)'),
	(136,'UNICRED COOPERATIVA'),
	(74,'BANCO RIBEIRÃO PRETO'),
	(739,'BANCO CETELEM S.A'),
	(743,'BANCO SEMEAR S.A'),
	(100,'PLANNER CORRETORA DE VALORES S.A'
);

INSERT INTO Conta (
	IdConta,
	NomeConta,
	IdUsuario,
	IdBanco,
	CodAgencia,
	CodConta,
	Gerente,
	TelGerente,
	EmailGerente
	)
	VALUES
	('34112340123456' ,
	 'Itau Pessoal' ,
	 'jsilva',
	 341,
	 1234,
	 0123456,
	 'Manuel',
	 '11911223344',
	 'manuel@itau.com.br'),
	('237443388271901',
	 'Bradesco Familia',
	 'jsilva',
	 237,
	 4433,
	 088271901,
	 'José', '11954640099'
	 ,'jose@bradesco.com.br');

INSERT INTO Categoria (NomeCategoria, TipoCategoria)
Values
('Salário', 'Receita'),
('Comissão', 'Receita'),
('Dividendos', 'Receita'),
('Retorno de Investimentos', 'Receita'),
('Herança', 'Receita'),
('Outras Receitas', 'Receita'),
('Aluguel', 'Debito'),
('Condominio', 'Debito'),
('Luz', 'Debito'),
('Agua', 'Debito'),
('Internet', 'Debito'),
('Mercado', 'Debito'),
('Transporte', 'Debito'),
('Presente', 'Debito'),
('Outros Débitos', 'Debito')
;

INSERT INTO Recorrente( NomeRecorrente )
VALUES
('Não Tem Recorrencia'),
('Semanal'),
('Quinzenal'),
('Mensal'),
('Bimestral'),
('Trimestral'),
('Semestral'),
('Anual');

INSERT INTO Receita (
	IdUsuario,
	Data,
	Valor,
	IdConta,
	IdCategoria,
	IdRecorrente,
	Efetuado,
	Descricao
	)
	Values
	('jsilva', '2023-03-10', 10000.00, '34112340123456' , 1, 4, 1, 'Salario'),
	('jsilva', '2023-03-20', 15000.00, '237443388271901', 2, 1, 1, 'Comissão vendas Fevereiro'),
	('jsilva', '2023-03-24', 1000.00, '34112340123456' , 1, 4, 0, 'andiantamento Salario')
	;

INSERT INTO Debito (
	IdUsuario,
	Data,
	Valor,
	IdConta,
	IdCategoria,
	IdRecorrente,
	Efetuado,
	Descricao
	)
	Values
	('jsilva', '2023-03-15', 2000.00,  '237443388271901' , 7, 4, 1, 'Aluguel Apto'),
	('jsilva', '2023-03-20', 500.00,   '237443388271901' , 9, 4, 1, 'Contas de Luz'),
	('jsilva', '2023-03-15', 800.00,   '237443388271901' , 8, 4, 1, 'Condominio'),
	('jsilva', '2023-03-20', 100.00,   '237443388271901' , 9, 4, 1, 'Contas de Agua'),
	('jsilva', '2023-03-24', 540.00,   '34112340123456'  , 11, 4, 1, 'Internet Familia'),
	('jsilva', '2023-03-24', 800.00,   '34112340123456'  , 13, 4, 1, 'Parcela Carro'),
	('jsilva', '2023-03-24', 278.00,   '34112340123456'  , 12, 1, 1, 'Compra Mercado Carrefour')
	;
