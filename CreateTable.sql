
create schema Dimensional;

create sequence Dimensional.ChaveVendedor;

create table Dimensional.DimensaoVendedor
(
    ChaveVendedor int default nextval('Dimensional.ChaveVendedor'::regclass) primary key,
    IdVendedor int,
    Nome varchar(50),
    DataInicioValidade date,
    DataFimValidade date
);


drop table Dimensional.DimensaoVendedor;