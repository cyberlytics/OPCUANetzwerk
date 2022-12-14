#include "IICBuffer.h"

#pragma region IICBuffer

void IICBuffer::clear()
{
	_rPtr = _wPtr = 0;
}

uint8_t IICBuffer::size()
{
	return _wPtr;
}

ERROR_t IICBuffer::write(const void* buf, uint8_t size)
{
	uint8_t wPtr = _wPtr;
	if (size > (_size - wPtr)) return ERROR_t::IIC_BUFFER_OVERFLOW;

	memcpy(_buffer + wPtr, buf, size);
	_wPtr = wPtr + size;

	return ERROR_t::GENERAL_OK;
}

ERROR_t IICBuffer::writeByte(uint8_t byte)
{
	uint8_t wPtr = _wPtr;
	if ((_size - wPtr) == 0) return ERROR_t::IIC_BUFFER_OVERFLOW;

	_buffer[wPtr++] = byte;
	_wPtr = wPtr;

	return ERROR_t::GENERAL_OK;
}

ERROR_t IICBuffer::read(void* buf, uint8_t size)
{
	uint8_t wPtr = _wPtr;
	uint8_t rPtr = _rPtr;
	if (size > (wPtr - rPtr)) return ERROR_t::IIC_BUFFER_EMPTY;

	memcpy(buf, _buffer + rPtr, size);
	rPtr += size;

	if (rPtr == wPtr)	_rPtr = _wPtr = 0;
	else				_rPtr = rPtr;

	return ERROR_t::GENERAL_OK;
}

uint8_t IICBuffer::readByte()
{
	uint8_t wPtr = _wPtr;
	uint8_t rPtr = _rPtr;
	if ((wPtr - rPtr) == 0) return 0x00;

	uint8_t res = _buffer[rPtr++];

	if (rPtr == wPtr)	_rPtr = _wPtr = 0;
	else				_rPtr = rPtr;

	return res;
}

#pragma endregion