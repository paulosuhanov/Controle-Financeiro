
Select SUM(Valor) from Receita where Data BETWEEN '2023-02-01' and '2023-02-' ;

Select round(sum(bs.valor + a.valor),2) from Receita bs, Debito a WHERE a.IdUsuario = bs.IdUsuario;

Select * from Receita;
Select * from Debito where IdUsuario = "jsilva";



SELECT
    bs.IdUsuario,
    SUM(round(bs.Valor,2)) VALOR,
    SUM(d.Valor) DESCONTO,
    SUM(bs.Valor) - SUM(d.valor) TOTAL
FROM
    Receita bs
INNER JOIN Debito D on bs.IdUsuario = D.IdUsuario
GROUP BY D.IdUsuario;


select (gd.Valor - re.valor) as valortotal from (Select SUM(Valor) valor from Receita WHERE IdUsuario = 'jsilva') gd, (Select SUM(valor) valor from Debito WHERE IdUsuario = 'jsilva') re;




select b. IdUsuario, Data, Valor, e.NomeConta, d.NomeRecorrente, Efetuado, Descricao, c.NomeCategoria  from Receita b, Categoria c, Recorrente d, Conta e WHERE b.IdCategoria = c.IdCategoria and b.IdRecorrente = d.IdRecorrente and b.IdConta = e.IdConta



(select b.Data, b.Valor, e.NomeConta, c.NomeCategoria, d.NomeRecorrente, CASE WHEN b.Efetuado = 0 THEN 'Não Efetuado' ELSE 'Efetuado' END AS Efetuado, b.Descricao
    from
        Receita b
       INNER JOIN Categoria c ON b.IdCategoria = c.IdCategoria
       INNER JOIN Recorrente d ON b.IdRecorrente = d.IdRecorrente
       INNER JOIN Conta e ON b.IdConta = e.IdConta
    WHERE b.Idusuario = 'jsilva')
UNION ALL
(select b.Data, (b.Valor)*-1, e.NomeConta, c.NomeCategoria, d.NomeRecorrente,
       CASE WHEN b.Efetuado = 0 THEN 'Não Efetuado' ELSE 'Efetuado' END AS Efetuado, b.Descricao
    from
        Debito b
       INNER JOIN Categoria c ON b.IdCategoria = c.IdCategoria
       INNER JOIN Recorrente d ON b.IdRecorrente = d.IdRecorrente
       INNER JOIN Conta e ON b.IdConta = e.IdConta
    WHERE b.IdUsuario = 'jsilva');