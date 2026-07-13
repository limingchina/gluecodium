

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/CrossFileConstants.h"

void register_CrossFileConstants(py::module_& module) {
    py::class_<CrossFileConstants>(module, "CrossFileConstants")
        ;
}

