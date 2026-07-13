

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/UnorderedMapHash.h"
#include "smoke/StructWithMap.h"
#include "string"
#include "unordered_map"

void register_StructWithMap(py::module_& module) {
    py::class_<StructWithMap>(module, "StructWithMap")
        .def_readwrite("field", &StructWithMap::field)
        ;
}

