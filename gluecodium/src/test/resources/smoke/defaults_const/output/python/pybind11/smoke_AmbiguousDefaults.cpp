

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/AmbiguousEnum.h"
#include "fire/SomeStruct.h"
#include "smoke/AmbiguousDefaults.h"

void register_AmbiguousDefaults(py::module_& module) {
    py::class_<AmbiguousDefaults>(module, "AmbiguousDefaults")
        .def_readwrite("field1", &AmbiguousDefaults::field1)
        .def_readwrite("field2", &AmbiguousDefaults::field2)
        ;
}

