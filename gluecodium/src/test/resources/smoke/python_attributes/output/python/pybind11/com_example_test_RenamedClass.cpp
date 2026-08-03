

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
#include "com/example/test/MyClass.h"
#include "cstdint"
#include "string"

using MyClass = ::com::example::test::MyClass;



void register_com_example_test_RenamedClass(py::module_& module) {
auto cls_RenamedClass = py::class_<MyClass, std::shared_ptr<MyClass>>(module, "com_example_test_RenamedClass")
        .def("__gluecodium_id__", [](const MyClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("visible_method", &MyClass::visible_method, py::arg("param"))
        ;


}
