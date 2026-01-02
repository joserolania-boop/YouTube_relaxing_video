# 🎬 FLUJO DIRECTOR DE ARTE: Bosque Lluvioso desde Ventana

## Fase 1: Obtener Imagen Fotorrealista (Midjourney)

### ✅ Prompt para Midjourney (Copia-Pega)

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

## Fase 2: Descargar & Preparar Imagen

1. Una vez Midjourney genere la imagen, **descárgala en máxima calidad**
2. Guarda la imagen en:
   ```
   assets/images/bosque_ventana_base.png
   ```
3. Verifica que exista el directorio `assets/images/` (se crea automático si no existe)

---

## Fase 3: Ejecutar Script con Imagen

### Opción A: Solo con imagen (audio rosa sintetizado)
```powershell
.\scripts\make_forest_preview_v2.ps1 -BackgroundImage "assets/images/bosque_ventana_base.png"
```

### Opción B: Con imagen + audio personalizado
```powershell
.\scripts\make_forest_preview_v2.ps1 -BackgroundImage "assets/images/bosque_ventana_base.png" -AudioFile "ruta/audio_lluvia.wav"
```

---

## Fase 4: Resultado Final

El script generará:
- **Archivo**: `out/forest_window_piloto_60s.mp4`
- **Duración**: 60 segundos exactos
- **Resolución**: 1280×720 HD
- **Codec**: MPEG4 (Q2 = alta calidad)
- **Audio**: AAC 256 kbps estéreo

### Efectos Aplicados:
✨ **Zoom Ken Burns suave**: Escala gradual de 1.0 a 1.15 durante los 60s
✨ **Marco ventana oscuro**: Enmarque sutil con borde de 4px
✨ **Capa de lluvia/gotas**: Blend en modo "screen" con 45% opacidad
✨ **Audio binaural**: Lluvia rosa a 44.1kHz (432Hz root frequency)

---

## Fase 5: Visualizar

```powershell
start "out/forest_window_piloto_60s.mp4"
```

---

## 📋 Especificaciones Técnicas

| Parámetro | Valor |
|-----------|-------|
| **Duración** | 60 segundos |
| **Resolución** | 1280×720 (16:9 HD) |
| **Frame Rate** | 30 fps |
| **Codec Video** | MPEG4 (mpeg4v) |
| **Bitrate Video** | ~200 kbps base (Q2) |
| **Codec Audio** | AAC (LC) |
| **Bitrate Audio** | 256 kbps estéreo |
| **Sample Rate** | 44.1 kHz |
| **Tamaño Aprox.** | 15-20 MB |

---

## 🎨 Ajustes Personalizables (editar script)

Si quieres modificar los efectos, abre `scripts/make_forest_preview_v2.ps1` y cambia:

- **Zoom speed**: `0.0025` → aumenta/disminuye velocidad del efecto Ken Burns
- **Rain opacity**: `0.45` → aumenta/disminuye intensidad de lluvia
- **Marco color**: `0x1a2f2a` → código hexadecimal del color
- **Gblur sigma**: `2` → aumenta difuminado de lluvia

---

## ✅ Checklist

- [ ] Prompt copiado a Midjourney
- [ ] Imagen generada y descargada
- [ ] Guardada en `assets/images/bosque_ventana_base.png`
- [ ] Script ejecutado: `.\scripts\make_forest_preview_v2.ps1 -BackgroundImage "assets/images/bosque_ventana_base.png"`
- [ ] Video generado en `out/forest_window_piloto_60s.mp4`
- [ ] Visualizado y aprobado

---

**Director de Arte listo. Producción en tus manos. 🎬**
