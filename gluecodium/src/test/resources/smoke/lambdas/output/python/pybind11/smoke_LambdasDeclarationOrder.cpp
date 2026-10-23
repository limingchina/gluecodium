

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
#include "smoke/LambdasDeclarationOrder.h"
#include "functional"
#include "string"

using LambdasDeclarationOrder = ::smoke::LambdasDeclarationOrder;
using SomeStruct = ::smoke::LambdasDeclarationOrder::SomeStruct;



void register_smoke_LambdasDeclarationOrder(py::module_& module) {
auto cls_LambdasDeclarationOrder = py::class_<LambdasDeclarationOrder, std::shared_ptr<LambdasDeclarationOrder>>(module, "smoke_LambdasDeclarationOrder")
        .def("__gluecodium_id__", [](const LambdasDeclarationOrder& self) {
            return gluecodium::python::native_identity(self);
        })
        ;

auto cls_LambdasDeclarationOrderSomeStruct = py::class_<SomeStruct>(cls_LambdasDeclarationOrder, "SomeStruct")
        .def_property("some_field", [](const SomeStruct& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        }, [](SomeStruct& self, const ::std::string& value) {

                self.some_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("some_field"))
        ;


}
