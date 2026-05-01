# Proyecto UADER-PI-B 230/24 DoE-VC

## Simulador de deuda técnica extendido con Monte Carlo, optimización y persistencia

El sistema debe permitir simular sprint a sprint la evolución de:

$$B_k, D_k, V_k, u_k, N_k, R_k, \nu_k$$

donde:

-   $B_k$: backlog funcional remanente.

-   $D_k$: deuda técnica remanente.

-   $V_k$: velocidad efectiva del sprint.

-   $u_k$: fracción del sprint dedicada a remediación.

-   $N_k$: funcionalidad nueva entregada.

-   $R_k$: deuda remediada.

-   $\nu_k$: valor económico generado.

# Épicas del backlog

## Épica A --- Núcleo determinístico del modelo

Implementar el modelo básico de evolución sprint a sprint.

## Épica B --- Políticas de decisión

Implementar distintas estrategias para seleccionar $u_k$.

## Épica C --- Simulación Monte Carlo

Ejecutar múltiples corridas variando parámetros.

## Épica D --- Optimización

Calcular $u_k$ *óptimo* bajo restricciones.

## Épica E --- Persistencia y reproducibilidad

Guardar escenarios, parámetros, corridas y resultados.

## Épica F --- Visualización y reporting

Generar CSV, gráficos y reportes comparativos.

# Backlog Scrum propuesto

## Épica A --- Núcleo determinístico

### Historia A1 --- Crear estructura de parámetros del modelo

**Complejidad:** baja.

**Como** investigador, **quiero** definir los parámetros principales del
modelo en una estructura Python, **para** ejecutar simulaciones
reproducibles.

#### Criterios de aceptación

-   Existe una clase `ModelParameters`.

-   Incluye al menos: `B0`, `D0`, `V0`, `alpha`, `beta`, `gamma`,
    `theta`, `lambda_`, `rho`, `K`.

-   Valida valores negativos no permitidos.

-   Puede imprimirse o serializarse.

**Riesgo de integración:** bajo.

### Historia A2 --- Calcular velocidad efectiva $V_k$

**Complejidad:** baja.

**Como** investigador, **quiero** calcular la velocidad efectiva
afectada por deuda, **para** modelar pérdida de productividad.

Ejemplo:

$$V_k = \frac{V_0}{1+\gamma D_k}$$

#### Criterios de aceptación

-   Dado $D_k=0$, se obtiene $V_k=V_0$.

-   Si $D_k$ aumenta, $V_k$ disminuye.

-   Hay tests unitarios.

**Riesgo de integración:** bajo.

### Historia A3 --- Simular un sprint con $u_k$ fijo

**Complejidad:** baja-media.

**Como** investigador, **quiero** calcular el estado $k+1$ a partir de
$B_k,D_k,u_k$, **para** construir trayectorias de evolución.

Variables básicas:

$$R_k = u_k V_k$$

$$N_k = (1-u_k)V_k$$

$$B_{k+1} = \max(0, B_k - N_k)$$

$$D_{k+1} = \max(0, D_k - R_k + \alpha N_k + \beta R_k)$$

#### Criterios de aceptación

-   $0 \leq u_k \leq 1$.

-   $B_k$ nunca queda negativo.

-   $D_k$ nunca queda negativo.

-   Se devuelve un objeto `SprintState`.

**Riesgo de integración:** medio, porque define el contrato central del
simulador.

### Historia A4 --- Simular varios sprints determinísticos

**Complejidad:** media.

**Como** investigador, **quiero** ejecutar una simulación de $K$
sprints, **para** observar la evolución del sistema.

#### Criterios de aceptación

-   Se genera una tabla con una fila por sprint.

-   Incluye $B_k,D_k,V_k,u_k,N_k,R_k$.

-   La simulación se detiene si $B_k=0$ y $D_k=0$.

-   Hay tests de regresión simples.

**Riesgo de integración:** medio.

## Épica B --- Políticas de decisión

### Historia B1 --- Política naive "deuda primero"

**Complejidad:** baja.

**Como** investigador, **quiero** una política donde $u_k=1$ mientras
exista deuda, **para** usarla como baseline.

#### Criterios de aceptación

-   Si $D_k>0$, entonces $u_k=1$.

-   Si $D_k=0$, entonces $u_k=0$.

-   Se integra con el simulador de varios sprints.

**Riesgo de integración:** bajo.

