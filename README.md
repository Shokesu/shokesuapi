
# ¿Qué es Shokesu?
Shokesu es una plataforma online para analizar las redes sociales como Twitter, Facebook, Youtube, Instagram, ...
Aplicación de Shokesu: https://app.shokesu.com/

# ¿Qué es shokesuapi?
shokesuapi es una pequeña librería implementada en python, capaz de extraer datos de la plataforma Shokesu haciendo peticiones HTTP.
Para usarla necesitarás el access token de una cuenta registrada en la aplicación.

El siguiente ejemplo muestra como obtener las publicaciones de un proyecto creado en Shokesu.
```
from api import API

shokesu = API(access_token = '{you ACCESS token here}')
posts = api.get_proyect_posts(site = '7046d09b-1050-4ca1-8a88-4a49cb91ea6d')

for post in posts:
    print(post.provider, post.body)
```

Para aprender a usar todas las funcionalidades de la librería, puedes ver más [ejemplos](tests/)
