

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "dontsmoke/UseCppExternalTypes.h"
#include "foo/Bar.h"
#include "foo/Bazz.h"
#include "include/ExternalTypes.h"
#include "non/Sense.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseCppExternalTypes = ::gluecodium::dontsmoke::UseCppExternalTypes;

void register_UseCppExternalTypes(py::module_& module) {
    py::class_<UseCppExternalTypes>(module, "UseCppExternalTypes")
        .def("use_struct", &UseCppExternalTypes::use_struct, py::arg("input"))
        .def("use_enum", &UseCppExternalTypes::use_enum, py::arg("input"))
        .def("use_class", &UseCppExternalTypes::use_class, py::arg("input"))
        ;
}

