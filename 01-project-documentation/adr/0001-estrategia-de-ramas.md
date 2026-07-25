# ADR 0001 · Estrategia de ramas

- **Estado**: Aceptada
- **Fecha**: 2026-07-25

## Contexto

El laboratorio debe demostrar un flujo profesional con separación clara entre
desarrollo y producción, y mapear ese flujo a los entornos de despliegue.

## Decisión

Usar **Git Flow simplificado** con dos ramas de larga vida:

- `develop` — integración; despliega al target `dev` del bundle.
- `main` — releases estables; despliega al target `prod`.
- `feature/*` — trabajo en curso; se integra vía Pull Request a `develop`.

Reglas de protección: PR obligatorio, checks en verde y al menos una revisión en
`develop` y `main`. Prohibido push directo a `main`.

## Alternativas consideradas

- **Trunk Based Development**: ideal con despliegue continuo maduro y feature flags.
  Se descarta por ahora porque Git Flow enseña mejor la separación dev→prod y mapea
  1:1 con los dos targets del bundle. El roadmap contempla migrar a TBD en un nivel
  avanzado.

## Consecuencias

- (+) Flujo claro y didáctico; mapeo directo a entornos.
- (+) Puntos de control naturales (PR, merge a main).
- (−) Algo más de ceremonia que TBD; ramas de larga vida a sincronizar.
