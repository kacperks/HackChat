#pragma once

#include "vendor/imgui.h"
#include "vendor/imgui_impl_glfw.h"
#include "vendor/imgui_impl_opengl3.h"
#include "app.hpp"

namespace hc {
	class GUI {
	public:
		GUI() : chat("hc"){}
	
		void init();
		void display();	
		void addmessage(std::string username, std::string message);
		
	private:
		void setstyle();
		void loginwindow();
		void chatwindow();
		void toolbar();
		void dockspace();
		
		std::string chat;
		char buf[40]; char buf3[40];
		char buf2[40]; bool ll2;
		char sendbuf[100];
		int option = 0; bool ll; 
		char ipbuf[30];
		char portdbuf[10];
		char skbuf[40];
	};
}
