

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SomeDartClassThatUsesInternal.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SomeDartClassThatUsesInternal = ::gluecodium::smoke::SomeDartClassThatUsesInternal;

void register_SomeDartClassThatUsesInternal(py::module_& module) {
    py::class_<SomeDartClassThatUsesInternal, std::shared_ptr<SomeDartClassThatUsesInternal>>(module, "SomeDartClassThatUsesInternal")
        .def("add_entity", &SomeDartClassThatUsesInternal::add_entity, py::arg("entity"))
        ;
}

