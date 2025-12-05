El proyecto inicial de Flask presentaba problemas fundamentales de diseño que lo hacían frágil y difícil de mantener. La refactorización se centró en aplicar los principios SOLID y patrones arquitectónicos probados para aislar responsabilidades y reducir el acoplamiento.

1. Desacoplamiento de Capas (SOLID: SRP, OCP, DIP)
El cambio más importante fue la separación de responsabilidades para crear una arquitectura de tres capas:

Capa Antigua -> Capa Nueva -> Principio Aplicado

Controlador Monolítico (Resource) -> Capa de Endpoints (Controlador): Solo maneja peticiones HTTP, validación de reqparse y llama al Repositorio. -> SRP (Single Responsibility)

DatabaseConnection (Objeto Dios) -> Capa de Repositorios: Encapsula la lógica de negocio y la integridad de datos (ej. generación segura de IDs, filtros). -> SRP y OCP

Lógica de Datos Hardcodeada -> Capa de Persistencia (JsonDatabase): Clase genérica que solo sabe leer y escribir un archivo JSON. No conoce entidades (productos, categorías). -> DIP (Dependency Inversion)

Resultado: Se logró una Inyección de Dependencias efectiva, donde los Endpoints dependen de la abstracción del Repositorio, haciendo que cambiar la base de datos (de JSON a una SQL) solo requiera modificar la capa de Repositorios.


2. Centralización y Eliminación de Repetición (DRY)
El código original repetía la lógica de autenticación en cada método HTTP (get, post, delete) de cada recurso.

Solución: Se implementó el patrón Decorator de Python (@token_required) en un nuevo módulo (utils/security.py).

Principio: DRY (Don't Repeat Yourself).

Resultado: El código de autenticación se eliminó de los Endpoints, centralizando la seguridad en un único punto.

3. Corrección de Integridad de Datos
La generación de IDs estaba rota (len(lista) + 1), causando duplicación de IDs al eliminar elementos.

Solución: La lógica de generación de IDs se movió y se corrigió dentro de la capa de Repositorios, usando max(id) + 1 para asegurar que cada nueva entidad tenga un identificador único y secuencial.

En resumen, la refactorización transformó un código altamente acoplado y repetitivo en una arquitectura limpia, estructurada y profesional, siguiendo estándares de la ingeniería de software moderna.