

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipFieldConstructorsClash.h"
#include "string"

void register_SkipFieldConstructorsClash(py::module_& module) {
    py::class_<SkipFieldConstructorsClash>(module, "SkipFieldConstructorsClash")
        .def_readwrite("param", &SkipFieldConstructorsClash::param)
        ;
}

