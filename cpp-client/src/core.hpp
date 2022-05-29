#pragma once

#include <set>
#include <map>
#include <array>
#include <tuple>
#include <queue>
#include <vector>
#include <string>
#include <bitset>
#include <stdio.h>
#include <memory>
#include <cassert>
#include <sstream>
#include <fstream>
#include <iostream>
#include <typeinfo>
#include <algorithm>
#include <functional>
#include <filesystem>
#include <unordered_map>

#if defined(_WIN32)
#include <windows.h>
#elif defined(__linux__)
#include <bits/stdc++.h>
#else
#error Not Supported Platform!
#endif

#include "ui.hpp"
#include "window.hpp"
#include "actions.hpp"