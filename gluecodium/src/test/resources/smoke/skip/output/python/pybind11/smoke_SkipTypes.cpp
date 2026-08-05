

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
#include "smoke/SkipTypes.h"
#include "string"
#include "vector"

using SkipTypes = ::smoke::SkipTypes;
using NotInJava = ::smoke::SkipTypes::NotInJava;
using NotInSwift = ::smoke::SkipTypes::NotInSwift;
using NotInDart = ::smoke::SkipTypes::NotInDart;
using NotInKotlin = ::smoke::SkipTypes::NotInKotlin;



void register_smoke_SkipTypes(py::module_& module) {
auto cls_SkipTypes = py::class_<SkipTypes, std::shared_ptr<SkipTypes>>(module, "smoke_SkipTypes")
        .def("__gluecodium_id__", [](const SkipTypes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_SkipTypesNotInJava = py::class_<NotInJava>(cls_SkipTypes, "NotInJava")
        .def_readwrite("foo_field", &NotInJava::foo_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        ;

auto cls_SkipTypesNotInSwift = py::class_<NotInSwift>(cls_SkipTypes, "NotInSwift")
        .def_readwrite("foo_field", &NotInSwift::foo_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        ;

auto cls_SkipTypesNotInDart = py::class_<NotInDart>(cls_SkipTypes, "NotInDart")
        .def_readwrite("foo_field", &NotInDart::foo_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        ;

auto cls_SkipTypesNotInKotlin = py::class_<NotInKotlin>(cls_SkipTypes, "NotInKotlin")
        .def_readwrite("foo_field", &NotInKotlin::foo_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("foo_field"))
        ;


}
