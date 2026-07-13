

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "dont/smoke/DontSmokeEnum.h"
#include "smoke/SkippedFunctionClass.h"

void register_SkippedFunctionClass(py::module_& module) {
    py::class_<SkippedFunctionClass>(module, "SkippedFunctionClass")
        .def("do_foo", &SkippedFunctionClass::do_foo, py::arg("input"))
        ;
}

