

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/DartInternalClassWithInternalTypedef.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DartInternalClassWithInternalTypedef = ::smoke::DartInternalClassWithInternalTypedef;

void register_DartInternalClassWithInternalTypedef(py::module_& module) {
    py::class_<DartInternalClassWithInternalTypedef, std::shared_ptr<DartInternalClassWithInternalTypedef>>(module, "DartInternalClassWithInternalTypedef")
        .def_property("numbers", py::overload_cast<>(&DartInternalClassWithInternalTypedef::get_numbers, py::const_), py::overload_cast<const ::std::unordered_map< ::std::string, int32_t >&>(&DartInternalClassWithInternalTypedef::set_numbers))
        .def_property("labels", py::overload_cast<>(&DartInternalClassWithInternalTypedef::get_labels, py::const_), py::overload_cast<const ::std::vector< ::std::string >&>(&DartInternalClassWithInternalTypedef::set_labels))
        ;
}

