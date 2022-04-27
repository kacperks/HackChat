#include "ui.hpp"

char buf[40]; char buf3[40];
char buf2[40]; bool ll2;
char sendbuf[100];
int option = 1; bool ll; 

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
        if(option == 1){
        if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}
        if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}
        if(ImGui::Button("Login")){ } ImGui::SameLine(); ImGui::Text("Dont have an account? Then Register"); 
        if(ImGui::Button("Create Account")){ option = 0;  }
        } else if(option == 0) {
        if (ImGui::InputText("your e-mail", buf, IM_ARRAYSIZE(buf))) {}
        if (ImGui::InputText("your password", buf2, IM_ARRAYSIZE(buf2))) {}
        if (ImGui::InputText("your username", buf3, IM_ARRAYSIZE(buf3))) {}
        if (ImGui::Button("Register")) { session.debuglogin(); } ImGui::SameLine();
        if (ImGui::Button("Go Back")) { option = 1; }
        }
        ImGui::End();
    }

    void GUI::chatwindow(){
    	ImGui::Begin("Chat Session", nullptr);
    	ImGui::TextColored(ImVec4(1,0,1,1), "HackChat v0.1");
    	ImGui::BeginChild("Scrolling");
    	ImGui::Text(chat.c_str());
    	ImGui::EndChild();
		if(ImGui::InputText("Your Message", sendbuf, IM_ARRAYSIZE(sendbuf))) {}
		ImGui::SameLine();
		if(ImGui::Button("Send")) { addmessage("jol", std::string(sendbuf)); }
    	
    	ImGui::End();
    }
}