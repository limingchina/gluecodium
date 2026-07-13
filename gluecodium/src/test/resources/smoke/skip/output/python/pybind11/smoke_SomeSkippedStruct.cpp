

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/SomeSkippedEnum.h"
#include "smoke/SomeSkippedStruct.h"
#include "vector"

void register_SomeSkippedStruct(py::module_& module) {
    py::class_<SomeSkippedStruct>(module, "SomeSkippedStruct")
        .def_readwrite("field", &SomeSkippedStruct::field)
        ;
}

