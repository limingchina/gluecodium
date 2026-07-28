

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DartInternalClassWithInternalTypedef.h"
#include "cstdint"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DartInternalClassWithInternalTypedef = ::smoke::DartInternalClassWithInternalTypedef;


void register_smoke_DartInternalClassWithInternalTypedef(py::module_& module) {
    py::class_<DartInternalClassWithInternalTypedef, std::shared_ptr<DartInternalClassWithInternalTypedef>>(module, "smoke_DartInternalClassWithInternalTypedef")
        .def("__gluecodium_id__", [](const DartInternalClassWithInternalTypedef& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_property("numbers", py::overload_cast<>(&DartInternalClassWithInternalTypedef::get_numbers, py::const_), py::overload_cast<const ::std::unordered_map< ::std::string, int32_t >&>(&DartInternalClassWithInternalTypedef::set_numbers))
        .def_property("labels", py::overload_cast<>(&DartInternalClassWithInternalTypedef::get_labels, py::const_), py::overload_cast<const ::std::vector< ::std::string >&>(&DartInternalClassWithInternalTypedef::set_labels))
        ;
}

