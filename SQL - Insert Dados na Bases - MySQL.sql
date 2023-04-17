--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- 
--=X=--           Inclusão de dados essenciais - MySQL          --=X=--
--=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=-- --=X=--


USE MinhaCarteira;
INSERT INTO Banco (IdBanco, NomeBanco)
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
(041,'BANRISUL – BANCO DO ESTADO DO RIO GRANDE DO SUL S.A'),
(389,'BANCO MERCANTIL DO BRASIL S.A'),
(422,'BANCO SAFRA S.A'),
(070,'BANCO DE BRASÍLIA (BRB)'),
(136,'UNICRED COOPERATIVA'),
(74,'BANCO RIBEIRÃO PRETO'),
(739,'BANCO CETELEM S.A'),
(743,'BANCO SEMEAR S.A'),
(100,'PLANNER CORRETORA DE VALORES S.A');

INSERT INTO CatReceita (CategoriaReceita)
Values
('Salário'),
('Comissão'),
('Dividendos'),
('Retorno de Investimentos'),
('Herança'),
('Outros');

INSERT INTO Receita (
	DtEntrada, VlReceita, IdCatReceita, DescReceita
	)
	Values
	('2023-03-10', 10000.00, 1, 'Salario andiantamento'),
	('2023-03-20', 15000.00, 2, 'Comissão vendas Fevereiro');