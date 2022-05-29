#include "app.hpp"
int main()
{
    hc::Session session = hc::Session("localhost:5000", "asd");
    session.login("kk1@kk.pl", "asd");
    return 0;
}