

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
#include "smoke/InternalClassWithStaticProperty.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalClassWithStaticProperty = ::smoke::InternalClassWithStaticProperty;


void register_smoke_InternalClassWithStaticProperty(py::module_& module) {
    py::class_<InternalClassWithStaticProperty, std::shared_ptr<InternalClassWithStaticProperty>>(module, "smoke_InternalClassWithStaticProperty")
        .def("__gluecodium_id__", [](const InternalClassWithStaticProperty& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("foo_bar", &InternalClassWithStaticProperty::get_foo_bar)
        .def_static("foo_bar_set", &InternalClassWithStaticProperty::set_foo_bar)
        ;
}

