

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/Bar.h"
#include "smoke/Enums.h"

void register_Enums(py::module_& module) {
    py::class_<Enums>(module, "Enums")
        .def("method_with_external_enum", &Enums::method_with_external_enum, py::arg("input"))
        ;
}

