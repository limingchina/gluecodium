

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
#include "smoke/NonEquatableClass.h"
#include "smoke/NonEquatableInterface.h"
#include "smoke/SimpleEquatableStruct.h"
#include "memory"

using SimpleEquatableStruct = ::smoke::SimpleEquatableStruct;



void register_smoke_SimpleEquatableStruct(py::module_& module) {
auto cls_SimpleEquatableStruct = py::class_<SimpleEquatableStruct>(module, "smoke_SimpleEquatableStruct")
        .def_readwrite("class_field", &SimpleEquatableStruct::class_field)
        .def_readwrite("interface_field", &SimpleEquatableStruct::interface_field)
        .def_readwrite("nullable_class_field", &SimpleEquatableStruct::nullable_class_field)
        .def_readwrite("nullable_interface_field", &SimpleEquatableStruct::nullable_interface_field)
        .def(py::init<>())
        .def(py::init<::std::shared_ptr< ::smoke::NonEquatableClass >, ::std::shared_ptr< ::smoke::NonEquatableInterface >>(), py::arg("class_field"), py::arg("interface_field"))
        .def(py::init<::std::shared_ptr< ::smoke::NonEquatableClass >, ::std::shared_ptr< ::smoke::NonEquatableInterface >, ::std::shared_ptr< ::smoke::NonEquatableClass >, ::std::shared_ptr< ::smoke::NonEquatableInterface >>(), py::arg("class_field"), py::arg("interface_field"), py::arg("nullable_class_field"), py::arg("nullable_interface_field"))
        .def("__eq__", [](const SimpleEquatableStruct& lhs, const SimpleEquatableStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const SimpleEquatableStruct& self) { return gluecodium::hash<SimpleEquatableStruct>{}(self); })
        ;


}
