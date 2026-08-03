

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
#include "gluecodium/VectorHash.h"
#include "smoke/CachedProperties.h"
#include "cstdint"
#include "memory"
#include "string"
#include "vector"

using CachedProperties = ::smoke::CachedProperties;



void register_smoke_CachedProperties(py::module_& module) {
auto cls_CachedProperties = py::class_<CachedProperties, std::shared_ptr<CachedProperties>>(module, "smoke_CachedProperties")
        .def("__gluecodium_id__", [](const CachedProperties& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_property_readonly("cached_property", py::overload_cast<>(&CachedProperties::get_cached_property, py::const_))
        .def_static("static_cached_property", &CachedProperties::get_static_cached_property)
        ;


}
