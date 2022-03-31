#include "actions.hpp"

namespace hc{
    int Session::register_user(const char* username, const char* email, const char* password){
        this->username = username;
        this->email = email;
        this->password = password;
        std::string l = std::string(ip) + "/user/";
        if(curl){
            curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
            curl_easy_setopt(curl, CURLOPT_URL, l.c_str());
            curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
            curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
            curl_slist *headers = NULL; headers = curl_slist_append(headers, "Content-Type: application/json");
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

            std::string data = std::string("{ \n \"username\": \"") + username + std::string("\", \n \"email\": \"") + email + std::string("\", \n \"password\": \"") + password + "\", \n \"token\": \"" + token + "\" \n } ";
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());
            res = curl_easy_perform(curl);
        }
        curl_easy_cleanup(curl);
        is_logged_in = true;
        return res["id"];
    }
    void Session::login(const char* email, const char* password){
        this->username = username;
        this->email = email;
        this->password = password;
        
        std::string l = std::string(ip) + "/useremail/" + std::string(email);
        if(curl) {
        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "GET");
        curl_easy_setopt(curl, CURLOPT_URL, l.c_str());
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
        struct curl_slist *headers = NULL;
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        std::string data = "{\r\n    \"token\": \"" + std::string(token) + "\"\r\n}";
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());
        res = curl_easy_perform(curl);

        if(&res["password"] == password){
            is_logged_in = true;
            std::cout << "Logged in!" << std::endl;
        }
        
        }

        curl_easy_cleanup(curl);
    }
}