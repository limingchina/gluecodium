

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/Alphabet.h"
#include "smoke/NameClashLists.h"
#include "smoke/foo/Alphabet.h"
#include "vector"

void register_NameClashLists(py::module_& module) {
    py::class_<NameClashLists>(module, "NameClashLists")
        .def_readwrite("field_a", &NameClashLists::field_a)
        .def_readwrite("field_b", &NameClashLists::field_b)
        ;
}

