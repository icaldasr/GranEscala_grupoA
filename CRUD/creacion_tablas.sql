create table departamentos(
    id_departamento int primary key,
    nombre varchar(50) not null
);

create table ciudad(
    codigo_postal int primary key,
    nombre varchar(50) not null,
    cod_departamento int references departamentos(id_departamento)
);

create table especializaciones(
    id_especializacion int primary key,
    nombre varchar(80) not null
);

create table eps(
    id_eps int primary key,
    nombre varchar(30) not null,
    descripcion varchar(100)
);

create table medicos(
    nro_documento int primary key,
    id_Eps int references eps(id_eps),
    nombres varchar(20),
    apellido varchar(30),
    id_espc int references especializaciones(id_especializacion)
);

create table ips(
    id_ips int primary key,
    nombre varchar(30),
    direccion varchar(30),
    id_ciudad int references ciudad(codigo_postal),
    id_Eps int references eps(id_eps)
);

create table consultorios(
    nro_consultorio int primary key,
    descripcion varchar(30),
    id_medico int references medicos(nro_documento),
    id_Ips int references ips(id_ips),
    fecha_inicial date,
    fecha_final date
);

create table horarios(
    nro_cita int primary key,
    fecha date not null,
    id_consultorio int references consultorios(nro_consultorio),
    documento_paciente int not null
);