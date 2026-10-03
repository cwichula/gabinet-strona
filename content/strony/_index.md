---
# Sekcja-kontener na podstrony. Sama nie ma strony w sieci (render: never),
# ale jej strony sa dostepne dla szablonow (list: always).
# Podstrony nie publikuja oryginalow zdjec - tylko wersje przetworzone
# przez szablon (WebP, zmniejszone).
title: "Strony"
build:
  render: never
  list: always
cascade:
  - build:
      publishResources: false
---
