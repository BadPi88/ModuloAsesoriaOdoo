from odoo import models, fields, api
import base64
from datetime import date

# Extensión del modelo res.company para incluir datos del administrador de la sociedad
class ResCompany(models.Model):
    _inherit = 'res.company'

    admin_name = fields.Char(string="Administrador - Nombre")
    admin_nif = fields.Char(string="Administrador - NIF")
    admin_position = fields.Char(string="Administrador - Cargo")

# Modelo principal para generar la declaración Modelo 200 y almacenar sus datos contables y fiscales
class Modelo200Declaration(models.Model):
    cnae = fields.Char(string="CNAE")
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # Campos faltantes detectados por comparación con XML
    t00001 = fields.Float(string="t00001 - Campo t00001")
    t00003 = fields.Float(string="t00003 - Campo t00003")
    t00006 = fields.Float(string="t00006 - Campo t00006")
    t00011 = fields.Float(string="t00011 - Campo t00011")
    t00012 = fields.Float(string="t00012 - Campo t00012")
    t00013 = fields.Float(string="t00013 - Campo t00013")
    t00030 = fields.Float(string="t00030 - Campo t00030")
    t00047 = fields.Float(string="t00047 - Campo t00047")
    t00064 = fields.Float(string="t00064 - Campo t00064")
    t00081 = fields.Float(string="t00081 - Campo t00081")
    t00098 = fields.Float(string="t00098 - Campo t00098")
    t00115 = fields.Float(string="t00115 - Campo t00115")
    t00132 = fields.Float(string="t00132 - Campo t00132")
    t00149 = fields.Float(string="t00149 - Campo t00149")
    t00166 = fields.Float(string="t00166 - Campo t00166")
    t00183 = fields.Float(string="t00183 - Campo t00183")
    t00200 = fields.Float(string="t00200 - Campo t00200")
    t00217 = fields.Float(string="t00217 - Campo t00217")
    t00234 = fields.Float(string="t00234 - Campo t00234")
    t00251 = fields.Float(string="t00251 - Campo t00251")
    t00268 = fields.Float(string="t00268 - Campo t00268")
    t00285 = fields.Float(string="t00285 - Campo t00285")
    t00302 = fields.Float(string="t00302 - Campo t00302")
    t00319 = fields.Float(string="t00319 - Campo t00319")
    t00336 = fields.Float(string="t00336 - Campo t00336")
    t00353 = fields.Float(string="t00353 - Campo t00353")
    t00370 = fields.Float(string="t00370 - Campo t00370")
    t00387 = fields.Float(string="t00387 - Campo t00387")
    t00404 = fields.Float(string="t00404 - Campo t00404")
    t00421 = fields.Float(string="t00421 - Campo t00421")
    t00438 = fields.Float(string="t00438 - Campo t00438")
    t00455 = fields.Float(string="t00455 - Campo t00455")
    t00472 = fields.Float(string="t00472 - Campo t00472")
    t00489 = fields.Float(string="t00489 - Campo t00489")
    t00506 = fields.Float(string="t00506 - Campo t00506")
    t00523 = fields.Float(string="t00523 - Campo t00523")
    t00540 = fields.Float(string="t00540 - Campo t00540")
    t00557 = fields.Float(string="t00557 - Campo t00557")
    t00570 = fields.Float(string="t00570 - Campo t00570")
    t00574 = fields.Float(string="t00574 - Campo t00574")
    t00591 = fields.Float(string="t00591 - Campo t00591")
    t00608 = fields.Float(string="t00608 - Campo t00608")
    t00625 = fields.Float(string="t00625 - Campo t00625")
    t00642 = fields.Float(string="t00642 - Campo t00642")
    t00659 = fields.Float(string="t00659 - Campo t00659")
    t00676 = fields.Float(string="t00676 - Campo t00676")
    t00693 = fields.Float(string="t00693 - Campo t00693")
    t00710 = fields.Float(string="t00710 - Campo t00710")
    t00727 = fields.Float(string="t00727 - Campo t00727")
    t00744 = fields.Float(string="t00744 - Campo t00744")
    t00757 = fields.Float(string="t00757 - Campo t00757")
    t00761 = fields.Float(string="t00761 - Campo t00761")
    t00778 = fields.Float(string="t00778 - Campo t00778")
    t00795 = fields.Float(string="t00795 - Campo t00795")
    t00812 = fields.Float(string="t00812 - Campo t00812")
    t00829 = fields.Float(string="t00829 - Campo t00829")
    t00846 = fields.Float(string="t00846 - Campo t00846")
    t00863 = fields.Float(string="t00863 - Campo t00863")
    t00876 = fields.Float(string="t00876 - Campo t00876")
    t00880 = fields.Float(string="t00880 - Campo t00880")
    t00897 = fields.Float(string="t00897 - Campo t00897")
    t00914 = fields.Float(string="t00914 - Campo t00914")
    t00931 = fields.Float(string="t00931 - Campo t00931")
    t00948 = fields.Float(string="t00948 - Campo t00948")
    t00965 = fields.Float(string="t00965 - Campo t00965")
    t00982 = fields.Float(string="t00982 - Campo t00982")
    t00999 = fields.Float(string="t00999 - Campo t00999")
    t01016 = fields.Float(string="t01016 - Campo t01016")
    t01033 = fields.Float(string="t01033 - Campo t01033")
    t01050 = fields.Float(string="t01050 - Campo t01050")
    t01063 = fields.Float(string="t01063 - Campo t01063")
    t01199 = fields.Float(string="t01199 - Campo t01199")
    t01250 = fields.Float(string="t01250 - Campo t01250")
    # Campos para DP200010
    t00001 = fields.Char(string="Inicio del identificador de modelo y página. [00001]")
    t00003 = fields.Integer(string="Modelo. [00003]")
    t00006 = fields.Integer(string="Página. [00006]")
    t00011 = fields.Char(string="Fin de identificador de modelo. [00011]")
    t00012 = fields.Integer(string="Indicador de página complementaria. [00012]")
    t00013 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo,  final del ejercicio anterior - Capital - Escriturado [00380] [00013]")
    t00030 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo,  final del ejercicio anterior - Capital - No exigido  [00381] [00030]")
    t00047 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo,  final del ejercicio anterior - Prima de emisión  [00382] [00047]")
    t00064 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo,  final del ejercicio anterior - Reservas  [00383] [00064]")
    t00081 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo,  final del ejercicio anterior - Acciones y participaciones en patrimonio propias  [00384] [00081]")
    t00098 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo,  final del ejercicio anterior - Resultados ejercicios anteriores  [00385] [00098]")
    t00115 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo,  final del ejercicio anterior - Otras aportaciones de socios  [00386] [00115]")
    t00132 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por cambio de criterio de ejercicios anteriores - Capital - Escriturado  [00394] [00132]")
    t00149 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por cambio de criterio de ejercicios anteriores - Capital - No exigido [00395] [00149]")
    t00166 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por cambio de criterio de ejercicios anteriores - Prima de emisión [00396] [00166]")
    t00183 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por cambio de criterio de ejercicios anteriores - Reservas [00397] [00183]")
    t00200 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por cambio de criterio de ejercicios anteriores - Acciones y participaciones en patrimonio propias [00398] [00200]")
    t00217 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por cambio de criterio de ejercicios anteriores - Resultados ejercicios anteriores [00399] [00217]")
    t00234 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por cambio de criterio de ejercicios anteriores - Otras aportaciones de socios [00400] [00234]")
    t00251 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por errores de ejercicios anteriores - Capital - Escriturado [00408] [00251]")
    t00268 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por errores de ejercicios anteriores - Capital - No exigido [00409] [00268]")
    t00285 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por errores de ejercicios anteriores - Prima de emisión [00410] [00285]")
    t00302 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por errores de ejercicios anteriores - Reservas [00411] [00302]")
    t00319 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por errores de ejercicios anteriores - Acciones y participaciones en patrimonio propias [00412] [00319]")
    t00336 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por errores de ejercicios anteriores - Resultados ejercicios anteriores [00413] [00336]")
    t00353 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ajustes por errores de ejercicios anteriores - Otras aportaciones de socios [00414] [00353]")
    t00370 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo ajustado, inicio del ejercicio - Capital - Escriturado [00422] [00370]")
    t00387 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo ajustado, inicio del ejercicio - Capital - No exigido [00423] [00387]")
    t00404 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo ajustado, inicio del ejercicio - Prima de emisión [00424] [00404]")
    t00421 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo ajustado, inicio del ejercicio - Reservas [00425] [00421]")
    t00438 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo ajustado, inicio del ejercicio - Acciones y participaciones en patrimonio propias [00426] [00438]")
    t00455 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo ajustado, inicio del ejercicio - Resultados ejercicios anteriores [00427] [00455]")
    t00472 = fields.Float(string="Estado de cambios patrimonio neto (II) - Saldo ajustado, inicio del ejercicio - Otras aportaciones socios [00428] [00472]")
    t00489 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Total ingresos y gastos reconocidos - Capital - Escriturado [00436] [00489]")
    t00506 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Total ingresos y gastos reconocidos - Capital - No exigido [00437] [00506]")
    t00523 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Total ingresos y gastos reconocidos - Prima de emisión [00438] [00523]")
    t00540 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Total ingresos y gastos reconocidos - Reservas [00439] [00540]")
    t00557 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Total ingresos y gastos reconocidos - Acciones y participaciones en patrimonio propias [00440] [00557]")
    t00574 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Total ingresos y gastos reconocidos - Resultados ejercicios anteriores [00441] [00574]")
    t00591 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Total ingresos y gastos reconocidos - Otras aportaciones de socios [00442] [00591]")
    t00608 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Resultado cuenta pérdidas y ganancias - Capital - Escriturado [00450] [00608]")
    t00625 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Resultado cuenta pérdidas y ganancias - Capital - No exigido [00451] [00625]")
    t00642 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Resultado cuenta pérdidas y ganancias - Prima de emisión [00452] [00642]")
    t00659 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Resultado cuenta pérdidas y ganancias - Reservas [00453] [00659]")
    t00676 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Resultado cuenta pérdidas y ganancias - Acciones y participaciones en patrimonio propias [00454] [00676]")
    t00693 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Resultado cuenta pérdidas y ganancias - Resultados ejercicios anteriores [00455] [00693]")
    t00710 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Resultado cuenta pérdidas y ganancias - Otras aportaciones de socios [00456] [00710]")
    t00727 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Capital - Escriturado [00464] [00727]")
    t00744 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Capital - No exigido [00465] [00744]")
    t00761 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Prima de emisión [00466] [00761]")
    t00778 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Reservas [00467] [00778]")
    t00795 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Acciones y participaciones en patrimonio propias [00468] [00795]")
    t00812 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Resultados ejercicios anteriores [00469] [00812]")
    t00829 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otras aportaciones de socios [00470] [00829]")
    t00846 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Capital - Escriturado [00478] [00846]")
    t00863 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Capital - No exigido [00479] [00863]")
    t00880 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Prima de emisión [00480] [00880]")
    t00897 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Reservas [00481] [00897]")
    t00914 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Acciones y participaciones en patrimonio propias  [00482] [00914]")
    t00931 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Resultados ejercicios anteriores [00483] [00931]")
    t00948 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Otras aportaciones de socios [00484] [00948]")
    t00965 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Capital - Escriturado [00492] [00965]")
    t00982 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Capital - No exigido [00493] [00982]")
    t00999 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Prima de emisión [00494] [00999]")
    t01016 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Reservas [00495] [01016]")
    t01033 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Acciones y participaciones en patrimonio propias  [00496] [01033]")
    t01050 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Resultados ejercicios anteriores [00497] [01050]")
    t01067 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Otras aportaciones de socios [00498] [01067]")
    t01084 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Capital - Escriturado [00506] [01084]")
    t01101 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Capital - No exigido [00507] [01101]")
    t01118 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Prima de emisión [00508] [01118]")
    t01135 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Reservas [00509] [01135]")
    t01152 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Acciones y participaciones en patrimonio propias [00510] [01152]")
    t01169 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Resultados ejercicios anteriores [00511] [01169]")
    t01186 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras aportaciones de socios [00512] [01186]")
    t01203 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Aumentos de capital - Capital - Escriturado [00520] [01203]")
    t01220 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Aumentos de capital - Capital - No exigido [00521] [01220]")
    t01237 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Aumentos de capital - Prima de emisión [00522] [01237]")
    t01254 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Aumentos de capital - Reservas [00523] [01254]")
    t01271 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Aumentos de capital - Acciones y participaciones en patrimonio propias  [00524] [01271]")
    t01288 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Aumentos de capital - Resultados ejercicios anteriores [00525] [01288]")
    t01305 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Aumentos de capital - Otras aportaciones de socios [00526] [01305]")
    t01322 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Reducciones de capital - Capital - Escriturado [00534] [01322]")
    t01339 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Reducciones de capital - Capital - No exigido [00535] [01339]")
    t01356 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Reducciones de capital - Prima de emisión [00536] [01356]")
    t01373 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Reducciones de capital - Reservas [00537] [01373]")
    t01390 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Reducciones de capital - Acciones y participaciones en patrimonio propias  [00538] [01390]")
    t01407 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Reducciones de capital - Resultados ejercicios anteriores [00539] [01407]")
    t01424 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Reducciones de capital - Otras aportaciones de socios [00540] [01424]")
    t01441 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Capital - Escriturado [00548] [01441]")
    t01458 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Capital - No exigido [00549] [01458]")
    t01475 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Prima de emisión [00550] [01475]")
    t01492 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Reservas [00551] [01492]")
    t01509 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Acciones y participaciones en patrimonio propias [00552] [01509]")
    t01526 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Resultados ejercicios anteriores [00553] [01526]")
    t01543 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Otras aportaciones de socios [00554] [01543]")
    t01560 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Distribución de dividendos - Capital - Escriturado [00562] [01560]")
    t01577 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Distribución de dividendos - Capital - No exigido [00563] [01577]")
    t01594 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Distribución de dividendos - Prima de emisión [00564] [01594]")
    t01611 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Distribución de dividendos - Reservas [00565] [01611]")
    t01628 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Distribución de dividendos - Acciones y participaciones en patrimonio propias  [00566] [01628]")
    t01645 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Distribución de dividendos - Resultados ejercicios anteriores [00567] [01645]")
    t01662 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - (-) Distribución de dividendos - Otras aportaciones de socios [00568] [01662]")
    t01679 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Capital - Escriturado [00576] [01679]")
    t01696 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Capital - No exigido [00577] [01696]")
    t01713 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Prima de emisión [00578] [01713]")
    t01730 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Reservas [00579] [01730]")
    t01747 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Acciones y participaciones en patrimonio propias [00580] [01747]")
    t01764 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Resultados ejercicios anteriores [00581] [01764]")
    t01781 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Otras aportaciones de socios [00582] [01781]")
    t01798 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Capital  - Escriturado [00590] [01798]")
    t01815 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Capital  - No exigido [00591] [01815]")
    t01832 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Prima de emisión [00592] [01832]")
    t01849 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Reservas [00593] [01849]")
    t01866 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Acciones y participaciones en patrimonio propias [00594] [01866]")
    t01883 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Resultados ejercicios anteriores [00595] [01883]")
    t01900 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Otras aportaciones de socios [00596] [01900]")
    t01917 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Capital -  Escriturado [00604] [01917]")
    t01934 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Capital - No exigido [00605] [01934]")
    t01951 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Prima de emisión [00606] [01951]")
    t01968 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Reservas [00607] [01968]")
    t01985 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Acciones y participaciones en patrimonio propias [00608] [01985]")
    t02002 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Resultados ejercicios anteriores [00609] [02002]")
    t02019 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Otras aportaciones de socios [00610] [02019]")
    t02036 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Capital - Escriturado [00618] [02036]")
    t02053 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Capital - No exigido [00619] [02053]")
    t02070 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Prima de emisión [00620] [02070]")
    t02087 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Reservas [00621] [02087]")
    t02104 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Acciones y participaciones en patrimonio propias [00622] [02104]")
    t02121 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Resultados ejercicios anteriores [00623] [02121]")
    t02138 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras aportaciones de socios [00624] [02138]")
    t02155 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Capital - Escriturado [00715] [02155]")
    t02172 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Movimiento reserva revalorización -  Capital - No exigido [00716] [02172]")
    t02189 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Prima de emisión [00717] [02189]")
    t02206 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Movimiento reserva revalorización -  Reservas [00718] [02206]")
    t02223 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Acciones y participaciones en patrimonio propias [00719] [02223]")
    t02240 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Resultados ejercicios anteriores [00720] [02240]")
    t02257 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Otras aportaciones de socios [00721] [02257]")
    t02274 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras variaciones - Capital - Escriturado [00729] [02274]")
    t02291 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras variaciones -  Capital - No exigido [00730] [02291]")
    t02308 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras variaciones - Prima de emisión [00731] [02308]")
    t02325 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras variaciones -  Reservas [00732] [02325]")
    t02342 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras variaciones - Acciones y participaciones en patrimonio propias  [00733] [02342]")
    t02359 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras variaciones - Resultados ejercicios anteriores [00734] [02359]")
    t02376 = fields.Integer(string="Estado de cambios patrimonio neto (II) - Otras variaciones del patrimonio neto - Otras variaciones - Otras aportaciones de socios [00735] [02376]")
    t02393 = fields.Float(string="Estado de cambios patrimonio neto (II) - SALDO, FINAL DEL EJERCICIO - Capital - Escriturado [00632] [02393]")
    t02410 = fields.Float(string="Estado de cambios patrimonio neto (II) - SALDO, FINAL DEL EJERCICIO - Capital - No exigido [00633] [02410]")
    t02427 = fields.Float(string="Estado de cambios patrimonio neto (II) - SALDO, FINAL DEL EJERCICIO - Prima de emisión [00634] [02427]")
    t02444 = fields.Float(string="Estado de cambios patrimonio neto (II) - SALDO, FINAL DEL EJERCICIO - Reservas [00635] [02444]")
    t02461 = fields.Float(string="Estado de cambios patrimonio neto (II) - SALDO, FINAL DEL EJERCICIO - Acciones y participaciones en patrimonio propias [00636] [02461]")
    t02478 = fields.Float(string="Estado de cambios patrimonio neto (II) - SALDO, FINAL DEL EJERCICIO - Resultados ejercicios  anteriores [00637] [02478]")
    t02495 = fields.Float(string="Estado de cambios patrimonio neto (II) - SALDO, FINAL DEL EJERCICIO - Otras aportaciones de socios [00638] [02495]")
    t02512 = fields.Integer(string="RESERVADO PARA LA AEAT [02512]")
    t02712 = fields.Char(string="Identificador de fin de registro [02712]")

    _name = 'modelo200.declaration'
    _description = "Declaración IS - Modelo 200"

    company_id = fields.Many2one('res.company', string="Empresa", required=True, default=lambda self: self.env.company)
    fiscal_year = fields.Char(string="Ejercicio", required=True, default=lambda self: str(fields.Date.today().year - 1))
    date_start = fields.Date(string="Inicio Ejercicio")
    date_end = fields.Date(string="Fin Ejercicio")
    state = fields.Selection([('draft', 'Borrador'), ('generated', 'Generado')], default='draft')

    bs_assets_total = fields.Float(string="Total Activo")
    bs_equity_liabs_total = fields.Float(string="Total PN y Pasivo")
    pl_net_turnover = fields.Float(string="Importe Neto Cifra Negocios")
    pl_profit_before_tax = fields.Float(string="Resultado Antes Impuestos")
    pl_profit_after_tax = fields.Float(string="Resultado del Ejercicio")
    equity_start = fields.Float(string="PN Inicial")
    equity_end = fields.Float(string="PN Final")
