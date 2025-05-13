#include <Arduino.h>
#include <SD.h>
#include "EmotiBit.h"
#include "SharedVitals.h"

#define SERIAL_BAUD    115200
#define LOG_FILENAME   "/test_LEESEUNGHUN_M25_nE3W2.csv"
const unsigned long LOG_INTERVAL = 1000;  // ms

EmotiBit emotibit;
bool     sdAvailable = false;
unsigned long lastLogTime = 0;

void setup() {
    Serial.begin(SERIAL_BAUD);
    while (!Serial);

    emotibit.setup();
    emotibit.acquireData.eda       = true;
    emotibit.acquireData.heartRate = true;

    sdAvailable = emotibit.setupSdCard(false);
    if (!sdAvailable) {
        Serial.println("ERROR: SD 카드 초기화 실패");
    } else if (!SD.exists(LOG_FILENAME)) {
        File headerFile = SD.open(LOG_FILENAME, FILE_WRITE);
        if (headerFile) {
            headerFile.println("timestamp_ms,eda_uS,hr_bpm,ibi_ms");
            headerFile.close();
        } else {
            Serial.println("ERROR: 헤더 파일 열기 실패");
        }
    }

    lastLogTime = millis();  // 초기화
}

void loop() {
    unsigned long now = millis();
    emotibit.update();  // 센서 데이터는 매 루프마다 갱신해도 무방

    // LOG_INTERVAL 경과 시점에만 기록
    if (now - lastLogTime >= LOG_INTERVAL) {
        lastLogTime += LOG_INTERVAL;  // 드리프트 보정

        // SharedVitals 값 읽기
        unsigned long ts   = now;
        float eda          = SharedVitals::eda;
        float hr           = SharedVitals::heartRate;
        float ibi          = SharedVitals::ibi;

        // 시리얼 출력
        Serial.printf("EDA: %.2f uS | HR: %.1f bpm | IBI: %.0f ms\n",
                      eda, hr, ibi);

        // SD 카드에 기록
        if (sdAvailable) {
            File logFile = SD.open(LOG_FILENAME, FILE_APPEND);
            if (logFile) {
                logFile.printf("%lu,%.2f,%.1f,%.0f\n", ts, eda, hr, ibi);
                logFile.close();
            } else {
                Serial.println("ERROR: 로그 파일 열기 실패");
            }
        }
    }
}
