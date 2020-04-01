--funcion ingresar medico
--  retorna 1 si se realizo el registro 
--  retorna 2 si el medico ya existe
--  retorna 0 si la eps o la especializacion no existen 
delimiter //
create function ingresar_medico (_nro_documento int, _eps varchar(50), _nombre varchar(50), 
                                 _apellido varchar(50), _espc varchar(50))
    returns int
begin
    declare _id_eps int;
    declare espc int;
    declare id_med int;
    
    select id_eps into _id_eps from eps where nombre = _eps;
    select id_especializacion into espc from especializaciones where nombre = _espc;
    if _id_eps IS NOT Null then
        if espc IS NOT Null then
            select nro_documento into id_med from medicos where nro_documento = _nro_documento;
            if id_med IS Null then
                insert into medicos (nro_documento, id_Eps, nombres, apellido, id_espc) 
                values (_nro_documento, _id_eps, _nombre, _apellido, espc);
                return 1;
            else
                return 2;
            end if;
        else
            return 0;
        end if;
    else
        return 0;
    end if;
END; //
delimiter ;










--funcion agregar ips
--  retorna 1 si se realizo el registro 
--  retorna 2 si la ips ya existe
--  retorna 0 si la eps o la ciudad no existen
delimiter //
create function ingresar_ips (_id_ips int, _nombre varchar(50), _direccion varchar(50), 
                              _ciudad varchar(50), _eps varchar(50))
    returns int
begin
    declare _id_ciudad int;
    declare _id_eps int;
    declare _idips int;
    select id_ips into _id_eps from ips where id_ips = _id_eps;
    if _idips IS Null then
        select id_eps into _id_eps from eps where nombre = _eps;
        select codigo_postal into _id_ciudad from ciudades where nombre = _ciudad;
        if _id_ciudad IS NOT Null then
            if _id_eps IS NOT Null then
                insert into ips (id_ips, nombre, direccion, _id_ciudad, id_Eps)
                values (_id_ips, _nombre, _direccion, _id_ciudad, _id_eps);
                return 1;
            else
                return 0;
            end if;
        else
            return 0;
        end if;
    else
        return 2;
    end if;
END; //
delimiter ;













-- FUNCIONES PARA INGRESAR CONSULTORIO

-- funcion consultorio maximo
--  retorna el id maximo + 1 de los consultorios de una ips
delimiter //
create function consultorio_maximo(_id_ips int)
    returns int
begin
    declare id_cons int;
    select max(nro_consultorio) into id_cons from consultorios inner join ips on (consultorios.id_Ips = ips.id_ips) 
    where ips.id_ips = _id_ips;
    if id_cons is Null then
        return 1;
    else
        set id_cons = id_cons + 1;
        return id_cons;
    end if;
end; //
delimiter ;

--funcion agregar consultorio 
-- (funcion para una sola eps en la base de datos)
--  retorna 1 si se ejecuta con exito
--  retorna 0 si el medico no existe
--  retorna 2 si la ips no existe
--  retorna 3 si el medico ya posee consultorio
delimiter //
create function ingresar_consultorio (_descrip varchar(50), _medico int, _ips varchar(50))
    returns int
begin
    declare _id_ips int;
    declare _id_cons int;
    declare id_med int;
    select id_ips into _id_ips from ips where nombre = _ips;
    if _id_ips is NOT Null then
        select consultorio_maximo(_id_ips) into _id_cons;
        select nro_documento into id_med from medicos where nro_documento = _medico;
        if id_med is NOT Null then
            select id_medico into id_med from consultorios where id_medico = _medico;
            if id_med is Null then
                insert into consultorios (nro_consultorio, descripcion, id_medico, id_Ips, fecha_inicial, fecha_final)
                values (_id_cons, _descrip, _medico, _id_ips, Null, Null);
                return 1;
            else
                return 3;
            end if;
        else
            return 0;
        end if;
    else
        return 2;
    end if;
END; //
delimiter ;









--FUNCIONES PARA AGENDAR CITAS

-- funcion cita maxima
--  retorna el numero maximo + 1 de las citas de un consultorio
delimiter //
create function cita_maximo(_id_cons int)
    returns int
begin
    declare cita int;
    select max(nro_cita) into cita from horarios where id_consultorio = _id_cons;
    if cita is Null then
        return 1;
    else
        set cita = cita + 1;
        return cita;
    end if;
END; //
delimiter ;


-- funcion agendar citas 
--  retorna 1 si la transaccion se realizo correctamente
--  retorna 0 si el medico con esta en l ips indicada o el consultorio no esta atendiendo
--  retorna 2 si el medico no existe
--  retorna 3 si la ips no existe
delimiter //
create function agendar_cita (_fecha date, _medico int, _ips varchar(50), id_paciente int)
    returns int
begin
    declare _id_ips int;
    declare id_med int;
    declare med_ips int;
    declare nro_cons int;
    declare cita_max int;
    select id_ips into _id_ips from ips where nombre = _ips;
    if _id_ips is not Null then
        select nro_documento into id_med from medicos where nro_documento = _medico;
        if id_med is NOT Null then
            select nro_consultorio into nro_cons from consultorios inner join ips on (consultorios.id_Ips = ips.id_ips) 
            inner join medicos on (consultorios.id_medico = medicos.nro_documento) 
            where medicos.nro_documento = _medico and consultorio.fecha_inicial is not Null;
            if nro_cons is not Null then
                select cita_maximo(nro_cons) into cita_max;
                insert into horarios (nro_cita, fecha, id_consultorio, documento_paciente)
                values (cita_max, _fecha, nro_cons, id_paciente);
                return 1;
            else
                return 0;
            end if;
        else
            return 2;
        end if;
    else
        return 3;
    end if;
END; //
delimiter ;

