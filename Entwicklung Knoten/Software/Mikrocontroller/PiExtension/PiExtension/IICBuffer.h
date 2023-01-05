#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: IICBuffer.h
 * @description	:
 *		TODO
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-06 12:58:59
 * @version		: 1.0
 */

#include <Arduino.h>
#include "Error.h"
#include "NonAssignable.h"

class IICSlave;

#define BUFFER_SIZE	16

#pragma region IICBuffer

class IICBuffer
{
private:
	uint8_t							_wPtr				= 0;
	uint8_t							_rPtr				= 0;
	uint8_t							_buffer[BUFFER_SIZE];

protected:
	ERROR_t							write(const void *buf, uint8_t size);
	ERROR_t							writeByte(uint8_t byte);

	ERROR_t							read(void *buf, uint8_t size);
	uint8_t							readByte();

public:
	void							clear();
	uint8_t							size();

	friend class					IICSlave;
};

#pragma endregion

#pragma region IICRequest

class IICRequest : public IICBuffer {
public:	
	template<typename Type>
	inline ERROR_t					read(Type& var);
	inline ERROR_t					read(void *var, uint8_t size);
};

template<typename Type>
inline ERROR_t IICRequest::read(Type& var)
{
	return IICBuffer::read(&var, sizeof(Type));
}

inline ERROR_t IICRequest::read(void *var, uint8_t size)
{
	return IICBuffer::read(var, size);
}

#pragma endregion

#pragma region IICResponse

class IICResponse : public IICBuffer {
public:
	template<typename Type>
	inline ERROR_t					write(Type var);
	inline ERROR_t					write(const void *var, uint8_t size);
};

template<typename Type>
inline ERROR_t IICResponse::write(Type var)
{
	return IICBuffer::write(&var, sizeof(Type));
}

inline ERROR_t IICResponse::write(const void *var, uint8_t size)
{
	return IICBuffer::write(var, size);
}

#pragma endregion
