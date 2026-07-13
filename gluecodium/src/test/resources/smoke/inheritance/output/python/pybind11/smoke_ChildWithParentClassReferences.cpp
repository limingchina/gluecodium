

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/ChildClassFromClass.h"
#include "smoke/ChildWithParentClassReferences.h"
#include "smoke/ParentClass.h"
#include "memory"

void register_ChildWithParentClassReferences(py::module_& module) {
    py::class_<ChildWithParentClassReferences>(module, "ChildWithParentClassReferences")
        ;
}

