

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foobar/CrossPackageChildClass.h"
#include "string"

void register_CrossPackageChildClass(py::module_& module) {
    py::class_<CrossPackageChildClass>(module, "CrossPackageChildClass")
        ;
}

