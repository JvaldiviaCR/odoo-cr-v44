# Plan de migración Odoo 18 + Hacienda v4.4

## Estado actual verificado

- Repositorio base: `odoocr/l10n_cr`
- Rama local actual: `main`
- Versión detectada en el módulo principal: `15.0.1.0.0`
- El repositorio no está aún preparado para Odoo 18; requiere una migración real de compatibilidad antes de tocar requisitos fiscales.

## Objetivo

Actualizar la base de módulos de facturación electrónica costarricense para Odoo 18 y dejarla compatible con Hacienda v4.4, manteniendo la lógica fiscal y reduciendo riesgo de regresión.

## Fase 1: Auditoría y portabilidad del core

### Tareas

- Revisar cada `__manifest__.py` y ajustar versión objetivo para Odoo 18.
- Eliminar dependencias obsoletas o duplicadas con la localización nativa.
- Revisar compatibilidad de vistas XML con la sintaxis moderna de Odoo 18.
- Cambiar `attrs` / `states` a expresiones inline `invisible`, `readonly`, `required`.
- Revisar API de modelos y campos que hayan cambiado entre Odoo 15 y 18.
- Validar el arranque del módulo con `odoo-bin` sin `ParseError`.

### Criterio de éxito

- Arranque limpio del repo con `--stop-after-init`.
- Cero `ParseError`.
- Cero advertencias de compatibilidad relevantes.

## Fase 2: Actualización fiscal v4.3 -> v4.4

### Tareas

- Analizar XSD v4.4 y mapear campos nuevos.
- Revisar `CodigoActividad`, `ProveedorSistemas` y nuevos medios de pago `06` y `07`.
- Ajustar totalizadores y descuentos por línea.
- Validar redondeos a 5 decimales por Hacienda.
- Corregir cálculos de exoneración y totales.

### Criterio de éxito

- XML generado validado con `lxml.etree.XMLSchema`.
- Sin diferencias de suma que violen la regla fiscal.

## Fase 3: Nuevos comprobantes y reglas vigentes

### Tareas

- Soportar REP (`Recibo Electrónico de Pago`) y casos de crédito.
- Actualizar parser `MensajeReceptor` con campos nuevos.
- Revisar firma digital y namespaces de v4.4.
- Validar autenticación OAuth2 y polling con Hacienda.

## Fase 4: Pruebas y salida a Sandbox

### Tareas

- Crear pruebas unitarias y de validación en `tests/`.
- Probar facturas y comprobantes por tipo.
- Certificar en Sandbox antes de producción.
- Solamente proceder a producción con aprobación explícita del responsable.

## Orden recomendado de ejecución

1. Fase 1: compatibilidad Odoo 18
2. Fase 2: XML y validación fiscal v4.4
3. Fase 3: REP y firma/autenticación
4. Fase 4: tests + sandbox + aprobación

## Riesgos principales

- Cambios de API de Odoo 18 no detectados.
- XML rechazado por Hacienda por suma o redondeo.
- Firma digital con namespaces incorrectos.
- Comprobantes nuevos no cubiertos por validación.

## Primera tarea concreta a ejecutar

- Revisar y corregir los manifests del módulo principal para preparar la base Odoo 18.
- Luego validar arranque y seguir con la migración de vistas XML y modelos.

## Registro de ejecución

- Fecha de base: 2026-11-11
- Estado: inicio del plan de migración documentado y verificado.
