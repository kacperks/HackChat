#include "actions.hpp"

namespace hc{
    void Session::register_user(const char* username, const char* email, const char* password){
        this->username = username;
        this->email = email;
        this->password = password;

        std::string url = std::string(ip) + "/user";
        if (curl) {

        std::string body = "{\"username\":\"" + std::string(username) + "\",\"email\":\"" + std::string(email) + "\",\"password\":\"" + std::string(password) + "\",\"token\":\"" + std::string(token) + "\"}";

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, body.size());
        curl_easy_setopt(curl, CURLOPT_POST, 1L);

        res = curl_easy_perform(curl);
        
        }
        std::cout << res << std::endl;
    }
    void Session::login(const char* email, const char* password){
        this->email = email;
        this->password = password;
        /*
        std::string url = std::string(ip) + "/usermail/" + std::string(email);
        

        if (curl) {

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POST, 0L);
        std::string data = std::string("{\r\n    \"token\": \"") + std::string(token) + std::string(" \"\r\n}");
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
        res = curl_easy_perform(curl);
        if (&res["password"] == password) {
            is_logged_in = true;
            std::cout << is_logged_in << std::endl;
        }
        else {
            is_logged_in = false;
            std::cout << is_logged_in << std::endl;
        }
        std::cout << res << std::endl;
        
        }


        curl_easy_cleanup(curl);
        */
    }

    int Session::getuseridbyname(const char* username_){
        if(curl) {
            std::string url = std::string(ip) + "/usernick/" + std::string(username_);
            curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "GET");
            curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
            curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
            curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
            struct curl_slist *headers = NULL;
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            std::string data = std::string("{\r\n    \"token\": \"") + std::string(token) + std::string(" \"\r\n}");
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
            res = curl_easy_perform(curl);
        }
        return res["id"];

        curl_easy_cleanup(curl);
    }

    void Session::logout(){
    	is_logged_in = false;
    }

    void Session::send_message(const char* message){
        if(curl) {
            std::string id = std::to_string(getuseridbyname(username));
            std::string url = std::string(ip) + "/message";
            curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
            curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
            curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
            curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
            struct curl_slist *headers = NULL;
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            std::string data = std::string("{\r\n    \"message\": \"") + std::string(message) + std::string("\",\r\n    \"user_id\": \"") + id + std::string("\",\r\n    \"") + ",\"token\":\"" + std::string(token) + std::string("\"}");
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
            res = curl_easy_perform(curl);
        }
        curl_easy_cleanup(curl);
    }
}
