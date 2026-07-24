

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/CachedProperties.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CachedProperties = ::smoke::CachedProperties;


void register_smoke_CachedProperties(py::module_& module) {
    py::class_<CachedProperties, std::shared_ptr<CachedProperties>>(module, "CachedProperties")
        .def_property_readonly("cached_property", py::overload_cast<>(&CachedProperties::get_cached_property, py::const_))
        .def_property_readonly("internal_cached_property", py::overload_cast<>(&CachedProperties::get_internal_cached_property, py::const_))
        .def_static("static_cached_property", &CachedProperties::get_static_cached_property)
        .def_static("internal_static_cached_property", &CachedProperties::get_internal_static_cached_property)
        ;
}

