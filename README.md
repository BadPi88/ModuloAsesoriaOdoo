## Descripción
Módulo desarrollado para Odoo 16 que permite la gestión de modelos fiscales y trámites administrativos para asesorías, autónomos y pequeñas empresas. El objetivo principal es organizar los trámites fiscales y permitir, en el futuro, la conexión directa con la Agencia Tributaria para la presentación telemática de modelos.

## Funcionalidades implementadas
- Generación del Modelo 200 con estructura completa desde la página 3 a la 10, siguiendo el esquema de la AEAT.
- Autorrelleno de campos del Balance (activo, pasivo y patrimonio neto) utilizando datos contables desde el plan de cuentas.
- Lógica contable específica para cada campo, vinculando códigos como 100000 (Capital social), 430000 (Clientes), 572001 (Banco), etc.
- Botón de cálculo para volcar datos contables en el formulario.
- Exportación en formato XML con etiquetas adaptadas al esquema de Hacienda.
- Interfaz estructurada por secciones según el formato del Modelo 200 oficial.
- Preparación de ejemplos de asientos contables para comprobar el correcto funcionamiento del cálculo automático.

## Tecnologías utilizadas
- Odoo 16
- Python
- PostgreSQL
- XML

## Estado del proyecto
**Versión 1.0** – Funcionalidades principales implementadas y operativas. Pendiente de mejoras en automatización de campos para medianas y grandes empresas.

## Autor
**Miguel Martin**  
2º DAM - Curso 2024/2025
