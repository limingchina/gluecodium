

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
#include "smoke/ClassInStruct.h"
#include "functional"
#include "memory"

using ClassInStruct = ::smoke::ClassInStruct;
using FooChecker = ::smoke::ClassInStruct::FooChecker;



void register_smoke_ClassInStruct(py::module_& module) {
auto cls_ClassInStruct = py::class_<ClassInStruct>(module, "smoke_ClassInStruct")
        .def(py::init<>())
        ;

auto cls_ClassInStructFooChecker = py::class_<FooChecker, std::shared_ptr<FooChecker>>(cls_ClassInStruct, "FooChecker")
        .def("__gluecodium_id__", [](const FooChecker& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
