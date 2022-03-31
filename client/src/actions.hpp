#pragma once

#include <curl/curl.h>
#include <iostream>

namespace hc{
    class Session{
    public:
        Session():curl(curl_easy_init()), token("9jWYLwQs34B780hVVuWJCoONXvz9n6vKn251rJ5t"), ip("http://2.tcp.ngrok.io:14198") {}
        int register_user(const char* username, const char* email,const char* password);
        void login(const char* email, const char* password);
        void logout();
        void send_message(const char* message);
        char get_messages();
        char get_allusers();

        const char* get_username() {return username;}
        const char* get_email() {return email;}
        const char* get_password() {return password;}
        const char* get_ip() {return ip;}

        bool _islogged_in() {return is_logged_in;}

    private:
        CURL *curl;
        CURLcode res;

        bool is_logged_in;

        const char* username;
        const char* email;
        const char* password;
        const char* token;
        const char* ip;
    };
}