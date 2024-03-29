#include "window.hpp"
#include "ui.hpp"
namespace hc {
    hcwindow::hcwindow(const char* title, int _sizex, int _sizey) : sizex(_sizex) , sizey(_sizey) {
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
        
        if (!glfwInit())
            return;
        
        window = glfwCreateWindow(sizex, sizey, title, NULL, NULL);
        glfwMakeContextCurrent(window);
        glfwSwapInterval(1);
        
		GLenum err = glewInit();
		if (GLEW_OK != err)
		{
		  fprintf(stderr, "Error: %s\n", glewGetErrorString(err));
		}
		
        glViewport(0, 0, sizex, sizey); 

        IMGUI_CHECKVERSION();
		GUI ui;
        ImGui::CreateContext();
        ImGuiIO& io = ImGui::GetIO(); (void)io;
        ImGui::StyleColorsDark();
        ImGui_ImplGlfw_InitForOpenGL(window, true);
        ImGui_ImplOpenGL3_Init("#version 110");
        ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);
        ImGui::GetIO().ConfigFlags |= ImGuiConfigFlags_DockingEnable;

        while (!glfwWindowShouldClose(window))
        {
            glfwPollEvents();
            ImGui_ImplOpenGL3_NewFrame();
            ImGui_ImplGlfw_NewFrame();
            ImGui::NewFrame();

            // CALL UI RENDER FUNCTION HERE

	    	ui.display();
				
            ImGui::Render();
            glfwGetFramebufferSize(window, &sizex, &sizey);
            glViewport(0, 0, sizex, sizey);
            glClearColor(clear_color.x * clear_color.w, clear_color.y * clear_color.w, clear_color.z * clear_color.w, clear_color.w);
            glClear(GL_COLOR_BUFFER_BIT);
            ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

            glfwSwapBuffers(window);
        }

    
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
        glfwTerminate();
        return;
	}
}