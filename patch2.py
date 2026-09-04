import re

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "r") as f:
    content = f.read()

# 1. Update Enums and Arrays
enum_old = r"enum Effect \{ SOLID, TETRIS, MATRIX_RAIN, PLASMA, GAME_OF_LIFE, FIRE, TEXT_FADE, TEXT_DROP, TEXT_SLIDE, CANDY_CRUSH, FIREWORKS, VU_METER, PACMAN, FALLING_SAND, SMART_SNAKE, WARP_SPEED, RAIN_RIPPLES, MUSIC_PULSE \};"
enum_new = "enum Effect { SOLID, TETRIS, MATRIX_RAIN, PLASMA, GAME_OF_LIFE, FIRE, TEXT_FADE, TEXT_DROP, TEXT_SLIDE, CANDY_CRUSH, FIREWORKS, VU_METER, PACMAN, FALLING_SAND, SMART_SNAKE, WARP_SPEED, RAIN_RIPPLES, MUSIC_PULSE, MUSIC_FIRE, MUSIC_RIPPLE, MUSIC_PIXELS };"
content = re.sub(enum_old, enum_new, content)

content = re.sub(r"uint8_t pxBrightnesses\[18\] = \{[0-9, ]+\};", "uint8_t pxBrightnesses[21] = {60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60};", content)
content = re.sub(r"uint8_t pxSpeeds\[18\] = \{[0-9, ]+\};", "uint8_t pxSpeeds[21] = {50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50};", content)

# 2. Update MQTT JSON assignment
effect_ternary_old = r'currentEffect == MUSIC_PULSE \? "music_pulse" : "candy_crush";'
effect_ternary_new = 'currentEffect == MUSIC_PULSE ? "music_pulse" : currentEffect == MUSIC_FIRE ? "music_fire" : currentEffect == MUSIC_RIPPLE ? "music_ripple" : currentEffect == MUSIC_PIXELS ? "music_pixels" : "candy_crush";'
content = re.sub(effect_ternary_old, effect_ternary_new, content)

# 3. Update incoming MQTT parsing
eff_parse_old = r'else if \(effStr == "music_pulse"\) currentEffect = MUSIC_PULSE;'
eff_parse_new = """else if (effStr == "music_pulse") currentEffect = MUSIC_PULSE;
    else if (effStr == "music_fire") currentEffect = MUSIC_FIRE;
    else if (effStr == "music_ripple") currentEffect = MUSIC_RIPPLE;
    else if (effStr == "music_pixels") currentEffect = MUSIC_PIXELS;"""
content = re.sub(eff_parse_old, eff_parse_new, content)

# 4. Add processAudio calls
process_audio_old = r'if \(currentEffect == MUSIC_PULSE \|\| currentEffect == VU_METER\) processAudio\(\);'
process_audio_new = 'if (currentEffect == MUSIC_PULSE || currentEffect == VU_METER || currentEffect == MUSIC_FIRE || currentEffect == MUSIC_RIPPLE || currentEffect == MUSIC_PIXELS) processAudio();'
content = re.sub(process_audio_old, process_audio_new, content)

