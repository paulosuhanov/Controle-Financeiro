--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- 
--=X=--                 Store Procedure - MySQL                 --=X=--
--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=--
CREATE DATABASE MinhaCarteira;

USE MinhaCarteira;

DELIMITER // 
CREATE PROCEDURE sp_criaUsuario
( 
    IN v_usuario VARCHAR(11), 
    IN v_senha VARCHAR(30)) 
    BEGIN 
        IF ( select exists (select 1 from Usuario where Usuario = v_usuario) ) 
        THEN
            select 'Usuário Existente !!';
        ELSE
            insert into Usuario
                ( 
                    Usuario, 
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
    IN v_id_usuario VARCHAR(11), 
    IN v_nome VARCHAR(50),
    IN v_sobrenome VARCHAR(50),
    IN v_dt_nascimento DATE,
    IN v_email VARCHAR ( 50),
    IN v_celular INT)
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
CREATE PROCEDURE sp_criaBancoCustomizado
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
    IN v_id_usuario VARCHAR(11), 
    IN v_id_banco INT,
    IN v_agencia INT,
    IN v_conta INT,
    IN v_gerente VARCHAR (50),
    IN v_tel_gerente INT,
    IN v_email_gerente VARCHAR(50))
    BEGIN 
    IF ( select exists (select 1 from Conta where IdUsuario = v_id_usuario and Conta = v_conta ) )
        THEN
            update Conta
                SET
                    IdBanco = v_id_banco,
                    Agencia = v_agencia,
                    Conta = v_conta,
                    Gerente = v_gerente,
                    TelGerente = v_tel_gerente,
                    EmailGerente = v_email_gerente
                where 
                    IdUsuario = v_id_usuario and Conta = v_conta;
        ELSE
            insert into Conta
                ( 
                    IdBanco,
                    Agencia,
                    Conta,
                    Gerente,
                    TelGerente,
                    EmailGerente
                ) 
                values 
                ( 
                    v_id_banco,
                    v_agencia,
                    v_conta,
                    v_gerente,
                    v_tel_gerente,
                    v_email_gerente
                );
        END IF;
    END 
// DELIMITER ;


DELIMITER // 
CREATE PROCEDURE sp_CriaCategoriaReceita
(  
    IN v_categoria VARCHAR(20)) 
    BEGIN 
        IF ( select exists (select 1 from CatReceita where CategoriaReceita = v_categoria) ) 
        THEN
            select 'Categoria Existente.';
        ELSE
            insert into CatReceita
                (  
                    CategoriaReceita
                ) 
                values 
                (  
                    v_categoria
                );
        END IF;
    END 
// DELIMITER ;


DELIMITER // 
CREATE PROCEDURE sp_CriaReceita
( 
    IN v_id_usuario VARCHAR(11), 
    IN v_dt_entrada DATE,
    IN v_vl_receita DECIMAL (10,2),
    IN v_id_conta_receita INT,
    IN v_id_categoria VARCHAR (50),
    IN v_recorrencia VARCHAR (3),
    IN v_TipoRecorrente VARCHAR ( 15 ),
    IN v_desc_receita LONGTEXT)
    BEGIN 
    IF ( select exists (select 1 from Receita 
        where 
        IdUsuario = v_id_usuario and 
        Conta = v_conta and
        VlReceita = v_vl_receita and
        DtEntrada = v_dt_entrada ) )
        THEN
            update Receita
                SET
                    DtEntrada = v_dt_entrada,
                    VlReceita = v_vl_receita,
                    IdContaReceita = v_id_conta_receita ,
                    IdCatReceita = v_id_categoria ,
                    Recorrente = v_recorrencia ,
                    TipoRecorrente = v_TipoRecorrente ,
                    DescReceita = v_desc_receita
                where
                    IdUsuario = v_id_usuario and DtEntrada = v_dt_entrada;
        ELSE
            insert into Receita
                ( 
                    DtEntrada,
                    VlReceita,
                    IdContaReceita,
                    IdCatReceita,
                    Recorrente,
                    TipoRecorrente,
                    DescReceita
                ) 
                values 
                ( 
                    v_dt_entrada,
                    v_vl_receita,
                    v_id_conta_receita ,
                    v_id_categoria ,
                    v_recorrencia ,
                    v_TipoRecorrente ,
                    v_desc_receita
                );
        END IF;
    END 
// DELIMITER ;



