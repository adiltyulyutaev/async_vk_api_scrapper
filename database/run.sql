
create database vkapi;

create user adil with encrypted password 'adil';

grant all privileges on database vkapi to adil;


create table groups
(
    id    bigserial not null,
    name  text,
    vk_id bigint    not null
);

alter table groups
    owner to adil;

create unique index groups_id_uindex
    on groups (id);

create unique index groups_vk_id_uindex
    on groups (vk_id);
alter table groups
	add constraint groups_pk
		primary key (id);


create table users
(
    id         bigserial not null
        constraint users_pk
            primary key,
    first_name text,
    last_name  text,
    vk_id      bigint    not null
);

alter table users
    owner to adil;

create unique index users_id_uindex
    on users (id);

create unique index users_vk_id_uindex
    on users (vk_id);

create table subscribers
(
    group_vk_id bigint not null
        constraint subscribers_groups_vk_id_fk
            references groups (vk_id)
            on update cascade on delete cascade,
    user_vk_id  bigint not null
        constraint subscribers_users_vk_id_fk
            references users (vk_id)
            on update cascade on delete cascade,
    relevance   timestamp default now()
);

alter table subscribers
    owner to adil;

create unique index subscribers_group_vk_id_user_vk_id_uindex
    on subscribers (group_vk_id, user_vk_id);


create table subscribers_history
(
    group_vk_id bigint
        constraint subscribers_history_groups_vk_id_fk
            references groups (vk_id)
            on update cascade on delete cascade,
    user_vk_id  bigint
        constraint subscribers_history_users_vk_id_fk
            references users (vk_id)
            on update cascade on delete cascade,
    status      boolean   default true,
    relevance   timestamp default now()
);

alter table subscribers_history
    owner to adil;


create function subscribers_change() returns trigger
language plpgsql
as $$
begin
    if tg_op='INSERT' or tg_op='UPDATE' then insert into subscribers_history values (new.group_vk_id,new.user_vk_id,true);
    else update subscribers_history set status = false where user_vk_id = old.user_vk_id and group_vk_id = old.group_vk_id;
        end if;
    return null;
end;
    $$;

create trigger subscribers_history
    after insert or delete or update on subscribers
        for each row
execute procedure subscribers_change();
