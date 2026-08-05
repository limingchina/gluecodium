

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
#include "smoke/JavaInternalClass.h"

using JavaInternalClass = ::smoke::JavaInternalClass;



void register_smoke_JavaInternalClass(py::module_& module) {
auto cls_JavaInternalClass = py::class_<JavaInternalClass, std::shared_ptr<JavaInternalClass>>(module, "smoke_JavaInternalClass")
        .def("__gluecodium_id__", [](const JavaInternalClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
