

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
#include "smoke/PublicStructWithNonDefaultInternalField.h"
#include "cstdint"
#include "string"

using PublicStructWithNonDefaultInternalField = ::smoke::PublicStructWithNonDefaultInternalField;



void register_smoke_PublicStructWithNonDefaultInternalField(py::module_& module) {
auto cls_PublicStructWithNonDefaultInternalField = py::class_<PublicStructWithNonDefaultInternalField>(module, "smoke_PublicStructWithNonDefaultInternalField")
        .def_property("defaulted_field", [](const PublicStructWithNonDefaultInternalField& self) -> decltype(auto) {
            return
                (self.defaulted_field)
            ;
        }, [](PublicStructWithNonDefaultInternalField& self, const int32_t value) {

                self.defaulted_field = value;

        })
        .def_property("_internal_field", [](const PublicStructWithNonDefaultInternalField& self) -> decltype(auto) {
            return
                (self.internal_field)
            ;
        }, [](PublicStructWithNonDefaultInternalField& self, const ::std::string& value) {

                self.internal_field = value;

        })
        .def_property("public_field", [](const PublicStructWithNonDefaultInternalField& self) -> decltype(auto) {
            return
                (self.public_field)
            ;
        }, [](PublicStructWithNonDefaultInternalField& self, const bool value) {

                self.public_field = value;

        })
        .def(py::init<>())
        .def(py::init([](const bool& public_field) {
            return PublicStructWithNonDefaultInternalField(::std::string{}, public_field);
        }), py::arg("public_field"))
        .def(py::init([](const int32_t& defaulted_field, const bool& public_field) {
            return PublicStructWithNonDefaultInternalField(defaulted_field, ::std::string{}, public_field);
        }), py::arg("defaulted_field"), py::arg("public_field"))
        ;


}
