

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
#include "smoke/OuterClassWithLambdaAndProperty.h"
#include "cstdint"
#include "functional"

using OuterClassWithLambdaAndProperty = ::smoke::OuterClassWithLambdaAndProperty;



void register_smoke_OuterClassWithLambdaAndProperty(py::module_& module) {
auto cls_OuterClassWithLambdaAndProperty = py::class_<OuterClassWithLambdaAndProperty, std::shared_ptr<OuterClassWithLambdaAndProperty>>(module, "smoke_OuterClassWithLambdaAndProperty")
        .def("__gluecodium_id__", [](const OuterClassWithLambdaAndProperty& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_property("some_integer", [](const OuterClassWithLambdaAndProperty& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_some_integer();
            });
        }, [](OuterClassWithLambdaAndProperty& self, const int32_t value) {
            gluecodium::python::call_native([&] {
                self.set_some_integer(value);
            });
        })
        .def_static("another_integer", []() -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return OuterClassWithLambdaAndProperty::get_another_integer();
            });
        })
        .def_static("another_integer_set", [](const int32_t value) {
            gluecodium::python::call_native([&] {
                OuterClassWithLambdaAndProperty::set_another_integer(value);
            });
        })
        ;


}
