#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: IIICCallable.h
 * @description	:
 *		Implementiert eine Callable Schnittstelle, um I2C Messages in Unterklassen zu verarbeiten
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-15 07:47:13
 * @version		: 1.0
 */

#include <Arduino.h>
#include "Error.h"
#include "IICBuffer.h"
#include "NonAssignable.h"

enum Function : uint8_t {		//Data Package [] = optional, {} = datatype, () = default Value
	HEARTBEAT			=   1,	

	IOPIN_DIGITAL_IN	=  10,	// {byte}10, {byte}GPIO,  [{bool}pullup(false)] | {bool}value
	IOPIN_DIGITAL_OUT	=  11,	// {byte}11, {byte}GPIO,   {bool}value          | 
	 
	ADCPIN_SAMPLE		=  20,	// {byte}20, {byte}presc,  {byte}ref		    | {uint16_t}value
};

class IIICCallable : private NonAssignable {
public:
	virtual ERROR_t					call(Function func, IICRequest* req, IICResponse* rsp);
};