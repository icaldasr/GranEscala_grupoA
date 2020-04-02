delimiter //
create function actualizar_consultorios(_id_cons int, fecha_i datetime, fecha_f datetime)
    returns int
begin
    declare cons int;
    declare mes_i date;
    declare ano_i date;
    declare mes_f date;
    declare ano_f date;
    declare ano date;
    declare mes date;

    select nro_consultorio into  cons from consultorios where nro_consultorio = _id_cons;
    if cons is not null then
        select year(now()) into ano;
        select month(now()) into mes;
        select year(fecha_i) into ano_i;
        select month(fecha_i) into mes_i;
        select year(fecha_f) into ano_f;
        select month(fecha_f) into mes_f;
        if ano_f >= ano and ano_i >= ano then
            if ano_f > ano_i then
                update consultorios set fecha_inicial = fecha_i, fecha_final = fecha_f
                where nro_consultorio = _id_cons;
                return 1;
            elseif ano_f = ano_i then
                if mes_f >= mes_i then 
                    update consultorios set fecha_inicial = fecha_i, fecha_final = fecha_f
                    where nro_consultorio = _id_cons;
                    return 1;
                else
                    return 0;
                end if;
            else
                return 0;
            end if;
        else
            return 0;
        end if;
