/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: PIExtension.ino
 * @description	:
 *		Implementiert das Hauptprogramm des Mikrocontrollers auf der Erweiterungsplatine für einen Sensorknoten.
 *		Steuert die GPIOs des 5V Sensor-Interfaces. Implementiert verschiedene Funktionen zum Ansteuern/Auslesen
 *		von Sensoren/Aktoren.
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-06 07:10:12
 * @version		: 1.0
 */

#include <Arduino.h>
#include "ATTINY_x4_Register.h"
#include "SLTask.h"
#include "IICSlave.h"
#include "IIICCallable.h"
#include "ADCPin.h"
#include "PWM8Pin.h"



#define OSC_CALIBRATION		128
#define IIC_ADDRESS			100
#define N_GPIOS				5



ERROR_t iic_heartbeat(IICRequest* req, IICResponse* rsp);
ERROR_t iic_received(IICRequest* req, IICResponse* rsp);
int main();

ADCPin	gpio0(HW::port_a, 3); //GPIO0_5V
ADCPin	gpio1(HW::port_a, 2); //GPIO1_5V
ADCPin	gpio2(HW::port_a, 1); //GPIO2_5V
ADCPin	gpio3(HW::port_a, 0); //GPIO3_5V
PWM8Pin gpio4(HW::port_b, 2); //Sound Signal

IIICCallable* gpios[N_GPIOS]{ &gpio0, &gpio1, &gpio2, &gpio3, &gpio4 };


//Schreibt alle empfangenen Bytes wieder zurück
ERROR_t iic_heartbeat(IICRequest* req, IICResponse* rsp) {
	uint8_t len = req->size();
	for (uint8_t i = 0; i < len; i++) {
		ERROR_t e;
		byte b;
		
		if ((e = req->read(b))  != ERROR_t::GENERAL_OK) return e;
		if ((e = rsp->write(b)) != ERROR_t::GENERAL_OK) return e;
	}

	return ERROR_t::GENERAL_OK;
}

ERROR_t iic_received(IICRequest* req, IICResponse* rsp) {
	ERROR_t e;

	//Erstes Byte entspricht cmd
	uint8_t cmd;
	if ((e = req->read(cmd)) != ERROR_t::GENERAL_OK) return e;
	if (cmd == Function::HEARTBEAT) return iic_heartbeat(req, rsp); //Heartbeat? -> Eingabepuffer 1:1 wieder zurückschreiben

	///Ab hier entspricht 2tes Byte der GPIO-Pinnummer
	uint8_t gpioNr;
	if ((e = req->read(gpioNr)) != ERROR_t::GENERAL_OK) return e;
	if (gpioNr >= N_GPIOS) return ERROR_t::GPIO_NOT_EXISTING;
	return gpios[gpioNr]->call((Function)cmd, req, rsp); //GPIO ansprechen
}

int main() {
	//INIT 
	HW::sys->osccal = OSC_CALIBRATION;
	IIC.begin(IIC_ADDRESS, iic_received);
	
	sei();
	
	//LOOP
	for (;;) {
		SLTask::proceedTasks();
	}
	
	return 0;
}