#include <GL/glut.h>    // hlavickovy soubor funkci GLUTu
#include <GL/gl.h>  // Header File For The OpenGL32 Library
#include <GL/glu.h> // Header File For The GLu32 Library
#include "glui.h"
#include <SOIL.h>
#include <sstream>
#include <math.h>
#include <string.h>


//////////////////////////////////////////////////////////////////////////////////////////
		//																				//
		//							VYPISE TEXT NA OBRAZOVKU							//
		//																				//
		//	//	x - Xova souradnice														//
		//	//	y - Yova souradnice														//
		//	//	*font - font z GLUT knihovny; sezanm http://www.opengl.org/resources/libraries/glut/spec3/node76.html
		//	//	*string - retezec vypisovaneho textu									//
		//																				//
//////////////////////////////////////////////////////////////////////////////////////////

void renderBitmapString(float x, float y, void *font,const char *string){
	const char *c;
	glRasterPos2f(x, y);
	for (c=string; *c != '\0'; c++) {
		glutBitmapCharacter(font, *c);
	}
}


std::string IntToString(int N)
{
	std::stringstream ss("");
	ss << N;
	return ss.str();
}






void get_sun_pos(float lat, float lon, char dt_type, float mo, float da, float hour, float minute, float *alt, float *az){
   /*
	   calculate the Sun's altitude and azimuth	
		inputs: 'lat'itude, 'lon'gitude, dt_type('u'|'l'), 'mo'nth, 'da'y, hour, minute
		dt_type contains 'u'tc date/time, or 'l'ocal date/time flag indicating whether mo, da, hour and minute are utc or local
	   outputs: 'alt'itude, 'az'imuth 
		code based upon Prof. Richard B. Goldstein's sun position calculator at http://www.providence.edu/mcs/rbg/java/sungraph.htm
		Appears to give fairly accurate results for the next 10 years or so
	*/

	float ti, local_hour;
	
	if (dt_type == 'l')	local_hour = hour; 
	else /* dt_type == 'u' */
	{
		/* calculate local date/time from utc date/time */
		float time_offset = round(lon / 15); //longitude -> hours
		local_hour = hour + time_offset;

		//adjust hour, day, month as needed (ignore years and seconds)...  
		if (local_hour < 0){
			local_hour += 24;
			da--;
			if (da < 1){
				mo--;
				if (mo < 1) mo = 12;
				da = (mo==4||mo==6||mo==9||mo==11)?30:(mo==1||mo==3||mo==5||mo==7||mo==10)?31:28;
			}
		}
		else if (local_hour > 23){
			local_hour -= 24;
			da++;
			if (da > (mo==4||mo==6||mo==9||mo==11)?30:(mo==1||mo==3||mo==5||mo==7||mo==10)?31:28){
				mo++;
				if (mo > 12) mo = 1;
				da = 1;
			}
		}
		
	}
	
	//total hours and minutes and adjust for +/- offset from noon...
   ti = (local_hour + minute / 60) - 12;
	  
	float pi180=M_PI/180;
	float adjtime;
	float za[] = {-0.5,30.5,58.5,89.5,119.5,150.5,180.5,211.5,242.5,272.5,303.5,333.5}; // days from jan at noon
	float zi;
	float zzi;
	float cth; // cosine of latitude
	float sth; // sine of latitude
	float cph; 
	float sph;
	float cti;
	float sti;
	float x;
	float y;
	float loc;
	float phi;
	float sin_tau, cos_tau;

	loc = round(lon / 15) * 15; // 
	adjtime = (lon - loc) / 40; // offset 
	zi = za[(int)mo - 1];       // 
	zzi = 360 * (zi + 0.5 + da - 82) / 365; // 
	cos_tau = cos(zzi * pi180);
	sin_tau = sin(zzi * pi180);
	phi = acos(cos_tau * cos_tau + sin_tau * sin_tau * cos(23.45 * pi180)); // formula for sun declination (varies +/- 23.45 deg. over a year)
	phi = round(1000 * phi / pi180) / 1000; //
	if (sin_tau < 0){phi = -phi;}// sign +/- depends on the time of year   
	ti = ti * 15; // hours +/- offset from noon to degrees from Prime Meridian
	cth = cos(lat * pi180);
	sth = sin(lat * pi180);
	cph = cos(phi * pi180);
	sph = sin(phi * pi180);
	cti = cos(ti * pi180);

	//altitude = sin-1(sin theta * sin phi + cos theta * cos phi * cos tau)

	*alt = sth * sph + cth * cph * cti;
	*alt = asin(*alt) / pi180;
	*alt = round(1000 * *alt) / 1000;

	//azimuth = tan-1(-x'/y')=tan-1(cos phi sin tau/(cos theta sin phi - sin theta cos phi cos tau))

	sti = sin(ti * pi180);
	x = -cph * sti;
	y = cth * sph - sth * cph * cti;
	*az = 90 - atan2(y, x) / pi180;
	if(*az < 0) *az = *az + 360;
	*az = round(1000 * *az) / 1000;
}


void Pozadi()
{
	float Pozadi_alt, Pozadi_az;
	get_sun_pos(49, 14, 'u', 10, 29, 20, 20, &Pozadi_alt, &Pozadi_az);

	if (Pozadi_alt < 18.0)
	{
		glClearColor(0.45, 0.02, 0.06, 0.0);
	}else{
		glClearColor(0.18, 0.27, 0.41, 0.0);
	}

	glClear(GL_COLOR_BUFFER_BIT);   

	int krokH, pocetH;
	int krokV, pocetV;

	pocetH = glutGet(GLUT_SCREEN_HEIGHT_MM)/15;
	krokH = glutGet(GLUT_WINDOW_HEIGHT)/pocetH;

	pocetV = glutGet(GLUT_SCREEN_WIDTH_MM)/15;
	krokV = glutGet(GLUT_WINDOW_WIDTH)/pocetV;
	
	if (Pozadi_alt < 18.0)
	{
		glColor3f(0.7f, 0.04f, 0.04f);
	}else{
		glColor3f(0.28f, 0.37f, 0.52f);
	}

	glBegin(GL_LINES);
	for (int i = 0; i < pocetH; ++i)
	{
		glVertex2i(0,krokH*i+krokH/2);
		glVertex2i(glutGet(GLUT_WINDOW_WIDTH),krokH*i+krokH/2);
	}
	for (int i = 0; i < pocetV; ++i)
	{
		glVertex2i(krokV*i+krokV/2,0);
		glVertex2i(krokV*i+krokV/2,glutGet(GLUT_WINDOW_WIDTH));
	}
	glEnd();
}


void MainScreenInit(){

	glClearColor(0.2f, 0.2f, 0.2, 0.0);

glClear(GL_COLOR_BUFFER_BIT);
glColor3f(0.2f, 0.2f, 0.2f);

glBegin(GL_TRIANGLES);                      // vykresleni klasickeho RGB trojuhelniku
		glColor3f(1.0f, 0.0f, 0.0f);
		glVertex2i(30, 20);
		glColor3f(0.0f, 1.0f, 0.0f);
		glVertex2i(505, 50);
		glColor3f(0.0f, 0.0f, 1.0f);
		glVertex2i(327, 322);
	glEnd();
	glFlush(); 



}