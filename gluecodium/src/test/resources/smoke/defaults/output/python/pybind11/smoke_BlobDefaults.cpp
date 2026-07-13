

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/BlobDefaults.h"
#include "cstdint"
#include "memory"
#include "vector"

void register_BlobDefaults(py::module_& module) {
    py::class_<BlobDefaults>(module, "BlobDefaults")
        .def_readwrite("empty_list", &BlobDefaults::empty_list)
        .def_readwrite("dead_beef", &BlobDefaults::dead_beef)
        ;
}