### Historia B2 --- Política backlog primero

**Complejidad:** baja.

**Como** investigador, **quiero** una política donde $u_k=0$ mientras
exista backlog funcional, **para** comparar contra deuda primero.

#### Criterios de aceptación

-   Si $B_k>0$, entonces $u_k=0$.

-   Si $B_k=0$ y $D_k>0$, entonces $u_k=1$.

-   Se integra con el simulador.

**Riesgo de integración:** bajo.

### Historia B3 --- Política proporcional

**Complejidad:** media.

**Como** investigador, **quiero** definir $u_k$ proporcional a la deuda
relativa, **para** tener una política heurística intermedia.

Ejemplo:

$$u_k = \frac{D_k}{B_k+D_k}$$

#### Criterios de aceptación

-   $u_k=0$ si $D_k=0$.

-   $u_k=1$ si $B_k=0$ y $D_k>0$.

-   $u_k\in[0,1]$.

-   Maneja correctamente $B_k=D_k=0$.

**Riesgo de integración:** medio.

### Historia B4 --- Interfaz común de políticas

**Complejidad:** media.

**Como** desarrollador, **quiero** que todas las políticas implementen
una interfaz común, **para** poder intercambiarlas sin modificar el
motor de simulación.

#### Criterios de aceptación

-   Existe una interfaz `Policy`.

-   Cada política implementa `decide_u(state, params)`.

-   El motor no depende de clases concretas.

**Riesgo de integración:** alto, porque refactoriza historias previas.

## Épica C --- Simulación Monte Carlo

### Historia C1 --- Definir distribuciones uniformes de parámetros

**Complejidad:** media.

**Como** investigador, **quiero** definir parámetros aleatorios con
distribución uniforme, **para** explorar incertidumbre.

Ejemplo:

-   $s \sim U(1.0,1.4)$.

-   $\gamma \sim U(0.00,0.05)$.

-   $\theta \sim U(0,0.9)$.

-   $(1-\beta) \sim U(0.5,0.9)$.

-   $\lambda \sim U(0.2,1.0)$.

#### Criterios de aceptación

-   Se pueden fijar semillas aleatorias.

-   Se puede muestrear un conjunto completo de parámetros.

-   Hay tests con semilla fija.

**Riesgo de integración:** medio.

### Historia C2 --- Ejecutar $N$ simulaciones Monte Carlo

**Complejidad:** media.

**Como** investigador, **quiero** ejecutar muchas corridas, **para**
estimar distribuciones de resultados.

#### Criterios de aceptación

-   Permite configurar `n_runs`.

-   Devuelve resultados agregados.

-   Conserva los resultados individuales.

-   Usa una política seleccionable.

**Riesgo de integración:** alto, porque combina modelo, políticas y
parámetros aleatorios.

### Historia C3 --- Agregar métricas de salida

**Complejidad:** media.

**Como** investigador, **quiero** calcular métricas por corrida,
**para** comparar estrategias.

Métricas sugeridas:

-   Sprints hasta finalizar backlog.

-   Sprints hasta eliminar deuda.

-   Deuda final.

-   Valor acumulado descontado.

-   $u_k$ promedio.

-   Varianza de $u_k$.

-   Productividad efectiva promedio.

-   Defectos/inconsistencias detectadas.

#### Criterios de aceptación

-   Las métricas se calculan para cada corrida.

-   Se puede obtener media, desvío estándar y percentiles.

-   Se exportan a CSV.

**Riesgo de integración:** alto.

## Épica D --- Optimización

### Historia D1 --- Implementar búsqueda por grilla de $u_k$

**Complejidad:** media.

**Como** investigador, **quiero** evaluar muchos valores posibles de
$u_k$, **para** encontrar una decisión aproximadamente *óptima*.

Ejemplo:

$$u_k \in \{0.0,0.01,0.02,\dots,1.0\}$$

#### Criterios de aceptación

-   Evalúa una función objetivo.

-   Respeta $0 \leq u_k \leq 1$.

-   Devuelve el mejor $u_k$.

-   Maneja el caso $D_k=0 \Rightarrow u_k=0$.

**Riesgo de integración:** medio-alto.

### Historia D2 --- Definir función objetivo económica

**Complejidad:** alta.

**Como** investigador, **quiero** optimizar $u_k$ según una función
económica, **para** balancear entrega de valor y reducción de deuda.

Ejemplo conceptual:

