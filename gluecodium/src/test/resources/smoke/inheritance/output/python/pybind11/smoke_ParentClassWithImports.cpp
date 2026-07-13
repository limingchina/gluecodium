

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentClassWithImports.h"
#include "functional"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentClassWithImports = ::gluecodium::smoke::ParentClassWithImports;

void register_ParentClassWithImports(py::module_& module) {
    py::class_<ParentClassWithImports, std::shared_ptr<ParentClassWithImports>>(module, "ParentClassWithImports")
        .def("root_method", &ParentClassWithImports::root_method, py::arg("input1"), py::arg("input2"))
        .def_property("root_property", py::overload_cast<>(&ParentClassWithImports::get_root_property, py::const_), py::overload_cast<const ::smoke::IncludableLambda&>(&ParentClassWithImports::set_root_property))
        ;
}

