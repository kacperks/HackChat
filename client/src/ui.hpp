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
	};
}