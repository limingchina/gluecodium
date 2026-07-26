

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
#include "gluecodium/VectorHash.h"
#include "smoke/DartInternalClassWithInternalTypedef.h"
#include "smoke/SomeDartClassThatUsesInternal.h"
#include "memory"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeDartClassThatUsesInternal = ::smoke::SomeDartClassThatUsesInternal;


void register_smoke_SomeDartClassThatUsesInternal(py::module_& module) {
    py::class_<SomeDartClassThatUsesInternal, std::shared_ptr<SomeDartClassThatUsesInternal>>(module, "smoke_SomeDartClassThatUsesInternal")
        .def("add_entity", &SomeDartClassThatUsesInternal::add_entity, py::arg("entity"))
        ;
}

