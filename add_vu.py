import re

# ----------------- 1. INDEX.HTML -----------------
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

vu_panel = """
          <div class="section" id="vuCalibPanel" style="display: none; padding: 12px 16px; margin-top: 8px;">
              <div class="section-title">VU Meter Calibration</div>
              <div style="font-size: 11px; color: var(--subtext); margin-bottom: 12px;">Map the physical corners of your TV strip.</div>

              <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;"><span style="color:var(--subtext)">Left Bottom</span><span id="vlbVal" style="color:#fff">0</span></div>
              <input type="range" id="vlb" min="0" max="300" value="0" style="width: 100%; margin-bottom: 12px;">
              
              <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;"><span style="color:var(--subtext)">Left Top</span><span id="vltVal" style="color:#fff">50</span></div>
              <input type="range" id="vlt" min="0" max="300" value="50" style="width: 100%; margin-bottom: 12px;">

              <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;"><span style="color:var(--subtext)">Right Bottom</span><span id="vrbVal" style="color:#fff">150</span></div>
              <input type="range" id="vrb" min="0" max="300" value="150" style="width: 100%; margin-bottom: 12px;">

              <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;"><span style="color:var(--subtext)">Right Top</span><span id="vrtVal" style="color:#fff">100</span></div>
              <input type="range" id="vrt" min="0" max="300" value="100" style="width: 100%; margin-bottom: 12px;">
          </div>
"""

html = html.replace('<div class="section" id="customSeqPanel"', vu_panel + '\n          <div class="section" id="customSeqPanel"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)


# ----------------- 2. MAIN.JS -----------------
with open("main.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add to live listeners array
old_live = "const liveSliders = ["
new_live = "const liveSliders = [\n              { el: document.getElementById('vlb'), key: 'vlb' },\n              { el: document.getElementById('vlt'), key: 'vlt' },\n              { el: document.getElementById('vrb'), key: 'vrb' },\n              { el: document.getElementById('vrt'), key: 'vrt' },"
js = js.replace(old_live, new_live)

update_ui_vu = """
                      if(data.vlb !== undefined && document.getElementById('vlb')) document.getElementById('vlb').value = data.vlb;
                      if(data.vlt !== undefined && document.getElementById('vlt')) document.getElementById('vlt').value = data.vlt;
                      if(data.vrb !== undefined && document.getElementById('vrb')) document.getElementById('vrb').value = data.vrb;
                      if(data.vrt !== undefined && document.getElementById('vrt')) document.getElementById('vrt').value = data.vrt;
"""
js = js.replace('updateUI();', update_ui_vu + '\n                      updateUI();')

old_panel_vis = "document.getElementById('customSeqPanel').style.display = 'block';"
new_panel_vis = "document.getElementById('customSeqPanel').style.display = 'block';\n                        } else if (tvEffect === 'music_meter' && document.getElementById('vuCalibPanel')) {\n                            document.getElementById('vuCalibPanel').style.display = 'block';"
js = js.replace(old_panel_vis, new_panel_vis)

old_panel_hide = "document.getElementById('customSeqPanel').style.display = 'none';"
new_panel_hide = "document.getElementById('customSeqPanel').style.display = 'none';\n                        if(document.getElementById('vuCalibPanel')) document.getElementById('vuCalibPanel').style.display = 'none';"
js = js.replace(old_panel_hide, new_panel_hide)

payload_add = """
                vlb: parseInt(document.getElementById('vlb') ? document.getElementById('vlb').value : 0),
                vlt: parseInt(document.getElementById('vlt') ? document.getElementById('vlt').value : 50),
                vrb: parseInt(document.getElementById('vrb') ? document.getElementById('vrb').value : 150),
                vrt: parseInt(document.getElementById('vrt') ? document.getElementById('vrt').value : 100),
"""
js = js.replace('brightness: b,', 'brightness: b,' + payload_add)

with open("main.js", "w", encoding="utf-8") as f:
    f.write(js)

# ----------------- 3. TV_BACKLIGHT_LED.INO -----------------
with open("../tv_backlight_led/tv_backlight_led.ino", "r", encoding="utf-8") as f:
    cpp = f.read()

cpp = cpp.replace('uint8_t currentSensitivity = 50;', 'uint8_t currentSensitivity = 50;\nint vuLeftBase = 0, vuLeftTop = 50, vuRightBase = 150, vuRightTop = 100;\n')

parse = """
      if (doc.containsKey("vlb")) vuLeftBase = doc["vlb"];
      if (doc.containsKey("vlt")) vuLeftTop = doc["vlt"];
      if (doc.containsKey("vrb")) vuRightBase = doc["vrb"];
      if (doc.containsKey("vrt")) vuRightTop = doc["vrt"];
"""
cpp = cpp.replace('if (doc.containsKey("speed"))', parse + '\n      if (doc.containsKey("speed"))')

old_meter = re.search(r'case MUSIC_METER:.*?FastLED\.show\(\);\n\s*\}\n\s*break;', cpp, re.DOTALL)
if old_meter:
    new_meter = """case MUSIC_METER:
        {
          FastLED.setBrightness(currentBrightness);
          fill_solid(leds, activePixels, CRGB::Black);

          int leftLen = abs(vuLeftTop - vuLeftBase) + 1;
          int rightLen = abs(vuRightTop - vuRightBase) + 1;

          int leftLit = map(smoothedVolume, 0, 255, 0, leftLen);
          int rightLit = map(smoothedVolume, 0, 255, 0, rightLen);

          int leftDir = (vuLeftTop >= vuLeftBase) ? 1 : -1;
          int rightDir = (vuRightTop >= vuRightBase) ? 1 : -1;

          static float leftPeak = 0;
          static float rightPeak = 0;

          // Peak physics
          if (leftLit > leftPeak) leftPeak = leftLit;
          else leftPeak -= 0.5; // Fall speed
          if (leftPeak < 0) leftPeak = 0;

          if (rightLit > rightPeak) rightPeak = rightLit;
          else rightPeak -= 0.5;
          if (rightPeak < 0) rightPeak = 0;

          // Inner lambda for traditional colors
          auto getVuColor = [](int i, int len) -> CRGB {
              float pct = (float)i / (float)len;
              if (pct < 0.50) return CRGB::Green;
              if (pct < 0.75) return CRGB::Yellow;
              if (pct < 0.90) return CRGB::Orange;
              return CRGB::Red;
          };

          // Draw Left VU
          for (int i = 0; i < leftLit; i++) {
            int idx = vuLeftBase + (i * leftDir);
            if (idx >= 0 && idx < activePixels) leds[idx] = getVuColor(i, leftLen);
          }
          // Draw Right VU
          for (int i = 0; i < rightLit; i++) {
            int idx = vuRightBase + (i * rightDir);
            if (idx >= 0 && idx < activePixels) leds[idx] = getVuColor(i, rightLen);
          }

          // Draw Falling Peaks (White dots)
          int lpIdx = vuLeftBase + ((int)leftPeak * leftDir);
          if (lpIdx >= 0 && lpIdx < activePixels) leds[lpIdx] = CRGB::White;

          int rpIdx = vuRightBase + ((int)rightPeak * rightDir);
          if (rpIdx >= 0 && rpIdx < activePixels) leds[rpIdx] = CRGB::White;

          FastLED.show();
        }
        break;"""
    cpp = cpp[:old_meter.start()] + new_meter + cpp[old_meter.end():]

with open("../tv_backlight_led/tv_backlight_led.ino", "w", encoding="utf-8") as f:
    f.write(cpp)

print("Done generating code.")
