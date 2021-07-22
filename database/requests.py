def get_group_query(columns, values, keys):
    query = '''
    insert into groups {columns} values {values} on conflict {keys} do update set name = excluded.name
    '''.format(
        columns=columns,
        keys=keys,
        values=values)
    return query


def get_user_query(columns, values, keys):
    query = '''
        insert into users {columns} values {values} on conflict {keys} do update set first_name = excluded.first_name, last_name = excluded.last_name
    '''.format(columns=columns,
               values=values,
               keys=keys
               )
    return query


def get_subscribers_query(values):
    query = '''insert into subscribers values {values} on conflict (group_vk_id,user_vk_id) 
    do nothing'''.format(values=values)
    return query
