

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/EquatableStructWithAccessors.h"
#include "string"

using EquatableStructWithAccessors = ::smoke::EquatableStructWithAccessors;



void register_smoke_EquatableStructWithAccessors(py::module_& module) {
auto cls_EquatableStructWithAccessors = py::class_<EquatableStructWithAccessors>(module, "smoke_EquatableStructWithAccessors")
        .def_property("foo_field", [](const EquatableStructWithAccessors& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_foo_field();
            });
        }, [](EquatableStructWithAccessors& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_foo_field(value);
            });
        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        .def("__gluecodium_copy__", [](const EquatableStructWithAccessors& self) { return EquatableStructWithAccessors(self); })
        .def("__gluecodium_equals__", [](const EquatableStructWithAccessors& lhs, const EquatableStructWithAccessors& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const EquatableStructWithAccessors& self) { return gluecodium::hash<EquatableStructWithAccessors>{}(self); })
        ;


}
