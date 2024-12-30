create sequence if not exists product_price_rec_seq start with 1 increment by 1 cache 50
;
create type record_creation_type as enum ('auto', 'manual')
;
create table if not exists product_prices
(
    record_id bigint primary key default nextval('product_price_rec_seq'),
    record_type record_creation_type not null,
    created_at timestamp default now() not null,
    product_id bigint not null,
    product_name text not null,
    product_status varchar(80),
    product_price_old int,
    product_price_old_curr varchar(3),
    product_price_new int,
    product_price_new_curr varchar(3)
);
