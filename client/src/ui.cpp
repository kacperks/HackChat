#include "ui.hpp"

char buf[40]; char buf3[40];
char buf2[40]; bool ll2;
int option = 1; bool ll; 

namespace hc{
	
    void GUI::loginwindow(){
        if(session._islogged_in() == true) ll = false; else ll = true;
        ImGui::Begin("Welcome to HackChat!", &ll);
        if(option == 1){
        if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}
        if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}
        if(ImGui::Button("Login")){ } ImGui::SameLine(); ImGui::Text("Dont have an account? Then Register"); 
        if(ImGui::Button("Create Account")){ option = 0;  }
        } else if(option == 0) {
        if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}
        if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}
        if (ImGui::InputText("your username", buf3, IM_ARRAYSIZE(buf3))) {}
        if (ImGui::Button("Register")) {}
        }
        ImGui::End();
    }

    void GUI::chatwindow(){
    	ImGui::Begin("Chat Session");
    	ImGui::BeginChild("Scrolling");
    	for (int n = 0; n < 50; n++)
    	    ImGui::Text("%04d: Some text", n);
    	ImGui::EndChild();
    	ImGui::End();
    }
}