# Suma los movimientos contables de las cuentas cuyo código comience con los prefijos indicados
# Esta función filtra las líneas del diario dentro del ejercicio fiscal y compañía actual

    # Función interna para obtener el saldo de todas las cuentas contables cuyo código empieza por determinados prefijos
    # Usa dominios de búsqueda de Odoo sobre 'account.move.line' para filtrar los apuntes contables
    def _sum_accounts(self, account_prefixes):
        domain = [
            ('date', '>=', self.date_start),
            ('date', '<=', self.date_end),
            ('company_id', '=', self.company_id.id),
            ('move_id.state', '=', 'posted')
        ]
        prefix_domain = [('account_id.code', '=like', f'{p}%') for p in account_prefixes]
        lines = self.env['account.move.line'].search(domain + ['|'] * (len(prefix_domain) - 1) + prefix_domain)
        return sum(line.debit - line.credit for line in lines)

# Calcula automáticamente los valores contables clave para el Modelo 200 a partir de los apuntes contables

        # Calcula automáticamente los datos contables relevantes para el Modelo 200
        # Esta función se ejecuta antes de generar el XML para asegurar que los valores estén actualizados
    def compute_financials(self):
        for rec in self:
            year = int(rec.fiscal_year)
            rec.date_start = date(year, 1, 1)
            rec.date_end = date(year, 12, 31)
            rec.bs_assets_total = rec._sum_accounts(['2', '3', '4', '5'])
            rec.bs_equity_liabs_total = rec._sum_accounts(['1', '5'])
            rec.pl_net_turnover = rec._sum_accounts(['70']) - rec._sum_accounts(['706']) + rec._sum_accounts(['705'])
            ingresos = rec._sum_accounts(['7'])
            gastos = rec._sum_accounts(['6'])
            rec.pl_profit_before_tax = ingresos - gastos
            resultado = rec._sum_accounts(['129'])
            impuesto = rec._sum_accounts(['630'])
            rec.pl_profit_after_tax = resultado if resultado else rec.pl_profit_before_tax - impuesto
            rec.equity_end = rec._sum_accounts(['1'])
            opening_lines = self.env['account.move.line'].search([
                ('date', '<', rec.date_start),
                ('account_id.code', '=like', '1%'),
                ('company_id', '=', rec.company_id.id),
                ('move_id.state', '=', 'posted')
            ])
            rec.equity_start = sum(line.debit - line.credit for line in opening_lines)

