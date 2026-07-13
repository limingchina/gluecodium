

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "dont/smoke/DontSmokeEnum.h"
#include "smoke/SomeSkippedClass.h"

void register_SomeSkippedClass(py::module_& module) {
    py::class_<SomeSkippedClass>(module, "SomeSkippedClass")
        .def("do_foo", &SomeSkippedClass::do_foo)
        ;
}

