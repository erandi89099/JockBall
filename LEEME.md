# JockBall - Fase 0 (proyecto base)

## Instalar (una sola vez)
1. JDK 25: https://adoptium.net (elige Temurin 25, Windows/Mac/Linux).
2. IntelliJ IDEA Community: https://www.jetbrains.com/idea/download
3. Descomprime esta carpeta, abre IntelliJ -> Open -> selecciona la carpeta `jockball`.
4. File > Project Structure > SDK = JDK 25. Settings > Build Tools > Gradle > Gradle JVM = 25.
5. Espera a que Gradle termine de descargar (la primera vez tarda varios minutos).
6. Arriba a la derecha, ejecuta la tarea `Minecraft Client` (o en terminal: `gradle runClient`).

## Que deberia pasar
Se abre Minecraft 26.2 con el mod cargado. En el log aparece:
"JockBall cargado. Fase 0: el proyecto base funciona."

Si falla algo, copiame el error completo (o captura) y lo corrijo.

## Texturas
`python3 tools/gen_textures.py` regenera las texturas provisionales (requiere Pillow).

## Fase 1 (armaduras, Trofeo, bonus de set)
- 20 piezas: casco, hombreras, fundas y tachos x 5 niveles. Estan en la pestana de Combate del modo creativo.
- Trofeo en la pestana de Ingredientes.
- Mejora: en la mesa de herreria pon la Plantilla de Mejora, la pieza (base) y 1 Trofeo (material); la plantilla se consume
  y la Plantilla de Mejora en la ranura de plantilla. Sube la pieza un nivel.
- Bonus de set: se usa el nivel de la pieza mas baja; si falta una pieza, no hay bonus.
- Balance: edita las tablas en gear/SetBonus.java y gear/GearLevel.java.
- Regenerar assets: python3 tools/gen_assets.py y python3 tools/gen_textures.py

## Obtener el .jar para la carpeta mods
Opcion A (local): en la carpeta del proyecto ejecuta `gradle build`. El archivo queda en build/libs/jockball-0.1.0.jar
(no uses el que termina en -sources.jar).
Opcion B (sin instalar nada): sube el proyecto a un repositorio de GitHub; en la pestana Actions, abre la ejecucion
"Compilar JockBall" y descarga el artefacto "jockball-jar".
Para jugar necesitas ademas Fabric Loader y Fabric API 0.150.1+26.2 (o superior) en la carpeta mods.
