# Publicación y privacidad

Este repositorio se inició desde una distribución limpia, con un historial nuevo. No incorpora el historial de la copia de trabajo anterior ni sus documentos personales.

## Antes de subir cambios

```sh
python tools/check_publication.py
python tools/security_guards.py
git diff
git diff --cached
```

Revisá los archivos nuevos y los cambios antes de crear un commit. No publiques currículums reales, perfiles personales, credenciales ni resultados privados. `.gitignore` no protege archivos que Git ya sigue.

Usá una copia privada para personalizar el perfil mediante `/setup`. Conservá los ejemplos públicos vacíos. Si se agrega información personal a un commit, borrar el archivo en un commit posterior no elimina esa información del historial.

La comprobación automática detecta algunos patrones y plantillas personalizadas; no identifica todos los datos personales posibles. Revisá también la identidad de autor de Git y usá el correo privado de GitHub si no querés publicar tu correo personal.

Se conserva la licencia MIT y la atribución del proyecto original. La documentación principal está en español; parte de las instrucciones técnicas heredadas permanece en inglés.
