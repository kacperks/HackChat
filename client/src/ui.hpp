#pragma once

#include "vendor/imgui.h"
#include "vendor/imgui_impl_glfw.h"
#include "vendor/imgui_impl_opengl3.h"
#include "app.hpp"


namespace hc {
    void drawstartup(){
        if(!session._islogged_in()){
            int option = 1;
            ImGui::Begin("Welcome to HackChat!");
            if(option == 0){
                if(ImGui::Button("Login")){
                    option = 1;
                }
                if(ImGui::Button("Register")){
                    option = 2;
                }
            }
            else if(option == 1){
                char buf[20];
                if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}

                char buf2[20];
                if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}

                if(ImGui::Button("Login")){
                   // session.login(input.c_str(), input2.c_str());
                }
            }

            ImGui::End();
        }
    }
}