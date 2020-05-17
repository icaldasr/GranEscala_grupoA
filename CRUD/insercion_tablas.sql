--funcion ingresar medico
--  retorna 1 si se realizo el registro 
--  retorna 2 si el medico ya existe
--  retorna 0 si la eps o la especializacion no existen 
delimiter //
create function ingresar_medico (_nro_documento int, _eps varchar(50), _nombre varchar(50), 
                                 _apellido varchar(50), _espc varchar(50), _contra varchar(10), _correo varchar(100),
                                 _celular int, _t_documento varchar(100))
    returns int
begin
    declare _id_eps int;
    declare espc int;
    declare id_med int;
    declare corre varchar(100);
    declare tip int;
    
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
                        select id_tipo into tip from tipo_documento where descripcion = _t_documento;
                        if tip IS NOT Null then
                            insert into login (correo, contrasena, tipo)
                            values (_correo, _contra, 'medico');

                            insert into medicos (nro_documento, id_Eps, nombres, apellido, id_espc, Correo, id_tip, celular) 
                            values (_nro_documento, _id_eps, _nombre, _apellido, espc, _correo, tip, _celular);

                            return 1;
                        else
                            return 4;
                        end if;
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
        select codigo_postal into _id_ciudad from ciudad where nombre = _ciudad;
        if _id_ciudad IS NOT Null then
            if _id_eps IS NOT Null then
                insert into ips (id_ips, nombre, direccion, id_ciudad, id_Eps)
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
create function ingresar_consultorio (_descrip varchar(50), _medico int, _ips varchar(50), _fecha_inicial datetime, _fecha_final datetime)
    returns int
begin
    declare _id_ips int;
    declare _id_cons int;
    declare id_med int;
    declare id_med2 int;
    select id_ips into _id_ips from ips where nombre = _ips;
    if _id_ips is NOT Null then
        select consultorio_maximo(_id_ips) into _id_cons;
        select nro_documento into id_med from medicos where nro_documento = _medico;
        if id_med is NOT Null then
            select id_medico into id_med2 from consultorios where id_medico = _medico;
            if id_med2 is Null then
                insert into consultorios (nro_consultorio, descripcion, id_medico, id_Ips, fecha_inicial, fecha_final)
                values (_id_cons, _descrip, _medico, _id_ips, _fecha_inicial, _fecha_final);
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
                return cita_max;
            else
                return 0;
            end if;
        else
            return 0;
        end if;
    else
        return 0;
    end if;
END; //
delimiter ;









--funcion ingresar administrador
--retorna 1 si la insercion fue realizada
--retorna 0 si el correo ya existe
--retorna 2 si el admin ya existe (nro de documento)
--retorna 3 si el tipo de documento no existe

delimiter //
create function ingresar_admin (_id_admin int, _nombre varchar(20), _apellido varchar(20), _contra varchar(10), 
                                _correo varchar(100), _t_tipo varchar(100), _celular int)
    returns int
begin
    declare id_adm int;
    declare corre varchar(100);
    declare tip int;

    select nro_documento into id_adm from administrador where nro_documento = _id_admin;
    if id_adm IS Null then
        select nro_documento into id_adm from medicos where nro_documento = _id_admin;
        if id_adm IS Null then
            select correo into corre from login where correo = _correo;
            if corre IS Null then
                select id_tipo into tip from tipo_documento where descripcion = _t_tipo;
                if tip IS NOT Null then
                    insert into login (correo, contrasena, tipo)
                    values (_correo, _contra, 'administrador');

                    insert into administrador (nro_documento, nombres, apellido, Correo, celular, id_tip)
                    values (_id_admin, _nombre, _apellido, _correo, _celular, tip);
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
    else
        return 2;
    end if;
END; //
delimiter ;




delimiter //
create function solicitud_maxima()
    returns int
begin
    declare soli int;
    select max(id_solicitud) into soli from solicitudes;
    if soli is Null then
        return 1;
    else
        set soli = soli + 1;
        return soli;
    end if;
END; //
delimiter ;





delimiter //
create function ingresar_solicitud(_id_so int, _descripcion varchar(100), _estado varchar(30), 
                                   _paciente int, _med int)
    returns int
begin
    declare id_medi int;
    declare _soli int;

    select nro_documento into id_medi from medicos where nro_documento = _med;
    if id_medi is not Null then
        select solicitud_maxima() into _soli;
        insert into solicitudes (id_solicitud, descripcion, estado, justificacion, nro_paciente, id_medico)
        values (_soli, _descripcion, _estado, NUll, _paciente, id_medi);

        return 1;
    else
        return 0;
    end if;
END; //
delimiter ;






