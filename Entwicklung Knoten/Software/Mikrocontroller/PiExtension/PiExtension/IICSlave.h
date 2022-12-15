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
#include "SLTask.h"
#include "IICBuffer.h"

#define IIC_RECV_BUFFER_SIZE	16
#define IIC_SEND_BUFFER_SIZE	 8 //TODO ZUM TESTEN KLEINER ALS RECV BUFFER -> Wieder auf 16 zurückstellen!!!

typedef ERROR_t(*IICCallback)(IICRequest* request, IICResponse* response);

class IICSlave : private SLTask 
{
private:
	enum IIC_Mode					{ Idle, RecvAdr, RecvData, RecvAdrRestart, SendData, SendError, SendChksm };

	IICCallback						_callback			= NULL;

	ERROR_t							_cfgError			= ERROR_t::GENERAL_OK;
	const uint8_t					_adr				= 0;
	IIC_Mode						_mode				= IIC_Mode::Idle;
	uint8_t                         _chksm				= 0;
	IICRequest						_reqBuf				= IICRequest(IIC_RECV_BUFFER_SIZE);
	IICResponse						_rspBuf				= IICResponse(IIC_SEND_BUFFER_SIZE);
	volatile ERROR_t				_lastError			= ERROR_t::GENERAL_OK;

	inline void						reset();
	inline bool						isStop();
	inline void						sendACK(bool receiveNext);
	inline bool						getACK();

	void							startDetected();
	void							dataCompleted();
protected:
	virtual void					proceed() override;


public:
									IICSlave(uint8_t address, IICCallback callback);
};

