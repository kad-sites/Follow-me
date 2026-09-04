import re

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "r") as f:
    content = f.read()

vu_meter_old = """        case VU_METER:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 50, 10);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              FastLED.clear();

              // Use real audio volume
              static uint8_t heights[MATRIX_WIDTH] = {0};
              
              // Map volume 0-255 to matrix height 0-8
              uint8_t targetHeight = map(audioVolume, 0, 255, 0, 8);
              
              // Shift columns left (spectrogram style) or just bounce the middle
              // Let's do a classic equalizer look: center is highest, edges are lower
              for (int x = 0; x < MATRIX_WIDTH; x++) {
                int distFromCenter = abs(x - (MATRIX_WIDTH / 2));
                int colTarget = targetHeight - distFromCenter;
                if (colTarget < 0) colTarget = 0;
                
                // Add some random noise for visual variety
                if (colTarget > 0 && random8() < 50) colTarget += random8(0, 2);
                if (colTarget > 8) colTarget = 8;
                
                if (colTarget > heights[x]) {
                  heights[x] = colTarget; // Fast attack
                } else {
                  if (heights[x] > 0) heights[x]--; // Gravity decay
                }

                // Draw the column
                for (int y = 7; y >= 7 - heights[x]; y--) {
                  if (y < 0) break;
                  
                  // Color gradient from bottom to top
                  // Bottom (7) = Green, Middle (4) = Yellow, Top (0) = Red
                  uint8_t h = map(y, 0, 7, 0, 96); 
                  leds[XY(x, y)] = CHSV(h, 255, 255);
                }
              }
              FastLED.show();
            }
          }
          break;"""

vu_meter_new = """        case VU_METER:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 50, 10);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              FastLED.clear();

              static uint8_t heights[MATRIX_WIDTH] = {0};
              
              for (int x = 0; x < MATRIX_WIDTH; x++) {
                uint8_t targetHeight = 0;
                
                // Left = Bass, Middle = Vocal, Right = Treble
                if (x <= 1) {
                  targetHeight = map(audioBass, 0, 255, 0, 8);
                } else if (x >= 6) {
                  targetHeight = map(audioTreble, 0, 255, 0, 8);
                } else {
                  targetHeight = map(audioMid, 0, 255, 0, 8);
                }
                
                // Add a small amount of random noise to columns in the same band
                // so they don't look exactly identical, giving a 'real EQ' feel
                int colTarget = targetHeight;
                if (colTarget > 0 && random8() < 100) colTarget += random8(0, 2) - 1;
                
                if (colTarget < 0) colTarget = 0;
                if (colTarget > 8) colTarget = 8;
                
                if (colTarget > heights[x]) {
                  heights[x] = colTarget; // Fast attack
                } else {
                  if (heights[x] > 0) heights[x]--; // Gravity decay
                }

                // Draw the column
                for (int y = 7; y >= 7 - heights[x]; y--) {
                  if (y < 0) break;
                  
                  // Color gradient from bottom to top
                  uint8_t h = map(y, 0, 7, 0, 96); 
                  leds[XY(x, y)] = CHSV(h, 255, 255);
                }
              }
              FastLED.show();
            }
          }
          break;"""
content = content.replace(vu_meter_old, vu_meter_new)

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "w") as f:
    f.write(content)
