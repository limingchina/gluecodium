

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/AlienEnum4.h"
#include "smoke/EnumWrapperExternal.h"

void register_EnumWrapperExternal(py::module_& module) {
    py::class_<EnumWrapperExternal>(module, "EnumWrapperExternal")
        .def_readwrite("enum_field", &EnumWrapperExternal::enum_field)
        ;
}

