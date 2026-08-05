

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
#include "smoke/ExposeClass.h"

using ExposeClass = ::smoke::ExposeClass;



void register_smoke_ExposeClass(py::module_& module) {
auto cls_ExposeClass = py::class_<ExposeClass, std::shared_ptr<ExposeClass>>(module, "smoke_ExposeClass")
        .def("__gluecodium_id__", [](const ExposeClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