$$J(u_k)=
\text{valor entregado}
+
\text{valor de capacidad futura}
-
\text{costo de demora}
-
\text{costo de deuda residual}$$

#### Criterios de aceptación

-   La función objetivo es configurable.

-   Usa $B_k,D_k,V_k,\lambda,\rho,\theta$.

-   Puede compararse contra políticas naive.

-   Hay tests de casos límite.

**Riesgo de integración:** alto.

### Historia D3 --- Política *óptima* local

**Complejidad:** alta.

**Como** investigador, **quiero** una política que calcule $u_k$
*óptimo* en cada sprint, **para** comparar decisiones *óptimas* contra
heurísticas.

#### Criterios de aceptación

-   Implementa la interfaz `Policy`.

-   Calcula $u_k$ usando búsqueda por grilla.

-   Respeta restricciones de frontera.

-   Se integra con Monte Carlo.

**Riesgo de integración:** muy alto.

### Historia D4 --- Comparación entre políticas

**Complejidad:** alta.

**Como** investigador, **quiero** ejecutar el mismo escenario con varias
políticas, **para** comparar resultados.

#### Criterios de aceptación

-   Ejecuta naive, backlog-first, proporcional y *óptima*.

-   Produce métricas comparables.

-   Exporta una tabla por política.

-   Genera gráficos comparativos.

**Riesgo de integración:** muy alto.

## Épica E --- Persistencia

### Historia E1 --- Guardar resultados en CSV

**Complejidad:** baja.

**Como** investigador, **quiero** guardar resultados en CSV, **para**
analizarlos externamente.

#### Criterios de aceptación

-   Exporta estados sprint a sprint.

-   Exporta métricas finales.

-   Los nombres de columnas son estables.

**Riesgo de integración:** bajo.

### Historia E2 --- Guardar escenarios en JSON

**Complejidad:** media.

**Como** investigador, **quiero** guardar parámetros y configuración
experimental en JSON, **para** repetir una corrida.

#### Criterios de aceptación

-   Guarda parámetros.

-   Guarda política usada.

-   Guarda semilla aleatoria.

-   Puede recargarse el escenario.

**Riesgo de integración:** medio.

### Historia E3 --- Reproducibilidad completa

**Complejidad:** alta.

**Como** investigador, **quiero** reproducir una corrida completa desde
archivo, **para** validar resultados experimentales.

#### Criterios de aceptación

-   Un archivo JSON permite relanzar una simulación.

-   Con la misma semilla produce los mismos resultados.

-   Registra versión del modelo.

-   Registra fecha/hora de ejecución.

**Riesgo de integración:** alto.

## Épica F --- Visualización

### Historia F1 --- Graficar evolución de $B_k$ y $D_k$

**Complejidad:** baja.

**Como** investigador, **quiero** visualizar backlog y deuda por sprint,
**para** interpretar trayectorias.

#### Criterios de aceptación

-   Genera PNG.

-   Muestra $B_k$ y $D_k$.

-   Permite elegir corrida o promedio.

**Riesgo de integración:** bajo.

### Historia F2 --- Boxplot de $u_k$ *óptimo*

**Complejidad:** media.

**Como** investigador, **quiero** visualizar la distribución de $u_k$,
**para** observar variabilidad bajo incertidumbre.

#### Criterios de aceptación

-   Genera boxplot.

-   Agrupa por escenario.

-   Exporta PNG.

**Riesgo de integración:** medio.

### Historia F3 --- Heatmap de sensibilidad

**Complejidad:** alta.

**Como** investigador, **quiero** generar heatmaps variando dos
parámetros, **para** observar regiones de decisión.

Ejemplo:

-   Eje X: $B_k/(M s)$.

-   Eje Y: $D_k/B_k$.

-   Color: $u_k$ *óptimo* promedio.

#### Criterios de aceptación

-   Permite elegir dos parámetros de barrido.

-   Calcula promedio de $u_k$.

-   Exporta imagen y CSV.

-   Integra Monte Carlo + optimización.

**Riesgo de integración:** muy alto.

# Backlog resumido por complejidad

## Historias bajas

  **ID**   **Historia**
  -------- --------------------------
  A1       Parámetros del modelo
  A2       Velocidad efectiva
  B1       Política deuda primero
  B2       Política backlog primero
  E1       Exportar CSV
  F1       Gráfico $B_k,D_k$

