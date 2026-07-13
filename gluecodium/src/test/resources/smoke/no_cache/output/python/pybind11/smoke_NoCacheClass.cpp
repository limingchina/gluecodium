

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/NoCacheClass.h"
#include "memory"

void register_NoCacheClass(py::module_& module) {
    py::class_<NoCacheClass>(module, "NoCacheClass")
        .def("make", &NoCacheClass::make)
        .def("foo", &NoCacheClass::foo)
        ;
}

