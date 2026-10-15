

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
#include "gluecodium/VectorHash.h"
#include "smoke/SomeMutableCustomStructWithDefaults.h"
#include "cstdint"
#include "string"
#include "vector"

using SomeMutableCustomStructWithDefaults = ::smoke::SomeMutableCustomStructWithDefaults;



void register_smoke_SomeMutableCustomStructWithDefaults(py::module_& module) {
auto cls_SomeMutableCustomStructWithDefaults = py::class_<SomeMutableCustomStructWithDefaults>(module, "smoke_SomeMutableCustomStructWithDefaults")
        .def_property("int_field", [](const SomeMutableCustomStructWithDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](SomeMutableCustomStructWithDefaults& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("string_field", [](const SomeMutableCustomStructWithDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](SomeMutableCustomStructWithDefaults& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def_property("list_field", [](const SomeMutableCustomStructWithDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.list_field)
            );
        }, [](SomeMutableCustomStructWithDefaults& self, const ::std::vector< int32_t >& value) {

                self.list_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string, ::std::vector< int32_t >>(), py::arg("int_field"), py::arg("string_field"), py::arg("list_field"))
        ;


}
