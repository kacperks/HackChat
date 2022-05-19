#pragma once

#include <curl/curl.h>
#include <iostream>

namespace hc{
    struct user{
        std::string username;
        std::string email;
        std::string password;
        int id;
    };

    class Session{
    public: 
        Session();
        Session(const char*_ip, const char*_token):is_logged_in(false), curl(curl_easy_init()), token(_token), ip(_ip) {}
        void register_user(const char* username, const char* email,const char* password);
        void login(const char* email, const char* password);
        void logout();
        void send_message(const char* message);
        char get_last10messages();

        const char* get_username() {return username;}
        const char* get_email() {return email;}
        const char* get_password() {return password;}
        const char* get_ip() {return ip;}

        void set_ip(const char* _ip) {ip = _ip;}
        void set_token(const char* _token) {token = _token;}

        bool _islogged_in() {return is_logged_in;}
        int getuseridbyname(const char* username_);
        int getuseridbyemail(const char* email_);

    private:
        CURL *curl;
        CURLcode res;

        bool is_logged_in;

        const char* username;
        const char* email;
        const char* password;
        const char* token;
        const char* ip;
        int userid;
    };
}
