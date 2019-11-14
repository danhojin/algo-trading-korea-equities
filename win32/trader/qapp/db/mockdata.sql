insert into Tactic (name, endpoint) values ('hasla1', 'http://localhost:8000/hasla1');
insert into Tactic (name, endpoint) values ('hasla2', 'http://localhost:8000/hasla2');
insert into Tactic (name, endpoint) values ('sokcho1', 'http://localhost:8000/sokcho1');
insert into Tactic (name, endpoint) values ('samcheok1', 'http://localhost:8000/samcheok1');
insert into Asset (symbol, num_shares, max_shares, position_size, is_active, tactic) values (
    '000100', 0, 50, 1, 1, 5
);
insert into Asset (symbol, num_shares, max_shares, position_size, is_active, tactic) values (
    '000100', 0, 50, 2, 1, 3
);
insert into Asset (symbol, num_shares, max_shares, position_size, is_active, tactic) values (
    '005930', 10, 30, 4, 1, 2
);
insert into Asset (symbol, num_shares, max_shares, position_size, is_active, tactic) values (
    '005940', 10, 30, 3, 0, 1
);
insert into Entry (asset, date, price, 'order') values (1, '2018-02-03', 200.0, 2);
insert into Entry (asset, date, price, 'order') values (1, '2018-02-04', 220.0, 2);
insert into Entry (asset, date, price, 'order') values (1, '2018-02-05', 200.0, 2);
insert into Entry (asset, date, price, 'order') values (1, '2018-02-06', 250.0, -2);
insert into Entry (asset, date, price, 'order') values (1, '2018-02-07', 260.0, -2);
insert into Entry (asset, date, price, 'order') values (1, '2018-02-08', 240.0, 2);
insert into Entry (asset, date, price, 'order') values (2, '2018-02-03', 140.0, 2);
