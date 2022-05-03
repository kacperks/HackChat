#include "ui.hpp"

namespace hc{
	void GUI::display(){
		if(!session._islogged_in())
			loginwindow();
		else
			chatwindow();
	}

	void GUI::addmessage(std::string username, std::string message){ chat += "\n" + username + ": " + message;  }
	
    void GUI::loginwindow(){
        if(session._islogged_in() == true) ll = false; else ll = true;
        ImGui::Begin("Welcome to HackChat!", &ll);
        if(option == 0){
        if(ImGui::InputText("Server's IP Adress", ipbuf , IM_ARRAYSIZE(ipbuf))){}
        if(ImGui::InputText("Server's port", portdbuf , IM_ARRAYSIZE(portdbuf))) {}
        if(ImGui::InputText("Server's Secretkey", skbuf , IM_ARRAYSIZE(skbuf))) {}
        if(ImGui::Button("Connect")){ std::string ip = std::string(ipbuf)+":"+std::string(portdbuf); session = Session(ip.c_str(), std::string(skbuf).c_str()); option = 1; } 
        ImGui::SameLine(); if(ImGui::Button("public servers list")) {}
        }else if(option == 1){
        if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}
        if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}
        if(ImGui::Button("Login")){ } ImGui::SameLine(); ImGui::Text("Dont have an account? Then Register"); 
        if(ImGui::Button("Create Account")){ option = 2;  }
        } else if(option == 2) {
        if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}
        if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}
        if (ImGui::InputText("your username", buf3, IM_ARRAYSIZE(buf3))) {}
        if (ImGui::Button("Register")) { session.register_user(std::string(buf3).c_str(), std::string(buf).c_str(), std::string(buf2).c_str()); } ImGui::SameLine();
        if (ImGui::Button("Go Back")) { option = 1; }
        }
        ImGui::End();
    }

    void GUI::chatwindow(){
    	ImGui::Begin("Chat Session", nullptr);
    	ImGui::End();
    }
}
