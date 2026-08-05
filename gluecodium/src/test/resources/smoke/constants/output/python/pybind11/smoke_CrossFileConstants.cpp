

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
#include "smoke/CrossFileConstants.h"

using CrossFileConstants = ::smoke::CrossFileConstants;



void register_smoke_CrossFileConstants(py::module_& module) {
auto cls_CrossFileConstants = py::class_<CrossFileConstants>(module, "smoke_CrossFileConstants")
        .def(py::init<>())
        ;


}
