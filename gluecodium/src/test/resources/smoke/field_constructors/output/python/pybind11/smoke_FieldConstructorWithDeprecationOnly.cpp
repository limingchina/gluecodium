

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorWithDeprecationOnly.h"
#include "string"

using FieldConstructorWithDeprecationOnly = ::smoke::FieldConstructorWithDeprecationOnly;



void register_smoke_FieldConstructorWithDeprecationOnly(py::module_& module) {
auto cls_FieldConstructorWithDeprecationOnly = py::class_<FieldConstructorWithDeprecationOnly>(module, "smoke_FieldConstructorWithDeprecationOnly")
        .def_property("string_field", [](const FieldConstructorWithDeprecationOnly& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](FieldConstructorWithDeprecationOnly& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;


}
