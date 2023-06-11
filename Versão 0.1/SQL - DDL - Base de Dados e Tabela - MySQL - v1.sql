--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- 
--=X=-- DDL - Criação da Base de Dados e Tabelas - MySQL        --=X=--
--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=--
CREATE DATABASE MinhaCarteira;

USE MinhaCarteira;
CREATE TABLE Usuario(
    ID INT NOT NULL AUTO_INCREMENT,
    Usuario VARCHAR (11) NOT NULL,
    Senha VARCHAR (30),
    DtExpiracao DATE NOT NULL DEFAULT '1900-01-01' ,
    CONSTRAINT PK_Usuario PRIMARY KEY (ID),
    CONSTRAINT UQ_Login UNIQUE (Usuario)
);

CREATE TABLE DadosUsuario (
    ID INT NOT NULL AUTO_INCREMENT,
    IdUsuario VARCHAR ( 11 ) NOT NULL,
    Nome VARCHAR ( 50 ) NOT NULL,
    Sobrenome VARCHAR ( 50 ) NOT NULL,
    DtNascimento DATE NOT NULL DEFAULT '1900-01-01',
    Email VARCHAR ( 50 ) NOT NULL ,
    Celular INT NOT NULL ,
    Foto VARCHAR (255),CONSTRAINT PK_Usuario PRIMARY KEY (ID),
    CONSTRAINT FK_IdUsuario FOREIGN KEY (IdUsuario) 
        REFERENCES Usuario(Usuario),
    CONSTRAINT UQ_Celular UNIQUE ( Celular ),
    CONSTRAINT UQ_Email UNIQUE ( Email ),
    CONSTRAINT UQ_UsuarioId UNIQUE ( IdUsuario )
);

CREATE TABLE Banco (
    ID INT NOT NULL AUTO_INCREMENT,
    IdBanco INT NOT NULL,
    NomeBanco VARCHAR ( 100 ) NOT NULL ,
    CONSTRAINT PK_Banco PRIMARY KEY ( ID ),
    CONSTRAINT UQ_IdBanco UNIQUE (IdBanco)
);

CREATE TABLE Conta (
    IdUsuario VARCHAR ( 11 ) NOT NULL ,
    IdBanco INT NOT NULL ,
    Agencia INT NOT NULL ,
    Conta INT NOT NULL , 
    Gerente VARCHAR ( 50 ) ,
    TelGerente INT ,
    EmailGerente VARCHAR ( 50 ),
    CONSTRAINT FK_IdUsuario_Conta FOREIGN KEY ( IdUsuario ) 
        REFERENCES Usuario(Usuario),
    CONSTRAINT FK_Banco FOREIGN KEY ( IdBanco )
        REFERENCES Banco ( IdBanco ),
    CONSTRAINT UQ_Conta UNIQUE ( IdUsuario , IdBanco , Agencia , Conta )    
);

ALTER TABLE Conta 
    ADD CONSTRAINT PK_Conta PRIMARY KEY (IdUsuario,Conta,IdBanco);
    
CREATE TABLE CatReceita (
    ID INT NOT NULL AUTO_INCREMENT,
    CategoriaReceita VARCHAR ( 30 ),
    CONSTRAINT PK_CatReceita PRIMARY KEY ( ID )
);

CREATE TABLE Receita (
    ID INT NOT NULL AUTO_INCREMENT,
    IdUsuario VARCHAR ( 11 ) ,
    DtEntrada DATE NOT NULL DEFAULT '1900-01-01',
    VlReceita DECIMAL ( 10,2 ) NOT NULL,
    IdContaReceita INT ,
    IdCatReceita INT NOT NULL ,
    Recorrente VARCHAR ( 3 ) DEFAULT 'Não' ,
    TipoRecorrente VARCHAR ( 15 ) ,
    DescReceita LONGTEXT,
    CONSTRAINT PK_Receita PRIMARY KEY ( ID ),
    CONSTRAINT FK_IdCatReceita FOREIGN KEY ( IdCatReceita )
        REFERENCES CatReceita ( ID ),
    CONSTRAINT CK_TipoRecorrente CHECK 
        ( TipoRecorrente='Anual' or 
          TipoRecorrente='Semestral' or 
          TipoRecorrente='Trimestral' or 
          TipoRecorrente='Bimestral' or 
          TipoRecorrente='Mensal' or 
          TipoRecorrente='Quinzenal' or 
          TipoRecorrente='Semanal' or
          TipoRecorrente='Nenhum')
);
