

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SkipSetter.h"
#include "string"

void register_SkipSetter(py::module_& module) {
    py::class_<SkipSetter, std::shared_ptr<SkipSetter>>(module, "SkipSetter")
        .def_property("foo", &SkipSetter::get_foo)
        ;
}

