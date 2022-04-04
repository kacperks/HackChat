#pragma once

#include "vendor/imgui.h"
#include "vendor/imgui_impl_glfw.h"
#include "vendor/imgui_impl_opengl3.h"
#include "app.hpp"


char buf[40];
char buf2[40];
int option = 1; 

namespace hc {
    void set_style(){

    }
    void drawstartup(){
            bool ll; if(session._islogged_in() == true) ll = false; else ll = true;
            ImGui::Begin("Welcome to HackChat!", &ll);
            if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}
            if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}
            if(ImGui::Button("Login")){ session.login(buf, buf2); } ImGui::SameLine(); ImGui::Text("Dont have an account? Then Register"); 
            if(ImGui::Button("Create Account")){ }
            ImGui::End();
    }
}