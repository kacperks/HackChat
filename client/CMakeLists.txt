cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(hc-client)

if(WIN32)
add_subdirectory(thirdparty/curl)
add_subdirectory(thirdparty/glfw)
endif (WIN32)
include_directories(thirdparty/curl/include)
include_directories(thirdparty/glfw/include)

file(GLOB_RECURSE src "src/**.cpp" "src/**.hpp" "src/**.h")

add_executable(${PROJECT_NAME} ${src})

if(WIN32) # WINDOWS
target_link_libraries(${PROJECT_NAME} glad glfw3 libcurl)
endif(WIN32)

if(UNIX AND NOT APPLE) # LINUX 
target_link_libraries(${PROJECT_NAME} GL GLEW glfw curl)
endif()
