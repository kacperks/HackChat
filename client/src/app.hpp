#pragma once

#ifndef HCAPP
#define HCAPP

#include "window.hpp"
#include "actions.hpp"

namespace hc{
    inline hc::Session session = hc::Session("localhost:5000", "token");

    inline hc::hcwindow win;
}

#endif