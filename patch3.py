import re

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "r") as f:
    content = f.read()

# Add new globals
globals_old = """float audioVolume = 0.0;
float smoothedVolume = 0.0;
float agcMax = 8000.0;
float agcMin = 500.0;"""

globals_new = """float audioVolume = 0.0;
float smoothedVolume = 0.0;
float audioBass = 0.0, audioMid = 0.0, audioTreble = 0.0;
float agcMax = 8000.0, agcMin = 500.0;
float bassMax = 8000.0, midMax = 8000.0, trebleMax = 8000.0;"""
content = content.replace(globals_old, globals_new)

process_audio_old = """void processAudio() {
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
}"""

process_audio_new = """void processAudio() {
    int32_t raw_samples[BLOCK_SIZE];
    size_t bytes_read = 0;
    esp_err_t result = i2s_channel_read(rx_handle, &raw_samples, sizeof(raw_samples), &bytes_read, 0);
    if (result != ESP_OK || bytes_read == 0) return;
    
    int samples_read = bytes_read / sizeof(int32_t);
    
    static float bassFilter = 0;
    static float trebleFilter = 0;
    static float prevSample = 0;
    
    float rawVolume = 0;
    float rawBass = 0, rawMid = 0, rawTreble = 0;
    
    for (int i = 0; i < samples_read; i++) {
        float sample = (float)(raw_samples[i] >> 14); 
        float absSample = abs(sample);
        if (absSample > rawVolume) rawVolume = absSample;
        
        // Simple IIR filters (16kHz sample rate)
        bassFilter = 0.03 * sample + 0.97 * bassFilter; // Lowpass ~80Hz
        trebleFilter = 0.6 * (trebleFilter + sample - prevSample); // Highpass ~2000Hz
        prevSample = sample;
        float midFilter = sample - bassFilter - trebleFilter;
        
        if (abs(bassFilter) > rawBass) rawBass = abs(bassFilter);
        if (abs(midFilter) > rawMid) rawMid = abs(midFilter);
        if (abs(trebleFilter) > rawTreble) rawTreble = abs(trebleFilter);
    }
    
    // Global AGC tracking
    if (rawVolume > agcMax) agcMax = rawVolume;
    if (rawVolume < agcMin && rawVolume > 10) agcMin = rawVolume;
    agcMax -= (agcMax - 8000.0) * 0.001; 
    agcMin += (500.0 - agcMin) * 0.001;
    if (agcMax - agcMin < 1500.0) agcMax = agcMin + 1500.0;
    
    // Band AGC tracking (independent peak tracking)
    if (rawBass > bassMax) bassMax = rawBass; else bassMax -= (bassMax - 1000) * 0.002;
    if (rawMid > midMax) midMax = rawMid; else midMax -= (midMax - 1000) * 0.002;
    if (rawTreble > trebleMax) trebleMax = rawTreble; else trebleMax -= (trebleMax - 1000) * 0.002;
    
    float dynamicRange = agcMax - agcMin;
    float squelchPct = map((long)pxSpeeds[(int)currentEffect], 1, 100, 40, 5) / 100.0;
    float noiseGate = agcMin + (dynamicRange * squelchPct);
    
    if (rawVolume < noiseGate) rawVolume = 0;
    else rawVolume = map(rawVolume, noiseGate, agcMax, 0, 255);
    if (rawVolume > 255) rawVolume = 255; else if (rawVolume < 0) rawVolume = 0;
    audioVolume = rawVolume;
    
    if (audioVolume > smoothedVolume) smoothedVolume = audioVolume; 
    else smoothedVolume = smoothedVolume * 0.85 + audioVolume * 0.15; 
    
    // Process bands
    float b = 0, m = 0, t = 0;
    if (rawVolume > 0) { // Only calculate bands if above noise gate
        b = map(rawBass, 0, bassMax, 0, 255);
        m = map(rawMid, 0, midMax, 0, 255);
        t = map(rawTreble, 0, trebleMax, 0, 255);
        if (b > 255) b = 255; if (b < 0) b = 0;
        if (m > 255) m = 255; if (m < 0) m = 0;
        if (t > 255) t = 255; if (t < 0) t = 0;
    }
    
    // Smooth the bands
    if (b > audioBass) audioBass = b; else audioBass = audioBass * 0.7 + b * 0.3;
    if (m > audioMid) audioMid = m; else audioMid = audioMid * 0.7 + m * 0.3;
    if (t > audioTreble) audioTreble = t; else audioTreble = audioTreble * 0.7 + t * 0.3;
}"""
content = content.replace(process_audio_old, process_audio_new)

with open(r"C:\Users\ZOHEB\.gemini\antigravity\scratch\pixora_matrix\pixora_matrix.ino", "w") as f:
    f.write(content)