# Genera el archivo XML de la declaración con los datos calculados
# Este archivo puede ser importado en la sede electrónica de la AEAT

    # Función principal para generar el archivo XML del Modelo 200
    # Llama a compute_financials(), genera una cadena XML y la guarda como archivo adjunto binario

from ..utils.estructura_xml_fija import estructura_xml_fija
import xml.etree.ElementTree as ET
import base64
import logging
_logger = logging.getLogger(__name__)

class Modelo200Declaration(models.Model):
    _inherit = 'modelo200.declaration'

    xml_file = fields.Binary("Archivo XML", readonly=True)
    xml_filename = fields.Char("Nombre del archivo XML")

    def action_generate_xml(self):
        self.ensure_one()
        root = ET.Element("Modelo200")

        for tipo_pagina, campos in estructura_xml_fija.items():
            nodo_pagina = ET.SubElement(root, tipo_pagina)
            for etiqueta in campos:
                campo_odoo = "t" + etiqueta[1:]
                valor = getattr(self, campo_odoo, '')
                if valor in [False, None]:
                    valor = ''
                nodo = ET.SubElement(nodo_pagina, etiqueta)
                nodo.text = str(valor)
                _logger.info(f"Campo {campo_odoo}: {valor}")

        xml_bytes = ET.tostring(root, encoding="utf-8", method="xml")
        self.xml_file = base64.b64encode(xml_bytes)
        self.xml_filename = "modelo200.xml"

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content?model={self._name}&id={self.id}&field=xml_file&download=true&filename={self.xml_filename}",
            "target": "self",
        }