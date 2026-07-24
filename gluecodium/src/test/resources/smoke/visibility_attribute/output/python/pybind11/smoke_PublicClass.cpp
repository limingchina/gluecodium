

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/PublicClass.h"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PublicClass = ::smoke::PublicClass;


void register_smoke_PublicClass(py::module_& module) {
    py::class_<PublicClass, std::shared_ptr<PublicClass>>(module, "PublicClass")
        .def_property("internal_struct_property", py::overload_cast<>(&PublicClass::get_internal_struct_property, py::const_), py::overload_cast<const ::smoke::PublicClass::InternalStruct&>(&PublicClass::set_internal_struct_property))
        ;
}

