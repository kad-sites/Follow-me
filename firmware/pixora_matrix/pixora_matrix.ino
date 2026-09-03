#include <WiFi.h>
#include <PubSubClient.h>
#include <FastLED.h>
#include <ArduinoOTA.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include "font.h"

// --- WiFi & MQTT Config ---
const char* ssid = "Official";
const char* password = "zoheb123";
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_topic_cmd = "kad/pixora/cmd/zoheb";
const char* mqtt_topic_status = "kad/pixora/status/zoheb";

WiFiClient espClient;
PubSubClient client(espClient);
Preferences preferences;

// --- Matrix Config ---
#define LED_PIN 8
#define MATRIX_WIDTH 7
#define MATRIX_HEIGHT 8
#define NUM_LEDS (MATRIX_WIDTH * MATRIX_HEIGHT)
CRGB leds[NUM_LEDS];

// IMPORTANT: Set to true if your LEDs snake back and forth.
// --- HARDWARE WIRING CONFIG ---
// Your matrix: 7 horizontal strips, each 8 LEDs, all data runs same direction.
// Strips stacked top-to-bottom. First strip = top row.
// Adjust these if letters appear mirrored or upside-down:
const bool FLIP_X = false;  // Set true if letters are left-right mirrored
const bool FLIP_Y = false;  // Set true if letters are upside-down
// Set to true if your matrix strips run vertically instead of horizontally

// --- State Variables ---
bool pxIsOn = true;
uint8_t pxBrightnesses[17] = {60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60};
uint8_t pxSpeeds[17] = {50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50};
uint8_t targetR = 255, targetG = 147, targetB = 41;
String pxText = "ZOHEB";
int textIndex = 0;
unsigned long lastUpdate = 0;

enum Effect { SOLID, TETRIS, MATRIX_RAIN, PLASMA, GAME_OF_LIFE, FIRE, TEXT_FADE, TEXT_DROP, TEXT_SLIDE, CANDY_CRUSH, FIREWORKS, VU_METER, PACMAN, FALLING_SAND, SMART_SNAKE, WARP_SPEED, RAIN_RIPPLES };
Effect currentEffect = SOLID;

// --- Helper Functions ---
// Convert (x, y) coordinates to 1D array index
uint16_t XY(uint8_t x, uint8_t y) {
  // 7 vertical strips of 8 LEDs each. ZIG-ZAG Layout.
  // x = strip/column index (0=leftmost, 6=rightmost)
  // y = row (0=top, 7=bottom)
  // Even columns (0,2,4,6) run Bottom-to-Top. Odd columns (1,3,5) run Top-to-Bottom.
  uint8_t pos;
  if (x % 2 == 0) {
    // Even column: Bottom to Top (y=7 is LED 0)
    pos = (MATRIX_HEIGHT - 1) - y;
  } else {
    // Odd column: Top to Bottom (y=0 is LED 0)
    pos = y;
  }
  return (uint16_t)x * MATRIX_HEIGHT + pos;
}

void loadSettings() {
  preferences.begin("pixora", false);
  pxIsOn = preferences.getBool("isOn", true);
  for (int i = 0; i < 9; i++) {
    pxSpeeds[i] = preferences.getUInt(("spd" + String(i)).c_str(), 50);
  }
  targetR = preferences.getUInt("tR", 255);
  targetG = preferences.getUInt("tG", 147);
  targetB = preferences.getUInt("tB", 41);
  currentEffect = (Effect)preferences.getUInt("eff", SOLID);
  pxText = preferences.getString("txt", "ZOHEB");
}


void saveSettings() {
  preferences.putBool("isOn", pxIsOn);
  for (int i = 0; i < 9; i++) {
    preferences.putUInt(("spd" + String(i)).c_str(), pxSpeeds[i]);
  }
  preferences.putUInt("tR", targetR);
  preferences.putUInt("tG", targetG);
  preferences.putUInt("tB", targetB);
  preferences.putUInt("eff", currentEffect);
  preferences.putString("txt", pxText);
}


void publishStatus() {
  StaticJsonDocument<256> doc;
  doc["isOn"] = pxIsOn;
  doc["brightness"] = pxBrightnesses[(int)currentEffect];
  doc["speed"] = pxSpeeds[(int)currentEffect];
  doc["r"] = targetR;
  doc["g"] = targetG;
  doc["b"] = targetB;
  doc["effect"] = currentEffect == SOLID ? "solid" : currentEffect == TETRIS ? "tetris" : currentEffect == MATRIX_RAIN ? "matrix_rain" : currentEffect == PLASMA ? "plasma" : currentEffect == GAME_OF_LIFE ? "game_of_life" : currentEffect == FIRE ? "fire" : currentEffect == TEXT_FADE ? "text_fade" : currentEffect == TEXT_DROP ? "text_drop" : currentEffect == TEXT_SLIDE ? "text_slide" : currentEffect == FIREWORKS ? "fireworks" : currentEffect == VU_METER ? "vu_meter" : currentEffect == PACMAN ? "pacman" : currentEffect == FALLING_SAND ? "falling_sand" : currentEffect == SMART_SNAKE ? "smart_snake" : currentEffect == WARP_SPEED ? "warp_speed" : currentEffect == RAIN_RIPPLES ? "rain_ripples" : "candy_crush";
  doc["text"] = pxText;
  char buffer[256];
  serializeJson(doc, buffer);
  client.publish(mqtt_topic_status, buffer);
}

