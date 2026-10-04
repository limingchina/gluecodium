

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
#include "include/ExternalTypes.h"
#include "cstdint"
#include "string"




void register_smoke_StructWithOverloads(py::module_& module) {
auto cls_StructWithOverloads = py::class_<external::ClassWithOverloads::StructWithOverloads>(module, "smoke_StructWithOverloads")
        .def_property("overloaded_accessors", [](const external::ClassWithOverloads::StructWithOverloads& self) {
            return self.overloadedAccessors();
        }, [](external::ClassWithOverloads::StructWithOverloads& self, const int32_t value) {
            self.overloadedAccessors(value);
        })
        .def(py::init<>())
        .def(py::init([](const int32_t& overloaded_accessors) {
            external::ClassWithOverloads::StructWithOverloads result{};
            result.overloadedAccessors(overloaded_accessors);
            return result;
        }), py::arg("overloaded_accessors"))
        .def("overloaded_method", [](external::ClassWithOverloads::StructWithOverloads& self) {
            return self.overloadedMethod();
        })
        .def("overloaded_method", [](external::ClassWithOverloads::StructWithOverloads& self, const ::std::string& input) {
            return self.overloadedMethod(input);
        }, py::arg("input"))
        .def("overloaded_method", [](external::ClassWithOverloads::StructWithOverloads& self, const ::std::string& input_string, const bool input_bool) {
            return self.overloadedMethod(input_string, input_bool);
        }, py::arg("input_string"), py::arg("input_bool"))
        ;


}
