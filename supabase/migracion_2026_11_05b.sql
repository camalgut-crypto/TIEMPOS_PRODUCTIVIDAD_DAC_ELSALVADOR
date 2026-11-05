-- Solo feriados nacionales: fuera las Fiestas Patronales de San Salvador. schema.sql ya viene sin ellas.
delete from dac_sv.dac_feriados where fecha in ('2026-08-03', '2026-08-05', '2027-08-03', '2027-08-05');
