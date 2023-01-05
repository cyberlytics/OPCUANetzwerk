#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: IICSlave.h
 * @description	:
 *		TODO
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-14 17:25:52
 * @version		: 1.0
 */

#include <Arduino.h>
#include "Error.h"
#include "IICBuffer.h"

extern "C" void USI_START_vect(void)  __attribute__((signal));
extern "C" void USI_OVF_vect(void)	  __attribute__((signal));

typedef ERROR_t(*IICCallback)(IICRequest* request, IICResponse* response);

class IICSlave 
{
private:
	enum IIC_Mode					{ Idle, RecvAdr, RecvData, RecvAdrRestart, SendData, SendError, SendChksm };

	IICCallback						_callback			= NULL;

	uint8_t							_adr				= 0;
	IIC_Mode						_mode				= IIC_Mode::Idle;
	uint8_t                         _chksm				= 0;
	IICRequest						_reqBuf;
	IICResponse						_rspBuf;
	volatile ERROR_t				_lastError			= ERROR_t::GENERAL_OK;

	inline void						reset();
	inline bool						isStop();
	inline void						sendACK(bool receiveNext);
	inline bool						getACK();

	void							startDetected();
	void							dataCompleted();

	friend void						USI_START_vect(void);
	friend void						USI_OVF_vect(void);

public:
	ERROR_t							begin(uint8_t address, IICCallback callback);
};

extern IICSlave IIC;

