

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
#include "smoke/NonEquatableClass.h"
#include "smoke/NonEquatableInterface.h"
#include "smoke/SimpleEquatableStruct.h"
#include "memory"

using SimpleEquatableStruct = ::smoke::SimpleEquatableStruct;



void register_smoke_SimpleEquatableStruct(py::module_& module) {
auto cls_SimpleEquatableStruct = py::class_<SimpleEquatableStruct>(module, "smoke_SimpleEquatableStruct")
        .def_property("class_field", [](const SimpleEquatableStruct& self) -> decltype(auto) {
            return
                (self.class_field)
            ;
        }, [](SimpleEquatableStruct& self, const ::std::shared_ptr< ::smoke::NonEquatableClass >& value) {

                self.class_field = value;

        })
        .def_property("interface_field", [](const SimpleEquatableStruct& self) -> decltype(auto) {
            return
                (self.interface_field)
            ;
        }, [](SimpleEquatableStruct& self, const ::std::shared_ptr< ::smoke::NonEquatableInterface >& value) {

                self.interface_field = value;

        })
        .def_property("nullable_class_field", [](const SimpleEquatableStruct& self) -> decltype(auto) {
            return
                (self.nullable_class_field)
            ;
        }, [](SimpleEquatableStruct& self, const ::std::shared_ptr< ::smoke::NonEquatableClass >& value) {

                self.nullable_class_field = value;

        })
        .def_property("nullable_interface_field", [](const SimpleEquatableStruct& self) -> decltype(auto) {
            return
                (self.nullable_interface_field)
            ;
        }, [](SimpleEquatableStruct& self, const ::std::shared_ptr< ::smoke::NonEquatableInterface >& value) {

                self.nullable_interface_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::shared_ptr< ::smoke::NonEquatableClass >, ::std::shared_ptr< ::smoke::NonEquatableInterface >>(), py::arg("class_field"), py::arg("interface_field"))
        .def(py::init<::std::shared_ptr< ::smoke::NonEquatableClass >, ::std::shared_ptr< ::smoke::NonEquatableInterface >, ::std::shared_ptr< ::smoke::NonEquatableClass >, ::std::shared_ptr< ::smoke::NonEquatableInterface >>(), py::arg("class_field"), py::arg("interface_field"), py::arg("nullable_class_field"), py::arg("nullable_interface_field"))
        .def("__gluecodium_copy__", [](const SimpleEquatableStruct& self) { return SimpleEquatableStruct(self); })
        .def("__gluecodium_equals__", [](const SimpleEquatableStruct& lhs, const SimpleEquatableStruct& rhs) { return lhs == rhs; })
        .def("__gluecodium_hash__", [](const SimpleEquatableStruct& self) { return gluecodium::hash<SimpleEquatableStruct>{}(self); })
        ;


}
