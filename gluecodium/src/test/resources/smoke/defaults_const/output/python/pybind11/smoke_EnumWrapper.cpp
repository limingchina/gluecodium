

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/Enum4.h"
#include "smoke/EnumWrapper.h"

void register_EnumWrapper(py::module_& module) {
    py::class_<EnumWrapper>(module, "EnumWrapper")
        .def_readwrite("enum_field", &EnumWrapper::enum_field)
        ;
}

