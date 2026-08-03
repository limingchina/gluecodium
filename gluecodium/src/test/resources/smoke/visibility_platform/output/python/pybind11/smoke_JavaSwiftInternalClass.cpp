

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
#include "smoke/JavaSwiftInternalClass.h"

using JavaSwiftInternalClass = ::smoke::JavaSwiftInternalClass;



void register_smoke_JavaSwiftInternalClass(py::module_& module) {
auto cls_JavaSwiftInternalClass = py::class_<JavaSwiftInternalClass, std::shared_ptr<JavaSwiftInternalClass>>(module, "smoke_JavaSwiftInternalClass")
        .def("__gluecodium_id__", [](const JavaSwiftInternalClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
