

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "dontsmoke/UseCppExternalTypes.h"
#include "foo/Bar.h"
#include "foo/Bazz.h"
#include "include/ExternalTypes.h"
#include "non/Sense.h"
#include "memory"

void register_UseCppExternalTypes(py::module_& module) {
    py::class_<UseCppExternalTypes>(module, "UseCppExternalTypes")
        .def("use_struct", &UseCppExternalTypes::use_struct, py::arg("input"))
        .def("use_enum", &UseCppExternalTypes::use_enum, py::arg("input"))
        .def("use_class", &UseCppExternalTypes::use_class, py::arg("input"))
        ;
}

