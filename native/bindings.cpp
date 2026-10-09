#include <pybind11/pybind11.h>
#include <string>

namespace py = pybind11;

std::string version()
{
    return "VisionBridge 0.1.0";
}

int add(int a, int b)
{
    return a + b;
}

PYBIND11_MODULE(_visionbridge, m)
{
    m.doc() = "VisionBridge native core";

    m.def("version", &version,
          "Return the native core version");

    m.def("add", &add,
          "Test native integer addition");
}