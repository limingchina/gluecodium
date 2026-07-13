

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/EnumsInTypeCollection.h"
#include "smoke/EnumsInTypeCollectionInterface.h"

void register_EnumsInTypeCollectionInterface(py::module_& module) {
    py::class_<EnumsInTypeCollectionInterface>(module, "EnumsInTypeCollectionInterface")
        .def("flip_enum_value", &EnumsInTypeCollectionInterface::flip_enum_value, py::arg("input"))
        ;
}