## Historias medias

  **ID**   **Historia**
  -------- -----------------------------
  A3       Simular un sprint
  A4       Simular varios sprints
  B3       Política proporcional
  B4       Interfaz común de políticas
  C1       Distribuciones uniformes
  C2       Corridas Monte Carlo
  C3       Métricas
  D1       Búsqueda por grilla
  E2       Escenarios JSON
  F2       Boxplots

## Historias altas

  **ID**   **Historia**
  -------- ----------------------------
  D2       Función objetivo económica
  D3       Política *óptima* local
  D4       Comparación de políticas
  E3       Reproducibilidad completa
  F3       Heatmap de sensibilidad

# Orden sugerido de integración

Para generar problemas de interacción medibles, no conviene integrar
todo linealmente. Conviene usar secuencias alternativas.

## Secuencia base

1.  A1 --- Parámetros.

2.  A2 --- Velocidad.

3.  A3 --- Un sprint.

4.  A4 --- Simulación determinística.

5.  B1 --- Deuda primero.

6.  B2 --- Backlog primero.

7.  B3 --- Proporcional.

8.  B4 --- Interfaz común.

9.  C1 --- Distribuciones.

10. C2 --- Monte Carlo.

11. C3 --- Métricas.

12. D1 --- Grilla.

13. D2 --- Función objetivo.

14. D3 --- Política *óptima*.

15. D4 --- Comparación.

16. E1/E2/E3 --- Persistencia.

17. F1/F2/F3 --- Visualización.

## Secuencia alternativa para inducir fricción

1.  A1.

2.  A2.

3.  B1.

4.  B2.

5.  E1.

6.  A3.

7.  A4.

8.  C1.

9.  F1.

10. B4.

11. C2.

12. C3.

13. D1.

14. D2.

15. D3.

16. F2.

17. F3.

18. E3.

Esta segunda secuencia fuerza refactorizaciones porque introduce
políticas y exportación antes de consolidar el motor.

# Diseño de Experimentos factorial

## Objetivo del DoE

Medir cómo distintas condiciones de desarrollo afectan:

-   Productividad.

-   Defectos funcionales.

-   Defectos de integración.

-   Retrabajo.

-   Estabilidad del código.

-   Dificultad de integración entre historias.

-   Calidad del resultado generado por Vibe Coding.

# Factores experimentales

## Factor A --- Complejidad de historia

  **Nivel**   **Descripción**
  ----------- -----------------
  A1          Baja
  A2          Media
  A3          Alta

## Factor B --- Tipo de acoplamiento dominante

  **Nivel**   **Descripción**
  ----------- -------------------------
  B1          Acoplamiento de datos
  B2          Acoplamiento de control
  B3          Acoplamiento temporal
  B4          Acoplamiento matemático

Ejemplos:

-   Datos: CSV, JSON, estructuras compartidas.

-   Control: políticas que modifican el flujo.

-   Temporal: Monte Carlo, semillas, orden de ejecución.

-   Matemático: función objetivo, optimización, restricciones.

## Factor C --- Orden de integración

  **Nivel**   **Descripción**
  ----------- -----------------------------------
  C1          Orden incremental natural
  C2          Orden con refactorización forzada
  C3          Orden aleatorizado controlado

## Factor D --- Modalidad de desarrollo

  **Nivel**   **Descripción**
  ----------- ---------------------------------------
  D1          Programación manual tradicional
  D2          Vibe Coding con prompts simples
  D3          Vibe Coding con prompts estructurados
  D4          Vibe Coding con tests previos

## Factor E --- Nivel de especificación

  **Nivel**   **Descripción**
  ----------- ----------------------------------------
  E1          Historia breve
  E2          Historia + criterios de aceptación
  E3          Historia + criterios + tests esperados
  E4          Historia + contrato de interfaces

# Diseño factorial mínimo recomendado

Un factorial completo sería demasiado grande:

$$3 \times 4 \times 3 \times 4 \times 4 = 576$$

Eso es excesivo. Se recomienda un diseño fraccional o por bloques.

## Diseño inicial recomendado

Usar estos factores principales:

  **Factor**                **Niveles**
  ------------------------- --------------------------------------------------------
  Complejidad               baja, media, alta
  Modalidad                 manual, vibe simple, vibe estructurado, vibe con tests
  Nivel de especificación   breve, criterios, tests, contrato

Total:

$$3 \times 4 \times 4 = 48$$

