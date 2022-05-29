#pragma once

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "vendor/imgui.h"
#include "vendor/imgui_impl_glfw.h"
#include "vendor/imgui_impl_opengl3.h"

namespace hc {
    class hcwindow {
		public:
			hcwindow( const char* title,int _sizex, int _sizey);
			hcwindow() { hcwindow("HackChat", 480, 480); }
			int sizex, sizey;
			GLFWwindow* window;
	};
}