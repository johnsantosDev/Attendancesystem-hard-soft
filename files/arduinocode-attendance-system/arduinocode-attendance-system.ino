
#include <SoftwareSerial.h>
#include <SPI.h>
#include <SD.h> 
#include "LiquidCrystal_I2C.h"
#include "MFRC522.h"
#include "MFRC522Extended.h"
#include "RTClib.h"


#define CS_RFID 10
#define RST_RFID 9
#define CS_SD 4
#define I2C_ADDR 0x27
LiquidCrystal_I2C lcd(I2C_ADDR, 20, 4);
MFRC522 rfid(CS_RFID, RST_RFID); 

File myFile;
String uidString;
RTC_DS1307 rtc;

const int checkInHour =22;
const int checkInMinute = 5;
int userCheckInHour;
int userCheckInMinute;

const int redLED = 6;
const int greenLED = 7;
const int buzzer = 5;
const int lcdpot = A0;

void setup() {
  pinMode(redLED, OUTPUT);  
  pinMode(greenLED, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  Serial.begin(9600);
  lcd.begin(16,2);
  while(!Serial); 
  SPI.begin(); 
  rfid.PCD_Init(); 
  Serial.print("checking SD card.........");
  lcd.setCursor(0, 2);
  lcd.print("ATTENDANCE SYSTEM");
  lcd.clear()
  lcd.setCursor(0, 2);
  lcd.print("Initializing SD...");
  delay(1000);
  lcd.clear();
  if(SD.begin(CS_SD)){
    Serial.println("SD Ready for write...");
    lcd.setCursor(0, 2);
    lcd.print("SD Ready for write");
    }
  else if(!SD.begin(CS_SD)) {
    Serial.println("Data storage unavailable.... failure!");
    lcd.setCursor(0, 2);
    lcd.print("Unable to Store data");
    //return;
  }
  if(!rtc.begin()) {
    Serial.println("RealTime unavailable");
    lcd.setCursor(0,3);
    lcd.print("RealTime unavailable");
    while(1);
  }
  else {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  if(!rtc.isrunning()) {
    Serial.println("RealTime Running failed");
    lcd.setCursor(0,3);
    lcd.print("RealTime failure");
  }
  else {
    Serial.println("Running system on RealTime Clock...");
    lcd.setCursor(0,3);
    lcd.print("running RealTime");
    }
}

void loop() {
  //show title each second 
  lcd.setCursor(0, 1);
  lcd.print("ATTENDANCE SYSTEM");
  lcd.setCursor(0, 4);
  lcd.print("");//date and time
  //look for new cards
  if(rfid.PICC_IsNewCardPresent()) {
    readRFID();
    logCard();
    verifyCheckIn();
  }
  delay(10);
}

void readRFID() {
  rfid.PICC_ReadCardSerial();
  lcd.clear();
  Serial.print("Tag UID: ");
  lcd.print("Tag UID: ");
  uidString = String  ("Roll number" ) +(rfid.uid.uidByte[0]);
  Serial.println(uidString);
  lcd.setCursor(0, 1);
  lcd.print(uidString);
  delay(2000);
 
  
  tone(buzzer, 2000); 
  delay(200);        
  noTone(buzzer);
  
  delay(200);
}

void logCard() {
  
  digitalWrite(CS_SD,LOW);
  
  
  myFile=SD.open("Class 9B log.txt", FILE_WRITE);

 
  if (myFile) {
    Serial.println("File opened ok");
    lcd.clear();
    lcd.print("File opened ok");
    delay(2000);
    myFile.print(uidString);
    myFile.print(", ");   
    
    
    DateTime now = rtc.now();
    myFile.print(now.year(), DEC);
    myFile.print('/');
    myFile.print(now.month(), DEC);
    myFile.print('/');
    myFile.print(now.day(), DEC);
    myFile.print(',');
    myFile.print(now.hour(), DEC);
    myFile.print(':');
    myFile.println(now.minute(), DEC);
    
   
    Serial.print(now.year(), DEC);
    Serial.print('/');
    Serial.print(now.month(), DEC);
    Serial.print('/');
    Serial.print(now.day(), DEC);
    Serial.print(' ');
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.println(now.minute(), DEC);
    Serial.println("sucessfully written on SD card");

    lcd.clear();
    lcd.print(now.year(), DEC);
    lcd.print(':');
    lcd.print(now.month(), DEC);
    lcd.print(':');
    lcd.print(now.day(), DEC);
    lcd.print(' ');
    lcd.setCursor(11, 0);
    lcd.print(now.hour(), DEC);
    lcd.print(':');
    lcd.print(now.minute(), DEC);
    lcd.setCursor(0, 1);
    lcd.print("Written on SD...");
    delay(2000);
    
    myFile.close();

    // Save check in time;
    userCheckInHour = now.hour();
    userCheckInMinute = now.minute();
  }
  else {
    
    Serial.println("error opening data.txt");  
    lcd.clear();
    lcd.print("error opening data.txt");
  }
  // Disables SD card chip select pin  
  digitalWrite(CS_SD,HIGH);
}

void verifyCheckIn(){
  if((userCheckInHour < checkInHour)||((userCheckInHour==checkInHour) && (userCheckInMinute <= checkInMinute))){
    digitalWrite(greenLED, HIGH);
    delay(2000);
    digitalWrite(greenLED,LOW);
    Serial.println(" welcome!");
    lcd.clear();
    lcd.print(" Welcome!");
  }
  else{
    digitalWrite(redLED, HIGH);
    delay(2000);
    digitalWrite(redLED,LOW);
    Serial.println("You are late...");
    lcd.clear();
    lcd.print("You are Late...");
    delay(3000);
    lcd.clear();
    lcd.print("Put RFID to Scan");
  }
}
