#pragma once

#include "vendor/imgui.h"
#include "vendor/imgui_impl_glfw.h"
#include "vendor/imgui_impl_opengl3.h"
#include "app.hpp"

namespace hc {
	class GUI {
	public:
		GUI() {}
	
		void init();
		void display();	
		void addmessage(const char* username, const char* message);
		
	private:
		void setstyle();
		void loginwindow();
		void chatwindow();
		void toolbar();
		void dockspace();
	};
}