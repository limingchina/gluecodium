

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
#include "smoke/EquatableStructWithAccessors.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EquatableStructWithAccessors = ::smoke::EquatableStructWithAccessors;

void register_smoke_EquatableStructWithAccessors(py::module_& module) {
    py::class_<EquatableStructWithAccessors>(module, "smoke_EquatableStructWithAccessors")
        .def_property("foo_field", static_cast<const ::std::string& (EquatableStructWithAccessors::*)() const &>(&EquatableStructWithAccessors::get_foo_field), py::overload_cast<const ::std::string&>(&EquatableStructWithAccessors::set_foo_field))
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        .def("__eq__", [](const EquatableStructWithAccessors& lhs, const EquatableStructWithAccessors& rhs) { return lhs == rhs; })
        .def("__hash__", [](const EquatableStructWithAccessors& self) { return gluecodium::hash<EquatableStructWithAccessors>{}(self); })
        ;
}

