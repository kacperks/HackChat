cmake_minimum_required(VERSION 3.16 FATAL_ERROR)

project(hc-client)

if (WIN32)
    set(PLATFORM "Windows")
endif (WIN32)

if(UNIX AND NOT APPLE)
    set(PLATFORM "Linux")
endif()

add_subdirectory(thirdparty/curl)
add_subdirectory(thirdparty/glfw)
add_subdirectory(thirdparty/glad)

include_directories(thirdparty/curl/include)
include_directories(thirdparty/glfw/include)
include_directories(thirdparty/glad/include)

file(GLOB_RECURSE src "src/**.cpp" "src/**.hpp" "src/**.h")

add_executable(${PROJECT_NAME} ${src})
target_link_libraries(${PROJECT_NAME} glad glfw3 libcurl)