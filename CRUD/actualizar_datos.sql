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
    else
        return 0;
    end if;
end; //
delimiter ;








delimiter //
create function actualizar_solicitud(id int, _estado varchar(30), _justificacion varchar(100))
    returns int
begin
    declare id_soli int;

    select id_solicitud into id_soli from id_solicitudes where id_solicitud = id;
    if id_soli is not null then
        update id_solicitudes set estado = _estado, justificacion = _justificacion where id_solicitud = id_soli;
        return 1;
    else
        return 0;
    end if;
end; //
delimiter ;