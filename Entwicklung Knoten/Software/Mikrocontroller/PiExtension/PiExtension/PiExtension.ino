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
#include "SLTask.h"
#include "IICSlave.h"

#include "ATTINY_x4_Register.h"

#define IIC_ADDRESS 100

enum CMD : uint8_t {
	Heartbeat =   1,
};

ERROR_t iic_received(IICRequest* req, IICResponse* rsp);
ERROR_t cmd_heartbeat(IICRequest* req, IICResponse* rsp);



ERROR_t iic_received(IICRequest* req, IICResponse* rsp) {
	ERROR_t e;
	uint8_t cmd;

	if((e = req->read(cmd)) != ERROR_t::GENERAL_OK) return e;

	switch (cmd) {
		case CMD::Heartbeat:	return cmd_heartbeat(req, rsp);
		default:				return ERROR_t::UNKNOWN_CMD;
	}
}

ERROR_t cmd_heartbeat(IICRequest* req, IICResponse* rsp) {
	for (int i = 0; i < req->size(); i++) {
		ERROR_t e;
		byte b;

		if ((e = req->read(b))  != ERROR_t::GENERAL_OK) return e;
		if ((e = rsp->write(b)) != ERROR_t::GENERAL_OK) return e;
	}

	return ERROR_t::GENERAL_OK;
}


int main() {
	HW::port_b->ddr  |=  (1 << 2);
	HW::port_b->port &= ~(1 << 2);

	IICSlave iic(IIC_ADDRESS, iic_received);

	for (;;) {
		SLTask::proceedTasks();
	}
	return 0;
}