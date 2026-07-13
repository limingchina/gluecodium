

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/VectorHash.h"
#include "smoke/CachedProperties.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

void register_CachedProperties(py::module_& module) {
    py::class_<CachedProperties>(module, "CachedProperties")
        .def_property("cached_property", &CachedProperties::get_cached_property)
        .def_property("internal_cached_property", &CachedProperties::get_internal_cached_property)
        .def_property("static_cached_property", &CachedProperties::get_static_cached_property)
        .def_property("internal_static_cached_property", &CachedProperties::get_internal_static_cached_property)
        ;
}

