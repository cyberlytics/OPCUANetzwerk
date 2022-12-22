#pragma once

/**
 * @project		: OPCUA Sensor Netzwerk im Fach "Web Semantic Technology" Wintersemester 2022/23 Team Gruen
 * @file		: NonAssignable.h
 * @description	:
 *		Grundklasse zum Blockieren des Copy-Konstruktors für Ressourcen-Objekte
 *
 * @author		: Manuel Zimmermann <m.zimmermann1@oth-aw.de>
 * @date		: 2022-12-06 07:59:49
 * @version		: 1.0
 */

class NonAssignable
{
private:
	NonAssignable(NonAssignable const&);
	NonAssignable& operator=(NonAssignable const&);

public:
	NonAssignable() {}
};