# 5. Add the 3 new cases to loop
new_cases = """
      case MUSIC_FIRE:
        {
          uint16_t delayMs = 30; // Fast update
          if (now - lastUpdate > delayMs) {
            lastUpdate = now;
            
            static byte heat[MATRIX_WIDTH][MATRIX_HEIGHT];
            
            // Step 1. Cool down every cell a little
            for( int x = 0; x < MATRIX_WIDTH; x++) {
              for( int y = 0; y < MATRIX_HEIGHT; y++) {
                heat[x][y] = qsub8(heat[x][y], random8(0, 1200 / MATRIX_HEIGHT + 2));
              }
            }
          
            // Step 2. Heat from each cell drifts 'up' (y-1) and diffuses
            for( int x = 0; x < MATRIX_WIDTH; x++) {
              for( int y = 0; y < MATRIX_HEIGHT - 1; y++) {
                heat[x][y] = (heat[x][y+1] + heat[(x-1+MATRIX_WIDTH)%MATRIX_WIDTH][y+1] + heat[(x+1)%MATRIX_WIDTH][y+1]) / 3;
              }
            }
            
            // Step 3. Ignite new sparks at bottom based on audio volume
            for( int x = 0; x < MATRIX_WIDTH; x++) {
              if(random8() < audioVolume) {
                heat[x][MATRIX_HEIGHT-1] = qadd8(heat[x][MATRIX_HEIGHT-1], audioVolume);
              } else {
                // Decay the bottom row heavily if no beat
                heat[x][MATRIX_HEIGHT-1] = qsub8(heat[x][MATRIX_HEIGHT-1], 20);
              }
            }
          
            // Step 4. Map heat to palette colors
            for( int x = 0; x < MATRIX_WIDTH; x++) {
              for( int y = 0; y < MATRIX_HEIGHT; y++) {
                // Scale the heat value to the palette index (0-240)
                byte colorIndex = scale8(heat[x][y], 240);
                leds[XY(x,y)] = ColorFromPalette(HeatColors_p, colorIndex);
              }
            }
            FastLED.show();
          }
        }
        break;

      case MUSIC_RIPPLE:
        {
          uint16_t delayMs = 20;
          if (now - lastUpdate > delayMs) {
            lastUpdate = now;
            FastLED.clear();
            
            static float radius = 0;
            static float energy = 0;
            
            // Audio injects energy
            if (audioVolume > 150) {
               energy += (audioVolume - 150) * 0.1;
            }
            
            // Energy converts to radius
            if (energy > 0) {
               radius += energy * 0.2;
               energy *= 0.8;
            }
            radius += 0.1; // slow baseline expansion
            
            if (radius > MATRIX_WIDTH) radius = 0;
            
            CHSV baseHSV = rgb2hsv_approximate(CRGB(targetR, targetG, targetB));
            float cx = (MATRIX_WIDTH-1)/2.0;
            float cy = (MATRIX_HEIGHT-1)/2.0;
            
            for(int x=0; x<MATRIX_WIDTH; x++){
              for(int y=0; y<MATRIX_HEIGHT; y++){
                float dist = sqrt((x-cx)*(x-cx) + (y-cy)*(y-cy));
                float diff = abs(dist - radius);
                
                if (diff < 1.5) {
                   float brightF = map(audioVolume, 0, 255, 100, 255) * (1.0 - diff/1.5);
                   if(brightF<0) brightF=0;
                   if(brightF>255) brightF=255;
                   leds[XY(x,y)] = CHSV(baseHSV.hue + radius*10, baseHSV.sat, (byte)brightF);
                }
              }
            }
            FastLED.show();
          }
        }
        break;

      case MUSIC_PIXELS:
        {
          uint16_t delayMs = 30;
          if (now - lastUpdate > delayMs) {
            lastUpdate = now;
            
            // Fade existing pixels
            for(int i=0; i<NUM_LEDS; i++) leds[i].fadeToBlackBy(40);
            
            // Spawn new pixels based on volume
            int spawnCount = map(audioVolume, 0, 255, 0, 4);
            CHSV baseHSV = rgb2hsv_approximate(CRGB(targetR, targetG, targetB));
            
            for(int i=0; i<spawnCount; i++) {
               int rx = random8(MATRIX_WIDTH);
               int ry = random8(MATRIX_HEIGHT);
               leds[XY(rx,ry)] = CHSV(baseHSV.hue + random8(64) - 32, baseHSV.sat, map(audioVolume, 0, 255, 150, 255));
            }
            FastLED.show();
          }
        }
        break;
"""
content = re.sub(r'(case MUSIC_PULSE:\n)', new_cases + r'\n      \1', content)

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "w") as f:
    f.write(content)
