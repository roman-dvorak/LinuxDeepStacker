#------------------------------------------------------------------------------

SOURCE=LinuxSkyStacker.cpp
MYPROGRAM=LinuxSkyStacker
ARG_magick=`Magick++-config --cppflags --cxxflags --ldflags --libs`
ARG_lbt=-lbluetooth
ARG_glut=-L/usr/X11R6/lib -lglut -lGL -lGLU -lm -lX11 -lXmu
ARG_gtkmm=`pkg-config gtkmm-3.0 --cflags --libs`
CC=g++

#------------------------------------------------------------------------------

$(MYPROGRAM): $(SOURCE)

	$(CC) $(SOURCE) -o $(MYPROGRAM) $(ARG_gtkmm) $(ARG_magick) -lSOIL -I /usr/include/SOIL