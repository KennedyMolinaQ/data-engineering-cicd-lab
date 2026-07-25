# Configuración de Git

## Identidad

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

## Estrategia de ramas (Git Flow)

```bash
# Rama de integración
git checkout -b develop

# Trabajo en una feature
git checkout -b feature/nombre-descriptivo

# Al terminar: push y abrir Pull Request hacia develop
git push -u origin feature/nombre-descriptivo
```

Ver la estrategia completa en
[`../01-project-documentation/adr/0001-estrategia-de-ramas.md`](../01-project-documentation/adr/0001-estrategia-de-ramas.md).

## Recomendado

```bash
git config --global pull.rebase true      # historial lineal
git config --global init.defaultBranch main
```
