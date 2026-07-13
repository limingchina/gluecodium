

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foobar/CrossPackageChildInterface.h"

void register_CrossPackageChildInterface(py::module_& module) {
    py::class_<CrossPackageChildInterface, std::shared_ptr<CrossPackageChildInterface>>(module, "CrossPackageChildInterface")
        ;
}

