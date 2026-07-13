

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "smoke/StructWithSet.h"
#include "unordered_set"

void register_StructWithSet(py::module_& module) {
    py::class_<StructWithSet>(module, "StructWithSet")
        .def_readwrite("field", &StructWithSet::field)
        ;
}

