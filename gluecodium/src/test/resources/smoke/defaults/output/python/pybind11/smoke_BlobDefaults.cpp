

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
#include "smoke/BlobDefaults.h"
#include "cstdint"
#include "memory"
#include "vector"

using BlobDefaults = ::smoke::BlobDefaults;



void register_smoke_BlobDefaults(py::module_& module) {
auto cls_BlobDefaults = py::class_<BlobDefaults>(module, "smoke_BlobDefaults")
        .def_readwrite("empty_list", &BlobDefaults::empty_list)
        .def_readwrite("dead_beef", &BlobDefaults::dead_beef)
        .def(py::init<>())
        .def(py::init<::std::shared_ptr< ::std::vector< uint8_t > >, ::std::shared_ptr< ::std::vector< uint8_t > >>(), py::arg("empty_list"), py::arg("dead_beef"))
        ;


}
