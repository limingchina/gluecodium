

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/Calculator.h"
#include "smoke/CalculatorListener.h"
#include "memory"

void register_Calculator(py::module_& module) {
    py::class_<Calculator>(module, "Calculator")
        .def("register_listener", &Calculator::register_listener, py::arg("listener"))
        .def("unregister_listener", &Calculator::unregister_listener, py::arg("listener"))
        ;
}