Con 2 repeticiones:

$$48 \times 2 = 96 \text{ ejecuciones}$$

# Variables dependientes

## Productividad

  **Métrica**                             **Descripción**
  --------------------------------------- ----------------------
  Tiempo de implementación                Minutos por historia
  Tiempo hasta primer código ejecutable   Minutos
  Tiempo hasta pasar tests                Minutos
  Cantidad de iteraciones de prompt       Número

## Calidad

  **Métrica**               **Descripción**
  ------------------------- -----------------------------------------
  Defectos unitarios        Errores dentro de una historia
  Defectos de integración   Errores al combinar historias
  Defectos matemáticos      Inconsistencias del modelo
  Defectos de borde         Errores con $B_k=0$, $D_k=0$, $u_k=0/1$

## Mantenibilidad

  **Métrica**                                       **Descripción**
  ------------------------------------------------- ----------------------------------------
  Complejidad ciclomática                           Complejidad estructural del código
  Duplicación                                       Repetición de fragmentos o estructuras
  Tamaño de archivos                                Longitud y distribución del código
  Cantidad de refactorizaciones                     Cambios estructurales necesarios
  Cambios necesarios para integrar nueva historia   Medida de esfuerzo de integración

## Robustez

  **Métrica**                         **Descripción**
  ----------------------------------- -------------------------------------------
  Tests pasados                       Proporción o cantidad de pruebas exitosas
  Cobertura                           Cobertura de tests
  Fallos ante valores extremos        Robustez frente a condiciones de borde
  Reproducibilidad con semilla fija   Capacidad de repetir resultados

# Hipótesis experimentales

## H1 --- Productividad

El Vibe Coding con prompts estructurados reduce el tiempo de
implementación frente a programación manual.

## H2 --- Calidad

El Vibe Coding con tests previos reduce defectos de integración frente a
Vibe Coding con prompts simples.

## H3 --- Complejidad

La ventaja de productividad del Vibe Coding disminuye en historias de
alta complejidad matemática.

## H4 --- Especificación

Las historias con contrato de interfaces producen menos defectos de
integración que las historias breves.

## H5 --- Interacción

Existe interacción entre modalidad de desarrollo y nivel de
especificación:

$$\text{Vibe Coding simple} + \text{historia breve}$$

producirá más errores que:

$$\text{Vibe Coding estructurado} + \text{contrato de interfaces}$$

# Modelo estadístico sugerido

Para analizar resultados:

$$Y =
\mu
+ A_i
+ D_j
+ E_k
+ (A D)_{ij}
+ (A E)_{ik}
+ (D E)_{jk}
+ \varepsilon$$

donde:

-   $Y$: métrica observada.

-   $A_i$: efecto de complejidad.

-   $D_j$: efecto de modalidad de desarrollo.

-   $E_k$: efecto de nivel de especificación.

-   $(AD)$, $(AE)$, $(DE)$: interacciones.

-   $\varepsilon$: error experimental.

Métricas posibles para $Y$:

-   Tiempo de implementación.

-   Número de defectos.

-   Defectos de integración.

-   Número de prompts.

-   Cobertura alcanzada.

-   Esfuerzo de retrabajo.

# Unidad experimental

La unidad experimental recomendada es:

> Una historia implementada bajo una combinación concreta de
> complejidad, modalidad de desarrollo y nivel de especificación.

Ejemplo:

  **Historia**   **Complejidad**   **Modalidad**    **Especificación**
  -------------- ----------------- ---------------- ------------------------
  D3             Alta              Vibe con tests   Contrato de interfaces

# Resultado esperado del experimento

El estudio debería permitir responder:

1.  Vibe Coding acelera la implementación?

2.  Dónde introduce defectos?

3.  Qué historias son más riesgosas?

4.  Qué nivel de especificación reduce errores?

5.  Cuándo aparecen problemas de integración?

6.  La generación asistida funciona mejor con tests previos?

7.  Qué tipo de acoplamiento degrada más la productividad?

# Recomendación final

Para la investigación, este backlog debe usarse como instrumento
experimental y no solo como especificación funcional.

La combinación más valiosa sería:

$$\text{Complejidad}
\times
\text{Modalidad de desarrollo}
\times
\text{Nivel de especificaci\'on}$$

con foco especial en medir:

$$\text{defectos de integraci\'on}$$

porque ahí es donde probablemente aparezca la señal más interesante del
experimento.
