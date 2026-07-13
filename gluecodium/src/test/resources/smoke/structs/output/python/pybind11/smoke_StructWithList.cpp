

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/StructWithList.h"
#include "vector"

void register_StructWithList(py::module_& module) {
    py::class_<StructWithList>(module, "StructWithList")
        .def_readwrite("field", &StructWithList::field)
        ;
}

