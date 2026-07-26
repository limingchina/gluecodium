

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "smoke/Enums.h"
#include "cstdint"
#include "string"
#include "unordered_map"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Enums = ::smoke::Enums;


void register_smoke_Enums(py::module_& module) {
    py::class_<Enums, std::shared_ptr<Enums>>(module, "smoke_Enums")
        .def_static("method_with_enumeration", &Enums::method_with_enumeration, py::arg("input"))
        .def_static("flip_enum_value", &Enums::flip_enum_value, py::arg("input"))
        .def_static("extract_enum_from_struct", &Enums::extract_enum_from_struct, py::arg("input"))
        .def_static("create_struct_with_enum_inside", &Enums::create_struct_with_enum_inside, py::arg("type"), py::arg("message"))
        ;
}

