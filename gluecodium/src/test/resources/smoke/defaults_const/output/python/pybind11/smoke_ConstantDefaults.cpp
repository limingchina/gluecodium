

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/SomeStruct.h"
#include "smoke/ConstantDefaults.h"

void register_ConstantDefaults(py::module_& module) {
    py::class_<ConstantDefaults>(module, "ConstantDefaults")
        .def_readwrite("field1", &ConstantDefaults::field1)
        .def_readwrite("field2", &ConstantDefaults::field2)
        ;
}

