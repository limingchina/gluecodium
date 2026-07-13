

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "dont/smoke/DontSmokeEnum.h"
#include "smoke/SomeSkippedClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeSkippedClass = ::smoke::SomeSkippedClass;

void register_SomeSkippedClass(py::module_& module) {
    py::class_<SomeSkippedClass, std::shared_ptr<SomeSkippedClass>>(module, "SomeSkippedClass")
        .def("do_foo", &SomeSkippedClass::do_foo)
        ;
}

