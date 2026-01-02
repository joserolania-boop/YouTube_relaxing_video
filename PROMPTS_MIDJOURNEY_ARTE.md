# Prompts Técnicos para Director de Arte – Video Piloto Bosque Lluvioso

## PROMPT PRINCIPAL – Midjourney (Imagen Base 4K)

```
/imagine prompt:
View from inside a warm, minimalist room looking through a large rain-soaked window 
at a lush temperate rainforest at dusk. 

COMPOSICIÓN:
- Ventana panorámica centra el 70% del encuadre
- Vidrio mojado con gotas prominentes y reflejos borrosos
- Marco de ventana de madera clara (pino/roble), sutilmente visible
- Interior apenas visible (borde izquierdo/derecho con luz cálida)

ATMÓSFERA VISUAL:
- Luz ambiente: Dorado cálido interior + azul-verde bosque exterior
- Niebla volumétrica entre los árboles (profundidad y misticismo)
- Lluvia suave visible en medio plano, bokeh de gotas de agua
- Reflejos de luces lejanas (cabaña o luz natural filtrada)

FLORA & NATURALEZA:
- Heléchos gigantes en primer plano (ligeramente desenfocados)
- Árboles majestuosos (eucaliptos, helechos arborescentes, pinos)
- Musgo verde profundo en troncos
- Rayos de luz suave penetrando la canopia (volumetric light rays)

CALIDAD TÉCNICA:
- Resolución: 4K Ultra HD (3840x2160 o compatible 16:9)
- Estilo: Fotografía cinematográfica, realismo fotográfico
- Iluminación: Suave, sin sombras duras (luz difusa de lluvia)
- Color grading: Tonos cálidos interiores (3000K) + fríos bosque (5500K)
- Depth of field: Profundo, enfoque en gotas de vidrio
- Lentes: Perspectiva 50mm (equivalente humano, natural)

MOOD:
- Paz profunda, tranquilidad, introspección
- Sensación de estar protegido observando la naturaleza
- Atmósfera de "hygge" nórdica + bosque tropical

--ar 16:9 --v 6 --quality 2 --chaos 15
```

---

## PROMPT ALTERNATIVO – DALL-E 3 (Si Midjourney no está disponible)

```
Generate a 4K photorealistic image: Interior view from a warm, dimly-lit room 
looking through a large floor-to-ceiling rain-covered window. Outside, a lush 
tropical rainforest in the evening mist. The window glass is heavily spattered 
with raindrops and condensation, creating a soft focus effect on the forest beyond. 
Warm amber light from inside contrasts with cool blue-green tones of the misty forest. 
Tall ferns, moss-covered trees, and volumetric light rays pierce through the canopy. 
The mood is peaceful, contemplative, cinematic. Shot with a 50mm lens, shallow 
depth of field on the water droplets. Style: Cinematic photography, ultra-detailed, 
professional color grading, warm interior lighting (3000K) meeting cool forest 
ambient (5500K).
```

---

## ESPECIFICACIONES TÉCNICAS PARA ENSAMBLAJE

**Formato de Salida Recomendado:**
- Nombre archivo: `bosque_ventana_4k.png` o `.jpg` (sin compresión pesada)
- Resolución: 1920x1080 mínimo (o 4K si tienes capaz)
- Color space: sRGB
- Ubicación: `assets/images/bosque_ventana_base.png`

**Integración con Script:**
1. Descarga la imagen de Midjourney
2. Colócala en: `assets/images/bosque_ventana_base.png`
3. Ejecuta: `.\scripts\make_forest_preview.ps1 -BackgroundImage "assets/images/bosque_ventana_base.png"`