void callback(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, payload, length);
  if (error) return;

  bool changed = false;

  if (doc.containsKey("power")) { pxIsOn = doc["power"]; changed = true; }
  if (doc.containsKey("brightness")) { pxBrightnesses[(int)currentEffect] = doc["brightness"]; changed = true; }
  if (doc.containsKey("speed")) { pxSpeeds[(int)currentEffect] = doc["speed"]; changed = true; }
  
  if (doc.containsKey("r") && doc.containsKey("g") && doc.containsKey("b")) {
    targetR = doc["r"];
    targetG = doc["g"];
    targetB = doc["b"];
    changed = true;
  }
  if (doc.containsKey("text")) {
    pxText = doc["text"].as<String>();
    pxText.toUpperCase();
    textIndex = 0;
    changed = true;
  }

  
  if (doc.containsKey("effect")) {
    String effStr = doc["effect"].as<String>();
    if (effStr == "solid") currentEffect = SOLID;
    else if (effStr == "tetris") currentEffect = TETRIS;
    else if (effStr == "matrix_rain") currentEffect = MATRIX_RAIN;
    else if (effStr == "plasma") currentEffect = PLASMA;
    else if (effStr == "game_of_life") currentEffect = GAME_OF_LIFE;
      else if (effStr == "fire") currentEffect = FIRE;
      else if (effStr == "text_fade") currentEffect = TEXT_FADE;
      else if (effStr == "text_drop") currentEffect = TEXT_DROP;
      else if (effStr == "text_slide") currentEffect = TEXT_SLIDE;
      else if (effStr == "candy_crush") currentEffect = CANDY_CRUSH;
      else if (effStr == "fireworks") currentEffect = FIREWORKS;
      else if (effStr == "vu_meter") currentEffect = VU_METER;
      else if (effStr == "pacman") currentEffect = PACMAN;
      else if (effStr == "falling_sand") currentEffect = FALLING_SAND;
      else if (effStr == "smart_snake") currentEffect = SMART_SNAKE;
      else if (effStr == "warp_speed") currentEffect = WARP_SPEED;
      else if (effStr == "rain_ripples") currentEffect = RAIN_RIPPLES;
    changed = true;
    FastLED.clear(); // Clear board on effect change
  }

  if (doc.containsKey("save") && doc["save"] == true) {
    saveSettings();
  }

  if (changed) {
    publishStatus();
  }
}

void setup() {
  Serial.begin(115200);
  
  loadSettings();

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(pxBrightnesses[(int)currentEffect]);
  FastLED.clear();
  FastLED.show();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  // Setup Over-The-Air (OTA) Updates
  ArduinoOTA.setHostname("PixoraMatrix");
  ArduinoOTA.begin();
  Serial.println("WiFi connected.");

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void reconnect() {
  static unsigned long lastReconnectAttempt = 0;
  unsigned long now = millis();
  
  // Only try to reconnect every 5 seconds so we don't block animations
  if (now - lastReconnectAttempt > 5000) {
    lastReconnectAttempt = now;
    
    // Check if WiFi dropped, try to reconnect to WiFi first
    if (WiFi.status() != WL_CONNECTED) {
      WiFi.reconnect();
      return; // Skip MQTT this time, wait for WiFi first
    }
    
    String clientId = "Pixora-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      client.subscribe(mqtt_topic_cmd);
      publishStatus();
    }
  }
}


// --- CANDY CRUSH VARS ---
CRGB candyGrid[MATRIX_WIDTH][MATRIX_HEIGHT];
int currentCandyX = 3, currentCandyY = 0;
CRGB currentCandyColor;
bool candyActive = false;
CRGB ccColors[4] = {CRGB::Red, CRGB::Green, CRGB::Blue, CRGB::Yellow};

// --- TETRIS ANIMATION VARS ---
int currentTetX = 3, currentTetY = 0, targetTetX = 3;
int currentTetType = 0;
bool tetrisGrid[MATRIX_WIDTH][MATRIX_HEIGHT] = {false};
CRGB tetrisColors[MATRIX_WIDTH][MATRIX_HEIGHT];

