

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Locale.h"
#include "gluecodium/UnorderedSetHash.h"
#include "smoke/OuterStruct.h"
#include "unordered_set"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InnerClass = ::smoke::OuterStruct::InnerClass;


void register_OuterStructInnerClass(py::module_& module) {
    py::class_<InnerClass, std::shared_ptr<InnerClass>>(module, "OuterStructInnerClass")
        .def("foo_bar", &InnerClass::foo_bar)

        ;
}

