#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <iostream>
#include <sstream> 
#include <Magick++.h>
#include <math.h>
#include <gtkmm.h>



void on_button_clicked()
{
    std::cout << "Hello World" << std::endl;
	
}




class MainWindow :public Gtk::Window {
		public:
				MainWindow();
		protected:

				void Stisknito();
				void NextFrameVybrat();

				Gtk::Label		napis;
				Gtk::Label		napisB;
				Gtk::Label		napisC;
				Gtk::Label		napisD;
				Gtk::Button 	tlac;
				Gtk::Button 	tlac2;
				Gtk::VBox		obalka;
				Gtk::HBox		oblka_panel;
				Gtk::VBox		v_box[10];
				Gtk::HBox		h_box[10];
				Gtk::ScrolledWindow l_panel;
				Gtk::VBox		l_panel_layout;
				Gtk::Frame		l_panel_layout_frame[10];
				Gtk::Button 	l_panel_layout_next[10];
				Gtk::DrawingArea	canvas_area;
				Gtk::Statusbar	status_bar;
				Gtk::RadioButton	radio_button[100];
				Gtk::RadioButton::Group		group_typ_zapracovani;



};

MainWindow::MainWindow(){


	set_default_size(800, 600);
	set_title("Linux Sky Stacker v.0.1 - ");


	tlac.set_label("Tlacitko");
	tlac2.set_label("Tlacitko2");
	napis.set_label("Tady bude Menu ........................................");
	//napis.override_color (GTK_STATE_FLAGS_NORMAL, Gdk::RGBA(1.0 , 0.0 , 0.0, 1.0);
	napisB.set_label("Tady bude StatusLine ........................................");
	napisC.set_label("Tady bude Sbbbb");
	napisD.set_label("Tady bude aaa.");
	//canvas_area.set_size_request(get_width()-65,get_width()-65);
	status_bar.push("Tohle je status bar");
	l_panel_layout_frame[1].set_label("Typ zparcovani");
	l_panel_layout_frame[1].set_border_width(10);
	l_panel_layout_frame[1].set_size_request(100,50);
	l_panel_layout_next[1].set_label("Dalsi");

	radio_button[1].set_label("Zarovnani hvezd");
	radio_button[2].set_label("Zarovnani na jine objekty");
	radio_button[3].set_label("StarTrails");
	radio_button[4].set_label("Reserved");
	radio_button[5].set_label("Reserved");
	radio_button[6].set_label("Manually");

	radio_button[1].set_group(group_typ_zapracovani);
	radio_button[2].set_group(group_typ_zapracovani);
	radio_button[3].set_group(group_typ_zapracovani);
	radio_button[4].set_group(group_typ_zapracovani);
	radio_button[5].set_group(group_typ_zapracovani);
	radio_button[6].set_group(group_typ_zapracovani);



		add(obalka);
			obalka.pack_start(napis);
			obalka.pack_start(oblka_panel);
				oblka_panel.pack_start(l_panel);
					l_panel.add(l_panel_layout);
						l_panel_layout.pack_start(l_panel_layout_frame[1]);
							l_panel_layout_frame[1].add(v_box[1]);
								v_box[1].pack_start(radio_button[1]);							// Align stars
								v_box[1].pack_start(radio_button[2]);							// Align other
								v_box[1].pack_start(radio_button[3]);							// Startrails
	//							v_box[1].pack_start(radio_button[4]);							// Reserved
	//							v_box[1].pack_start(radio_button[5]);							// Reserved
								v_box[1].pack_start(radio_button[6]);							// Manually
								v_box[1].pack_start(l_panel_layout_next[1]);
				oblka_panel.pack_start(canvas_area);
			obalka.pack_start(status_bar);
        show_all_children();


        //tlac.signal_clicked().connect(sigc::mem_fun(*this, &MainWindow::Stisknito));
			//tlac.signal_clicked().connect(sigc::ptr_fun(&on_button_clicked));
		
		l_panel_layout_next[1].signal_clicked().connect(sigc::mem_fun(*this, &MainWindow::NextFrameVybrat));
        
}

//---------------------------------------------------------------------
// Hlavni funkce konzolove aplikace
//---------------------------------------------------------------------
int main(int argc, char **argv)
{


        Gtk::Main kit(argc, argv);
        MainWindow okno;
        Gtk::Main::run(okno);
        return 0;


}



void MainWindow::Stisknito(){

	std::cout << "AHOJ, naco bylo stisknuto" <<  std::endl;
	tlac2.hide();
	v_box[1].pack_start(radio_button[5]);
	show_all();
}



void MainWindow::NextFrameVybrat(){
	l_panel_layout.pack_start(l_panel_layout_frame[2]);
	l_panel_layout_frame[2].set_label("Vyber souborů");
	l_panel_layout_frame[2].set_border_width(10);
	show_all();

}