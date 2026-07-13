

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/DurationHash.h"
#include "smoke/DurationDefaults.h"
#include "chrono"

void register_DurationDefaults(py::module_& module) {
    py::class_<DurationDefaults>(module, "DurationDefaults")
        .def_readwrite("dayz", &DurationDefaults::dayz)
        .def_readwrite("hourz", &DurationDefaults::hourz)
        .def_readwrite("minutez", &DurationDefaults::minutez)
        .def_readwrite("secondz", &DurationDefaults::secondz)
        .def_readwrite("milliz", &DurationDefaults::milliz)
        .def_readwrite("microz", &DurationDefaults::microz)
        .def_readwrite("nanoz", &DurationDefaults::nanoz)
        ;
}

