--funcion ingresar medico
--  retorna 1 si se realizo el registro 
--  retorna 2 si el medico ya existe
--  retorna 0 si la eps o la especializacion no existen 
delimiter //
create function ingresar_medico (_nro_documento int, _eps varchar(50), _nombre varchar(50), 
                                 _apellido varchar(50), _espc varchar(50), _contra varchar(10), _correo varchar(100))
    returns int
begin
    declare _id_eps int;
    declare espc int;
    declare id_med int;
    declare corre varchar(100);
    
    select id_eps into _id_eps from eps where nombre = _eps;
    select id_especializacion into espc from especializaciones where nombre = _espc;
    if _id_eps IS NOT Null then
        if espc IS NOT Null then
            select nro_documento into id_med from medicos where nro_documento = _nro_documento;
            if id_med IS Null then
                select nro_documento into id_med from administrador where nro_documento = _nro_documento;
                if id_med IS Null then
                    select correo into corre from login where correo = _correo;
                    if corre IS Null then
                        insert into login (correo, contrasena, tipo)
                        values (_correo, _contra, 'medico');

                        insert into medicos (nro_documento, id_Eps, nombres, apellido, id_espc, Correo) 
                        values (_nro_documento, _id_eps, _nombre, _apellido, espc, _correo);

                        return 1;
                    else
                        return 3;
                    end if;
                else
                    return 2;
                end if;
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
--  retorna 0 si el medico no con esta en la ips indicada o el consultorio no esta atendiendo
--  retorna 2 si el medico no existe
--  retorna 3 si la ips no existe
delimiter //
create function agendar_cita (_fecha datetime, _medico int, _ips varchar(50), id_paciente int)
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
            where medicos.nro_documento = _medico and consultorios.fecha_inicial is not Null;
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










--funcion ingresar administrador
--retorna 1 si la insercion fue realizada
--retorna 0 si el correo ya existe
--retorna 2 si el admin ya existe (nro de documento)

delimiter //
create function ingresar_admin (_id_admin int, _nombre varchar(20), _apellido varchar(20), _contra varchar(10), 
                                _correo varchar(100))
    returns int
begin
    declare id_adm int;
    declare corre varchar(100);

    select nro_documento into id_adm from administrador where nro_documento = _id_admin;
    if id_adm IS Null then
        select nro_documento into id_adm from medicos where nro_documento = _id_admin;
        if id_adm IS Null then
            select correo into corre from login where correo = _correo;
            if corre IS Null then
                insert into login (correo, contrasena, tipo)
                values (_correo, _contra, 'administrador');

                insert into administrador (nro_documento, nombres, apellido, Correo)
                values (_id_admin, _nombre, _apellido, _correo);

                return 1;
            else
                return 0;
            end if;
        else
            return 2;
        end if;
    else
        return 2;
    end if;
END; //
delimiter ;

