import re

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "r") as f:
    content = f.read()

# 1. Add I2S include and vars
i2s_vars = """
#include <driver/i2s_std.h>
i2s_chan_handle_t rx_handle = NULL;
#define I2S_SCK 5
#define I2S_WS 6
#define I2S_SD 7
#define SAMPLE_RATE 16000
#define BLOCK_SIZE 128
float audioVolume = 0.0;
float smoothedVolume = 0.0;
float agcMax = 8000.0;
float agcMin = 500.0;
"""
content = re.sub(r'(#include <PubSubClient\.h>\n)', r'\1' + i2s_vars + '\n', content)

# 2. Add functions
i2s_funcs = """
void setup_i2s() {
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
    esp_err_t err = i2s_new_channel(&chan_cfg, NULL, &rx_handle);
    if (err != ESP_OK) {
        Serial.println("Failed to create I2S channel");
        return;
    }
    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(SAMPLE_RATE),
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_32BIT, I2S_SLOT_MODE_MONO),
        .gpio_cfg = {
            .mclk = I2S_GPIO_UNUSED,
            .bclk = (gpio_num_t)I2S_SCK,
            .ws = (gpio_num_t)I2S_WS,
            .dout = I2S_GPIO_UNUSED,
            .din = (gpio_num_t)I2S_SD,
            .invert_flags = { .mclk_inv = false, .bclk_inv = false, .ws_inv = false }
        }
    };
    std_cfg.slot_cfg.slot_mask = I2S_STD_SLOT_LEFT;
    i2s_channel_init_std_mode(rx_handle, &std_cfg);
    i2s_channel_enable(rx_handle);
}

void processAudio() {
    int32_t raw_samples[BLOCK_SIZE];
    size_t bytes_read = 0;
    esp_err_t result = i2s_channel_read(rx_handle, &raw_samples, sizeof(raw_samples), &bytes_read, 0); // Non-blocking
    if (result != ESP_OK || bytes_read == 0) return;
    
    int samples_read = bytes_read / sizeof(int32_t);
    float rawVolume = 0;
    for (int i = 0; i < samples_read; i++) {
        float sample = abs((float)(raw_samples[i] >> 14)); 
        if (sample > rawVolume) rawVolume = sample;
    }
    
    if (rawVolume > agcMax) agcMax = rawVolume;
    if (rawVolume < agcMin && rawVolume > 10) agcMin = rawVolume;
    agcMax -= (agcMax - 8000.0) * 0.001; 
    agcMin += (500.0 - agcMin) * 0.001;
    if (agcMax - agcMin < 1500.0) agcMax = agcMin + 1500.0;
    
    float dynamicRange = agcMax - agcMin;
    float squelchPct = map((long)pxSpeeds[(int)currentEffect], 1, 100, 40, 5) / 100.0;
    float noiseGate = agcMin + (dynamicRange * squelchPct);
    
    if (rawVolume < noiseGate) rawVolume = 0;
    else rawVolume = map(rawVolume, noiseGate, agcMax, 0, 255);
    
    if (rawVolume > 255) rawVolume = 255;
    if (rawVolume < 0) rawVolume = 0;
    
    audioVolume = rawVolume;
    if (audioVolume > smoothedVolume) smoothedVolume = audioVolume; 
    else smoothedVolume = smoothedVolume * 0.85 + audioVolume * 0.15; 
}
"""
content = re.sub(r'(void setup\(\) {\n)', i2s_funcs + r'\n\1', content)

# 3. Call setup_i2s in setup
content = re.sub(r'(Serial\.begin\(115200\);\n)', r'\1    setup_i2s();\n', content)

# 4. Call processAudio in loop
content = re.sub(r'(unsigned long now = millis\(\);\n)', r'\1\n  if (currentEffect == MUSIC_PULSE || currentEffect == VU_METER) processAudio();\n', content)

# 5. Add case MUSIC_PULSE
pulse_case = """
      case MUSIC_PULSE:
        {
          float normVol = smoothedVolume / 255.0;
          normVol = normVol * normVol * normVol; // cubic curve
          uint8_t minBright = pxBrightnesses[(int)currentEffect] / 10;
          if (minBright < 5) minBright = 5;
          uint8_t pulseBright = minBright + (normVol * (pxBrightnesses[(int)currentEffect] - minBright));
          
          fill_solid(leds, NUM_LEDS, CRGB(targetR, targetG, targetB));
          FastLED.setBrightness(pulseBright);
          FastLED.show();
        }
        break;
"""
content = re.sub(r'(case TETRIS:\n)', pulse_case + r'\n      \1', content)

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "w") as f:
    f.write(content)
