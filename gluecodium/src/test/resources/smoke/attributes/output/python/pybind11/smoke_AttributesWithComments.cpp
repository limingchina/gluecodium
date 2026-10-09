

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
#include "smoke/AttributesWithComments.h"
#include "string"

using AttributesWithComments = ::smoke::AttributesWithComments;
using SomeStruct = ::smoke::AttributesWithComments::SomeStruct;



void register_smoke_AttributesWithComments(py::module_& module) {
auto cls_AttributesWithComments = py::class_<AttributesWithComments, std::shared_ptr<AttributesWithComments>>(module, "smoke_AttributesWithComments")
        .def("__gluecodium_id__", [](const AttributesWithComments& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("very_fun", &AttributesWithComments::very_fun, py::call_guard<py::gil_scoped_release>())
        .def_property("prop", [](const AttributesWithComments& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_prop();
            });
        }, [](AttributesWithComments& self, const ::std::string& value) {
            gluecodium::python::call_native([&] {
                self.set_prop(value);
            });
        })
        ;

auto cls_AttributesWithCommentsSomeStruct = py::class_<SomeStruct>(cls_AttributesWithComments, "SomeStruct")
        .def_property("field", [](const SomeStruct& self) -> decltype(auto) {
            return
                (self.field)
            ;
        }, [](SomeStruct& self, const ::std::string& value) {

                self.field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("field"))
        ;


}
