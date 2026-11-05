-- Producto PYME (antes PYMES) en el esquema ya creado. schema.sql ya lo trae para instalaciones nuevas.
alter table dac_sv.dac_solicitudes drop constraint if exists dac_solicitudes_producto_check;
alter table dac_sv.dac_solicitudes add constraint dac_solicitudes_producto_check check (producto in ('PYME','PERS'));
alter table dac_sv.dac_analistas drop constraint if exists dac_analistas_producto_check;
alter table dac_sv.dac_analistas add constraint dac_analistas_producto_check check (producto in ('PYME','PERS'));
update dac_sv.dac_config set valor = '{"PERS": 30, "PYME": 50}' where clave = 'metas';
