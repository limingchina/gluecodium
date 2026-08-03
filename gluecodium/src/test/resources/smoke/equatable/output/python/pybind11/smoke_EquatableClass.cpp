

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
#include "smoke/EquatableClass.h"
#include "smoke/PointerEquatableClass.h"
#include "cstdint"
#include "memory"
#include "string"

using EquatableClass = ::smoke::EquatableClass;
using EquatableStruct = ::smoke::EquatableClass::EquatableStruct;



void register_smoke_EquatableClass(py::module_& module) {
auto cls_EquatableClass = py::class_<EquatableClass, std::shared_ptr<EquatableClass>>(module, "smoke_EquatableClass")
        .def("__gluecodium_id__", [](const EquatableClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_EquatableClassEquatableStruct = py::class_<EquatableStruct>(cls_EquatableClass, "EquatableStruct")
        .def_readwrite("int_field", &EquatableStruct::int_field)
        .def_readwrite("string_field", &EquatableStruct::string_field)
        .def_readwrite("nested_equatable_instance", &EquatableStruct::nested_equatable_instance)
        .def_readwrite("nested_pointer_equatable_instance", &EquatableStruct::nested_pointer_equatable_instance)
        .def(py::init<>())
        .def(py::init<int32_t, ::std::string, ::std::shared_ptr< ::smoke::EquatableClass >, ::std::shared_ptr< ::smoke::PointerEquatableClass >>(), py::arg("int_field"), py::arg("string_field"), py::arg("nested_equatable_instance"), py::arg("nested_pointer_equatable_instance"))
        .def("__eq__", [](const EquatableStruct& lhs, const EquatableStruct& rhs) { return lhs == rhs; })
        .def("__hash__", [](const EquatableStruct& self) { return gluecodium::hash<EquatableStruct>{}(self); })
        ;


}
