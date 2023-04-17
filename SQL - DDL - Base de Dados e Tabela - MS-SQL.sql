--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- 
--=X=-- DDL - Criação da Base de Dados e Tabelas - SQL Server   --=X=--
--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=--

CREATE DATABASE MinhaCarteira;
GO

USE My_Wallet;
GO

CREATE TABLE Usuario (
    ID INT NOT NULL IDENTITY ( 1,1 ) ,
    [LOGIN] VARCHAR ( 11 ) NOT NULL,
    Senha VARCHAR ( 30 ),
    DtExpiracao DATE NOT NULL DEFAULT '1900-01-01' ,
    CONSTRAINT PK_Usuario PRIMARY KEY ( ID ),
    CONSTRAINT UQ_Login UNIQUE ( [Login] ),
);
GO

CREATE TABLE DadosUsuario (
    ID INT NOT NULL IDENTITY ( 1,1 ) ,
    IdUsuario VARCHAR ( 11 ) NOT NULL ,
    Nome VARCHAR ( 50 ) NOT NULL ,
    Sobrenome VARCHAR ( 50 ) NOT NULL,
    DtNascimento DATE NOT NULL DEFAULT '1900-01-01',
    Email VARCHAR ( 50 ) NOT NULL ,
    Celular INT NOT NULL ,
    Foto VARCHAR ( 255 ),
    CONSTRAINT PK_Usuario PRIMARY KEY ( ID ) ,
    CONSTRAINT FK_IdUsuario FOREIGN KEY ( IdUsuario ) 
        REFERENCES Usuario( [LOGIN] ) ,
    CONSTRAINT UQ_Celular UNIQUE ( Celular ) ,
    CONSTRAINT UQ_Email UNIQUE ( Email ),
    CONSTRAINT UQ_UsuarioId UNIQUE ( IdUsuario ),
);
GO

CREATE TABLE Banco (
    ID INT NOT NULL IDENTITY ( 1,1 ) ,
    NomeBanco VARCHAR ( 20 ) NOT NULL ,
    CONSTRAINT PK_Banco PRIMARY KEY ( ID ),   
);
GO

CREATE TABLE Conta (
    ID INT NOT NULL IDENTITY ( 1,1 ) ,
    IdProprietario VARCHAR ( 11 ) NOT NULL ,
    IdBanco INT NOT NULL ,
    Agencia INT NOT NULL ,
    Conta INT NOT NULL , 
    Gerente VARCHAR ( 50 ) ,
    TelGerente INT ,
    EmailGerente VARCHAR ( 50 ),
    CONSTRAINT PK_Conta PRIMARY KEY ( ID ) ,
    CONSTRAINT FK_IdProprietario FOREIGN KEY ( IdProprietario ) 
        REFERENCES Usuario( [LOGIN] ) ,
    CONSTRAINT FK_Banco FOREIGN KEY ( IdBanco )
        REFERENCES Banco ( ID ),
    CONSTRAINT UQ_Conta UNIQUE ( IdProprietario , IdBanco , Agencia , Conta ) ,
);
GO

CREATE TABLE CatReceita (
    ID INT NOT NULL IDENTITY ( 1,1 ),
    CategoriaReceita VARCHAR ( 30 ),
    CONSTRAINT PK_CatReceita PRIMARY KEY ( ID ) ,
);
GO

CREATE TABLE Receita (
    ID INT NOT NULL IDENTITY ( 1,1 ) ,
    IdUsuarioReceita VARCHAR ( 11 ) , --NOT NULL ,
    DtEntradaReceita DATE NOT NULL DEFAULT '1900-01-01',
    VlReceita DECIMAL ( 10,2 ) NOT NULL,
    IdContaReceita INT NOT NULL ,
    IdCatReceita INT NOT NULL ,
    Recorrente VARCHAR ( 3 ) DEFAULT 'Não' ,
    TipoRecorrente VARCHAR ( 15 ) ,
    DescReceita VARCHAR ( MAX ),
    CONSTRAINT PK_Receita PRIMARY KEY ( ID ),
    CONSTRAINT FK_IdUsuarioReceita FOREIGN KEY ( IdUsuarioReceita )
        REFERENCES Usuario( [LOGIN] ),
    CONSTRAINT FK_IdContaReceita FOREIGN KEY ( IdContaReceita )
        REFERENCES Conta ( ID ),
    CONSTRAINT FK_IdCatReceita FOREIGN KEY ( IdCatReceita )
        REFERENCES CatReceita ( ID ),
    CONSTRAINT CK_TipoRecorrente CHECK 
        ( TipoRecorrente='Anual' or 
          TipoRecorrente='Semestral' or 
          TipoRecorrente='Trimestral' or 
          TipoRecorrente='Bimestral' or 
          TipoRecorrente='Mensal' or 
          TipoRecorrente='Quinzenal' or 
          TipoRecorrente='Semanal' ),
);
GO




docker run --name mysql \
    --restart=always \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=Secure987 \
    -e MYSQL_DATABASE=MinhaCarteira \
    -e MYSQL_USER=pfelix \
    -e MYSQL_PASSWORD=Secure987 \
    -d mysql/mysql-server:latest-aarch64