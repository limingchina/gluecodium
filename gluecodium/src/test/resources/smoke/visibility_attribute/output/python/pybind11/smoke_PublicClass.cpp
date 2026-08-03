

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
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/PublicClass.h"
#include "string"
#include "unordered_map"
#include "vector"

using PublicClass = ::smoke::PublicClass;
using PublicStruct = ::smoke::PublicClass::PublicStruct;
using PublicStructWithInternalDefaults = ::smoke::PublicClass::PublicStructWithInternalDefaults;



void register_smoke_PublicClass(py::module_& module) {
auto cls_PublicClass = py::class_<PublicClass, std::shared_ptr<PublicClass>>(module, "smoke_PublicClass")
        .def("__gluecodium_id__", [](const PublicClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;

auto cls_PublicClassPublicStruct = py::class_<PublicStruct>(cls_PublicClass, "PublicStruct")
        .def(py::init<>())
        .def(py::init([]() {
            return PublicStruct(::smoke::PublicClass::InternalStruct{});
        }))
        ;

auto cls_PublicClassPublicStructWithInternalDefaults = py::class_<PublicStructWithInternalDefaults>(cls_PublicClass, "PublicStructWithInternalDefaults")
        .def_readwrite("public_field", &PublicStructWithInternalDefaults::public_field)
        .def(py::init<>())
        .def(py::init<float>(), py::arg("public_field"))
        .def(py::init([](const float& public_field) {
            return PublicStructWithInternalDefaults(::std::string{}, public_field);
        }), py::arg("public_field"))
        ;


}