// Tetromino definitions (4x4 grids)
bool tetrominoes[7][4][4] = {
  // 0: 1x1 Dot
  {{1,0,0,0}, {0,0,0,0}, {0,0,0,0}, {0,0,0,0}},
  // 1: 2x1 Horizontal
  {{1,1,0,0}, {0,0,0,0}, {0,0,0,0}, {0,0,0,0}},
  // 2: 3x1 Horizontal
  {{1,1,1,0}, {0,0,0,0}, {0,0,0,0}, {0,0,0,0}},
  // 3: 1x2 Vertical
  {{1,0,0,0}, {1,0,0,0}, {0,0,0,0}, {0,0,0,0}},
  // 4: 1x3 Vertical
  {{1,0,0,0}, {1,0,0,0}, {1,0,0,0}, {0,0,0,0}},
  // 5: 2x2 Square (for fun)
  {{1,1,0,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
  // 6: 1x1 Dot again
  {{1,0,0,0}, {0,0,0,0}, {0,0,0,0}, {0,0,0,0}}
};
CRGB tetColors[7] = {CRGB::Cyan, CRGB::Blue, CRGB::Orange, CRGB::Yellow, CRGB::Green, CRGB::Purple, CRGB::Red};
CRGB customTetrisColors[3];
uint8_t numCustomTetrisColors = 0;

bool checkCollision(int x, int y, int type) {
  for(int r=0; r<4; r++) {
    for(int c=0; c<4; c++) {
      if(tetrominoes[type][r][c]) {
        int gx = x + c;
        int gy = y + r;
        if(gx < 0 || gx >= MATRIX_WIDTH || gy >= MATRIX_HEIGHT) return true; // Bounds
        if(gy >= 0 && tetrisGrid[gx][gy]) return true; // Hit other block
      }
    }
  }
  return false;
}

void lockTetromino() {
  for(int r=0; r<4; r++) {
    for(int c=0; c<4; c++) {
      if(tetrominoes[currentTetType][r][c]) {
        int gx = currentTetX + c;
        int gy = currentTetY + r;
        if(gy >= 0 && gy < MATRIX_HEIGHT && gx >= 0 && gx < MATRIX_WIDTH) {
          tetrisGrid[gx][gy] = true;
          tetrisColors[gx][gy] = tetColors[currentTetType];
        }
      }
    }
  }
  
  for(int r=MATRIX_HEIGHT-1; r>=0; r--) {
    bool full = true;
    for(int c=0; c<MATRIX_WIDTH; c++) if(!tetrisGrid[c][r]) full = false;
    
    if(full) {
      // Magic flash row to the winning brick's color
      for(int c=0; c<MATRIX_WIDTH; c++) leds[XY(c,r)] = tetColors[currentTetType];
      FastLED.show();
      delay(200); 
      
      for(int r2=r; r2>0; r2--) {
        for(int c=0; c<MATRIX_WIDTH; c++) {
          tetrisGrid[c][r2] = tetrisGrid[c][r2-1];
          tetrisColors[c][r2] = tetrisColors[c][r2-1];
        }
      }
      for(int c=0; c<MATRIX_WIDTH; c++) tetrisGrid[c][0] = false;
      r++; 
    }
  }
}
  

void spawnTetromino() {
  int colHeights[MATRIX_WIDTH] = {0};
  for (int c = 0; c < MATRIX_WIDTH; c++) {
    for (int r = 0; r < MATRIX_HEIGHT; r++) {
      if (tetrisGrid[c][r]) colHeights[c]++;
    }
  }
  
  int lowestH = 99;
  for (int c = 0; c < MATRIX_WIDTH; c++) {
    if (colHeights[c] < lowestH) lowestH = colHeights[c];
  }
  
  // Find all columns with lowestH
  int validCols[MATRIX_WIDTH];
  int numValid = 0;
  for (int c = 0; c < MATRIX_WIDTH; c++) {
    if (colHeights[c] == lowestH) {
      validCols[numValid++] = c;
    }
  }
  
  // Pick a random lowest column
  int lowestC = validCols[random(numValid)];
  
  // Find gap width from this random lowest column
  int gapWidth = 1;
  for (int c = lowestC + 1; c < MATRIX_WIDTH; c++) {
    if (colHeights[c] == lowestH) gapWidth++;
    else break;
  }
  
  if (gapWidth >= 3) {
    int choices[] = {0, 1, 2, 3, 4, 5};
    currentTetType = choices[random(6)];
  } else if (gapWidth == 2) {
    int choices[] = {0, 1, 3, 4, 5};
    currentTetType = choices[random(5)];
  } else {
    int choices[] = {0, 3, 4};
    currentTetType = choices[random(3)];
  }
  targetTetX = lowestC;
  
  // Randomize the color of this brick type so it isn't always the same!
  tetColors[currentTetType] = CHSV(random8(), 255, 255);
  
  // Spawn in a random location at the top so it has to steer to target
  currentTetX = random(MATRIX_WIDTH - (currentTetType + 1));
  currentTetY = -1;
  
  if(checkCollision(currentTetX, 0, currentTetType)) {
    for(int r=0; r<MATRIX_HEIGHT; r++) {
      for(int c=0; c<MATRIX_WIDTH; c++) {
        tetrisGrid[c][r] = false;
      }
    }
  }
}


// --- MAIN LOOP ---

// --- TEXT EFFECTS ---

uint8_t getCharRow(char c, uint8_t row) {
  if (c >= 'a' && c <= 'z') c -= 32;
  if (c >= 'A' && c <= 'Z') {
    return pgm_read_byte(&Font5x7[c - 'A'][row]);
  }
  return 0;
}

bool getFontPixel(uint8_t rowByte, uint8_t displayCol) {
  return bitRead(rowByte, 4 - displayCol);
}

void drawTextFade(uint16_t delayTime) { 
  static unsigned long lastFrame = 0;
  
  if (millis() - lastFrame > delayTime) {
    lastFrame = millis();
    if (pxText.length() == 0) return;
    
    char c = pxText[textIndex % pxText.length()];
    FastLED.clear();
    CRGB color = CHSV((textIndex * 45) % 256, 255, 255);
    
    for (int row = 0; row < 7; row++) {
      uint8_t r_curr = getCharRow(c, row);
      for (int col = 0; col < 5; col++) {
        if (getFontPixel(r_curr, col)) {
           leds[XY(col + 1, row)] = color;
        }
      }
    }
    FastLED.show();
    
    textIndex = (textIndex + 1) % pxText.length();
  }
}

void drawTextDrop(uint16_t delayTime) {
  static int currentPixelIdx = 0; 
  static int dropY = -1;
  static unsigned long lastFrame = 0;
  static bool letterComplete = false;
  
  int frameDelay = delayTime / 20;
  if (frameDelay < 5) frameDelay = 5;
  
  if (millis() - lastFrame > frameDelay) {
    lastFrame = millis();
    if (pxText.length() == 0) return;
    
    char c = pxText[textIndex % pxText.length()];
    FastLED.clear();
    CRGB color = CHSV((textIndex * 45) % 256, 255, 255);
    
    if (letterComplete) {
      for (int row = 0; row < 7; row++) {
        uint8_t r_curr = getCharRow(c, row);
        for (int col = 0; col < 5; col++) {
          if (getFontPixel(r_curr, col)) {
             leds[XY(col + 1, row)] = color;
          }
        }
      }
      FastLED.show();
      
      static int holdTime = 0;
      holdTime++;
      if (holdTime > (2000 / frameDelay)) { 
        holdTime = 0;
        letterComplete = false;
        currentPixelIdx = 0;
        dropY = -1;
        textIndex = (textIndex + 1) % pxText.length();
      }
      return;
    }
    
    for (int p = 0; p < currentPixelIdx; p++) {
      int p_row = p / 5;
      int p_col = p % 5;
      if (getFontPixel(getCharRow(c, p_row), p_col)) {
        leds[XY(p_col + 1, p_row)] = color;
      }
    }
    
    if (currentPixelIdx < 35) {
      int targetRow = currentPixelIdx / 5;
      int targetCol = currentPixelIdx % 5;
      
      if (getFontPixel(getCharRow(c, targetRow), targetCol)) {
        if (dropY >= 0 && dropY <= targetRow) {
           leds[XY(targetCol + 1, dropY)] = color;
        }
        dropY++;
        if (dropY > targetRow) {
          dropY = -1;
          currentPixelIdx++;
        }
      } else {
        currentPixelIdx++; 
      }
    } else {
      letterComplete = true;
    }
    FastLED.show();
  }
}

void drawTextSlide(uint16_t delayTime) {
  static int slideOffset = 6;
  static unsigned long lastFrame = 0;
  static int holdTime = 0;
  
  if (millis() - lastFrame > (delayTime / 3)) {
    lastFrame = millis();
    if (pxText.length() == 0) return;
    
    char c = pxText[textIndex % pxText.length()];
    FastLED.clear();
    CRGB color = CHSV((textIndex * 45) % 256, 255, 255);
    
    for (int row = 0; row < 7; row++) {
      uint8_t r_curr = getCharRow(c, row);
      for (int col = 0; col < 5; col++) {
        if (getFontPixel(r_curr, col)) {
          int actualX = col + 1 + slideOffset;
          if (actualX >= 0 && actualX < MATRIX_WIDTH) { 
             leds[XY(actualX, row)] = color;
          }
        }
      }
    }
    FastLED.show();
    
    if (slideOffset == 0 && holdTime < (2000 / (delayTime / 3))) {
      holdTime++;
    } else {
      holdTime = 0;
      slideOffset--;
      if (slideOffset < -6) {
        slideOffset = 6;
        textIndex = (textIndex + 1) % pxText.length();
      }
    }
  }
}


void loop() {
  ArduinoOTA.handle();
  if (!client.connected()) {
    reconnect();
  } else {
    client.loop(); // Only call client.loop() if actually connected
  }

  if (!pxIsOn) {
    FastLED.clear();
    FastLED.show();
    return;
  }

  FastLED.setBrightness(pxBrightnesses[(int)currentEffect]);
  unsigned long now = millis();

  switch (currentEffect) {
    case SOLID:
      fill_solid(leds, NUM_LEDS, CRGB(targetR, targetG, targetB));
      FastLED.show();
      break;

    case TETRIS:
      {
        uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 800, 100);
        if (now - lastUpdate > delayMs) {
          lastUpdate = now;
          
          // AI Steering
          if (currentTetX < targetTetX) {
            if (!checkCollision(currentTetX + 1, currentTetY, currentTetType)) currentTetX++;
          } else if (currentTetX > targetTetX) {
            if (!checkCollision(currentTetX - 1, currentTetY, currentTetType)) currentTetX--;
          }
          
          if(checkCollision(currentTetX, currentTetY + 1, currentTetType)) {
            lockTetromino();
            spawnTetromino();
          } else {
            currentTetY++;
          }
          
          FastLED.clear();
          // Draw grid
          for(int r=0; r<MATRIX_HEIGHT; r++) {
            for(int c=0; c<MATRIX_WIDTH; c++) {
              if(tetrisGrid[c][r]) leds[XY(c,r)] = tetrisColors[c][r];
            }
          }
          // Draw falling piece
          for(int r=0; r<4; r++) {
            for(int c=0; c<4; c++) {
              if(tetrominoes[currentTetType][r][c]) {
                int gx = currentTetX + c;
                int gy = currentTetY + r;
                if(gy >= 0 && gy < MATRIX_HEIGHT && gx >= 0 && gx < MATRIX_WIDTH) {
                  leds[XY(gx,gy)] = tetColors[currentTetType];
                }
              }
            }
          }
          FastLED.show();
        }
      }
      break;

    case MATRIX_RAIN:
      {
        uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 200, 30);
        if (now - lastUpdate > delayMs) {
          lastUpdate = now;
          
          // Fade all
          for(int i=0; i<NUM_LEDS; i++) leds[i].fadeToBlackBy(40);
          
          // Spawn new drops
          if(random8() < 60) {
            int x = random(MATRIX_WIDTH);
            leds[XY(x, 0)] = CRGB(targetR, targetG, targetB); // Custom color rain
          }
          
          // Move drops down
          for(int x=0; x<MATRIX_WIDTH; x++) {
            for(int y=MATRIX_HEIGHT-1; y>0; y--) {
              if(leds[XY(x,y-1)].getAverageLight() > 100) {
                 leds[XY(x,y)] = leds[XY(x,y-1)];
              }
            }
          }
          FastLED.show();
        }
      }
      break;

    case PLASMA:
      {
        uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 50, 10);
        if (now - lastUpdate > delayMs) {
          lastUpdate = now;
          uint16_t t = millis() / 10;
          for (int x = 0; x < MATRIX_WIDTH; x++) {
            for (int y = 0; y < MATRIX_HEIGHT; y++) {
              byte noise = inoise8(x * 40, y * 40, t);
              // Mix selected color with noise hue
              leds[XY(x,y)] = CHSV(noise, 255, 255); 
            }
          }
          FastLED.show();
        }
      }
      break;
      
    case GAME_OF_LIFE:
      {
        uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 800, 100);
        if (now - lastUpdate > delayMs) {
          lastUpdate = now;
          
          static bool grid[MATRIX_WIDTH][MATRIX_HEIGHT];
          static bool nextGrid[MATRIX_WIDTH][MATRIX_HEIGHT];
          static bool initialized = false;
          
          if (!initialized) {
            for(int x=0; x<MATRIX_WIDTH; x++)
              for(int y=0; y<MATRIX_HEIGHT; y++)
                grid[x][y] = (random8() > 180);
            initialized = true;
          }
          
          int aliveCount = 0;
          for(int x=0; x<MATRIX_WIDTH; x++) {
            for(int y=0; y<MATRIX_HEIGHT; y++) {
              int neighbors = 0;
              for(int i=-1; i<=1; i++) {
                for(int j=-1; j<=1; j++) {
                  if(i==0 && j==0) continue;
                  int nx = (x+i+MATRIX_WIDTH)%MATRIX_WIDTH;
                  int ny = (y+j+MATRIX_HEIGHT)%MATRIX_HEIGHT;
                  if(grid[nx][ny]) neighbors++;
                }
              }
              if (grid[x][y] && (neighbors == 2 || neighbors == 3)) nextGrid[x][y] = true;
              else if (!grid[x][y] && neighbors == 3) nextGrid[x][y] = true;
              else nextGrid[x][y] = false;
              
              if (nextGrid[x][y]) aliveCount++;
            }
          }
          
          if (aliveCount < 3) initialized = false; // Reset if dead
          
          for(int x=0; x<MATRIX_WIDTH; x++) {
            for(int y=0; y<MATRIX_HEIGHT; y++) {
              grid[x][y] = nextGrid[x][y];
              if(grid[x][y]) leds[XY(x,y)] = CRGB(targetR, targetG, targetB);
              else leds[XY(x,y)].fadeToBlackBy(100);
            }
          }
          FastLED.show();
        }
      }
      break;

    case FIRE:
      {
        uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 60, 20);
        if (now - lastUpdate > delayMs) {
          lastUpdate = now;
          
          static byte heat[MATRIX_WIDTH][MATRIX_HEIGHT];
          
          for(int x=0; x<MATRIX_WIDTH; x++) {
            // Cool down
            for(int y=0; y<MATRIX_HEIGHT; y++) {
              heat[x][y] = qsub8(heat[x][y], random8(0, 1200 / MATRIX_HEIGHT + 2));
            }
            // Drift up
            for(int y=0; y<MATRIX_HEIGHT-1; y++) {
              heat[x][y] = (heat[x][y+1] * 2 + heat[x][(y+2)%MATRIX_HEIGHT]) / 3;
            }
            // Spark at bottom
            if(random8() < 120) {
              heat[x][MATRIX_HEIGHT-1] = qadd8(heat[x][MATRIX_HEIGHT-1], random8(160, 255));
            }
          }
          
          for(int x=0; x<MATRIX_WIDTH; x++) {
            for(int y=0; y<MATRIX_HEIGHT; y++) {
              // Custom Fire Palette (No White, No Green)
                CRGBPalette16 customFire = CRGBPalette16(
                  CRGB::Black,
                  CRGB(128, 0, 0), // Dark Red
                  CRGB::Red,
                  CRGB::Yellow
                );
                leds[XY(x,y)] = ColorFromPalette(customFire, heat[x][y]);
            }
          }
          FastLED.show();
        }
      }
      break;
      case TEXT_FADE:
        drawTextFade(map(pxSpeeds[TEXT_FADE], 1, 100, 1500, 200));
        break;
      case TEXT_DROP:
        drawTextDrop(map(pxSpeeds[TEXT_DROP], 1, 100, 1500, 200));
        break;
            case CANDY_CRUSH:
        {
          uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 300, 30);
          if (now - lastUpdate > delayMs) {
            lastUpdate = now;
            
                          // Spawn new candy
              if (!candyActive) {
                currentCandyX = random(MATRIX_WIDTH);
                currentCandyY = -1;
                
                // 20% chance to explicitly match the color of the candy it will land on
                if (random(100) < 20) {
                  CRGB forcedColor = ccColors[random(4)]; // fallback
                  for (int r = 0; r < MATRIX_HEIGHT; r++) {
                    if (candyGrid[currentCandyX][r]) {
                      forcedColor = candyGrid[currentCandyX][r];
                      break;
                    }
                  }
                  currentCandyColor = forcedColor;
                } else {
                  currentCandyColor = ccColors[random(4)];
                }
                
                candyActive = true;
              
              // If board is full, reset
              if(candyGrid[currentCandyX][0]) {
                for(int r=0; r<MATRIX_HEIGHT; r++) {
                  for(int c=0; c<MATRIX_WIDTH; c++) candyGrid[c][r] = CRGB(0,0,0);
                }
              }
            } else {
              // Move down
              if (currentCandyY + 1 >= MATRIX_HEIGHT || candyGrid[currentCandyX][currentCandyY + 1]) {
                // Landed
                if (currentCandyY >= 0) {
                  candyGrid[currentCandyX][currentCandyY] = currentCandyColor;
                }
                candyActive = false;
                
                // Check matches (horizontal and vertical)
                bool matched[MATRIX_WIDTH][MATRIX_HEIGHT] = {false};
                bool matchFound = false;
                
                // Horizontal
                for(int r=0; r<MATRIX_HEIGHT; r++) {
                  for(int c=0; c<MATRIX_WIDTH-2; c++) {
                    if(candyGrid[c][r] && candyGrid[c][r] == candyGrid[c+1][r] && candyGrid[c][r] == candyGrid[c+2][r]) {
                      matched[c][r] = true; matched[c+1][r] = true; matched[c+2][r] = true;
                      matchFound = true;
                    }
                  }
                }
                // Vertical
                for(int c=0; c<MATRIX_WIDTH; c++) {
                  for(int r=0; r<MATRIX_HEIGHT-2; r++) {
                    if(candyGrid[c][r] && candyGrid[c][r] == candyGrid[c][r+1] && candyGrid[c][r] == candyGrid[c][r+2]) {
                      matched[c][r] = true; matched[c][r+1] = true; matched[c][r+2] = true;
                      matchFound = true;
                    }
                  }
                }
                
                // Square (2x2)
                for(int c=0; c<MATRIX_WIDTH-1; c++) {
                  for(int r=0; r<MATRIX_HEIGHT-1; r++) {
                    if(candyGrid[c][r] && 
                       candyGrid[c][r] == candyGrid[c+1][r] && 
                       candyGrid[c][r] == candyGrid[c][r+1] && 
                       candyGrid[c][r] == candyGrid[c+1][r+1]) {
                      matched[c][r] = true; matched[c+1][r] = true;
                      matched[c][r+1] = true; matched[c+1][r+1] = true;
                      matchFound = true;
                    }
                  }
                }
                
                if (matchFound) {
                  // Blink matched in their own color
                  for(int b=0; b<2; b++) {
                    // Turn OFF the matched candies to create the blink effect
                    FastLED.clear();
                    for(int r=0; r<MATRIX_HEIGHT; r++) {
                      for(int c=0; c<MATRIX_WIDTH; c++) {
                        if(!matched[c][r] && candyGrid[c][r]) leds[XY(c,r)] = candyGrid[c][r];
                      }
                    }
                    FastLED.show();
                    delay(60);
                    
                    // Turn ON the matched candies in their original bright color
                    FastLED.clear();
                    for(int r=0; r<MATRIX_HEIGHT; r++) {
                      for(int c=0; c<MATRIX_WIDTH; c++) {
                        if(candyGrid[c][r]) leds[XY(c,r)] = candyGrid[c][r];
                      }
                    }
                    FastLED.show();
                    delay(60);
                  }
                  
                  // Remove matched and apply gravity
                  for(int c=0; c<MATRIX_WIDTH; c++) {
                    for(int r=MATRIX_HEIGHT-1; r>=0; r--) {
                      if(matched[c][r]) {
                        // pull everything above it down
                        for(int r2=r; r2>0; r2--) {
                          candyGrid[c][r2] = candyGrid[c][r2-1];
                          matched[c][r2] = matched[c][r2-1]; // shift match mask too
                        }
                        candyGrid[c][0] = CRGB(0,0,0);
                        matched[c][0] = false;
                        r++; // check this row again
                      }
                    }
                  }
                }
              } else {
                currentCandyY++;
              }
            }
            
            // Draw
            FastLED.clear();
            for(int r=0; r<MATRIX_HEIGHT; r++) {
              for(int c=0; c<MATRIX_WIDTH; c++) {
                if(candyGrid[c][r]) leds[XY(c,r)] = candyGrid[c][r];
              }
            }
            if (candyActive && currentCandyY >= 0) leds[XY(currentCandyX, currentCandyY)] = currentCandyColor;
            FastLED.show();
          }
        }
        break;
              case FIREWORKS:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 100, 20);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              
              // Fade everything by a fraction to leave trails
              for(int i = 0; i < NUM_LEDS; i++) {
                leds[i].fadeToBlackBy(40);
              }

              static int fwState = 0; // 0=waiting, 1=launching, 2=exploding
              static int fwX = 3;
              static int fwY = 7;
              static CRGB fwColor;

              if (fwState == 0) {
                if (random8() < 20) { // Random chance to launch
                  fwX = random8(1, 6);
                  fwY = 7; // Bottom
                  fwState = 1;
                  fwColor = CHSV(random8(), 255, 255);
                }
              } else if (fwState == 1) {
                // Draw launch trail (white core)
                leds[XY(fwX, fwY)] = CRGB::White;
                fwY--; // Move up
                if (fwY <= random8(1, 3)) { // Explode somewhere near top
                  fwState = 2;
                }
              } else if (fwState == 2) {
                // Explode! Draw a cross pattern
                if (fwX > 0) leds[XY(fwX-1, fwY)] = fwColor;
                if (fwX < MATRIX_WIDTH-1) leds[XY(fwX+1, fwY)] = fwColor;
                if (fwY > 0) leds[XY(fwX, fwY-1)] = fwColor;
                if (fwY < MATRIX_HEIGHT-1) leds[XY(fwX, fwY+1)] = fwColor;
                leds[XY(fwX, fwY)] = CRGB::White;
                
                // Explode diagonals
                if (fwX > 0 && fwY > 0) leds[XY(fwX-1, fwY-1)] = fwColor;
                if (fwX < MATRIX_WIDTH-1 && fwY > 0) leds[XY(fwX+1, fwY-1)] = fwColor;
                if (fwX > 0 && fwY < MATRIX_HEIGHT-1) leds[XY(fwX-1, fwY+1)] = fwColor;
                if (fwX < MATRIX_WIDTH-1 && fwY < MATRIX_HEIGHT-1) leds[XY(fwX+1, fwY+1)] = fwColor;

                fwState = 0; // Reset for next firework
              }
              FastLED.show();
            }
          }
          break;

        case VU_METER:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 100, 30);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              FastLED.clear();

              // For each column, generate a random height
              for (int x = 0; x < MATRIX_WIDTH; x++) {
                // Generate a smooth bouncing height
                // We simulate an audio envelope for each column
                static uint8_t heights[7] = {0,0,0,0,0,0,0};
                
                // Randomly punch the height up
                if (random8() < 50) {
                  heights[x] = random8(3, 8); // Jump to random height
                } else {
                  if (heights[x] > 0) heights[x]--; // Gravity decay
                }

                // Draw the column
                for (int y = 7; y >= 7 - heights[x]; y--) {
                  if (y < 0) break;
                  
                  // Color gradient from bottom to top
                  // Bottom (7) = Green, Middle (4) = Yellow, Top (0) = Red
                  uint8_t h = map(y, 0, 7, 0, 96); // Red is 0, Green is ~96
                  leds[XY(x, y)] = CHSV(h, 255, 255);
                }
              }
              FastLED.show();
            }
          }
          break;

                case PACMAN:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 300, 50);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              FastLED.clear();
              static int px = 3, py = 4;
              static int gx = 0, gy = 0;
              static bool initP = false;
              if (!initP) { gx = random8(7); gy = random8(8); initP = true; }
              
              // Ghost moves randomly but favors edges
              if (random8() < 128) gx += (random8(2) == 0 ? 1 : -1);
              else gy += (random8(2) == 0 ? 1 : -1);
              if (gx < 0) gx = 6; if (gx > 6) gx = 0;
              if (gy < 0) gy = 7; if (gy > 7) gy = 0;
              
              // Pacman chases ghost
              if (px < gx) px++;
              else if (px > gx) px--;
              else if (py < gy) py++;
              else if (py > gy) py--;
              
              // Keep 2x2 pacman in bounds
              if (px > MATRIX_WIDTH - 2) px = MATRIX_WIDTH - 2;
              if (py > MATRIX_HEIGHT - 2) py = MATRIX_HEIGHT - 2;

              if (px == gx && py == gy) {
                initP = false; // Just respawn ghost instantly
              } else {
                // Draw 2x2 Pacman
                if (px >= 0 && px < MATRIX_WIDTH && py >= 0 && py < MATRIX_HEIGHT) leds[XY(px, py)] = CRGB::Yellow;
                if (px+1 >= 0 && px+1 < MATRIX_WIDTH && py >= 0 && py < MATRIX_HEIGHT) leds[XY(px+1, py)] = CRGB::Yellow;
                if (px >= 0 && px < MATRIX_WIDTH && py+1 >= 0 && py+1 < MATRIX_HEIGHT) leds[XY(px, py+1)] = CRGB::Yellow;
                
                // Animate mouth (open/close) by hiding one corner
                bool mouthOpen = ((millis() / 250) % 2 == 0);
                if (!mouthOpen) {
                  if (px+1 >= 0 && px+1 < MATRIX_WIDTH && py+1 >= 0 && py+1 < MATRIX_HEIGHT) leds[XY(px+1, py+1)] = CRGB::Yellow;
                }
                
                // Ghost
                if (gx >= 0 && gx < MATRIX_WIDTH && gy >= 0 && gy < MATRIX_HEIGHT) leds[XY(gx, gy)] = ((millis() / 500) % 2 == 0) ? CRGB::Red : CRGB::Blue;
              }
              FastLED.show();
            }
          }
          break;

        case FALLING_SAND:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 150, 10);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              static uint8_t grid[MATRIX_WIDTH][MATRIX_HEIGHT] = {0};
              static int sandCount = 0;

              if (sandCount > 40) { // Screen full, reset
                memset(grid, 0, sizeof(grid));
                sandCount = 0;
                FastLED.clear();
              }

              // Move sand
              for (int y = MATRIX_HEIGHT - 2; y >= 0; y--) {
                for (int x = 0; x < MATRIX_WIDTH; x++) {
                  if (grid[x][y]) {
                    if (!grid[x][y+1]) { // Fall straight down
                      grid[x][y+1] = grid[x][y];
                      grid[x][y] = 0;
                    } else { // Try diagonal
                      int dir = (random8(2) == 0) ? 1 : -1;
                      if (x + dir >= 0 && x + dir < MATRIX_WIDTH && !grid[x+dir][y+1]) {
                        grid[x+dir][y+1] = grid[x][y];
                        grid[x][y] = 0;
                      } else if (x - dir >= 0 && x - dir < MATRIX_WIDTH && !grid[x-dir][y+1]) {
                        grid[x-dir][y+1] = grid[x][y];
                        grid[x][y] = 0;
                      }
                    }
                  }
                }
              }

              // Spawn new sand
              if (random8() < 100) {
                int sx = random8(MATRIX_WIDTH);
                if (!grid[sx][0]) {
                  grid[sx][0] = random8(50, 255); // Hue
                  sandCount++;
                }
              }

              // Draw
              FastLED.clear();
              for (int x = 0; x < MATRIX_WIDTH; x++) {
                for (int y = 0; y < MATRIX_HEIGHT; y++) {
                  if (grid[x][y]) {
                    leds[XY(x,y)] = CHSV(grid[x][y], 255, 255);
                  }
                }
              }
              FastLED.show();
            }
          }
          break;

        case SMART_SNAKE:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 300, 50);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              FastLED.clear();
              static int8_t sx[56] = {3,3,3};
              static int8_t sy[56] = {4,5,6};
              static int slen = 3;
              static int8_t ax = -1, ay = -1;
              static uint8_t snakeHue = 96; // Start green

              // Spawn apple
              if (ax == -1) {
                while(true) {
                  ax = random8(MATRIX_WIDTH); ay = random8(MATRIX_HEIGHT);
                  bool onSnake = false;
                  for (int i=0; i<slen; i++) { if (sx[i]==ax && sy[i]==ay) onSnake = true; }
                  if (!onSnake) break;
                }
              }

              // AI Move towards apple
              int8_t hx = sx[0], hy = sy[0];
              if (hx < ax) hx++;
              else if (hx > ax) hx--;
              else if (hy < ay) hy++;
              else if (hy > ay) hy--;

              // Check wall or self collision
              bool dead = false;
              if (hx < 0 || hx >= MATRIX_WIDTH || hy < 0 || hy >= MATRIX_HEIGHT) dead = true;
              for (int i=0; i<slen-1; i++) { if (sx[i]==hx && sy[i]==hy) dead = true; }

              if (dead || slen >= 55) {
                slen = 3; sx[0]=3; sy[0]=4; sx[1]=3; sy[1]=5; sx[2]=3; sy[2]=6; ax = -1;
                snakeHue = random8(32, 224); // Pick a new color (avoiding 0/Red for the apple)
                return;
              }

              // Move body
              for (int i = slen - 1; i > 0; i--) {
                sx[i] = sx[i-1];
                sy[i] = sy[i-1];
              }
              sx[0] = hx; sy[0] = hy;

              // Eat apple
              if (hx == ax && hy == ay) {
                slen++;
                sx[slen-1] = sx[slen-2]; sy[slen-1] = sy[slen-2];
                ax = -1; // respawn
              }

              // Draw
              if (ax != -1) leds[XY(ax, ay)] = CRGB::Red; // Apple
              for (int i = 0; i < slen; i++) {
                // Head is brighter (value 255), body is slightly dimmer (value 150)
                leds[XY(sx[i], sy[i])] = CHSV(snakeHue, 255, (i == 0) ? 255 : 150);
              }
              FastLED.show();
            }
          }
          break;

        case WARP_SPEED:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 150, 20);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              // Fade background
              for(int i = 0; i < NUM_LEDS; i++) leds[i].fadeToBlackBy(80);

              static float starsX[6], starsY[6], starsVX[6], starsVY[6];
              static bool sInit[6] = {false};

              for (int i=0; i<6; i++) {
                if (!sInit[i] || starsX[i] < 0 || starsX[i] >= MATRIX_WIDTH || starsY[i] < 0 || starsY[i] >= MATRIX_HEIGHT) {
                  starsX[i] = 3.0; starsY[i] = 3.5;
                  // Random velocity outward
                  float angle = random(360) * 0.0174533;
                  float speed = random(10, 30) / 20.0;
                  starsVX[i] = cos(angle) * speed;
                  starsVY[i] = sin(angle) * speed;
                  sInit[i] = true;
                }
                
                starsX[i] += starsVX[i];
                starsY[i] += starsVY[i];

                int ix = (int)starsX[i];
                int iy = (int)starsY[i];
                if (ix >= 0 && ix < MATRIX_WIDTH && iy >= 0 && iy < MATRIX_HEIGHT) {
                  leds[XY(ix, iy)] = CRGB::White;
                }
              }
              FastLED.show();
            }
          }
          break;

        case RAIN_RIPPLES:
          {
            uint16_t delayMs = map(pxSpeeds[(int)currentEffect], 1, 100, 150, 20);
            if (now - lastUpdate > delayMs) {
              lastUpdate = now;
              FastLED.clear();

              static int dropX = -1, dropY = 0;
              static int rippleX = -1, rippleRadius = 0;

              // Spawner
              if (dropX == -1 && rippleX == -1) {
                if (random8() < 30) {
                  dropX = random8(MATRIX_WIDTH);
                  dropY = 0;
                }
              }

              // Drop Falling
              if (dropX != -1) {
                leds[XY(dropX, dropY)] = CRGB::Aqua;
                dropY++;
                if (dropY >= MATRIX_HEIGHT) { // Hit bottom
                  rippleX = dropX;
                  rippleRadius = 1;
                  dropX = -1;
                }
              }

              // Ripple expanding
              if (rippleX != -1) {
                bool drewRipple = false;
                if (rippleX - rippleRadius >= 0) { leds[XY(rippleX - rippleRadius, MATRIX_HEIGHT-1)] = CRGB::Blue; drewRipple = true; }
                if (rippleX + rippleRadius < MATRIX_WIDTH) { leds[XY(rippleX + rippleRadius, MATRIX_HEIGHT-1)] = CRGB::Blue; drewRipple = true; }
                
                rippleRadius++;
                if (!drewRipple) rippleX = -1; // Off screen
              }
              
              FastLED.show();
            }
          }
          break;

        case TEXT_SLIDE:
        drawTextSlide(map(pxSpeeds[TEXT_SLIDE], 1, 100, 1500, 200));
        break;
  }
}
